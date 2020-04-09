from selenium import webdriver
from selenium.webdriver.support.select import Select
import time

class Block3():

    def scrape(self, driver):
        driver.get('https://blockthreebottleshop.com')
        time.sleep(2)

        birthYear = Select(driver.find_element_by_id('bouncer_datepicker_year'))
        birthYear.select_by_index(20)

        submit = driver.find_element_by_id('bouncer_modal_submit')
        submit.click()
        time.sleep(2)

        nameElements = driver.find_elements_by_class_name('product-single__title')
        nameElements = nameElements[0:-1]

        names = []

        for nameElement in nameElements:
            names.append(nameElement.text.strip())

        tagElements = driver.find_elements_by_class_name('shopify-section.index-section.index-section--featured-product')
        tags = []
        for tagElement in tagElements:
            tags.append(tagElement.get_attribute('id')[16:])

        priceElements = []
        for tag in tags:
            priceElements.append(driver.find_element_by_id('ProductPrice-' + tag))
        priceElements = priceElements[0:-1]

        prices = []

        for priceElement in priceElements:
            value = priceElement.text.strip()
            value = value.replace('.', '')
            value = value.replace('$', '')
            prices.append(int(value) / 100)

        volumeElements = []
        for tag in tags:
            volumeElements.append(Select(driver.find_element_by_id('SingleOptionSelector-' + tag + '-0')))
        volumeElements = volumeElements[0:-1]

        volumes = []

        for volumeElement in volumeElements:
            text = volumeElement.first_selected_option.text.strip()
            value = 0
            if 'bottle' in text or 'Bottle' in text:
                value = 500
            elif 'can' in text or 'Can' in text:
                value = 473
            else:
                continue
            volumes.append(value)

        percentageElements = driver.find_elements_by_class_name('product-single__description.rte')
        percentageElements = percentageElements[0:-1]

        percentages = []

        for percentageElement in percentageElements:
            count = 0
            value = percentageElement.text.strip()
            for character in value:
                if character == '%':
                    value = value[count - 3 : count]
                    value = value.replace('.', '')
                    if len(value) == 2:
                        percentages.append(int(value) / 10)
                    else:
                        percentages.append(int(value[-1:]))
                    break
                count += 1

        return zip(names, prices, volumes, percentages)
