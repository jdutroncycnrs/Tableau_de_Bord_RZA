import pandas as pd

def prepa_date(tableau, rule="6ME"):
    tableau_date = tableau.copy()
    tableau_date['Date'] = pd.to_datetime(tableau['Date'], format='mixed', utc=True)
    tableau_date.sort_values(by="Date", inplace=True)
    tableau_date.set_index('Date', inplace=True)
    tableau_date_resampled = tableau_date.resample(rule=rule).size()
    liste_dates = tableau_date_resampled.index.values
    liste_comptes = tableau_date_resampled.values
    df_date = pd.DataFrame([liste_dates,liste_comptes], index=['Date','Compte_resampled']).T
    df_date['Date'] = pd.to_datetime(df_date['Date'], format='mixed', utc=True)
    return df_date