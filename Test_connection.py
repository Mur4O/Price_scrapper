import psycopg

conn = psycopg.connect(f"postgresql://postgres@dbserver.lan/albion")

cursor = conn.cursor()

# cursor.execute("insert into Products (Name, Price) values ('RTX 3060', 50000)")
# conn.commit()

cursor.execute("select * from Products")
cursor.fetchone()

cursor.close()
conn.close()