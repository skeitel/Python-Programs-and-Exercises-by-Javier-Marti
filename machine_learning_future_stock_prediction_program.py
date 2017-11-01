#Machine learning price predictor
#Obtains the list of prices of a csv file and predicts next share price based on historical price, using three techniques to fit the data
#Dataset obtained from Google Finance https://finance.google.com/finance/historical?q=NASDAQ:AMZN
#JavierMarti.co.uk

import csv
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt


dates = []
prices = []

#Extract data with stock market price for last 30 days from CSV
def get_data(filename):
    with open(filename, 'r') as csvfile:
        csvFileReader = csv.reader(csvfile)
        next(csvFileReader)
        for row in csvFileReader:
            dates.append(int(row[0].split('-')[0]))
            prices.append(float(row[1]))
    return

#Predict prices developing 3 predictive models
def predict_prices(dates, prices, x):
    dates = np.reshape(dates,(len(dates),1))

    svr_lin = SVR(kernel= 'linear', C=1e3)
    svr_poly = SVR(kernel= 'poly', degree= 2)
    svr_rbf = SVR(kernel='rbf', gamma=0.1)

    svr_lin.fit(dates, prices)
    svr_poly.fit(dates, prices)
    svr_rbf.fit(dates, prices)

    plt.scatter(dates, prices, color='black', label='Data')
    plt.plot(dates, svr_rbf.predict(dates), color= 'red', label = 'RBF model')
    plt.plot(dates, svr_lin.predict(dates), color='green', label= 'Linear model')
    plt.plot(dates, svr_poly.predict(dates), color='blue', label='Polynomial model')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Support Vector Regression')
    plt.legend()
    plt.show()

    return svr_rbf.predict(x)[0], svr_lin.predict(x)[0], svr_poly.predict(x)[0]

get_data('amzn.csv')
predicted_price = predict_prices(dates, prices, 31)
print(predicted_price)