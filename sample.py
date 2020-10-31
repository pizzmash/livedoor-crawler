import time
from selenium import webdriver


url = "https://news.livedoor.com/topics/category/dom/"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


driver = webdriver.Chrome(options=options)
driver.get(url)
articles = driver.find_elements_by_class_name("articleList")
print(articles)

"""
driver.get('https://www.google.com/')
time.sleep(5)
search_box = driver.find_element_by_name("q")
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5)
driver.quit()
"""
