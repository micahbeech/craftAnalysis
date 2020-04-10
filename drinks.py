from selenium import webdriver
from pathlib import Path
import os

from block3 import Block3
from heartwood import Heartwood

class Drink():

    PERCENT_CONVERSION = 100

    drinks = {}
    home = str(Path.home())

    def makeSpreadsheet(self, details, filename):

        rates = []
        names = []
        for name, price, volume, percentage in details:
            numerator = percentage * volume
            denominator = self.PERCENT_CONVERSION * price
            rates.append(numerator / denominator)
            names.append(name)

        results = zip(names, rates)
        rankings = sorted(results, key = lambda ranking: ranking[1], reverse=True)

        with open(filename + '.csv', 'w+') as excelFile:
            excelFile.write('Name,mL/$\n')

            for name, rate in rankings:
                excelFile.write('%s,' % name)
                excelFile.write('%f\n' % rate)

        os.system('open ' + filename + '.csv')

    def run(self):
        driver = webdriver.Chrome(self.home + '/chromedriver')
        self.drinks['block3'] = Block3()
        self.drinks['heartwood'] = Heartwood()
        for drink in self.drinks:
            self.makeSpreadsheet(self.drinks[drink].scrape(driver), drink)
        driver.quit()

drink = Drink()
drink.run()