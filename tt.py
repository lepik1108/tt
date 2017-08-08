import datetime
import time

from pprint import pprint

from pymongo import MongoClient

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


####
# check_pages - used to check products on N pages and write bestsellers to database 
# @doc - table/collections in database
# @pages - number of pages to search bestsellers
####

def check_pages(doc, pages):
	#result = {}
	page=1
	while page <= pages:
		time.sleep(10)
		print ("reached page "+(str(page)))
		products = driver.find_elements_by_xpath('//div[@class="g-i-tile g-i-tile-catalog"]') 
		for product in products:
			try:
				product.find_element_by_xpath('.//*[@class="g-tag g-tag-icon-middle-popularity sprite"]')
				print ("found marker in " + str(product))
				title = product.find_element_by_xpath('.//*[@class="g-i-tile-i-title clearfix"]')
				name = title.find_element_by_xpath('.//a').text
				price = product.find_element_by_xpath('.//*[@class="g-price-uah"]').text
				print (name+" - "+price)
				obj =  {"name": name,
						"price": price,
						"date_added": datetime.datetime.utcnow()}
				doc.insert_one(obj)
			except:
				print ("marker not found")
		page+=1
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//a[contains(text(), "'+str(page+1)+'") and @class="novisited paginator-catalog-l-link"]')))
		driver.find_element_by_xpath('//a[contains(text(), "'+str(page+1)+'") and @class="novisited paginator-catalog-l-link"]').click()
	print ("Result:\n")
	pprint ([cursor for cursor in doc.find({})])
		

if __name__ == "__main__":	

	category = "Телефоны, MP3, GPS"
	sub_category = "Смартфоны"
	sub_sub_category = "Все смартфоны"
	marker = "Топ Продаж"


	#### docker container with headless chrome
	driver = webdriver.Remote(
	command_executor='http://127.0.0.1:4444/wd/hub',
	desired_capabilities=DesiredCapabilities.CHROME)
	####
	
	#### local chrome
	##options = webdriver.ChromeOptions()
	##options.binary_location = '/opt/google/chrome-unstable/google-chrome-unstable'
	##options.add_argument('headless')
	##driver = webdriver.Chrome(chrome_options=options)
	####

	#### local Firefox // send_keys does not work in geckodriver :(
	#driver = webdriver.Firefox(executable_path="./geckodriver")
	####

	##driver.maximize_window()
	driver.get('http://rozetka.com.ua')
	search = driver.find_element_by_css_selector("[tabindex='1']")
	##search = driver.find_element_by_class_name("rz-header-search-input-text passive")
	search.send_keys(category)
	search.send_keys(Keys.ENTER)

	driver.find_element_by_xpath('//a[contains(text(), "' + category + '") and @class="m-cat-l-i-title-link novisited"]').click()
	driver.find_element_by_xpath('//a[contains(text(), "' + category + '") and @class="novisited"]').click()
	driver.find_element_by_link_text(sub_category).click()
	driver.find_element_by_link_text(sub_sub_category).click()
	#driver.execute_script("window.stop();") 
	#driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)
	
	client = MongoClient('localhost', 27017)
	db = client.rozetka
	table = db.top_products
	
	check_pages(table, 3)

	time.sleep(3) 

	driver.close()
