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

	f = open('./test.csv', 'w')
	writer = csv.writer(f)
	writer.writerow(csv_header)

	for i, article in enumerate(crawler.crawl(sleep_time=5)):
		writer.writerow(article)
		print("csvに書き込みました({}件完了)\n".format(i+1))
	f.close()


if __name__ == "__main__":
	main()
