from selenium import webdriver
import time
from tools import ScrapeTools

class Heartwood():

    def scrape(self, driver):

        driver.get('https://heartwoodfarm.ca/collections/craft-cider')

        try:
            popup = ScrapeTools.safeFind(driver.find_element_by_class_name, 'fancybox-item.fancybox-close.ss-icon', 5)
            ScrapeTools.safeClick(popup, driver)
        except:
            pass

        linkIndex = 0

        links = ScrapeTools.safeFind(driver.find_elements_by_partial_link_text, '$')
        now = time.time()
        while len(links) == 0:
            if now + 30 < time.time():
                raise Exception('Could not find any products for Heartwood')
            links = ScrapeTools.safeFind(driver.find_elements_by_partial_link_text, '$')

        names = []
        volumes = []
        prices = []
        percentages = []

        while linkIndex < len(links):
            links = ScrapeTools.safeFind(driver.find_elements_by_partial_link_text, '$')
            ScrapeTools.safeClick(links[linkIndex], driver)
            linkIndex += 1

            name = ScrapeTools.safeFind(driver.find_element_by_class_name, 'product_name')
            price = None
            percent = None

            try:
                price = driver.find_element_by_xpath('//*[@id="shopify-section-product-template"]/div/div/div/div[2]/div[2]/p[2]/span[2]/span[1]')
                percent = driver.find_element_by_xpath('//*[@id="shopify-section-product-template"]/div/div/div/div[2]/div[2]/p[2]/span[2]/span[2]')
            except:
                price = ScrapeTools.safeFind(driver.find_element_by_xpath, '//*[@id="shopify-section-product-template"]/div/div/div/div[2]/div[2]/p[2]/span[1]')

            text = price.text.strip()
            if percent is not None:
                text = text + percent.text.strip()
            
            volumeIndex = text.find('ml:')
            priceIndex = text.find('$')
            percentIndex = text.find('%')

            while volumeIndex != -1:
                names.append(name.text.strip() + ' ('+ text[volumeIndex - 3 : volumeIndex] + 'mL)')
                volumes.append(int(text[volumeIndex - 3 : volumeIndex]))
                prices.append(int(text[priceIndex + 1 : priceIndex + 3]))
                percentages.append(int(text[percentIndex - 3 : percentIndex].replace('.', '')) / 10)

                volumeIndex = text.find('ml:', volumeIndex + 3)
                priceIndex = text.find('$', priceIndex + 1)

            ScrapeTools.goBack(driver)
        
        return zip(names, prices, volumes, percentages)

