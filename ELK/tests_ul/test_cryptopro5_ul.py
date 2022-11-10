from urllib.parse import urlparse, parse_qs
import  json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

def auto_func(yes_no):
    global auto
    auto = yes_no

auto_func('y')

# настройка запуска Chrome и запуск ЕЛК
def test_setup():
    global driver
    driver = webdriver.Chrome(executable_path="C:/chromedriver.exe")
    driver.get("https://elk-ladoga.taxcom.ru")
    driver.implicitly_wait(15)


# авторизация в ЕЛК
def test_login():

    # вход под сертификатом
    driver.find_element(By.XPATH, "//div[@data-thumbprint='ED647769C9FE2B757507525DAAF79EB82929EDF1']").click()
    driver.implicitly_wait(15)


# оформление покупки криптопро5
def test_buy_cert():

    # выбор прдукта криптопро5
    driver.find_element(By.XPATH,
                        "//div[contains(text(), 'КриптоПро 5.0')]/../../../div[@class = 'product-footer']/div[@class='product-link']/div/div[@class='ng-scope']/a[@class='product-link-button btn ng-binding ng-scope btn-primary product-can-enable']").click()

    driver.implicitly_wait(15)

    if auto == 'y':

        # Заполнение огрн
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_Ogrn']")
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_Ogrn']").click()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_Ogrn']").clear()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_Ogrn']").send_keys('1105753000352')

        driver.implicitly_wait(15)

        # Заполнение Полного имени компании
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_CompanyFullName']").click()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_CompanyFullName']").clear()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_CompanyFullName']").send_keys(
            'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "РУБЕТЕК РУС"')

        driver.implicitly_wait(15)

        # Заполнение Короткого имени компании
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_CompanyShortName']").click()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_CompanyShortName']").clear()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_CompanyShortName']").send_keys(
            'ООО "РУБЕТЕК РУС"')

        driver.implicitly_wait(15)

        # Заполнение фио руководителя
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Boss_FIO']").click()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Boss_FIO']").clear()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Boss_FIO']").send_keys('ЕВСТАФЬЕВА ДАРЬЯ ИГОРЕВНА')

        driver.implicitly_wait(15)

        # Заполнение должность руководителя
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Boss_Post']").click()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Boss_Post']").clear()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Boss_Post']").send_keys('ГЕНЕРАЛЬНЫЙ ДИРЕКТОР')

        driver.implicitly_wait(15)

        # Заполнение фио руководителя
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Contact_FIO']").click()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Contact_FIO']").clear()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Contact_FIO']").send_keys('ЕВСТАФЬЕВА ДАРЬЯ ИГОРЕВНА')

        driver.implicitly_wait(15)

        # Заполнение телефона контактного лица
        driver.find_element(By.XPATH, "//input[@name = 'regCard_ContactPerson_Phone']").click()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_ContactPerson_Phone']").clear()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_ContactPerson_Phone']").send_keys('9208294615')

        driver.implicitly_wait(15)

        # Заполнение почты контактного лица
        driver.find_element(By.XPATH, "//input[@name = 'regCard_ContactPerson_Email']").click()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_ContactPerson_Email']").clear()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_ContactPerson_Email']").send_keys('order@rubetek.com')

        driver.implicitly_wait(15)

    # нажатие "далее" на форме
    driver.find_element(By.XPATH,
                        "//button[@class='button button--primary']")
    driver.find_element(By.XPATH,
                        "//button[@class='button button--primary']").click()

    driver.implicitly_wait(15)

    # отправление заявки на оформление услуги
    driver.find_element(By.XPATH,
                        "//button[contains(text(), 'Отправить заявку')]").click()


# отмена оформленной заявки
def test_cancel():
    driver.implicitly_wait(15)
    # проверкв нахождения на странице с информацией о заявке
    driver.find_element(By.XPATH,
                        "//h1[@class='product-name']")

    # получение текущей url
    urlpars = driver.current_url

    # парсинг ссылки
    r = urlparse(urlpars)

    # сохранение нужного параметра ссылки
    requestid = parse_qs(r.query)['requestId'][0]

    # сохранение тееущего requestid
    res_str = requestid.replace('requestId=', '')

    # запись requestid и thumbprint файликом
    directory_folder = r"C:\Users\User\Desktop\for_zaglushki\last_request_id\cryptopro5"
    with open(fr'{directory_folder}\{res_str}.json', 'x') as outfile:
        json.dump({
            "thumbprint": 'ED647769C9FE2B757507525DAAF79EB82929EDF1',
        }, outfile)

    # создание ссылки для отмены заявки
    newurl = f'https://elk-ladoga.taxcom.ru/Request/CancelRequestByRequestId?requestId={res_str}'

    # переход по созданной ссылке
    driver.get(newurl)

    # проверка работоспособности ссылки
    prov = requests.get(newurl)
    print(prov.status_code)
    if prov.status_code == 200:
        print('Response OK')
    else:
        print('Response Failed')
        print('Проблема при отмене заявки')
        driver.close()
        driver.quit()


# завершение автотеста с закрытием окон
def test_teardown():
    driver.close()
    driver.quit()
    print("Test Completed")
