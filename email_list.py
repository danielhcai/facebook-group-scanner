import os
email_path = "./emails/"

if __name__ == "__main__":
	email_set = set()

	for filename in os.listdir(email_path):
		file = open(email_path + filename)
		for email in file:
			email_set.add(email)
		file.close()

	file = open(email_path + "final_list.txt", "w")
	for email in email_set:
		file.write(email)
	file.close()
