import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import statsmodels.api as s
from MplCanvasQt import MplCanvas
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

# Чтение данных из Excel-файла

def grafics(y_pred,DN, dover):
    def plotseasonal(res):
        # plt.figure(3)
        sc2.axes.plot(res.seasonal,color="red")
        # res.seasonal.plot( color="red",legend=False)
        sc2.axes.set_ylabel('Сезонность')
        # plt.ylabel('Сезонность')
    
    sc = MplCanvas( width=14, height=6, dpi=100)
    maingrafic = QtWidgets.QMdiSubWindow()
    

    file="./train_indb/"+str(DN)+'.xlsx'
    with open(file, 'rb') as f:
      data = pd.read_excel(f, names=["Дата","Значение"])
    df = data
    df.index = df["Дата"]
    del df["Дата"]
    
    df.plot(ax= sc.axes, figsize = (14, 6), legend = True, color='purple')



#Plot the forecasted values
    y_pred.predicted_mean.plot(ax= sc.axes, label='Предсказание', figsize = (14, 6), grid=True)

#Plot the confidence intervals
    sc.axes.fill_between(dover.index,
                dover.iloc[: , 0],
                dover.iloc[: , 1], color='yellow', alpha = .5)
    # plt.ylabel('шт')
    sc.axes.set_ylabel('шт')
    sc.axes.legend(loc='upper left', prop={'size': 12})
    # plt.legend(loc='upper left', prop={'size': 12})
    toolbar = NavigationToolbar(sc)
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(toolbar)
    layout.addWidget(sc)
    widget = QtWidgets.QWidget()
    widget.setLayout(layout)
    maingrafic.setWidget(widget)
    maingrafic.setWindowTitle("Прогнозирование")

    widgets_graphics = []
    widgets_graphics.append(maingrafic)

    #-----------------------------------------------------------------------------------------------------------
    # return maingrafic
    # plt.show()
#annotation

  


    #сглаженный тренд+данные
    # plt.figure(2)
    sc1 = MplCanvas( width=14, height=6, dpi=100)
    maingrafic1 = QtWidgets.QMdiSubWindow()

    # df.plot(ax=sc1.axes)
    trend = df.rolling(window=8).mean()
    sc1.axes.plot(df.index, trend,color='blue', label='Тренд')
    sc1.axes.plot(df, color='r', label='Данные')
    sc1.axes.legend()
    toolbar1 = NavigationToolbar(sc1)
    layout1 = QtWidgets.QVBoxLayout()
    layout1.addWidget(toolbar1)
    layout1.addWidget(sc1)
    widget1 = QtWidgets.QWidget()
    widget1.setLayout(layout1)
    maingrafic1.setWidget(widget1)
    maingrafic1.setWindowTitle("Сглаженный тренд")
    widgets_graphics.append(maingrafic1)
    #-----------------------------------------------------------------------------------------------------------

    # return widgets_graphics
    # plt.plot(df.index, trend,color='blue', label='Тренд')
    # plt.plot(df, color='r', label='Данные')
    # plt.legend()
    #сезонность+данные

    #находим выбросы. перекидывыаем в массив. и удаляем с исходных данных
    sc2 = MplCanvas( width=14, height=6, dpi=100)
    maingrafic2 = QtWidgets.QMdiSubWindow()
    # df.plot(ax=sc2.axes)
    outliers = df[df['Значение'] > df['Значение'].mean() + 2 * df['Значение'].std()] 
    df_clean = df.drop (index= outliers.index )
    dfc=df_clean
    dfc=dfc.squeeze()
    decomposition = s.tsa.seasonal_decompose(dfc,period=12)
    
    plotseasonal(decomposition)
    # df.plot(ax=sc2.axes)
    toolbar2 = NavigationToolbar(sc2)
    layout2 = QtWidgets.QVBoxLayout()
    layout2.addWidget(toolbar2)
    layout2.addWidget(sc2)
    widget2 = QtWidgets.QWidget()
    widget2.setLayout(layout2)
    maingrafic2.setWidget(widget2)
    maingrafic2.setWindowTitle("Сезоность")
    widgets_graphics.append(maingrafic2)
    #-----------------------------------------------------------------------------------------------------------



    # fig, axes = 
    # sc1.axes.get_figure().add_subplot(111)
    # plt.subplots(ncols=1, nrows=1, sharex=True, figsize=(12,5))
 



    # Выбросы
    outliers = df[df['Значение'] > df['Значение'].mean() + 2 * df['Значение'].std()] 
    print(outliers)

    # Вывод выбросов на графике
    # plt.figure(4)
    sc3 = MplCanvas( width=14, height=6, dpi=100)
    maingrafic3 = QtWidgets.QMdiSubWindow()
    sc3.axes.plot(outliers.index, outliers['Значение'], marker='o', color='blue', linestyle='', label='Выбросы')
    sc3.axes.plot(df, color='r', label='Данные')
    # plt.plot(outliers.index, outliers['Значение'], marker='o', color='blue', linestyle='', label='Выбросы')
    # plt.plot(df, color='r', label='Данные')
    # plt.legend(df, color='r', label='Данные')
    toolbar3 = NavigationToolbar(sc3)
    layout3 = QtWidgets.QVBoxLayout()
    layout3.addWidget(toolbar3)
    layout3.addWidget(sc3)
    widget3 = QtWidgets.QWidget()
    widget3.setLayout(layout3)
    maingrafic3.setWidget(widget3)
    maingrafic3.setWindowTitle("Выбросы")
    widgets_graphics.append(maingrafic3)



    # plt.figure(4)
    # plt.plot(df, color='r', label='Данные')
    # plt.plot(fh,y_pred.predicted_mean, marker='+',color='blue', label='Расчёт модели')
    # plt.legend()


    #общий вывод
    # plt.show()
    return widgets_graphics
#grafics(fh,y_pred,button)

