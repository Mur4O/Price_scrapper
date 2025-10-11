import pyodbc as db

conn = db.connect(
                  'driver={ODBC Driver 18 for SQL Server};'
                  'server=100.98.191.77;'
                  'database=Scrapper;'
                  'uid=sa;'
                  'pwd=Qwerty11;'
                  'encrypt=no;'
                  'TrustServerCertificate=yes;')

cursor = conn.cursor()

query = '''
        select count(*) as cnt from dbo.RawData
'''

cursor.execute(query)
cnt = cursor.fetchone()
cnt = round(cnt[0] / 100, 0)

query = '''
        select * from dbo.RawData as rd order by rd.InsertDate desc
'''

while cnt > 0

cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchmany(1)
rows = cursor.fetchmany(1)

print(rows)