import pandas as  pd

df = pd.read_csv('websites.csv')

WEBSITE_LIST = df[['Nom', 'Adresse', 'Cookie selector', 'Link selector', 'Content selector', 'Title selector', 'Date selector', 'Author selector']].values.tolist()
INITIAL_WEBSITE_LIST = df.loc[df['Initial crawling']==  'x'][['Nom', 'Adresse', 'Cookie selector', 'Link selector', 'Content selector', 'Title selector', 'Date selector', 'Author selector']].values.tolist()