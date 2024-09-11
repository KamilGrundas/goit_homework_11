from mongoengine import connect
from models import Authors, Quotes

connect(
    host="mongodb+srv://kamilgrundas:ecpO4IACAqyqpSbD@cluster01.1utb5h1.mongodb.net/",
    db="big_people",
    ssl=True,
)


def search_by_author(name):
    results = []

    author = Authors.objects(fullname=name).first()

    quotes = Quotes.objects(author=author)

    for quote in quotes:
        results.append(quote.quote)

    return results


def search_by_tags(tags):
    results = []

    for tag in tags:
        quotes = Quotes.objects(tags=tag.strip())

        for quote in quotes:
            if quote.quote not in results:
                results.append(quote.quote)

    return results


while True:
    results = []
    command = input("\nAvailabe commands:\n\nname - e.g. name: Steve Martin\ntag - e.g. tag:life\ntags - e.g. tags:life,live\nexit \n\nInsert command: \n")

    if command == "exit":
        break

    command = command.split(":")
    arguments = command[1].split(",")

    if command[0] == "name":
        results = search_by_author(arguments[0].strip())
    elif command[0] == "tag" or "tags":
        results = search_by_tags(arguments)

    for result in results:
        print(result.encode(encoding="UTF-8"))
