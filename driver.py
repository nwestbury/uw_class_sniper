from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from time import sleep

class ElementCondition():
	presence = EC.presence_of_element_located
	clickable = EC.element_to_be_clickable

class Driver():
	def __init__(self, username, password):
		"""
		Initalize login for driver. *Warning* your password is going to be held in plaintext in memory
		and in the commandline
		"""
		self.__username = username
		self.__password = password
		self.__login_url = "https://quest.pecs.uwaterloo.ca/psp/SS/ACADEMIC/"
		self.__add_url = "https://quest.pecs.uwaterloo.ca/psc/SS/ACADEMIC/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL"
		self.__driver = webdriver.Chrome()
		self.__wait_time = 60*60*2

	def start(self):
		self.__login()
		self.__go_to_add_page()
		self.__select_latest_term()

		attempt_num = 0
		while True:
			self.__attempt_add()
			self.__restart_add()
			attempt_num += 1
			print("Done attempt", attempt_num)
			sleep(self.__wait_time)

	def __insert_in_input(self, input_field, text):
		input_field.clear()
		input_field.send_keys(text)

	def __wait_for_xpath(self, xpath, timeout=10, condition=ElementCondition.presence):
		timeout = 10 # seconds to wait
		try:
			# Wait until a particular name input is loaded
			element_presence = condition((By.XPATH, xpath))
			WebDriverWait(self.__driver, timeout).until(element_presence)
		except TimeoutException:
			print("Failed to find {} within {} seconds of page load".format(xpath, timeout))
			raise

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

	def __switch_to_internal_iframe(self):
		iframe_xpath = "//iframe[@id='ptifrmtgtframe']"
		self.__wait_for_xpath(iframe_xpath)
		frame = self.__driver.find_element_by_id("ptifrmtgtframe")
		self.__driver.switch_to.frame(frame)

	def __go_to_add_page(self):
		self.__driver.get(self.__add_url)

	def __select_latest_term(self):
		# second option in term select, I assume there will only be two options and the second will be the latest
		self.__wait_for_xpath("//input[@id='SSR_DUMMY_RECV1$sels$1$$0']")
		self.__wait_for_xpath("//a[@id='DERIVED_SSS_SCT_SSR_PB_GO']")

		radio_button = self.__driver.find_element_by_id("SSR_DUMMY_RECV1$sels$1$$0")
		radio_button.click()

		self.__driver.execute_script("submitAction_win0(document.win0,'DERIVED_SSS_SCT_SSR_PB_GO');")

	def __attempt_add(self):
		try:
			self.__wait_for_xpath("//a[@id='DERIVED_REGFRM1_LINK_ADD_ENRL$82$'", timeout=2)
		except TimeoutException:
			pass
		
		self.__driver.execute_script("submitAction_win0(document.win0,'DERIVED_REGFRM1_LINK_ADD_ENRL$82$');")

		try:
			self.__wait_for_xpath("//a[@id='DERIVED_REGFRM1_SSR_PB_SUBMIT'", timeout=2)
		except TimeoutException:
			pass

		self.__driver.execute_script("submitAction_win0(document.win0,'DERIVED_REGFRM1_SSR_PB_SUBMIT');")

	def __restart_add(self):
		try:
			self.__wait_for_xpath("//a[@id='DERIVED_REGFRM1_SSR_LINK_STARTOVER'", timeout=2)
		except TimeoutException:
			pass

		self.__driver.execute_script("submitAction_win0(document.win0,'DERIVED_REGFRM1_SSR_LINK_STARTOVER');")
		
	def exit(self):
		self.__driver.close()

