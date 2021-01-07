import csv
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

NUM_SCROLLS = 5
SCROLL_PAUSE_TIME = 3

if __name__ == "__main__":
	# Command line args
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--username", type=str, default="")
	parser.add_argument("-p", "--password", type=str, default="")
	parser.add_argument("-g", "--group", type=str, default="")
	args = parser.parse_args()

	# Check for no username or password
	if args.username == "" or args.password == "" or args.group == "":
		print("Bad arguemnts")
	else:
		# Open browser and go to facebook
		driver = webdriver.Firefox(executable_path=r".\geckodriver.exe")
		driver.get("https://www.facebook.com/")

		# Login to facebook and go to facebook group
		username_input = driver.find_element_by_id("email")
		username_input.send_keys(args.username)
		password_input = driver.find_element_by_id("pass")
		password_input.send_keys(args.password)
		login_button = driver.find_element_by_id("u_0_b")
		login_button.click()
		driver.get(args.group)

		# Sort by recent posts
		# time.sleep(1)
		# driver.find_element_by_xpath("//div[@role='feed']//div[@role='button']").click()
		# time.sleep(1)
		# driver.find_element_by_xpath("//div[@role='menuitemradio'][@aria-checked='false']").click()
		
		# TODO: Scroll until last posts or scroll until all posts for the day have been obtained


		# TODO: Scroll to the element
		# Scroll to get posts
		for i in range(NUM_SCROLLS):
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(SCROLL_PAUSE_TIME)

			# Click "See More"
			see_more_divs = driver.find_elements_by_xpath("//div[contains(text(),'See More')][@role='button']")  
			for div in see_more_divs:
				div.click()
				time.sleep(1)
			
			# Expand post comments
			comment_divs = driver.find_elements_by_xpath("//div[@role='button']/span/span[contains(text(),'View ')][contains(text(), ' more comment')]") 
			for div in comment_divs:
				div.click()
				time.sleep(1)
			
			# See comment replies
			reply_divs = driver.find_elements_by_xpath("//div[@role='button']/span/span/div/div[contains(text(),'replied')]")  
			for div in reply_divs:
				div.click()
				time.sleep(1)

			# Click "See More"
			see_more_divs = driver.find_elements_by_xpath("//div[contains(text(),'See More')][@role='button']")  
			for div in see_more_divs:
				div.click()
				time.sleep(1)
			
			# TODO: save posts as browser is scrolling

		# Get posts and convert to beautiful soup
		feed = driver.find_element_by_xpath("//div[@role='feed']")
		soup = BeautifulSoup(feed.get_attribute("innerHTML"), 'html.parser')
		text = soup.get_text(separator=" ", strip=True)
		# re."[(]*([0-9]){3}[-) ]*([0-9]){3}[- ]*([0-9]){4}"
		#"[a-zA-Z]+[@][a-zA-Z]+[.][a-zA-Z]+"
		
		import pdb; pdb.set_trace()
		# Close browser
		driver.close()