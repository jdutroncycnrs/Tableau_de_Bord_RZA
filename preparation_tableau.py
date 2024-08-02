import pandas as pd
from datetime import datetime
import numpy as np

def prepa_date(tableau, rule="6ME"):
    tableau_date = tableau.copy()
    tableau_date.set_index('Date', inplace=True)
    tableau_date_resampled = tableau_date.resample(rule=rule).size()
    liste_dates = tableau_date_resampled.index.values
    liste_comptes = tableau_date_resampled.values
    df_date = pd.DataFrame([liste_dates,liste_comptes], index=['Date','Compte_resampled']).T
    df_date['Date'] = pd.to_datetime(df_date['Date'], format='mixed', utc=True)
    return df_date

def year(tableau):
    tableau_year = tableau.copy()
    tableau_year['Date'] = pd.to_datetime(tableau_year['Date'], format='mixed', utc=True)
    tableau_year.sort_values(by="Date", inplace=True)
    for i in range(len(tableau_year)):
        try:
            y = datetime.date(tableau_year.loc[i,'Date']).year
            if y==1:
                y=np.NaN
        except:
            y = np.NAN
        tableau_year.loc[i,'Year']= y
    return tableau_year