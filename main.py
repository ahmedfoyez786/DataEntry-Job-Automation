from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time

FORM_URL = "https://forms.gle/rAFhMgjjs7dsskH96"
DATA_URL = ("https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapV"
            "isible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A37.90678867945806%2C%22south%22%3A37.64356092669135%"
            "2C%22east%22%3A-122.224589265625%2C%22west%22%3A-122.642069734375%7D%2C%22mapZoom%22%3A11%2C%22filterState"
            "%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%2"
            "2value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22"
            "auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22price%22%3A%7B%22min%22%3"
            "Anull%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3Anull%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22"
            "min%22%3A1%2C%22max%22%3Anull%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22region"
            "Id%22%3A20330%2C%22regionType%22%3A6%7D%5D%7D")
headers = {
    "Accept-Language": "en-US,en;q=0.9,en-GB-oxendict;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
}
response = requests.get(DATA_URL, headers=headers)
html_data = response.text
soup = BeautifulSoup(html_data, "html.parser")

address_tag = soup.select("li address")
all_address = [address.getText().strip() for address in address_tag]

link_tag = soup.select("li .jnnxAW")
all_links = []
for link in link_tag:
    href = link["href"]
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)
price_tag = soup.select("li .iMKTKr")
all_price = [price.getText().strip() for price in price_tag]

# print(len(all_address))
# print(len(all_links))
# print(len(all_price))
# print(all_links)
# print(all_address)
# print(all_price)


# Selenium
driver_path = r"C:\Development\msedgedriver.exe"
edge_service = Service(executable_path=driver_path)
edge_option = webdriver.EdgeOptions()
prefs = {
    "browser": {
        "show_hub_popup_on_download_start": False
    },
    "user_experience_metrics": {
        "personalization_data_consent_enabled": True
    }
}
edge_option.add_experimental_option("prefs", prefs)
edge_option.add_experimental_option("detach", True)
driver = webdriver.Edge(service=edge_service, options=edge_option)

for n in range(len(all_links)):
    driver.get(FORM_URL)
    time.sleep(2)
    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]'
                                            '/div/div[1]/input')

    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/'
                                          'div/div[1]/input')
    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/'
                                         'div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')

    address.send_keys(all_address[n])
    price.send_keys(all_price[n])
    link.send_keys(all_links[n])
    submit_button.click()
