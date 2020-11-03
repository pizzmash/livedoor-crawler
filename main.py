from writer import Writer
from crawler import Crawler


def main():
	writer = Writer('./test.csv')
	crawler = Crawler(docker=True)

	for i, article in enumerate(crawler.crawl(sleep_time=5)):
		writer.write(article)
		print("csvに書き込みました({}件完了)\n".format(i+1))
	f.close()


if __name__ == "__main__":
	main()
