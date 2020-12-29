import time
from selenium import webdriver
from bs4 import BeautifulSoup

def login(driver, username, password):
	username_input = driver.find_element_by_id("email")
	username_input.send_keys(username)

	password_input = driver.find_element_by_id("pass")
	password_input.send_keys(password)

	login_button = driver.find_element_by_id("u_0_b")
	login_button.click()

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--username", type=str, default="")
	parser.add_argument("-p", "--password", type=str, default="")
	parser.add_argument("-g", "--group", type=str, default="")
	args = parser.parse_args()

	# Check for no username or password
	if args.username == "" or args.password == "":
		print("Enter a username or password")
	else:
		driver = webdriver.Firefox(executable_path=r".\geckodriver.exe")
		driver.get("https://www.facebook.com/")
		login(driver, args.username, args.password)
		driver.get(args.group)

		SCROLL_PAUSE_TIME = 2
		# Get scroll height
		height = driver.execute_script("return document.body.scrollHeight")

		for i in range(10):
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(SCROLL_PAUSE_TIME)

		posts = driver.find_elements_by_xpath("//div[@data-ad-preview='message']")
		for i in range(10):
			soup = BeautifulSoup(posts[i].get_attribute("innerHTML"), 'html.parser')
			print(soup.text + "\n")

		# group = input("Pick a group: ")
		# num_posts = input("How many posts should be saved: ")
		#driver.close()