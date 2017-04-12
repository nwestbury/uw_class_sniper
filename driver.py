from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

class Driver():
	def __init__(self, username, password, login_url="https://quest.pecs.uwaterloo.ca/psp/SS/ACADEMIC/"):
		"""
		Initalize login for driver. *Warning* your password is going to be held in plaintext in memory
		"""
		self.__username = username
		self.__password = password
		self.__login_url = login_url
		self.__driver = webdriver.Chrome()

	def start(self):
		self.__login()
		self.__go_to_enroll_page()
		self.__select_tab('add')

	def __insert_in_input(self, input_field, text):
		input_field.clear()
		input_field.send_keys(text)

	def __wait_for_xpath(self, xpath, timeout=10):
		timeout = 10 # seconds to wait
		try:
			# Wait until a particular name input is loaded
			element_presence = EC.presence_of_element_located((By.XPATH, xpath))
			WebDriverWait(self.__driver, timeout).until(element_presence)
		except TimeoutException:
			raise TimeoutException("Failed to find {} within {} seconds of page load".format(xpath, timeout))

	def __login(self):
		self.__driver.get(self.__login_url)

		# To be safe, explictely wait for all elements
		self.__wait_for_xpath("//input[@name='userid']")
		self.__wait_for_xpath("//input[@name='pwd']")
		self.__wait_for_xpath("//input[@name='Submit']")
		
		username_input = self.__driver.find_element_by_name("userid")
		password_input = self.__driver.find_element_by_name("pwd")
		submit_button = self.__driver.find_element_by_name("Submit")
		
		self.__insert_in_input(username_input, self.__username)
		self.__insert_in_input(password_input, self.__password)
		submit_button.click()

	def __go_to_enroll_page(self):
		try:
			WebDriverWait(self.__driver, 5)
		except TimeoutException:
			print("WaitED")
		
		self.__driver.excute_script("submitAction_win0(document.win0,'DERIVED_SSS_SCR_SSS_LINK_ANCHOR3');")

	def __select_tab(self, name):
		xpath = "//a[@class=SSSTABMAINTEXT and text()[normalize-space(.)='{}']".format(name)
		self.__wait_or_xpath(xpath)
		tab = self.__driver.find_element_by_xpath(xpath)
		tab.click()

	def __select_latest_term(self):
		# second option in term select, I assume there will only be two options and the second will be the latest
		self.__wait_for_xpath("//input[@id='SSR_DUMMY_RECV1$sels$1$$0']")
		self.__wait_for_xpath("//a[@id='DERIVED_SSS_SCT_SSR_PB_GO']")

		radio_button = self.__driver.find_element_by_id("SSR_DUMMY_RECV1$sels$1$$0")
		submit_button = self.__driver.find_element_by_id("DERIVED_SSS_SCT_SSR_PB_GO")
		radio_button.click()
		submit_button.click()
		
		
		
	def exit(self):
		self.__driver.close()

