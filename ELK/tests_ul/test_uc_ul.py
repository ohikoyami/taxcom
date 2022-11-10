from urllib.parse import urlparse, parse_qs
import json
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


def test_buy_cert():

    # оформление покупки ЭП
    driver.find_element(By.XPATH,
                        "//div[@class='ng-scope']//a[@class='product-link-button btn btn-primary product-can-enable']").click()

    # выбор ЭП
    driver.find_element(By.XPATH, "//div[@class='ng-scope']//a[contains(@href,'QSERTULFNS')]").click()

    driver.implicitly_wait(15)

    if auto == 'y':

        # Заполнение почты
        driver.find_element(By.XPATH, "//input[@name = 'regCard_AbonentContext_Email']").click()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_AbonentContext_Email']").clear()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_AbonentContext_Email']").send_keys('order@rubetek.com')

        driver.implicitly_wait(15)

        # Заполнение огрн
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_Ogrn']").click()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_Ogrn']").clear()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_Ogrn']").send_keys('1105753000352')

        driver.implicitly_wait(15)

        # Заполнение Полного имени компании
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_CompanyFullName']").click()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_CompanyFullName']").clear()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_CompanyFullName']").send_keys('ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "РУБЕТЕК РУС"')

        driver.implicitly_wait(15)

        # Заполнение Короткого имени компании
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_CompanyShortName']").click()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_CompanyShortName']").clear()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_CompanyData_CompanyShortName']").send_keys('ООО "РУБЕТЕК РУС"')

        driver.implicitly_wait(15)

        # Заполнение телефона
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Boss_Phone']").click()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Boss_Phone']").clear()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Boss_Phone']").send_keys('9208294615')

        driver.implicitly_wait(15)

        # Заполнение почты руководителя
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Boss_Email']").click()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Boss_Email']").clear()
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Boss_Email']").send_keys('order@rubetek.com')

        driver.implicitly_wait(15)

        # Заполнение фио контактного лица
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

    # отправление заявки на оформление услуги
    driver.find_element(By.XPATH, "//a[@class='btn btn-success step-button pull-right']").click()


# отмена оформленной заявки
def test_cancel():
    driver.implicitly_wait(15)

    driver.find_element(By.XPATH, "//div[@id='requestCancelButton']//a[@class='btn btn-danger']")

    # получение текущей url
    urlpars = driver.current_url

    # парсинг ссылки
    r = urlparse(urlpars)

    # сохранение нужного параметра ссылки
    requestid = parse_qs(r.query)['requestId'][0]

    # сохранение тееущего requestid
    res_str = requestid.replace('requestId=', '')

    # запись requestid и thumbprint файликом
    directory_folder = r"C:\Users\User\Desktop\for_zaglushki\last_request_id\uc"
    with open(fr'{directory_folder}\{res_str}.json', 'x') as outfile:
        json.dump({
            "thumbprint": 'ED647769C9FE2B757507525DAAF79EB82929EDF1',
        }, outfile)

    # нажатие на кнопку отмена
    driver.find_element(By.XPATH, "//div[@id='requestCancelButton']//a[@class='btn btn-danger']").click()

    driver.implicitly_wait(15)

    # подтверждение отмены заявки
    driver.find_element(By.XPATH, "//div[@class='modal-footer']//a[contains(@href,'CancelRequestByRequestId')]").click()


# завершение автотеста с закрытием окон
def test_teardown():
    driver.close()
    driver.quit()
    print("Test Completed")
