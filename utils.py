DATABASE_PATH = "articles/"

def format_article_into_json(title, author, date, content):
    return {
        "title": title,
        "author": author,
        "date": date,
        "content": content
    }
