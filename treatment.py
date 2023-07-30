import pandas as pd
import re
import openpyxl
from openpyxl import load_workbook


# year_file = input("Введи название файла: ")

def CreateTrainExcelFile(year_file):
    '''Функция обрабатывает файл excel с данными о продажах(пономенклатурно)
        и записывает в заранее созданный для модели excel файл
        (который содержит суммарное количество деталей по DN)'''

    # Отделение года от названия файла(фактически отрезаем с конца ".xls")
    #for i in year_file:
    #    if i.isnumeric():
    #        if len(yearss)<=4:
    #            yearss += i
    k = ''
    for i in year_file:
        if i.isdigit() and len(k) < 4:
            k += i

    #nums = re.findall(r'\d+', year_file[:-4])
    #year = [int(i) for i in nums][0]
    year = int(k)
    # Читаем указанный файл
    data = pd.read_excel(year_file)
    # Проверяем, сколько раз встречается год в названиях столбца(так мы определяем, сколько месяцев заполнено в таблице)
    # Удаляем первые 8 строк (бесполезные скрытые строки в excel)
    data = data.drop(range(8))
    # Первую строку делаем столбцами, т.к. так надо
    data.columns = data.iloc[0]
    # Выбрасываем первый столбец т.к. он пустой
    data = data.drop(columns = data.columns[0], axis=0).fillna(0)
    # ВЫБРАСЫВАЕМ ИТОГ 
    data = data.drop(columns = 'Итог', axis=0).fillna(0)
    # Удаляем первые две строки за бесполезностью
    data = data.iloc[2:]
    kol_month = sum([1 if str(year) in i else 0 for i in list(data.columns)])
    
    # Список всех DN
    Dn_list=[15, 20, 25, 32, 40, 50, 65, 80, 100, 125, 150, 200]
    
    for i in Dn_list:
        DN = str(i)
        # копируем обработанный файл для безопасности
        data_now = data.copy()
        # Удаляем строки без "шт" в названии
        data_now = data_now[data_now['Номенклатура, Базовая единица измерения'].str.contains('шт')] 
        # Выбираем все строки с нужным диаметром
        data_now_DN = data_now[data_now['Номенклатура, Базовая единица измерения'].str.contains('DN' + DN +" ")] 
        # Удаляем лишний столбец
        del data_now_DN['Номенклатура, Базовая единица измерения']
        # считаем сумму, чтобы получить количество нужного диаметра
        data_now_DN_sum = data_now_DN.astype(int).sum(axis=0)
        # получаем временной интервал наших значений
        index_now_DN = list(pd.date_range(str(year) + "-01-01", freq='M', periods=kol_month))
        # Делаем индекс временным интервалом для машинного
        data_now_DN_sum.index = index_now_DN
        
        direc = "./train_indb/DN" + str(DN) + ".xlsx" # название обработанного файла excel за прошлые года
        # двумерный список из файла excel за прошлые года
        data_old = pd.read_excel(direc, index_col = False).fillna(0)
        # Делаем Series датафреймом
        data_now_DN_sum = data_now_DN_sum.to_frame()
        # Меняем название колонки чтоб совпало с другим
        data_now_DN_sum.columns = ['Value']
        data_old.index = data_old.pop(data_old.columns[0])
        # удаляем первую колонку (время) и делаем её индексом, в общем удалили столбик с индексами 
        # сохраняем объединение старого и нового
        df3 = pd.concat([data_old, data_now_DN_sum])
        df3 = df3[~df3.index.duplicated(keep='first')]

        df3.to_excel(direc,index=True)

# CreateTrainExcelFile(year_file)
