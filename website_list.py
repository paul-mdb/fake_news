import pandas as  pd

df = pd.read_csv('websites.csv')

WEBSITE_LIST = df[['Nom', 'Adresse', 'css selector']].values.tolist()

INITIAL_WEBSITE_LIST = df.loc[df['Initial crawling']==  'x'][['Nom', 'Adresse', 'css selector']].values.tolist()

dict = {
    "Paris innovation review" : "div[role = 'listitem'] a",
    "Egalité & Réconciliation"  : "div.chapo_content a",
    "Réseau Voltaire" : "div.one-mot a",
    "Réseau International" : "div.module-blog-wrap a",
    


}