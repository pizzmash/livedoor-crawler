# scraping-livedoorNEWS
## About
SeleniumとChromeDriverでlivedoorNEWSから記事を持ってきてcsvに出力するやつ

livedoorNEWSの各カテゴリについて，記事一覧ページ(最大300ページ)に乗っている各記事(最大300ページx20記事)を見に行く

## Usage
output.csvに出力
```
python main.py output.csv
```
dockerを使っている場合
```
python main.py output.csv --docker
```
各カテゴリについて，記事一覧ページ10ページ分の記事を見に行きたい(各カテゴリについて10ページx20記事)
```
python main.py output.csv --npages=10
```
2020年11月1日以降の記事を取得したい
```
python main.py output.csv --date 202011010000
```
以前に生成されたprevious.csv以降に出版された記事を集めたい
```
python main.py output.csv --ref previous.csv
```
