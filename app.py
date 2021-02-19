import csv
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

EMAIL_REG_EX = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"

if __name__ == "__main__":
	# Command line args
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--file", type=str, default="temp")
	args = parser.parse_args()

	# Open browser and go to facebook
	driver = webdriver.Firefox(executable_path=r".\geckodriver.exe")
	driver.get("https://www.facebook.com/")

	input("Press enter to continue...")

	# Get posts and convert to beautiful soup
	feed = driver.find_element_by_xpath("//html")
	soup = BeautifulSoup(feed.get_attribute("innerHTML"), 'html.parser')
	text = soup.get_text(separator=" ", strip=True)

	# "[a-zA-Z0-9.]+[@][a-zA-Z0-9]+[.][a-zA-Z]+"
	emails = re.findall("[a-zA-Z0-9.]+[@][a-zA-Z0-9]+[.][a-zA-Z]+", text)
	unique_emails = set()

	file = open("emails/" + args.file + ".txt", "w")
	for email in emails:
		if email not in unique_emails:
			file.write(email + "\n")
			unique_emails.add(email)

	file.close()

	# Close browser
	driver.close()