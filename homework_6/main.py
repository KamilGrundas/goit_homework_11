from sqlalchemy import create_engine

if __name__ == "__main__":
    uri = "sqlite:///school"
    engine = create_engine(uri)

    with open("query_2.sql","r") as f:
        sql = f.read()
    
    result = engine.execute(sql, 3)
    for row in result.fetchall():
        print(row)
