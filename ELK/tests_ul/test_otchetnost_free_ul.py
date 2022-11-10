from telnetlib import EC
from urllib.parse import urlparse, parse_qs
import  json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def auto_func(yes_no):
    global auto
    auto = yes_no

auto_func('y')

# настройка запуска Chrome и запуск ЕЛК
def test_setup():
    global driver
    driver = webdriver.Chrome(executable_path="C:/chromedriver.exe")
    driver.maximize_window()
    driver.get("https://elk-ladoga.taxcom.ru")
    driver.implicitly_wait(15)


# авторизация в ЕЛК
def test_login():

    # вход под сертификатом
    driver.find_element(By.XPATH, "//div[@data-thumbprint='ED647769C9FE2B757507525DAAF79EB82929EDF1']").click()
    driver.implicitly_wait(15)


# оформление покупки отчетности
def test_buy_cert():

    # выбор прдукта отчетности
    driver.find_element(By.XPATH,
                        "//div[@class='ng-scope']//a[@class='product-link-button btn btn-primary product-can-enable ng-binding ng-scope']").click()

    # выбор тарифа Удобный.Спецрежим
    driver.find_element(By.XPATH,
                        "//div[@class='tariff tariff-container-common']//a[contains(@data-tplan,'Ознакомительный')]").click()

    driver.implicitly_wait(15)

    if auto == 'y':

        #Заполнение фнс вручную
        driver.find_element(By.XPATH,
                            "//input[@name='inputFns']")
        driver.find_element(By.XPATH,
                            "//input[@name='inputFns']").click()
        driver.find_element(By.XPATH, "//input[@name='inputFns']").clear()
        driver.find_element(By.XPATH, "//input[@name='inputFns']").send_keys('0277')

        driver.find_element(By.XPATH,
                            "//form/span/ul/li/a[contains( @title, '0277')]")
        driver.find_element(By.XPATH,
                            "//a[contains( @title, '0277')]").click()

        driver.implicitly_wait(15)

    # переход на страницу данные о владельце электронной подписи
    driver.find_element(By.XPATH, "//button[@class='button button--primary']")
    driver.find_element(By.XPATH, "//button[@class='button button--primary']").click()

    driver.implicitly_wait(15)

    if auto == 'y':

        # Заполнение огрн
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
        driver.find_element(By.XPATH, "//input[@name = 'regCard_Boss_FIO']").send_keys('order@rubetek.com')

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

    # переход на страницу заключения договора
    driver.find_element(By.XPATH,
                        "//a[@class='button button_border ng-hide']/../button[contains(text(), 'Продолжить')]").click()
    driver.find_element(By.XPATH, "//button[@class='button button--secondary']").click()

    # ожидание загрузки заявления на оказание услуг
    WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.ID, "zayavPdf"))).click()

    driver.implicitly_wait(15)

    # подтверждение заявления на оказание услг и оформление заявки
    driver.find_element(By.XPATH, "//div[@class = 'modal-footer']/button[@class='button button--primary']").click()


# отмена оформленной заявки
def test_cancel():
    driver.implicitly_wait(15)
    driver.find_element(By.XPATH, "//a[contains(@href,'#confirmCancelModal')]")

    # получение текущей url
    urlpars = driver.current_url

    # парсинг ссылки
    r = urlparse(urlpars)

    # сохранение нужного параметра ссылки
    requestid = parse_qs(r.query)['requestId'][0]

    # сохранение тееущего requestid
    res_str = requestid.replace('requestId=', '')

    # запись requestid и thumbprint файликом
    directory_folder = r"C:\Users\User\Desktop\for_zaglushki\last_request_id\otchetnost_free"
    with open(fr'{directory_folder}\{res_str}.json', 'x') as outfile:
        json.dump({
            "thumbprint": 'ED647769C9FE2B757507525DAAF79EB82929EDF1',
        }, outfile)

    # нажатие на кнопку отмена
    driver.find_element(By.XPATH, "//a[contains(@href,'#confirmCancelModal')]").click()

    driver.implicitly_wait(15)

    # подтверждение отмены заявки
    driver.find_element(By.XPATH, "//div[@class='modal-footer']//a[contains(@href,'CancelRequestByRequestId')]").click()

# отмена оформленной заявки
def test_teardown():
    driver.close()
    driver.quit()
    print("Test Completed")