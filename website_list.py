import pandas as  pd

df = pd.read_csv('websites.csv')

WEBSITE_LIST = df[['Nom', 'Adresse', 'Cookie selector', 'Link selector', 'Content selector', 'Title selector', 'Date selector', 'Author selector', 'Page url complement', 'Number of pages', 'paginator formula']].values.tolist()
INITIAL_WEBSITE_LIST = df.loc[df['Initial crawling']==  'x'][['Nom', 'Adresse', 'Cookie selector', 'Link selector', 'Content selector', 'Title selector', 'Date selector', 'Author selector', 'Page url complement', 'Number of pages', 'paginator formula']].values.tolist()
TEST_WEBSITE_LIST = df.loc[df['Nom']==  'Egalité & Réconciliation'][['Nom', 'Adresse', 'Cookie selector', 'Link selector', 'Content selector', 'Title selector', 'Date selector', 'Author selector', 'Page url complement', 'Number of pages', 'paginator formula']].values.tolist()