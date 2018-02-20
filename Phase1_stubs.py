def main():
	# here, we need to implement for the flow
	# display the menu
	choice = "0"
	while (choice != "4"):
		print("\n   Main Menu")
		print("=======================")
		print("1. Drop/ Empty Collections")
		print("2. Crawl Data")
		print("3. Search Course")
		print("4. Predict Waiting List Size")
		print("5. Train Wating List Size")
		print("6. Exit")



		# allow the user to choose one of the functions in the menu
		choice = input("Please input your choice (1-4): ")

		print("")

		# check the input and call the correspondence function
		if (choice == '1'):
			dropAndEmptySuccessful()
		elif (choice == '2'):
			crawlData('default')
		elif (choice == "3"):
			callUpdateAddressHandler()
		elif (choice == "4"):
			print("")
		else:
			print("Invalid Input!")


# 5.1
def dropAndEmptySuccessful():
    # checking should be done
    print("Collection dropping and empty collection creating are successful")

# 5.2
def crawlData(enteredURL):
    if enteredURL == 'default':
        print("Data Crawling is successful and all data are inserted into the database")
    else:
        URL = enteredURL
        print("Data Crawling is successful and all data are inserted into the database")
