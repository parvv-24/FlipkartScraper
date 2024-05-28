import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import lxml.html as lh
from time import sleep
from bs4 import BeautifulSoup

output = open('Flipkart Scraper.csv', 'a', newline='', encoding='utf-8-sig')
writer = csv.writer(output)

# Create Edge options
edge_options = webdriver.EdgeOptions()

# Create Edge WebDriver instance
driver = webdriver.Edge(options=edge_options)

url = 'https://www.flipkart.com/'
driver.get(url)

driver.maximize_window()
print(url)
sleep(2)

# Wait for the close button to be clickable with a timeout
try:
    close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, '_2KpZ6l')]")))
    close_button.click()
except TimeoutException:
    print("Close button not found within the specified time.")

input_field = driver.find_element(By.XPATH, "//input[@class='_3704LK']")
input_field.send_keys('iphone 15 pink')
sleep(5)

# SEARCH BUTTON
search_enter = driver.find_element(By.XPATH, '//button[@type="submit"]')
search_enter.click()
sleep(3)

html = driver.page_source
doc = lh.fromstring(html)
try:
    no = doc.xpath('//div[@class="_2MImiq"]/span[1]/text()')[0]
    page = no.replace("Page 1 of ", "")
    page = int(page)
    print(page)
except:
    page = 1

main_url = driver.current_url

for i in range(1, page + 1):
    c_url = main_url + '&page=' + str(i)
    driver.get(c_url)
    sleep(3)
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    for i in range(1, total_height, 5):
        driver.execute_script("window>scrollTo(0, {});".format(i))
    sleep(3)
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, 'html.parser')
    doc = lh.fromstring(page_html)
    result = soup.findAll('div', attrs={'class': '_2kHMtA'})
    for data in result:
        name = data.find('div', attrs={'class': '_4rR01T'}).text
        desc = data.find('div', attrs={'class': 'fMghEO'}).text
        new_price = data.find('div', attrs={'class': '_30jeq3 _1_WHN1'}).text
        try:
            old_price = data.find('div', attrs={'class': '_3I9_wc _27UcVY'}).text
        except:
            old_price = ''
        try:
            reviews = data.find('span', attrs={'class': '_2_R_DZ'})
            reviews = reviews.text
        except:
            reviews = ''
        try:
            rating = data.find('div', attrs={'class': '_3LWZlK'})
            rating = rating.text
        except:
            rating = ''
        try:
            discount = data.find('div', attrs={'class': '_3Ay6Sb'}).text
        except:
            discount = ''
        writer.writerow([name, desc, rating, reviews, new_price, old_price, discount])

driver.quit()
output.close()
