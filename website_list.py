import pandas as  pd

df = pd.read_csv('websites.csv')

WEBSITE_LIST = df[['Nom', 'Adresse']].values.tolist()