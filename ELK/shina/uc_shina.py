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

def out_red(red):
    print('\033[31m{}'.format(red))

def out_green(green):
    print('\033[32m{}'.format(green))

def out_gray(gray):
    print('\033[0m{}'.format(gray))

if len(os.listdir(r'C:\Users\User\Desktop\for_zaglushki\last_request_id\uc')) == 0:
    out_red("Directory is empty")
    num = 0
else:
    out_green("Directory is not empty")
    num = 1

while num != 0:

    num_files = sum(os.path.isfile(os.path.join(r'C:\Users\User\Desktop\for_zaglushki\last_request_id\uc', f)) for f in os.listdir(r'C:\Users\User\Desktop\for_zaglushki\last_request_id\uc'))
    out_gray(f'Осталось протестировать заявок: {num_files} ')
    # Запуск службы Taxcom Kafka Consumer Service
    subprocess.run([f'{dirname}/TKS_start.bat', '-u', 'root'])

    out_gray('Служба Taxcom Kafka Consumer Service запущена')

    time.sleep(5)

    # Запись RequestID в переменную requestid
    list_of_files = glob.glob(
        r"C:\Users\User\Desktop\for_zaglushki\last_request_id\uc\*")
    latest_file = min(list_of_files, key=os.path.getctime)
    path = Path(latest_file)
    requestid = path.stem

    out_green(f'Начало тестирования Заглушки по заявке {requestid}')

    out_gray('')

    # Остановка службы Taxcom Kafka Consumer Service
    subprocess.run([f'{dirname}/TKS_stop.bat', '-u', 'root'])

    out_gray('Служба Taxcom Kafka Consumer Service остановлена')

    # Присвоение заявке статуса 1
    cur = conn.cursor()
    sql = f"""
    update [ELK].[dbo].[bus_requests]
    set request_status = 1, status_date = GETDATE()
     where request_id = '{requestid}'
    """
    rows = cur.execute(sql)
    conn.commit()

    # Проверка, что в таблице bus_requests появилась эта заявка со статусом 1
    cur = conn.cursor()
    sql = f"""
    SELECT [request_status]
      FROM [ELK].[dbo].[bus_requests]
      where request_id = '{requestid}'
    """
    rows = cur.execute(sql)
    for row in rows.fetchall():
        if row[0] == 1:
            out_green(f'У заявки {requestid} корректный статус {row[0]}')
        else:
            out_red(f'У заявки {requestid} некорректный статус {row[0]}')
            sys.exit()
    conn.commit()

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


    # Добавление строчек о версии в найденный файл
    if corr > 0:
        xmlf = fr"\\LADOGA\DummyService\rdbservice\input\{nfname}"
        tree = et.parse(xmlf, parser=et.XMLParser(encoding="iso-8859-5"))
        root = tree.getroot()
        ver = et.Element('Version')
        ver.text = '701350022'
        root.insert(0, ver)

        name = root.find('Version')
        text = name.text
        name.clear()

        num = et.SubElement(name, "Number")
        num.text = text

        fv = et.SubElement(name, "FormatVersion")
        fv.text = 'AddEventDataXML.8.1.3.159'

        tree.write(xmlf)

        out_gray(f'В файл AddEventDataXML.{requestid}.xml успешно добавлены строчки')

    # Перенос и переименование файла AddEventDataXML.{requestid}.xml в папку result
        b_dir = fr"\\LADOGA\DummyService\rdbservice\input\{nfname}"
        n_dir = fr"\\LADOGA\DummyService\rdbservice\result\{nfname}"
        shutil.move(b_dir, n_dir)

        fold_name = os.path.join(fr"\\LADOGA\DummyService\rdbservice\result", nfname)
        fnew_name = os.path.join(fr"\\LADOGA\DummyService\rdbservice\result", f'AddEventDataXML.{requestid}.xml')
        os.rename(fold_name, fnew_name)

        out_green(f"Файл {fnew_name} успешно перенесен в папку result")
    else:
        out_red(f'AddEventDataXML.{requestid}.xml файла нет')
        sys.exit()

    out_gray('')

    # Перезапуск службы Taxcom Kafka Consumer Service
    subprocess.run([f'{dirname}/TKS_restart.bat', '-u', 'root'])


    out_gray('Служба Taxcom Kafka Consumer Service перезапущена')

    # Поиск инн в файле
    inn = fr"\\LADOGA\DummyService\rdbservice\result\AddEventDataXML.{requestid}.xml"
    e = et.parse(inn, parser=et.XMLParser(encoding="iso-8859-5"))
    for el in e.getroot().findall("Events/Event/Data/NewRCDataEvent/INN"):
        inn = el.text
    inn = int(inn)
    # Поиск номера в очереди заявки
    cur = conn.cursor()
    sql = f"""
    SELECT TOP(1)
    JSON_VALUE (LogEvent, '$.Properties.offset') as offset
    FROM [ttc_log].[dbo].[LogEvents] with(nolock)
    where inn = '{inn}'
    and Message like '%elk_uc_connection_ladoga%'
    and MessageTemplate LIKE '%Ожидание завершено.%'
    order by id desc
    """
    rows = cur.execute(sql)
    for row in rows.fetchall():
        offset = row[0]

    sql = f"""
       SELECT TOP(1)
       JSON_VALUE (LogEvent, '$.Properties.partition') as partition
       FROM [ttc_log].[dbo].[LogEvents] with(nolock)
       where inn = '{inn}'
       and Message like '%elk_uc_connection_ladoga%'
       and MessageTemplate LIKE '%Ожидание завершено.%'
       order by id desc
       """
    rows = cur.execute(sql)
    for row in rows.fetchall():
        partition = row[0]
    conn.commit()

    out_gray(f'Очередь заявки = {offset}')

    # Откат очереди заявки
    partition = partition.replace('[', '').replace(']', '')
    offset = int(offset)

    cur = conn.cursor()
    sql = f"""
    update [information_service].[dbo].[kafka_offsets]
    set lastoffset = {offset - 1}
    where topic = 'elk_uc_connection_ladoga' and partition_number = {partition};
    """
    cur.execute(sql)
    conn.commit()

    out_gray(f'Откат позиции lastoffset на единицу назад (до {offset - 1}) в partition {partition}')

    # Запуск службы Taxcom Kafka Consumer Service
    subprocess.run([f'{dirname}/TKS_start.bat', '-u', 'root'])

    out_gray('Служба Taxcom Kafka Consumer Service запущена')

    # Провекрка статуса заявки 3
    cur = conn.cursor()
    sql = f"""
    SELECT [request_status]
      FROM [ELK].[dbo].[bus_requests]
      where request_id = '{requestid}'
    """
    flag = 0
    while flag < 100:
        rows = cur.execute(sql)
        for row in rows.fetchall():
            time.sleep(5)
            if row[0] == 3:
                flag = 100
            flag = flag+1
    if row[0] != 3:
        out_red(f'У заявки {requestid} некорректный статус {row[0]}')
        sys.exit()
    else:
        out_green(f'У заявки {requestid} корректный статус {row[0]}')
    conn.commit()

    out_gray('')

    # Остановка службы Job Manager
    subprocess.run([f'{dirname}/Job_stop.bat', '-u', 'root'])

    out_gray('Служба Job Manager остановлена')

    # Добавление записи в Мегалог
    cur = conn.cursor()
    sql = f"""
    insert into [mega_log].[dbo].[Events]
    values
    (GETDATE(), GETDATE(), '{requestid}', 15, 2,'', 1,5,'','','', NULL, 0, NULL, NULL)
    """
    rows = cur.execute(sql)
    conn.commit()
    out_gray('В megalog добавлена запись со статусом 2')

    # Служба Job Manager запущена
    subprocess.run([f'{dirname}/Job_start.bat', '-u', 'root'])

    out_gray('Служба Job Manager запущена')

    # Проверка статуса заявки 7
    cur = conn.cursor()
    sql = f"""
    SELECT [request_status]
      FROM [ELK].[dbo].[bus_requests]
      where request_id = '{requestid}'
    """

    flag = 0
    while flag < 100:
        rows = cur.execute(sql)
        for row in rows.fetchall():
            time.sleep(5)
            if row[0] == 7:
                flag = 100
            flag = flag+1
    if row[0] != 7:
        out_red(f'У заявки {requestid} некорректный статус {row[0]}')
        sys.exit()
    else:
        out_green(f'У заявки {requestid} корректный статус {row[0]}')
    conn.commit()

    # Удаление заявок с теми же номерами счетов из базы
    cur = conn.cursor()
    sql = '''delete from [OMP16].[dbo].[Bill1CPaymentState]
    where _number = 'QL00985801' or _number = 'QL00985802' '''
    rows = cur.execute(sql)
    conn.commit()

    # Перенос и переименование файла GetEventDataXML.LoadRCDataCRM_DetailsProcessed.{requestid}.xml
    b_dir = r'\\LADOGA\xmls\GetEventDataXML.LoadRCDataCRM_DetailsProcessed.02067dd8-09fd-4a74-b87f-fe414bb13ad6.xml'
    n_dir = fr'\\LADOGA\DummyService\rdbservice\result\GetEventDataXML.LoadRCDataCRM_DetailsProcessed.{requestid}.xml'
    shutil.copy(b_dir, n_dir)
    out_gray(f'Файл GetEventDataXML.LoadRCDataCRM_DetailsProcessed.{requestid}.xml успешно перенесен в папку result')

    # Проверка статуса заявки 8
    cur = conn.cursor()
    sql = f"""
    SELECT [request_status]
      FROM [ELK].[dbo].[bus_requests]
      where request_id = '{requestid}'
    """

    flag = 0
    while flag < 100:
        rows = cur.execute(sql)
        for row in rows.fetchall():
            time.sleep(5)
            if row[0] == 8:
                flag = 100
            flag = flag+1
    if row[0] != 8:
        out_red(f'У заявки {requestid} некорректный статус {row[0]}')
        sys.exit()
    else:
        out_green(f'У заявки {requestid} корректный статус {row[0]}')
    conn.commit()

    # Служба Job Manager остановлена
    subprocess.run([f'{dirname}/Job_stop.bat', '-u', 'root'])

    out_gray('Служба Job Manager остановлена')

    # Добавление номера счетов заявки
    cur = conn.cursor()
    sql = '''insert into [OMP16].[dbo].[Bill1CPaymentState]
    values
    (4000, 4000,'QL00985801') '''
    rows = cur.execute(sql)
    sql = '''insert into [OMP16].[dbo].[Bill1CPaymentState]
    values
    (4000, 4000,'QL00985802') '''
    rows = cur.execute(sql)
    conn.commit()
    out_gray('Номера счетов заявки успешно добавлены в базу данных')

    # Служба Job Manager запущена
    subprocess.run([f'{dirname}/Job_start.bat', '-u', 'root'])

    out_gray('Служба Job Manager запущена')

    # Проверка статуса заявки 9
    cur = conn.cursor()
    sql = f"""
    SELECT [request_status]
      FROM [ELK].[dbo].[bus_requests]
      where request_id = '{requestid}'
    """
    flag = 0
    while flag < 100:
        rows = cur.execute(sql)
        for row in rows.fetchall():
            time.sleep(5)
            if row[0] == 9:
                flag = 100
            flag = flag+1
    if row[0] != 9:
        out_red(f'У заявки {requestid} некорректный статус {row[0]}')
        sys.exit()
    else:
        out_green(f'У заявки {requestid} корректный статус {row[0]}')
    conn.commit()

    # Перенос файла GetEventDataXML.NewCertSMEV.xml в папку reault
    b_dir = r'\\LADOGA\xmls\GetEventDataXML.NewCertSMEV.xml '
    n_dir = fr'\\LADOGA\DummyService\rdbservice\result\GetEventDataXML.NewCertSMEV.xml '
    shutil.copy(b_dir, n_dir)
    out_gray('Файл GetEventDataXML.NewCertSMEV.xml успешно перенесен в папку result')

    # Проверка статуса заявки 4
    cur = conn.cursor()
    sql = f"""
    SELECT [request_status]
      FROM [ELK].[dbo].[bus_requests]
      where request_id = '{requestid}'
    """
    flag = 0
    while flag < 100:
        rows = cur.execute(sql)
        for row in rows.fetchall():
            time.sleep(5)
            if row[0] == 4:
                flag = 100
            flag = flag+1
    if row[0] != 4:
        out_red(f'У заявки {requestid} некорректный статус {row[0]}')
        sys.exit()
    else:
        out_green(f'У заявки {requestid} корректный статус {row[0]}')
    conn.commit()

    out_gray('')

    # Служба Job Manager остановлена
    subprocess.run([f'{dirname}/Job_stop.bat', '-u', 'root'])

    out_gray('Служба Job Manager остановлена')

    # Перенос файла GetEventDataXML.Realization1C.xml в папку result
    b_dir = r'\\LADOGA\xmls\GetEventDataXML.Realization1C.xml'
    n_dir = fr'\\LADOGA\DummyService\rdbservice\result\GetEventDataXML.Realization1C.xml'
    shutil.copy(b_dir, n_dir)
    out_gray('Файл GetEventDataXML.Realization1C.xml успешно перенесен в папку result')

    # Перенос файла GetEventDataXML.RealizationRequest1C.xml в папку result
    b_dir = r'\\LADOGA\xmls\GetEventDataXML.RealizationRequest1C.xml'
    n_dir = fr'\\LADOGA\DummyService\rdbservice\result\GetEventDataXML.RealizationRequest1C.xml '
    shutil.copy(b_dir, n_dir)
    out_gray('Файл GetEventDataXML.RealizationRequest1C.xml успешно перенесен в папку result')

    # Перенос файла GetEventDataXML.LoadRCDataCRM_Done.{requestid}.xml в папку result
    b_dir = r'\\LADOGA\xmls\GetEventDataXML.LoadRCDataCRM_Done.380f9a13-b053-4b92-ad4b-0bef516842fe.xml'
    n_dir = fr'\\LADOGA\DummyService\rdbservice\result\GetEventDataXML.LoadRCDataCRM_Done.{requestid}.xml'
    shutil.copy(b_dir, n_dir)
    out_gray(f'Файл GetEventDataXML.LoadRCDataCRM_Done.{requestid}.xml успешно перенесен в папку result')

    # Служба Job Manager запущена
    subprocess.run([f'{dirname}/Job_start.bat', '-u', 'root'])

    out_gray('Служба Job Manager запущена')

    # Проверка статуса заявки 10
    cur = conn.cursor()
    sql = f"""
    SELECT [request_status]
      FROM [ELK].[dbo].[bus_requests]
      where request_id = '{requestid}'
    """
    flag = 0
    while flag < 100:
        rows = cur.execute(sql)
        for row in rows.fetchall():
            time.sleep(5)
            if row[0] == 10:
                flag = 100
            flag = flag+1
    if row[0] != 10:
        out_red(f'У заявки {requestid} некорректный статус {row[0]}')
        sys.exit()
    else:
        out_green(f'У заявки {requestid} корректный статус {row[0]}')
    conn.commit()


    # Отмена заявки
    cur = conn.cursor()
    sql = f"""
    update [ELK].[dbo].[bus_requests]
    set request_status = 5, status_date = GETDATE()
    where request_id = '{requestid}'
    """
    cur.execute(sql)
    out_gray('Заявка отменена')
    conn.commit()

    # Проверка статуса заявки 5
    cur = conn.cursor()
    sql = f"""
    SELECT [request_status]
      FROM [ELK].[dbo].[bus_requests]
      where request_id = '{requestid}'
    """
    flag = 0
    while flag < 100:
        rows = cur.execute(sql)
        for row in rows.fetchall():
            time.sleep(5)
            if row[0] == 5:
                flag = 100
            flag = flag+1
    if row[0] != 5:
        out_red(f'У заявки {requestid} некорректный статус {row[0]}')
        sys.exit()
    else:
        out_green(f'У заявки {requestid} корректный статус {row[0]}')
    conn.commit()

    out_gray('')

    # Служба Job Manager остановлена
    subprocess.run([f'{dirname}/Job_stop.bat', '-u', 'root'])

    out_gray('Служба Job Manager остановлена')


    # Остановка службы Taxcom Kafka Consumer Service
    subprocess.run([f'{dirname}/TKS_stop.bat', '-u', 'root'])

    out_gray('Служба Taxcom Kafka Consumer Service остановлена')

    # Перемещение файла рассмотренной заявки в папку обработано
    base_dir = os.path.dirname(path.name)
    new_dir = fr"C:\Users\User\Desktop\for_zaglushki\obrabotano\{path.name}"
    shutil.move(latest_file, new_dir)

    # Очищение папки result
    dir = r"\\LADOGA\DummyService\rdbservice\result"
    os.remove(os.path.join(dir, f'AddEventDataXML.{requestid}.xml'))
    os.remove(os.path.join(dir, f'GetEventDataXML.LoadRCDataCRM_Done.{requestid}.xml'))
    os.remove(os.path.join(dir, f'GetEventDataXML.LoadRCDataCRM_DetailsProcessed.{requestid}.xml'))
    os.remove(os.path.join(dir, f'GetEventDataXML.NewCertSMEV.xml'))
    os.remove(os.path.join(dir, f'GetEventDataXML.Realization1C.xml'))
    os.remove(os.path.join(dir, f'GetEventDataXML.RealizationRequest1C.xml '))
    os.remove(os.path.join(dir, f'GetEventDataXML.{requestid}.xml'))

    out_green("Тестирование завершено успешно")

    if len(os.listdir(r'C:\Users\User\Desktop\for_zaglushki\last_request_id\uc')) == 0:
        out_red("Directory is empty")
        num = 0
    else:
        out_green("Directory is not empty")
        num = 1
os.remove(os.path.join(dir, f'GetEventDataXML.xml'))
out_green('Все заявки были обработаны')
# os.chdir(dirname)
# os.startfile("TKS_start.bat")
# os.chdir(dirname)
# os.startfile("TKS_stop.bat")
# os.chdir(dirname)
# os.startfile("TKS_restart.bat")
