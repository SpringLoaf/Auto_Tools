import csv

from selenium import webdriver

count = 0

with open('scraper.csv', 'wt', newline='') as neu:
	scraperfile = csv.writer(neu, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

	url = ""
	driver = webdriver.Firefox()
	driver.get("https://www.google.com/maps/place/Florida,+USA")

	while True:
		curl = driver.current_url
		dat = curl.split('/')
		if dat[5] != url:
			cat = dat[5].split(',')
			if len(cat) >= 3:
				for x in range(len(cat)):
					cat[x] = cat[x].replace('+', ' ')
				scraperfile.writerow(cat[0:2])
				count += 1
				print(f'Address No. {count}:\t{cat[0:1]}')
			else:
				pass
			url = dat[5]
		else:
			pass
