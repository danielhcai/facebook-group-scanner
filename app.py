import csv
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

if __name__ == "__main__":
	# Command line args
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--username", type=str, default="")
	parser.add_argument("-p", "--password", type=str, default="")
	parser.add_argument("-g", "--group", type=str, default="")
	parser.add_argument("-f", "--file", type=str, default="temp")
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
		login_button = driver.find_element_by_name("login")
		login_button.click()
		driver.get(args.group)

		input("Press enter to continue...")

		# Get posts and convert to beautiful soup
		feed = driver.find_element_by_xpath("//html")
		soup = BeautifulSoup(feed.get_attribute("innerHTML"), 'html.parser')
		text = soup.get_text(separator=" ", strip=True)

		# "[(]*([0-9]){3}[-) ]*([0-9]){3}[- ]*([0-9]){4}"
		emails = re.findall("[a-zA-Z0-9.]+[@][a-zA-Z0-9]+[.][a-zA-Z]+", text)
		unique_emails = set(emails)

		file = open("emails/" + args.file + ".txt", "w")
		for email in unique_emails:
			file.write(email + "\n")
			unique_emails.add(email)

	file.close()

	# Close browser
	driver.close()