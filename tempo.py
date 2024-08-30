#authority = "10.48579"
#st.write(liste_identifiers_dataset)
        
#for identifier in liste_identifiers_dataset:
#    dataset = api.get_dataset(identifier=f"doi:{authority}/{identifier}")
#    dataset_ = dataset.json()
#    st.write(dataset_["data"]["latestVersion"]["metadataBlocks"]["citation"]["fields"][0]["value"])     

import pandas as pd

data = {
    'GEMET - INSPIRE themes': 444,
    'theme.EnvironnementFR.rdf,GEMET - INSPIRE themes,theme.thesaurus_costel.rdf': 81,
    'GEMET - INSPIRE themes,Vocabulaire MétaZABR': 48,
    'theme.EnvironnementFR.rdf,GEMET - INSPIRE themes': 35,
    'Régions administratives de France': 26,
    'theme.EnvironnementFR.rdf,theme.thesaurus_costel.rdf': 23,
    'GEMET - INSPIRE themes,GEMET - Concepts,sea regions of the world.,Régions administratives de France,countries,Continents': 23,
    'GEMET - INSPIRE themes,Continents,sea regions of the world.,countries,Régions administratives de France': 16,
    'GEMET - Concepts,GEMET - INSPIRE themes,Régions de France,Region': 15,
    'GEMET - Concepts,GEMET - INSPIRE themes': 14
}

# Convert it into a DataFrame
df = pd.DataFrame(list(data.items()), columns=['Themes', 'Counts'])

print(df)