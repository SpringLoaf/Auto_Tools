import re
import os
import csv
import json
import time
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#	Initiate Script Timer
TIME_START = time.perf_counter()

#	Initiate WebDriver
driver = webdriver.Firefox()
driver.install_addon('./ublock_origin-1.49.2.xpi', temporary=True)

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

def extract_contacts(contacts_raw):
	contacts_extract = []
	for x in contacts_raw:
		last_line = x[len(x)-1].strip()
		if last_line == 'View Details':
			contacts_extract.append(x)
	if len(contacts_extract) < 1:
		return 'N/A'
	return contacts_extract

def extract_selenium(selenium_data):
	selenium_extract = []
	for x in selenium_data:
		selenium_extract.append(x.text.split('\n'))
	return selenium_extract

def extract_phone(address):
	wait2 = WebDriverWait(driver, TIMEOUT, ignored_exceptions=(exceptions.NoSuchElementException,exceptions.StaleElementReferenceException)).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[3]/div/div[2]/div[2]/div[4]/div[2]/div[2]/div/div/a/span[1]")))
	source = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[2]/div[4]/div[2]/div[2]/div/div/a/span[1]").text
	page_content = driver.find_element(By.XPATH, "/html/body").text
	age = re.findall('(Age [\w\d]+)', page_content)
	if not age:
		return None
	print(age[0])
	age1 = age[0].split(' ')
	numbers = re.findall("(\([0-9]{3}\) [0-9]{3}-[0-9]{4})", page_content)
	if re.search(source, address):
		print(f'Address Match: {address}')
	else:
		print(f'Address does not match: {address}')
	if not numbers or not address == source or age1[1] > '75' or age1[1] < '20':
		return None
	return numbers[0]

###	Entire Process Is Controlled Here
#	Instructions:
#		1. Gets the address and city from the config variables, converts and insert into url-readable links
#		2. WebDriver gets url and visits the premade link
#		3. Selenium extracts data and process them into human readable format 
#		4. Extract contact from data
#		5. Die
def main():
	for row in INPUT_CSV:
		print(f'\n\nAddress: {row[0]}')
		contacts_list = 0
		contacts_found = 0
		contacts_number = []
		first_found = ''
		time.sleep(2)
		address = row[0].replace(' ', '%20')
		city = CITY.replace(' ', '%20')
		url = f'https://www.truepeoplesearch.com/resultaddress?streetaddress={address}&citystatezip={city},%20FL'
		print(f'Accessing = {url}')
		driver.get(url)
		contacts_number.append(row[0])
		while True:
			wait0 = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body')))
			blank_page = re.findall('We could not find any records for that search criteria.', driver.find_element(By.XPATH, "/html/body").text)
			if 'We could not find any records for that search criteria.' in blank_page:
				break
			print(f'\nContact # {contacts_list}')
			driver.implicitly_wait(1)
			wait1 = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/a')))
			contacts_raw = driver.find_elements(By.XPATH, "/html/body/div[3]/div/div[2]/div")
			links = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div[2]/a')
			contacts_processed = extract_selenium(contacts_raw)
			filtered_contacts = extract_contacts(contacts_processed)
			if len(links) == contacts_list or contacts_found == MAX_NUMBERS:
				break
			else:
				links[contacts_list].click()
				temp = extract_phone(row[0])
				print(filtered_contacts[contacts_list][0])
				if temp is not None and len(contacts_number) - 1 <= MAX_NAMES:
					contacts_number.append(filtered_contacts[contacts_list][0])
					contacts_number.append(temp)
					driver.back()
					contacts_list += 1
					contacts_found += 1
					continue
				elif temp is not None:
					contacts_number.append(temp)
					contacts_found += 1
				else:
					pass
				contacts_list += 1
				driver.back()
		print(contacts_number)
		OUTPUT_CSV.writerow(contacts_number)

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