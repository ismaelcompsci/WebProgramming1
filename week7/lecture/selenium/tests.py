import selenium
import os
import unittest
import pathlib
from selenium.webdriver.common.by import By


from selenium import webdriver


# Finds the Uniform Resourse Identifier of a file
def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

# Sets up web driver using Google chrome
driver = webdriver.Chrome()

driver.find_element()