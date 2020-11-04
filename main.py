import argparse
from csvtools import Reader, Writer
from crawler import Crawler


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('out', help='output csv file')
  parser.add_argument('--ref', help='If you have previously created csv and want to collect new articles')
  parser.add_argument('--docker', action='store_true', help='If you are using docker')
  args = parser.parse_args()

  if args.ref:
    reader = Reader(args.ref)
    print(reader.latest_date())
    del reader
    # exit()

  writer = Writer(args.out)
  crawler = Crawler(docker=args.docker)

  for i, article in enumerate(crawler.crawl(sleep_time=5)):
    writer.write(article)
    print("csvに書き込みました({}件完了)\n".format(i+1))
  del writer

if __name__ == "__main__":
  main()
