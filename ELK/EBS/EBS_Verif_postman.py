import json
import sys

import pyodbc
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

dirname = 'C:/Users/User/Desktop/for_zaglushki'

conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=STAGE-ELKDB;'
    'Database=ELK;'
    'UID=ttc;'
    'PWD=ttc;'
    'Trusted_Connection=no;')

requestid = 'F94F84E2-6C44-4D66-94BE-1231358DACA1'

dir = r"\\LADOGA\DummyService\rdbservice\result"

r = "https://id-stage.taxcom.ru/api/identification/TaxIdSessions"

cur = conn.cursor()
sql = f"""
select TOP(1) NEWID() as sessionid
    """
rows = cur.execute(sql)
for row in rows.fetchall():
    sessionid = row[0]
conn.commit()

data = {"sessionId": f"{sessionid}", "verificationType": "EBS", "sessionRequestSource": "TUS"}
req = requests.post(r, json=data)
TaxSessionID = json.loads(req.text)
new_url = TaxSessionID['redirectUrl']
print(sessionid)
print(new_url)

def launchBrowser():
    s = Service('C:/Users/User/Desktop/for_zaglushki/chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    driver.get(f'{new_url}')
    return driver


driver = launchBrowser()
#
# driver.implicitly_wait(15)
#
# driver.find_element(By.XPATH,
#                     "//button[@class = 'CtaButton_cta-button__zKL2w CtaButton_cta-button_primary__v0JEP']").click()

StartVer = f'https://id-stage.taxcom.ru/api/identification/WebSessions/{sessionid}/Verification'
reqStartVer = requests.post(StartVer)
PostStartVer = json.loads(reqStartVer.text)
new_url = PostStartVer['redirectUrl']
print('Start Verification')


def launchBrowser():
    driver.get(f'{new_url}')
    return driver


driver = launchBrowser()

driver.find_element(By.XPATH,
                    "//input[@id = 'login']").send_keys('+7 (916) 697-71-76')
driver.find_element(By.XPATH,
                    "//input[@id = 'password']").send_keys('GdvDXcjo2@')
driver.find_element(By.XPATH,
                    "//span[@class = 'ui-button-text']").click()

driver.implicitly_wait(15)

# cur = conn.cursor()
# sql = f"""
# SELECT TOP (1)[EsiaSid]
#   FROM [TaxcomID].[dbo].[EsiaSessions]
#   order by id desc
#     """
# rows = cur.execute(sql)
# for row in rows.fetchall():
#     EsiaSid = row[0]
# conn.commit()
#
# data = {
#     "personalData": {
#         "clientData": {
#             "rIdDoc": '201757',
#             "firstName": "Сидр",
#             "lastName": "Иванов-Сидоров",
#             "middleName": "Сидорович",
#             "birthDate": "1990-05-01T00:00:00",
#             "birthPlace": None,
#             "gender": None,
#             "trusted": True,
#             "citizenship": "RUS",
#             "snils": "032-539-153 34",
#             "inn": "181087944870",
#             "updatedOn": '1639750462',
#             "verifying": True,
#             "status": "REGISTERED"
#         },
#         "documents": [
#             {
#                 "type": "RF_PASSPORT",
#                 "vrfStu": "VERIFIED",
#                 "actNo": None,
#                 "actDate": None,
#                 "series": "4459",
#                 "number": "114381",
#                 "issueDate": "2009-02-01T00:00:00",
#                 "issueId": "715631",
#                 "issuedBy": "ОУФМС России",
#                 "expiryDate": None,
#                 "lastName": None,
#                 "firstName": None,
#                 "vrfValStu": None,
#                 "vrfReqId": None,
#                 "fmsValid": None,
#                 "eTag": "BEB733FEF60E445C692C5EA40B9A690B08E2381B"
#             }
#         ]
#     }
# }
# r = f'https://id-stage.taxcom.ru/api/identification/EsiaSessions/{EsiaSid}/VerifiedResults'
# req = requests.post(r, json=data)
# print(req)
# print('Save Verified Results')

GetEsia = f'https://id-stage.taxcom.ru/api/identification/EsiaSessions/{sessionid}/VerifiedResults'
reqGetEsia = requests.get(GetEsia)

print(reqGetEsia)
print('Get Results')

driver.implicitly_wait(15)

driver.find_element(By.XPATH,
                    "//h2[contains(text(), 'Личность подтверждена')]")

driver.close()
driver.quit()

print('Тестирование завершено успешно')
