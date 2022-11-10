from urllib.parse import urlparse, parse_qs

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


# настройка запуска Chrome и запуск ЕЛК
def test_setup():
    global driver
    driver = webdriver.Chrome(executable_path="C:/chromedriver.exe")
    driver.get("https://elk-ladoga.taxcom.ru")
    driver.implicitly_wait(15)


# авторизация в ЕЛК
def test_login():

    # вход под сертификатом
    driver.find_element(By.XPATH, "//div[@data-thumbprint='7CB12A15DB30ED51401596C0C1E5CEA10FACEBFF']").click()
    driver.implicitly_wait(15)


# оформление покупки криптопро
def test_buy_cert():

    # выбор прдукта криптопро
    driver.find_element(By.XPATH,
                        "//div[contains(text(), 'КриптоПро 4.0')]/../../../div[@class = 'product-footer']/div[@class='product-link']/div/div[@class='ng-scope']/a[@class='product-link-button btn ng-binding ng-scope btn-primary product-can-enable']").click()

    driver.implicitly_wait(15)

    # заполнение адресов
    driver.find_element(By.XPATH,
                       "//input[@class = 'input-field__element ng-pristine ng-untouched ng-valid-editable ng-valid-maxlength ng-empty ng-invalid ng-invalid-required']").send_keys(
       '89')
    driver.find_element(By.XPATH, "//a[contains(@title,'Вавилова')]").click()
    driver.find_element(By.XPATH,
                       "//input[@name = 'regCard_FactAddress']").send_keys('89')
    driver.find_element(By.XPATH, "//a[contains(@title,'Вавилова')]").click()
    driver.find_element(By.XPATH,
                       "//input[@name = 'regCard_PostAddress']").send_keys(
       '89')
    driver.find_element(By.XPATH, "//a[contains(@title,'Вавилова')]").click()

    # нажатие "далее" на форме
    driver.find_element(By.XPATH,
                        "//input[@id='CompanyData_Inn']/../../div/button[@class = 'button button--primary']")
    driver.find_element(By.XPATH,
                        "//input[@id='CompanyData_Inn']/../../div/button[@class = 'button button--primary']").click()

    # Выбор «КриптоПро CSP» сроком действия на 1 год
    driver.find_element(By.XPATH,
                        "//select[@class='form-control ng-pristine ng-untouched ng-valid ng-not-empty']/option[@selected='selected' and contains (text(), '1')]")

    # Проверка цены
    driver.find_element(By.XPATH,
                        "//p[contains(text(), '1100 ₽') and @class = 'ng-binding']")

    # Выбор «КриптоПро Office Signature» (бессрочная)
    driver.find_element(By.XPATH,
                        "//label[contains (text(), 'бессрочная')]/../../div/select[@class='form-control ng-pristine ng-untouched ng-valid ng-not-empty']/option[contains (text(), '1')]").click()
    # Проверка цены
    driver.find_element(By.XPATH,
                        "//p[contains(text(), '2300 ₽') and @class = 'ng-binding']")
    # Выбор «КриптоПро TSP Client»
    driver.find_element(By.XPATH,
                        "//label[contains (text(), 'TSP')]/../../div/select[@class='form-control ng-pristine ng-untouched ng-valid ng-not-empty']/option[contains (text(), '1')]").click()
    # Проверка цены
    driver.find_element(By.XPATH,
                        "//p[contains(text(), '4100 ₽') and @class = 'ng-binding']")
    # Выбор «КриптоПро OCSP Client»
    driver.find_element(By.XPATH,
                        "//label[contains (text(), 'OCSP')]/../../div/select[@class='form-control ng-pristine ng-untouched ng-valid ng-not-empty']/option[contains (text(), '1')]").click()
    # Проверка цены
    driver.find_element(By.XPATH,
                        "//p[contains(text(), '5900 ₽') and @class = 'ng-binding']")
    # Выбор «КриптоПро Revocation Provider»
    driver.find_element(By.XPATH,
                        "//label[contains (text(), 'Revocation')]/../../div/select[@class='form-control ng-pristine ng-untouched ng-valid ng-not-empty']/option[contains (text(), '1')]").click()
    # Проверка цены
    driver.find_element(By.XPATH,
                        "//p[contains(text(), '7700 ₽') and @class = 'ng-binding']")

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

    # запись requestid файликом
    directory_folder = r"C:\Users\User\Desktop\for_zaglushki\last_request_id\add_serv\cryptopro_add_serv"
    test = open(f'{directory_folder}/{res_str}.txt', 'w')
    test.write(f'No text. This is file {res_str}.txt')
    test.close()

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
