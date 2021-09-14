import pandas as  pd

df = pd.read_csv('websites.csv')

WEBSITE_LIST = df[['Nom', 'Adresse']].values.tolist()

INITIAL_WEBSITE_LIST = df.loc[df['Initial crawling']==  'x'][['Nom', 'Adresse']].values.tolist()