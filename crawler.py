import time
import os
from datetime import datetime
from selenium import webdriver
from urllib import parse


class Crawler:
  BASE = "https://news.livedoor.com/topics/category/"
  CATEGORIES = [
    "main",
    "dom",
    "world",
    "eco",
    "ent",
    "sports",
    # "52",
    # "gourmet",
    # "love",
    "trend"
  ]

  def __init__(self, docker=False):
    self.options = webdriver.ChromeOptions()
    if docker:
      self.options.add_argument('--headless')
      self.options.add_argument('--no-sandbox')
      self.options.add_argument('--disable-dev-shm-usage')

  def parse_time(self, jtime):
    pattern = '%Y年%m月%d日 %H時%M分'
    return datetime.strptime(jtime, pattern)

  def get(self, driver, url):
    try:
      driver.get(url)
      print("{}にアクセスしました".format(url))
      return True
    except Exception:
      print("{}にアクセスを試みましたがタイムアウトしました".format(url))
      return False

  def crawl(self, npages=300, date_tl=None, date_tl_cates=None, sleep_time=5):
    if date_tl or date_tl_cates:
      # カテゴリごとの完了したかのフラグ
      is_done = {category: False for category in self.CATEGORIES}
      if not date_tl and date_tl_cates:
        for category in self.CATEGORIES:
          if category not in date_tl_cates:
            is_done[category] = True
      # カテゴリごとの日時の閾値
      dtc = {category: date_tl_cates[category] if date_tl_cates
                                               and category in date_tl_cates
                       else date_tl if date_tl
                       else None for category in self.CATEGORIES}

    driver = webdriver.Chrome(options=self.options)

    visited_ids = []
    for page in range(1, npages+1):
      params = parse.urlencode({'p': str(page)})
      for category in self.CATEGORIES:
        # そのカテゴリについてまだクローリングするか確認
        if (date_tl or date_tl_cates) and is_done[category]:
          continue

        # カテゴリcategoryのpageページ目のURL
        category_url = parse.urljoin(self.BASE, category+"/") + "?{}".format(params)

        if not self.get(driver, category_url):
          print()
          continue

        articles = driver.find_elements_by_class_name("articleList")
        if not articles:
          print("記事の一覧を取得できませんでした\n")
          time.sleep(sleep_time)
          continue

        # articlesにそのページにある記事へのリンクのリストを格納
        articles = articles[0].find_elements_by_tag_name("li")
        articles = list(map(lambda x: x.find_elements_by_tag_name("a")[0].get_attribute("href"), articles))
        time.sleep(sleep_time)

        # 各ページへの処理
        for article_url in articles:
          path = parse.urlparse(article_url).path
          if path[-1] == "/":
            path = path[:-1]
          article_id = int(os.path.basename(path))
          if article_id in visited_ids:
            continue
          visited_ids.append(article_id)

          # 記事のページにアクセス
          if not self.get(driver, article_url):
            print()
            continue

          # 記事の時間の取得
          jtime = driver.find_elements_by_class_name("topicsTime")[0].text
          date = self.parse_time(jtime)

          # 指定した日時より古い記事だったらそのカテゴリは終わり
          if (date_tl or date_tl_cates) and date <= dtc[category]:
            is_done[category] = True
            print("カテゴリ{}のクローリングを終了します\n".format(category))
            time.sleep(sleep_time)
            break

          # 要約の取得
          summary_list = driver.find_elements_by_class_name("summaryList")
          if not summary_list:
            print("要約が存在しません\n")
            time.sleep(sleep_time)
            continue
          summary_list = summary_list[0].find_elements_by_tag_name("li")
          summary_list = [s.text for s in summary_list]
          if len(summary_list) != 3:
            print("要約の数が3文ではありませんでした\n")
            time.sleep(sleep_time)
            continue

          # 実際の記事内容へのリンクボタンの取得
          more_button = driver.find_elements_by_class_name("articleMore")
          if not more_button:
            print("本文が削除されています\n")
            time.sleep(sleep_time)
            continue

          # タイトルの取得
          title = driver.find_elements_by_class_name("topicsTtl")[0].text

          time.sleep(sleep_time)

          # 実際の記事の内容が書いてあるページにアクセス
          more_url = more_button[0].find_elements_by_tag_name("a")[0].get_attribute("href")
          if not self.get(driver, more_url):
            print()
            continue

          # 記事本文の取得
          body = driver.find_elements_by_xpath("//span[@itemprop='articleBody']")
          if not body:
            print("本文の取得に失敗しました\n")
            time.sleep(sleep_time)
            continue
          body = body[0].text

          yield [article_url, article_id,
                 date.year, date.month, date.day, date.hour, date.minute,
                 category,
                 title,
                 summary_list[0], summary_list[1], summary_list[2],
                 body]

          time.sleep(sleep_time)
    driver.quit()

