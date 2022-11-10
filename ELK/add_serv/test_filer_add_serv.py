from urllib.parse import urlparse, parse_qs

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

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


# оформление покупки файлера
def test_buy_cert():

    driver.implicitly_wait(15)

    # выбор прдукта файлер
    driver.find_element(By.XPATH,
                        "//div[contains(text(), 'Такском-Файлер')]/../../../div[@class = 'product-footer']/div[@class='product-link']/div/div[@class='ng-scope']/a[@class='product-link-button btn ng-binding ng-scope btn-primary product-can-enable']").click()

    driver.implicitly_wait(15)

    # выбор тарифа Исходящие
    driver.find_element(By.XPATH,
                        # "//div[@class='price ng-scope']/span[contains(text(), '1000')]/../../div/a[@class='tariff-select-button btn btn-default tariff-unselected']").click()
                        "//div[@class='filer-tariff-bottom']/span[contains(text(), 'Количество пакетов: 100')]/../div/a[@class='tariff-select-button btn btn-default tariff-unselected']").click()

    # переход на страницу Выбор инспекции и сертификатов
    driver.find_element(By.XPATH,
                        "//div[ @class ='ng-hide'] /../div/button[contains(text(), 'Продолжить')]").click()

    # выбор электронной подписи
    driver.find_element(By.XPATH,
                        "//input[@class ='ng-dirty ng-pristine ng-untouched ng-valid ng-empty']").click()

    # подтверждение лицензионного соглашения
    driver.find_element(By.XPATH,
                        "//span/../input[@class ='ng-dirty ng-pristine ng-untouched ng-valid ng-empty']").click()

    # переход на страницу Выбор опций
    driver.find_element(By.XPATH,
                        "//div[@class='form-registration']/../div/button[@class='button button--secondary pull-right']").click()

    driver.find_element(By.XPATH,
                        "//div[contains(text(), '1500 ₽') and @class = 'cart-total ng-binding']")

    # Выбор
    driver.find_element(By.XPATH,
                        "//div[contains(text(), 'Маркировка')]/../../div[@class = 'additional-filer-service-btn-price ng-scope']/div[contains(text(), 'Выбрать')]").click()
    # Проверка цены
    driver.find_element(By.XPATH,
                        "//div[contains(text(), '2500 ₽') and @class = 'cart-total ng-binding']")
    # Выбор
    driver.find_element(By.XPATH,
                        "//div[contains(text(), 'Web API')]/../../div[@class = 'additional-filer-service-btn-price ng-scope']/div[contains(text(), 'Выбрать')]").click()

    # Проверка цены
    driver.find_element(By.XPATH,
                        "//div[contains(text(), '10500 ₽') and @class = 'cart-total ng-binding']")
    # Выбор
    driver.find_element(By.XPATH,
                        "//div[contains(text(), 'обработка')]/../../div[@class = 'additional-filer-service-btn-price ng-scope']/div[contains(text(), 'Выбрать')]").click()
    # Проверка цены
    driver.find_element(By.XPATH,
                        "//div[contains(text(), '20500 ₽') and @class = 'cart-total ng-binding']")
    # Выбор
    driver.find_element(By.XPATH,
                        "//div[contains(text(), 'Станция Сканирования')]/../../div[@class = 'additional-filer-service-btn-price ng-scope']/div[contains(text(), 'Выбрать')]").click()

    # Проверка цены
    driver.find_element(By.XPATH,
                        "//div[contains(text(), '35500 ₽') and @class = 'cart-total ng-binding']")

    # переход на страницу Договор
    driver.find_element(By.XPATH,
                        "//div[ @class ='additional-filer-service-container'] /../div / button[@ class ='button button--secondary pull-right']").click()

    driver.find_element(By.XPATH,
                        "//div[contains(text(), 'Исходящие')]/../../../../div[@class = 'cart-items-container final']/div/div[@class = 'cart-item-quan']/div[contains(text(), '1500 ₽')]")
    driver.find_element(By.XPATH,
                        "//div[contains(text(), 'Маркировка')]/../../../../div[@class = 'cart-items-container final']/div/div[@class = 'cart-item-quan']/div[contains(text(), '1000 ₽')]")
    driver.find_element(By.XPATH,
                        "//div[contains(text(), 'Web API')]/../../../../div[@class = 'cart-items-container final']/div/div[@class = 'cart-item-quan']/div[contains(text(), '1000 ₽')]")
    driver.find_element(By.XPATH,
                        "//div[contains(text(), 'обработка')]/../../../../div[@class = 'cart-items-container final']/div/div[@class = 'cart-item-quan']/div[contains(text(), '1000 ₽')]")
    driver.find_element(By.XPATH,
                        "//div[contains(text(), 'Станция Сканирования')]/../../../../div[@class = 'cart-items-container final']/div/div[@class = 'cart-item-quan']/div[contains(text(), '1000 ₽')]")

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
    directory_folder = r"C:\Users\User\Desktop\for_zaglushki\last_request_id\add_serv\filer_add_serv"
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
