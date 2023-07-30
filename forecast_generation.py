from sktime.performance_metrics.forecasting import mean_absolute_percentage_error
from sktime.forecasting.sarimax import SARIMAX
from pmdarima import auto_arima
import pandas as pd
# import numpy as np
import statsmodels as sm
import warnings
import building_chart as k
# -------------------
# from pandas.core import window
# import pickle
# import pmdarima

# import mplcyberpunk
# import matplotlib.pyplot as plt

# import sktime
# from sktime.utils.plotting import plot_series
# import statsmodels.api as smapi

# train = pd.read_excel('trainDN15 .xlsx') # набор данных из excel (все данные помесячно за 2015-2021)
# train.columns = ['time', 'det'] # колонки со временем
# train.index = train.pop('time') #

warnings.filterwarnings("ignore")





def Click_OK(DN, srok):
# def Click_OK():
    '''
    DN - надпись на кнопке из listbox
    srok - надпись на кнопке для выбора срока (1 месяц/год)
    На выходе функция выдает прогноз по диаметру на указанную дату date (в выводе дата + число)
    '''
  # srok = '3 месяца' или = '1 год'

    # Название файла С ПРОБЕЛОМ (перед .xlsx)
    train = pd.read_excel('./train_indb/' + DN + '.xlsx')  # набор данных из excel (тестовые данные за 2022-2023 год)
    train.columns = ['time', 'det']  # колонки со временем
    train.index = train.pop('time')  # список всех дат из excel файла

    # Находим дату, к которой будем прибавлять
    time = str(train.index[-1])
    # date - дата, на которую мы делаем прогноз (берется из excel)

    #date = Set_prognoz_date(time, srok)

    date = time

    model = auto_arima(train, seasonal=True, m=12, trace=True, suppress_warnings=True, error_action='ignore',
                       stepwise=True)

    forecaster = SARIMAX(
        order=(int(str(model)[7]), int(str(model)[9]), int(str(model)[11])), \
        seasonal_order=(int(str(model)[14]), int(str(model)[16]), int(str(model)[18]), 12), trend='ct')
        
    forecaster = sm.tsa.statespace.sarimax.SARIMAX(train,
                                order=(int(str(model)[7]), int(str(model)[9]), int(str(model)[11])),
                                seasonal_order=(int(str(model)[14]), int(str(model)[16]), int(str(model)[18]), 12), trend = "ct")

    results = forecaster.fit()
    if srok == '3 месяца':
        fh = pd.date_range(date, freq='M', periods=3)
        y_pred = results.get_forecast(steps = 3)
    else:
        fh = pd.date_range(date, freq='M', periods=12)
        y_pred = results.get_forecast(steps = 12)
    

#Confidence intervals of the forecasted values
    forecast_ci = y_pred.conf_int()

    spisok = list()
    spisok.append(y_pred)
    spisok.append(fh)
    spisok.append(forecast_ci)
    #print(y_pred)

    return spisok

#print(Click_OK())
def main(DN, srok):
    spisok = Click_OK(DN, srok)
    dover = spisok[2]
    y_pred = spisok[0]
    fh = spisok[1]
# ВЫЗОВ ----------------------------------
#y_pred, fh = Click_OK()
    return k.grafics(y_pred,DN, dover), y_pred, dover, fh