# Making necessary imports
import requests
import os
import pandas as pd

# Declaring a dictioray with links to confirmed, recovered and deaths datasets
urls = {
    'confirmed' : "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv'",
    'recovery' : "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv",
    'death' : "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv",
    'testing' : "https://covid.ourworldindata.org/data/owid-covid-data.xlsx"
}

# Making a function that can download and save the dataset
save_link = "C:\\Users\\usama\\OneDrive\\Desktop\\github\\COVID19-visualization\\dataset\\"  #path to dataset folder
def download_files(url):
    dlink = requests.get(urls[url])
    fname = url + ".csv"
    data = open(os.path.join(save_link, fname), 'wb').write(dlink.content)

# Running a for loop to download all files
for url in urls:
    download_files(url)

# Coverting "Testing" file from xls to csv
testing_xls = pd.read_excel('./dataset/testing.csv', 'Sheet1', dtype=str, index_col=None)
testing_xls.to_csv('./dataset/testing.csv', encoding='utf-8', index=False)

print('Download complete')