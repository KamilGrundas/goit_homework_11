import json
from models import Authors, Quotes
from mongoengine import connect
from datetime import datetime

connect(
    host="mongodb+srv://kamilgrundas:ecpO4IACAqyqpSbD@cluster01.1utb5h1.mongodb.net/",
    db="big_people",
    ssl=True,
)

authors_json = "authors.json"
qoutes_json = "qoutes.json"


def format_date(date_str):
    return datetime.strptime(date_str, "%B %d, %Y").date()


def load_data(path):

    with open(path, "r") as f:
        data = json.load(f)
    return data


authors = load_data(authors_json)
quotes = load_data(qoutes_json)

for author in authors:
    new_author = Authors(
        fullname=author["fullname"],
        born_date=format_date(author["born_date"]),
        born_location=author["born_location"],
        description=author["description"],
    )
    new_author.save()

for quote in quotes:
    author = Authors.objects(fullname=quote["author"]).first()
    if author:
        del quote["author"]
        new_qoute = Quotes(author=author, **quote)
        new_qoute.save()
