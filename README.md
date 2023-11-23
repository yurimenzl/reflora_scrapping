# reflora_scrapping
Web scrap in Python to retrieve data from Reflora Website

# Required Libraries
* selenium
* chromedriver-autoinstaller
* pandas
* time

# Getting Started
- These commands are to execute in Google Colab environment. You'll need edit to use in Python raw

!pip install selenium

!apt-get update

!apt install chromium-chromedriver

!pip install chromedriver-autoinstaller

# Example
import ReadRefloraWebsite

refloraObj = ReadRefloraWebsite()

df = refloraObj.read_data(path="angiosperma_flora_do_brasil.csv", separator=";")

listTaxonId = refloraObj.get_taxon_ids(df, size=10)

data = refloraObj.get_scrapped_data(listTaxonId, start=0, end=10, step=1)

refloraObj.write_data(data)

refloraObj.close_driver()


