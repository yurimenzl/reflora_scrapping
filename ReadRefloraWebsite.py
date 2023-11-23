import sys
import pandas as pd
from pandas import DataFrame
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller

class ReadRefloraWebsite:
  def set_driver(self):
    sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

    # setup chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless') # ensure GUI is off
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # set path to chromedriver as per your configuration
    chromedriver_autoinstaller.install()

    # set up the webdriver
    self.driver = webdriver.Chrome(options=chrome_options)

    return self.driver

  def close_driver(self) -> None:
    self.driver.close()

  def write_data(self, data: list, filepath: str="scrapped_data.csv") -> None:
    if len(data) == 0:
      return "Data is empty!"

    f = open(filepath, "a")
    txt = ""
    for i in range(len(data)):
      txt = txt + str(data[i]) + "\n"
    f.write(txt)
    f.close()

  def read_data(self, path: str, separator: str) -> DataFrame:
    df = pd.read_csv(path, sep=separator)
    return df
  
  def get_taxon_ids(self, df: DataFrame, size: int=1000, search_field: str="taxonID") -> list:
    df_taxon_ids = df[search_field]
    taxonIds = []
    for i in range(size):
      taxonIds.append(str(df_taxon_ids[i]))

    return taxonIds

  def get_scrapped_data(self, data:list, start: int=0, end: int=1000, step: int=1) -> list:
    if end > len(data):
      return "end parameter is higher than data length"

    scrapped_data = []

    driver = self.set_driver()

    for j in range(start, end, step):
      # set the target URL
      url = "https://floradobrasil.jbrj.gov.br/consulta/ficha.html?idDadosListaBrasil=" + data[j]
      # Get the site content
      driver.get(url)
      # Sleep for 3 seconds to page load
      time.sleep(3)

      fields = []
      string = driver.find_elements('xpath', '//*[@id="informacoes"]/div')
      for i in range(len(string)):
          fields.append(string[i].text)
          name = driver.find_element('xpath', '//*[@id="name"]/span/div[1]/i').text
          matches = [match for match in fields if "Description with controlled fields" in match]
      if len(matches) > 0: 
            words = matches[0].split(";")
            scrapped_data.append(data[j] + "|" + name + "|" + str(words) + "|" + url)
      else:
            scrapped_data.append(data[j] + "|" + name + "|" + "NA" + "|" + url)

    return scrapped_data
