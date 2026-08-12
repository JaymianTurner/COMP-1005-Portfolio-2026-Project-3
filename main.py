import uuid
import re

class Client():
	def __init__(self,first_name:str,last_name:str,phone:str,email:str=""):
		self.uuid = uuid.uuid4() # 128-bit uuid.
		self.first_name, self.last_name = first_name, last_name
		self.phone = phone
		self.email = email

		self.__accounts = []
	
	# ReGex phone number validation string.
	# src: https://stackoverflow.com/questions/39990179/regex-for-australian-phone-number-validation
	PHONE_REGEX = r"^(?:\+?(61))? ?(?:\((?=.*\)))?(0?[2-57-8])\)? ?(\d\d(?:[- ](?=\d{3})|(?!\d\d[- ]?\d[- ]))\d\d[- ]?\d[- ]?\d{3})$"
	# Publically update client's phone number.
	def update_phone_number(self,phone:str):
		# Validate phone input w/ RegEx
		if re.fullmatch(self.PHONE_REGEX,phone):
			self.phone = phone
		else: print("Failed to update phone number - Invalid number.")

	# Regex email validation string.
	# src: https://www.geeksforgeeks.org/python/check-if-email-address-valid-or-not-in-python/
	EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
	# Publically update client's email.
	def update_email(self,email:str):
		# Validate email input w/ RegEx.
		if re.fullmatch(self.EMAIL_REGEX,email):
			self.email = email
		else: print("Failed to update email - Invalid email.")

	# Publically update client's name.
	def update_name(self,first_name:str,last_name:str):
		# Validate first and last name strings are of sensible length.
		if len(first_name) < 2 or len(first_name) > 50:
			print("Failed to update name - Invalid first name.")
		elif len(last_name) < 2 or len(last_name) > 50:
			print("Failed to update name - Invalid last name.")
		else: self.first_name, self.last_name = first_name, last_name

	# Open new account under client's name.
	# type: e.g. checking, saving.
	def open_account(self,type:str,opening_balance:float=0):
		try: # Validate opening balance
			o_bal = int(opening_balance)
			# Validate type
			if type in Account.valid_types:
				self.__accounts.append(Account(type, o_bal))
			else:
				print("Failed to open account - Invalid type.")
				print("Valid types:" + Account.valid_types)
		except ValueError:
			print("Failed to open account - Invalid type.")

	# Close account
	def close_account(self, uuid:uuid.UUID):
		for a in self.__accounts:
			if a.uuid == uuid:
				a.set_status("closed")
				break
		else:
			print("Failed to close account - No account with uuid found.")

	# Get all accounts.
	def get_accounts(self): return self.__accounts


class Account():

	valid_types = ["checking", "saving"]

	def __init__(self,type:str,opening_balance:float):
		self.uuid = uuid.uuid4()
		self.__acc_type = type
		self.__balance = opening_balance
		self.__status = "open"

	# Get, set balance for account.
	def get_balance(self): return self.__balance
	def update_balance(self,value:float):
		# Check if account is closed.
		if self.__status == "closed":
			print("Failed to update balance - Account closed.")
			return
		try: self.__balance = float(value) # Catch invalid value.
		except ValueError:
			print("Failed to update balance - Invalid value.")

	# Add balance to accound
	def add_balance(self,value:float):
		# Check if account is closed.
		if self.__status == "closed":
			print("Failed to add balance - Account closed.")
			return
		try: self.__balance += float(value) # Catch invalid value.
		except ValueError:
			print("Failed to add balance - Invalid value.")
	# Remove balance to account.
	def remove_balance(self,value:float):
		# Check if account is closed.
		if self.__status == "closed":
			print("Failed to remove balance - Account closed.")
			return
		try:
			val = float(value) # Catch invalid value.
			# Check if account has sufficient funds.
			if val > self.__balance: print("Failed to remove balance - Insufficent funds.")
			else: self.__balance -= val
		except ValueError:
			print("Failed to remove balance - Invalid value.")

	# Get, set account types.
	def get_type(self): return self.__acc_type
	def set_type(self,type:str):
		# Check if account is closed.
		if self.__status == "closed":
			print("Failed to set type - Account closed.")
		# Validate type.
		elif type in self.valid_types:
			self.acc_type = type
		else:
			print("Failed to set type - Invalid type.")
			print("Valid types:" + self.valid_types)

	# Get, set status of account (open/closed).
	def get_status(self): return self.__status
	def set_status(self,status:str):
		# Validate status.
		if status != "open" or status != "closed":
			print("Failed to set status - Invalid status.")
		else: self.__status = status

# Client and account tests.
client_1 = Client("john","doe","0123 456 789","johndoe@example.com")
client_2 = Client("jane","doe","+61 234 567 890","janedoe@example.com")
client_3 = Client("client","name","+61 345 678 901","clientname@example.com")

client_1.open_account("saving",500)
client_2.open_account("checking")
client_2.open_account("saving")
client_3.open_account("saving",1000)

print("-- Client attribute tests --")

print("Client 1 UUID:",client_1.uuid)
print("Client 2 Accounts:",client_2.get_accounts())

print("\n-- Client method tests")

print("Client 3 Email:",client_3.email)
client_3.update_email("clientnameupdated@example.com")
print("Client 3 Email:",client_3.email)

print("Client 3 Name:",client_3.first_name, client_3.last_name)
client_3.update_name("updated", "name")
print("Client 3 Name:",client_3.first_name, client_3.last_name)

print("\n-- Client account balance tests --")

print("Client 1 - Account 1 Balance:",client_1.get_accounts()[0].get_balance())
client_1.get_accounts()[0].add_balance(500)
print("Client 1 - Account 1 Balance:",client_1.get_accounts()[0].get_balance())

print("Client 2 - Account 2 Balance:",client_2.get_accounts()[1].get_balance())
client_2.get_accounts()[1].add_balance(1000)
print("Client 2 - Account 2 Balance:",client_2.get_accounts()[1].get_balance())

print("Client 3 - Account 1 Balance:",client_3.get_accounts()[0].get_balance())
client_3.get_accounts()[0].remove_balance(200)
print("Client 3 - Account 1 Balance:",client_3.get_accounts()[0].get_balance())

print("Client 2 - Account 1 Balance:",client_2.get_accounts()[0].get_balance())
client_2.get_accounts()[0].remove_balance(1000)
print("Client 2 - Account 1 Balance:",client_2.get_accounts()[0].get_balance())

print("\n-- Class uniqueness test --")

print("Client 1 Phone:",client_1.phone,"Client 2 Phone:",client_2.phone)
client_1.update_phone_number("+61 876 543 210")
print("Client 1 Phone:",client_1.phone,"Client 2 Phone:",client_2.phone)