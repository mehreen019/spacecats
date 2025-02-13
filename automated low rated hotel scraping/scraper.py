import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import sqlite3
import time
import random

os.environ['PATH'] += r"C:\\SeleniumDrivers"

ua = UserAgent()

conn = sqlite3.connect('hotels.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
                CREATE TABLE IF NOT EXISTS hotels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    url TEXT UNIQUE
);
                """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id INTEGER,
    rating INTEGER,
    date TEXT,
    FOREIGN KEY(hotel_id) REFERENCES hotels(id)
);
               """)

conn.commit()

def load_proxies(file_path="proxies.txt"):
    proxies = []
    with open(file_path, "r") as file:
        for line in file:
            proxy = line.strip()
            proxies.append(proxy)
    return proxies

def get_random_proxy():
    proxies = load_proxies()
    return random.choice(proxies)

def get_driver_with_proxy():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without opening browser
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--proxy-server={proxy}")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

proxy = get_random_proxy()

driver = get_driver_with_proxy()

driver.get("https://www.tripadvisor.com/Hotel_Review-g31281-d217203-Reviews-DoubleTree_by_Hilton_Phoenix_Mesa-Mesa_Arizona.html")
time.sleep(random.uniform(15, 20))

soup = BeautifulSoup(driver.page_source, "html.parser")
hotel_name = soup.select_one("h1").text.strip()
print("Hotel Name:", hotel_name)

reviews = soup.find_all("span", class_="QErCz")
print(reviews)
