#!/usr/bin/env python

"""

Browser: part of the brainbehavior python package

BrainBehavior: This module will work with three databases that
combined can make inferences about disorders and behaviors:

SAMPLE USAGE: Please see README included with package

"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_browser():
    return webdriver.Firefox()

def get_page(url):
    browser.get(url)

# Run javascript and get output
def run_javascript(browser,code):
    return browser.execute_script(code)

# Blogger Functions
# A function to click to the next page
def next_page(browser,page_number):
    browser.execute_script('''
        var page_number = parseInt(arguments[0])
        document.getElementsByClassName("gsc-cursor-page")[page_number].click()
        ''',page_number)

# A function to get blog urls on a page
def get_blogs(browser):
    return browser.execute_script('''
        var results = document.getElementsByClassName('gsc-url-top')
        var urls = [];
        for (i = 0; i < results.length-2; i++) { 
            urls.push(results[i].children[0].textContent)
        }
        return urls''')
