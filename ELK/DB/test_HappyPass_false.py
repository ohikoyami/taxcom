import pyodbc

conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=LADOGADB;'
    'Database=ELK;'
    'UID=ttc;'
    'PWD=ttc;'
    'Trusted_Connection=no;')
cur = conn.cursor()
sql = """
update [ELK].[dbo].[UCSpecialList]
set [Name] = 'УЦ ООО ""Такском"" (ГОСТ2012)'
where ProductType = 'UC,EDO,FILER,CryptoPro,CryptoProV5'
"""
cur.execute(sql)
conn.commit()
print(cur.rowcount, 'record(s) affected')
conn.close()
print('ok')
