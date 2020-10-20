
'''Seasonal data'''

import pandas as pd
import matplotlib.pyplot as plt
data = [25, 120, 40, 60, 30, 140, 60, 80, 35, 150, 55, 90]

'''No of periods in a season'''

N = 4  # should be determined from visualization (manual work)


# iterating list for alpha, beta, gama
constants = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]


class TimeSeries:

    def __init__(self, data, N):

        self.data = data
        self.series = [None] * len(data)
        self.trend = [None] * len(data)
        self.seasonal_factor = [None] * len(data)
        self.forecast = [None] * len(data)
        self.sum = 0
        self.average = 0

        for i in range(N):
            self.sum += self.data[i]
        self.average = self.sum / N

        for i in range(N):
            self.seasonal_factor[i] = self.data[i] / self.average
            self.series[i] = self.average
            self.trend[i] = 0

    ''' Winter's Model '''

    def winter_forecast(self, alpha, beta, gama):

        self.alpha = alpha
        self.beta = beta
        self.gama = gama
        self.bias = [None] * len(data)
        self.MAD = [None] * len(data)
        self.MSD = [None] * len(data)
        self.MSD_array = []

        for i in range(len(self.data) - N):

            '''Calculate series, trend, seasonal factor and forecast for winter's model'''

            self.series[i + N] = alpha * (self.data[i + N] / self.seasonal_factor[i]) + (
                1 - alpha) * (self.series[i + N - 1] + self.trend[i + N - 1])
            self.trend[i + N] = beta * (self.series[i + N] - self.series[i + N - 1]) + (
                1 - beta) * self.trend[i + N - 1]
            self.seasonal_factor[i + N] = gama * (self.data[i + N] / self.series[i + N]) + (
                1 - gama) * (self.seasonal_factor[i])
            self.forecast[i + N] = (self.series[i + N] +
                                    self.trend[i + N]) * self.seasonal_factor[i]

            '''Calculating errors'''

            self.bias[i + N] = self.data[i + N] - self.forecast[i + N]
            self.MAD[i + N] = abs(self.data[i + N] - self.forecast[i + N])
            self.MSD[i + N] = (self.data[i + N] - self.forecast[i + N]) * \
                (self.data[i + N] - self.forecast[i + N])

    '''Iterating for best parameters'''

    def minimize_error(self, constants=[]):

        self.alpha_optimal = 0
        self.beta_optimal = 0
        self.gama_optimal = 0
        MSD_min = float('inf')

        for i in range(len(constants)):
            for j in range(len(constants)):
                for k in range(len(constants)):

                    '''Executing Winter's model for different combinations of hyper parameters'''

                    self.winter_forecast(
                        constants[i], constants[j], constants[k])
                    total = 0
                    MSD_average = 0
                    for x in range(len(self.MSD) - N):
                        total += self.MSD[x + N]
                    MSD_average = total / (len(self.MSD) - N)
                    if MSD_average <= MSD_min:

                        '''Updating optimal parameters'''
                        MSD_min = MSD_average
                        self.alpha_optimal = constants[i]
                        self.beta_optimal = constants[j]
                        self.gama_optimal = constants[k]
        print('Minimum average MSD:', MSD_min, '\nbest alpha:', self.alpha_optimal,
              '\nbest beta:', self.beta_optimal, '\nbest gama', self.gama_optimal)


winter = TimeSeries(data, N)  # initialize class
winter.minimize_error(constants)  # Execute function to find optimal values

plt.plot(winter.data, label='demand', color='r')
plt.plot(winter.series, label='series', color='g')
plt.plot(winter.trend, label='trend', color='y')
plt.plot(winter.seasonal_factor, label='seasonal factor', color='c')
plt.plot(winter.forecast, label='forecast', color='b')
plt.title('Winters Forecast')
plt.xlabel('Time Period')
plt.ylabel('Demand')
plt.legend(loc='upper right', fontsize=10)
plt.show()
output = pd.DataFrame(winter.forecast, winter.data)
output = output.reset_index()
output.columns = ['Data', 'Forecast']
print('\n', output)
