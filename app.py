import time
from selenium import webdriver
from bs4 import BeautifulSoup

NUM_SCROLLS = 5
SCROLL_PAUSE_TIME = 2

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
		time.sleep(1)
		driver.find_element_by_xpath("//div[@role='feed']//div[@role='button']").click()
		time.sleep(1)
		driver.find_element_by_xpath("//div[@role='menuitemradio'][@aria-checked='false']").click()
		
		# TODO: Scroll until last posts or scroll until all posts for the day have been obtained

		# Scroll to get posts
		height = driver.execute_script("return document.body.scrollHeight")
		for i in range(NUM_SCROLLS):
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(SCROLL_PAUSE_TIME)

			# Click "See More"
			see_more_divs = driver.find_elements_by_xpath("//div[contains(text(),'See More')][@role='button']")  
			for div in see_more_divs:
				div.click()

		# Get posts and convert to beautiful soup
		feed = driver.find_element_by_xpath("//div[@role='feed']")
		soup = BeautifulSoup(feed.get_attribute("innerHTML"), 'html.parser')

		# Print posts
		posts = soup.children
		next(posts)
		for post in posts:
			text = post.findAll(id=lambda x: x and x.startswith("jsc_c_"))
			if len(text) >= 3:
				print("Author:", text[1].find("strong").text)
				print("Date:", " ".join(text[2].find("span", attrs={'class': None}, recursive=False).find("a").get("aria-label").split()[:2]))
				print(text[3].get_text(separator="\n", strip=True))
				print("")

				# TODO: Scan post for contact info

				# TODO: Save post in accesible format

		# Close browser
		driver.close()