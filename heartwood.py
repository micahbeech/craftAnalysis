from selenium import webdriver
import time

class Heartwood():

    def scrape(self, driver):

        driver.get('https://heartwoodfarm.ca/collections/craft-cider')
        time.sleep(4)

        try:
            popup = driver.find_element_by_class_name('fancybox-item.fancybox-close.ss-icon')
            popup.click()
            time.sleep(2)
        except:
            pass

        linkIndex = 0

        links = driver.find_elements_by_partial_link_text('$')
        names = []
        volumes = []
        prices = []
        percentages = []

        while linkIndex < len(links):
            links = driver.find_elements_by_partial_link_text('$')
            links[linkIndex].click()
            linkIndex += 1
            time.sleep(2)

            name = None
            price = None
            percent = None

            name = driver.find_element_by_class_name('product_name')
            try:
                price = driver.find_element_by_xpath('//*[@id="shopify-section-product-template"]/div/div/div/div[2]/div[2]/p[2]/span[2]/span[1]')
                percent = driver.find_element_by_xpath('//*[@id="shopify-section-product-template"]/div/div/div/div[2]/div[2]/p[2]/span[2]/span[2]')
            except:
                price = driver.find_element_by_xpath('//*[@id="shopify-section-product-template"]/div/div/div/div[2]/div[2]/p[2]/span[1]')

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

            driver.execute_script("window.history.go(-1)")
            time.sleep(2)
        
        return zip(names, prices, volumes, percentages)

