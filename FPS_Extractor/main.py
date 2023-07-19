import re
import os
import csv
import json
import time
import random
from tkinter import *
from tkinter.ttk import *
import undetected_chromedriver as udc
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#	Initiate Script Timer, Contact Counter, and GUI

TIME_START = time.perf_counter()


# Initiate Webdriver

cwd = os.getcwd()
options = udc.ChromeOptions()
options.add_experimental_option('prefs', { 'extensions.ui.developer_mode': True })
options.add_argument(f'--load-extension={cwd}/uBlock0_1.50.1b17.chromium/uBlock0.chromium')
# options.add_extension('./ublock_origin.crx')
driver = udc.Chrome(options=options)
#driver.install_addon('./ublock_origin-1.49.2.xpi', temporary=True)

#	Load Configuration
CONFIG = {}
CONFIG_FILENAME = "config.json"
DEFAULT_CONFIG = {
	"output_filename": "output.csv",
	"input_filename": "scraper.csv",
	"city": "Saint Cloud",
	"timeout": 9999,
	"max_numbers": 3,
	"max_names": 1
}

if os.path.exists(CONFIG_FILENAME):
	with open('config.json', 'r') as f:
		CONFIG.update(json.load(f))
		f.close()
else:
	with open(CONFIG_FILENAME, 'w') as f:
		json.dump(DEFAULT_CONFIG, f)
		CONFIG.update(DEFAULT_CONFIG)
		f.close()

CITY = CONFIG.get("city")
TIMEOUT = CONFIG.get("timeout")
MAX_NUMBERS = CONFIG.get("max_numbers")
MAX_NAMES = CONFIG.get("max_names")
INPUT_FILE = CONFIG.get("input_filename")
OUTPUT_FILE = CONFIG.get("output_filename")

def main():
    ADDRESSES_DONE = 0
    for lines in INPUT_CSV:
        print(f'Line #{ADDRESSES_DONE}\nSearching Address: {lines[0]}')
        time.sleep(1)
        result_temp = []
        contacts_found = 0
        address = str(lines[0].replace(' ', '-')).lower()
        city = str(CITY.replace(' ', '-')).lower()
        city_proper = f'{CITY}, FL'
        url = f'https://www.fastpeoplesearch.com/address/{address}_{city}-fl'
        driver.get(url)
        result_temp.append(lines[0])
        #wait1 = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/div/div[1]/div[3]/div[4]/div/div[1]')))
        wait1 = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/div/div[1]')))
        raw_data = driver.find_elements(By.XPATH, '/html/body/div[4]/div/div[1]/div[3]/div/div')
        for x in raw_data:
            page_content = x.text
            numbers = re.findall("(\([0-9]{3}\) [0-9]{3}-[0-9]{4})", page_content)
            if contacts_found >= 2:
                break
            elif len(numbers) >= 1:
                #print(page_content)
                test = re.findall(f'Current Home Address:\n{lines[0]}', page_content)
                text = x.text.split('\n')
                if len(test) > 0:
                    result_temp.append(text[0])
                    result_temp.append(numbers[0])
                    print("ADDRESS FOUND")
                    print("Name: {}\nPhone: {}".format(text[0], numbers[0]))
                    contacts_found += 1
            else:
                continue
            print("---------")
        OUTPUT_CSV.writerow(result_temp)
        ADDRESSES_DONE += 1
        

#	Do a try except statement to catch errors
try:
	#	Read Input File
	input_file = open(INPUT_FILE, 'rt', newline='')
	INPUT_CSV = csv.reader(input_file, delimiter=',')

	#	Prepare Output File
	with open(OUTPUT_FILE, 'wt', newline='') as output_open:
		OUTPUT_CSV = csv.writer(output_open, delimiter=',')
		main()
finally:
	driver.quit()
	TIME_STOP = time.perf_counter()
	print(f'Script Runtime: {(TIME_STOP - TIME_START)/60}')