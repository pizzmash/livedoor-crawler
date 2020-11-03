import csv
from crawler import Crawler

csv_header = [
	"url", "id",
	"year", "month", "day", "hour", "minute",
	"category",
	"title",
	"summary1", "summary2", "summary3",
	"body"
]


def main():
	crawler = Crawler(docker=True)

	f = open('./sample.csv', 'w')
	writer = csv.writer(f)
	writer.writerow(csv_header)

	for article in crawler.crawl(sleep_time=5):
		writer.writerow(article)

	f.close()


if __name__ == "__main__":
	main()
