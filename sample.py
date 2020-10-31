import time
import os
import re
import csv

from selenium import webdriver
from urllib import parse


base = "https://news.livedoor.com/topics/category/"
categories = [
	"main/",
	"dom/",
	# "world/",
	# "eco/",
	# "ent/",
	# "sports/",
	# "52/",
	# "gourmet/",
	# "love/",
	# "trend/"
]

sleep_time = 5

csv_header = [
	"url",
	"year", "month", "day", "hour", "minute",
	"category",
	"title",
	"summary1", "summary2", "summary3",
	"body"
]


def parse_time(jtime):
	pattern = r'(\d*)年(\d*)月(\d*)日 (\d*)時(\d*)分'
	m = re.match(pattern, jtime)
	return m.groups()


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')

driver = webdriver.Chrome(options=options)

visited_ids = []

written = 0

f = open('./sample.csv', 'w')
writer = csv.writer(f)
writer.writerow(csv_header)

for page in range(1, 301):
	if page == 3:
		break
	params = parse.urlencode({'p': str(page)})
	for category in categories:
		category_url = parse.urljoin(base, category) + "?{params}".format(params=params)
		driver.get(category_url)
		print("{}にアクセスしました".format(category_url))

		articles = driver.find_elements_by_class_name("articleList")
		if not articles:
			print("記事の一覧を取得できませんでした\n")
			time.sleep(sleep_time)
			continue
		articles = articles[0].find_elements_by_tag_name("li")
		articles = list(map(lambda x: x.find_elements_by_tag_name("a")[0].get_attribute("href"), articles))
		time.sleep(sleep_time)

		for article_url in articles:
			path = parse.urlparse(article_url).path
			if path[-1] == "/":
				path = path[:-1]
			id = int(os.path.basename(path))
			if id in visited_ids:
				continue
			visited_ids.append(id)
			driver.get(article_url)
			print("{}にアクセスしました".format(article_url))
			summary_list = driver.find_elements_by_class_name("summaryList")
			if not summary_list:
				print("要約が存在しません\n")
				time.sleep(sleep_time)
				continue
			more_button = driver.find_elements_by_class_name("articleMore")
			if not more_button:
				print("本文が削除されています\n")
				time.sleep(sleep_time)
				continue
			title = driver.find_elements_by_class_name("topicsTtl")[0].text
			jtime = driver.find_elements_by_class_name("topicsTime")[0].text
			date = [str(t) for t in parse_time(jtime)]
			summary_list = summary_list[0].find_elements_by_tag_name("li")
			summary_list = [s.text for s in summary_list]
			time.sleep(sleep_time)

			more_url = more_button[0].find_elements_by_tag_name("a")[0].get_attribute("href")
			driver.get(more_url)
			print("{}にアクセスしました".format(more_url))
			body = driver.find_elements_by_xpath("//span[@itemprop='articleBody']")
			if not body:
				print("本文の取得に失敗しました\n")
				time.sleep(sleep_time)
				continue
			body = body[0].text

			writer.writerow([
				article_url,
				date[0], date[1], date[2], date[3], date[4],
				category,
				title,
				summary_list[0], summary_list[1], summary_list[2],
				body
			])
			written += 1
			print("csvに書き込みました({}件完了)\n".format(written))
			time.sleep(sleep_time)

f.close()
driver.quit()
