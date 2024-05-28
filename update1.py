import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import subprocess


def scroll_down(driver):
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    for i in range(1, total_height, 50):
        driver.execute_script("window.scrollTo(0, {});".format(i))
        sleep(0.1)


def open_excel_file(file_path):
    try:
        subprocess.Popen(['start', 'excel', file_path], shell=True)
    except Exception as e:
        print(f"Error opening Excel file: {e}")


def scrape_flipkart_data():
    output_csv = open('Flipkart_Scraper.csv', 'a', newline='', encoding='utf-8-sig')
    writer = csv.writer(output_csv)

    edge_path = r"C:/Users/Administrator/Downloads/edgedriver_win64/msedgedriver.exe"

    driver = webdriver.Edge()

    url = 'https://www.flipkart.com/'
    driver.get(url)

    driver.maximize_window()
    print(url)
    sleep(2)

    input_field = driver.find_element(By.XPATH, "//input[@class='Pke_EE']")
    input_field.send_keys('iphone 15 pink')
    sleep(5)

    search_enter = driver.find_element(By.XPATH, '//button[@type="submit"]')
    search_enter.click()
    sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Get number of pages
    no = soup.select_one('div._2MImiq > span:nth-child(1)')
    if no:
        try:
            page = int(no.text.replace("Page 1 of ", ""))
        except ValueError:
            page = 1
    else:
        page = 1

    print(f"Number of pages: {page}")

    main_url = driver.current_url

    for i in range(1, page + 1):
        c_url = main_url + '&page=' + str(i)
        driver.get(c_url)
        sleep(3)

        scroll_down(driver)

        page_html = driver.page_source
        soup = BeautifulSoup(page_html, 'html.parser')
        results = soup.find_all('div', class_='_2kHMtA')

        for data in results:
            try:
                name = data.find('div', class_='_4rR01T').text
                desc = data.find('div', class_='fMghEO').text
                new_price = data.find('div', class_='_30jeq3 _1_WHN1').text
                old_price = data.find('div', class_='_3I9_wc _27UcVY').text if data.find('div',
                                                                                         class_='_3I9_wc _27UcVY') else ''
                reviews = data.find('span', class_='_2_R_DZ').text if data.find('span', class_='_2_R_DZ') else ''
                rating = data.find('div', class_='_3LWZlK').text if data.find('div', class_='_3LWZlK') else ''
                discount = data.find('div', class_='_3Ay6Sb').text if data.find('div', class_='_3Ay6Sb') else ''

                writer.writerow([name, desc, rating, reviews, new_price, old_price, discount])
            except Exception as e:
                print(f"Error scraping data: {e}")

    driver.quit()
    output_csv.close()

    # Debug: Check contents of CSV file
    try:
        df = pd.read_csv('Flipkart_Scraper.csv')
        print("CSV contents:")
        print(df.head())

        output_excel = 'Flipkart_Scraper.xlsx'
        df.to_excel(output_excel, index=False)
        print(f"Data exported to {output_excel}")
        open_excel_file(output_excel)
    except Exception as e:
        print(f"Error exporting data to Excel: {e}")


if __name__ == "__main__":
    scrape_flipkart_data()
