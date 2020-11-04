import argparse
from writer import Writer
from crawler import Crawler


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('out', help='output csv file')
  parser.add_argument('--docker', action='store_true', help='if you are using docker')
  args = parser.parse_args()

  writer = Writer(args.out)
  crawler = Crawler(docker=args.docker)

  for i, article in enumerate(crawler.crawl(sleep_time=5)):
    writer.write(article)
    print("csvに書き込みました({}件完了)\n".format(i+1))
  f.close()


if __name__ == "__main__":
  main()
