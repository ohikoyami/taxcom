from urllib.parse import urlparse, parse_qs

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
    driver.find_element(By.XPATH, "//div[@data-thumbprint='099EF5319867F8EBB7F7C801941ED811EE440D3F']").click()
    driver.implicitly_wait(15)


def test_buy_cert():

    # оформление покупки ЭП
    driver.find_element(By.XPATH,
                        "//div[@class='ng-scope']/a[@class='product-link-button btn btn-primary product-can-enable']").click()

    # выбор ЭП
    driver.find_element(By.XPATH, "//div[@class='ng-scope']/a[contains(@href,'QRUSR')]").click()

    driver.implicitly_wait(15)

    # заполнение электронной почты
    driver.find_element(By.XPATH,
                        "//input[@class = 'input-field__element ng-pristine ng-untouched ng-empty ng-invalid ng-invalid-required ng-valid-pattern ng-valid-maxlength']").send_keys(
        'hl@jk.kl')

   # заполнение адресов
   # driver.find_element(By.XPATH,
   #                     "//input[@class = 'input-field__element ng-pristine ng-untouched ng-valid-editable ng-valid-maxlength ng-empty ng-invalid ng-invalid-required']").send_keys(
   #     '89')
   # driver.find_element(By.XPATH, "//a[contains(@title,'Вавилова')]").click()

    driver.find_element(By.XPATH,
                        "//input[@value='Qual61']").click()

    # нажатие "далее" на форме
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

    # запись requestid файликом
    directory_folder = r"C:\Users\User\Desktop\for_zaglushki\last_request_id\add_serv\uc_rosreestr_add_serv"
    test = open(f'{directory_folder}/{res_str}.txt', 'w')
    test.write(f'No text. This is file {res_str}.txt')
    test.close()

    # нажатие на кнопку отмена
    driver.find_element(By.XPATH, "//div[@id='requestCancelButton']/a[@class='btn btn-danger']").click()

    driver.implicitly_wait(15)

    # подтверждение отмены заявки
    driver.find_element(By.XPATH, "//div[@class='modal-footer']//a[contains(@href,'CancelRequestByRequestId')]").click()


# завершение автотеста с закрытием окон
def test_teardown():
    driver.close()
    driver.quit()
    print("Test Completed")
