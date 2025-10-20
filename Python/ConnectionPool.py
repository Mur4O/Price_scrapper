import pyodbc as db

def connToSQL():
    conn = db.connect('driver={ODBC Driver 18 for SQL Server};'
              'server=100.98.191.77;'
              'database=Scrapper;'
              'uid=sa;'
              'pwd=Qwerty11;'
              'encrypt=no;'
              'TrustServerCertificate=yes;')
    return conn