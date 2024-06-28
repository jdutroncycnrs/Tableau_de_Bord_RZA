import json
import re
import pandas as pd

def transcript_json(json_data, file, prefix=""):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, dict) or isinstance(value, list):
                transcript_json(value,file, f"{prefix}.{key}" if prefix else key)
            else:
                #print(f"{prefix}.{key}: {value}" if prefix else f"{key}: {value}")
                file.write(f"{prefix}.{key}: {value}," if prefix else f"{key}: {value},")
    elif isinstance(json_data, list):
        for item in json_data:
            transcript_json(item,file, prefix)
    else:
        #print(f"{prefix}: {json_data}" if prefix else f"{json_data}")
        file.write(f"{prefix}: {json_data}," if prefix else f"{json_data},")


# Load your JSON data from a file or define it directly
fichier ='fc86ebf4-4f49-4b8d-8bf0-b0c4b768b85b'
with open(f'data/{fichier}.json', 'r') as f:
    data = json.load(f)

# Call the function to print concatenated keys and values
with open(f'tmp/{fichier}.txt', 'w') as file:
    transcript_json(data, file)

with open(f'tmp/{fichier}.txt', 'r') as f:
    d = f.read()

listi = re.split(',',d)
df = pd.DataFrame(listi[0:-1], columns=['Results'])
for i in range(len(df)):
    p = re.split(' ',df.loc[i,'Results'])
    df.loc[i,'Valeurs']=p[1]
    df.loc[i,'Clés']=p[0].replace('.','/')
for j in range(len(df)):
    pp = re.split('/',df.loc[j,'Clés'])
    df.loc[j,'K0']=pp[1]
    for k in range(15):
        try:
            df.loc[j,f'K{k+1}']=pp[k+2]
        except:
            pass
    

df.to_csv(f'data/{fichier}.csv')