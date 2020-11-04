import argparse
from datetime import datetime
from csvtools import Reader, Writer
from crawler import Crawler


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('out', help='output csv file')
  parser.add_argument('--npages', default=300, help='how many pages to crawl in each category')
  parser.add_argument('--sleep-time', default=5, help='sleep time')
  parser.add_argument('--ref', help='If you have previously created csv and want to collect new articles')
  parser.add_argument('--date', help='date threshould for format \"YYYYmmddHHMM\"')
  parser.add_argument('--docker', action='store_true', help='If you are using docker')
  args = parser.parse_args()

  # いつまでの記事を取得するか
  if args.date:
    date_tl = datetime.strptime(args.date, "%Y%m%d%H%M")
  else:
    date_tl = None

  # カテゴリごとにいつまでの記事を取得するか
  if args.ref:
    reader = Reader(args.ref)
    date_tl_cates = reader.latest_date()
    del reader
  else:
    date_tl_cates = None

  writer = Writer(args.out)
  crawler = Crawler(docker=args.docker)

  for i, article in enumerate(crawler.crawl(npages=args.npages,
                                            date_tl=date_tl,
                                            date_tl_cates=date_tl_cates,
                                            sleep_time=args.sleep_time)):
    writer.write(article)
    print("csvに書き込みました({}件完了)\n".format(i+1))
  del writer

if __name__ == "__main__":
  main()
