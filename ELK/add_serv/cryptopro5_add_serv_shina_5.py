import glob
import os
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as et
from pathlib import Path

import pyodbc

# Обозначение директории с RequestID
dirname = 'C:/Users/User/Desktop/for_zaglushki'

# Добавление файла GetEventDataXML.xml в папку result
b_dir = r'\\LADOGA\xmls\GetEventDataXML.xml'
n_dir = fr'\\LADOGA\DummyService\rdbservice\result\GetEventDataXML.xml'
shutil.copy(b_dir, n_dir)
print("В папку result добавлен файл GetEventDataXML.xml")

# Подключение к базе данных LADOGADB
conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=LADOGADB;'
    'Database=ELK;'
    'UID=ttc;'
    'PWD=ttc;'
    'Trusted_Connection=no;')

# Проверка наличия файлов в директории
if len(os.listdir(r'C:\Users\User\Desktop\for_zaglushki\last_request_id\add_serv\cryptopro5_add_serv_5')) == 0:
    print("Directory is empty")
    num = 0
else:
    print("Directory is not empty")
    num = 1

# Основной цикл программы
while num != 0:

    # Количество файлов, которые осталось протестировать
    num_files = sum(
        os.path.isfile(os.path.join(r'C:\Users\User\Desktop\for_zaglushki\last_request_id\add_serv\cryptopro5_add_serv_5', f)) for f in
        os.listdir(r'C:\Users\User\Desktop\for_zaglushki\last_request_id\add_serv\cryptopro5_add_serv_5'))
    print(f'Осталось протестировать заявок: {num_files} ')

    # Запуск службы Taxcom Kafka Consumer Service
    subprocess.run([f'{dirname}/TKS_start.bat', '-u', 'root'])

    print('Служба Taxcom Kafka Consumer Service запущена')

    time.sleep(5)

    # Запись RequestID в переменную requestid
    list_of_files = glob.glob(
        r"C:\Users\User\Desktop\for_zaglushki\last_request_id\add_serv\cryptopro5_add_serv_5\*")
    latest_file = min(list_of_files, key=os.path.getctime)
    path = Path(latest_file)
    requestid = path.stem

    print(f'Начало тестирования Заглушки по заявке {requestid}')

    # Остановка службы Taxcom Kafka Consumer Service
    subprocess.run([f'{dirname}/TKS_stop.bat', '-u', 'root'])

    print('Служба Taxcom Kafka Consumer Service остановлена')

    # Поиск файла с необходимым RequestID
    directory = r"\\LADOGA\DummyService\rdbservice\input\*"
    corr = 0
    for filename in glob.glob(directory):
        fname = os.path.basename(filename)
        e = et.parse(filename, parser=et.XMLParser(encoding="iso-8859-5"))
        for el in e.getroot().findall("Events/Event/Identificator"):
            identificator = el.text
            if identificator == requestid:
                corr = corr + 1
                nfname = fname
            else:
                corr = corr + 0

    # Запись дополнительных услуг и их количество в отдельную переменную
    if corr > 0:
        add_serv = ''
        print(f'Начало обработки файла {nfname}')
        xmlf = fr"\\LADOGA\DummyService\rdbservice\input\{nfname}"
        tree = et.parse(xmlf)
        root = tree.getroot()

        addparams = ""

        for item in root.findall('.//AdditionalParameters/Param'):
            id_ = item.attrib.get('Key')
            for child in list(item):
                addparams = addparams + " " + child.text

        if "CPLic50gLim 1" in addparams:
            print("CPLic50gLim Found")
            add_serv = add_serv + '1'
        else:
            print("CPLic50gLim Not Found")
            add_serv = add_serv + 'CPLic50gLim '

        if "CPLic50Num 1" in addparams:
            print("CPLic50Num Found")
            add_serv = add_serv + '1'
        else:
            print("CPLic50Num Not Found")
            add_serv = add_serv + 'CPLic50Num '

        if "CPSP50Serv 1" in addparams:
            print("CPSP50Serv Found")
            add_serv = add_serv + '1'
        else:
            print("CPSP50Serv Not Found")
            add_serv = add_serv + 'CPSP50Serv '

        if "CPOSCnt 1" in addparams:
            print("CPOSCnt Found")
            add_serv = add_serv + '1'
        else:
            print("CPOSCnt Not Found")
            add_serv = add_serv + 'CPOSCnt '

        if "CPTSP 1" in addparams:
            print("CPTSP Found")
            add_serv = add_serv + '1'
        else:
            print("CPTSP Not Found")
            add_serv = add_serv + 'CPTSP '

        # Проверка и вывод отсутствующих услуг
        if add_serv == '11111':
            print('Тестирование прошло успешно')
        else:
            add_serv = add_serv.replace('1', '')
            print(f'В шине отсутствуют данные услуги: {add_serv}')

    # Перенос обрабатываемого файла в папку cryptopro5
    base_dir = os.path.dirname(path.name)
    new_dir = fr"C:\Users\User\Desktop\for_zaglushki\last_request_id\cryptopro5\{path.name}"
    shutil.copy(latest_file, new_dir)

    print('Заявка перенесена в папку cryptopro5')

    # Перенос обрабатываемого файла в папку obrabotano_add_serv
    base_dir = os.path.dirname(path.name)
    new_dir = fr"C:\Users\User\Desktop\for_zaglushki\obrabotano_add_serv\{path.name}"
    shutil.move(latest_file, new_dir)

    print('Заявка перенесена в папку obrabotano_add_serv')

    print("Тестирование завершено")

    # Проверка наличия файлов в директории
    if len(os.listdir(r'C:\Users\User\Desktop\for_zaglushki\last_request_id\add_serv\cryptopro5_add_serv_5')) == 0:
        print("Directory is empty")
        num = 0
    else:
        print("Directory is not empty")
        num = 1
