import os
import json
import requests
from datetime import datetime
from gtts import gTTS
from bs4 import BeautifulSoup
from typing import List
import re

# フォルダ準備
today = datetime.now().strftime("%Y-%m-%d")
output_dir = os.path.join("output", today)
os.makedirs(output_dir, exist_ok=True)

# 設定ファイル読み込み
with open("keywords.json", "r", encoding="utf-8") as f:
    config = json.load(f)

        keywords = config["keywords"]
            lang_ratio = config["lang_ratio"]
                urls=config["urls"]

                # ニュース取得（Yahoo! 経済RSS）
                def fetch_yahoo_news(urls):
                    for url in urls:
                            r = requests.get(url)
                                    soup = BeautifulSoup(r.content, features="xml")
                                            items = soup.find_all("item")
                                                    articles = []
                                                            for item in items:
                                                                        title = item.title.text
                                                                                    link = item.link.text
                                                                                            # print(f"title: {title}")
                                                                                                        articles.append({"title": title, "link": link})
                                                                                                            print(len(articles), "articles fetched from Yahoo! News") #取得件数の確認
                                                                                                                # # 記事のランダム化
                                                                                                                    # import random
                                                                                                                        # random.shuffle(articles)
                                                                                                                            return articles

                                                                                                                            # フィルタリング                                                        
                                                                                                                            def filter_articles(articles, keywords):
                                                                                                                                filtered = []
                                                                                                                                    for article in articles:
                                                                                                                                            if any(kw in article["title"] for kw in keywords):
                                                                                                                                                        filtered.append(article)
                                                                                                                                                            return filtered

                                                                                                                                                            # 要約（ここでは仮の要約）
                                                                                                                                                            def summarize(title):
                                                                                                                                                                # ここでは単純にタイトルを要約として返す
                                                                                                                                                                    # 実際の要約処理は別途実装が必要
                                                                                                                                                                        sentences = re.split(r'[。．]', title)

                                                                                                                                                                            return f"タイトルは、{title} "

                                                                                                                                                                             # 音声化
                                                                                                                                                                             def speak(text, filename, lang='ja'):
                                                                                                                                                                               tts = gTTS(text, lang=lang)
                                                                                                                                                                                 tts.save(filename)

                                                                                                                                                                                 def filter_articles(articles, keywords):
                                                                                                                                                                                     filtered = []
                                                                                                                                                                                         for article in articles:
                                                                                                                                                                                                 if any(kw in article["title"] for kw in keywords):
                                                                                                                                                                                                             filtered.append(article)
                                                                                                                                                                                                                 return filtered

                                                                                                                                                                                                                 # 実行
                                                                                                                                                                                                                 def main():
                                                                                                                                                                                                                     articles = fetch_yahoo_news(urls)
                                                                                                                                                                                                                         filtered = filter_articles(articles, keywords)

                                                                                                                                                                                                                             summaries = []
                                                                                                                                                                                                                                 for i, article in enumerate(filtered[:8]):
                                                                                                                                                                                                                                         summary = summarize(article["title"])
                                                                                                                                                                                                                                                 summaries.append(f"{i+1}. {summary}")
                                                                                                                                                                                                                                                     # まとめて1つのテキストに
                                                                                                                                                                                                                                                         all_summaries = "\n".join(summaries)
                                                                                                                                                                                                                                                             # まとめて音声化
                                                                                                                                                                                                                                                                 mp3_path = os.path.join(output_dir, "summary_all_ja.mp3")
                                                                                                                                                                                                                                                                     speak(all_summaries, mp3_path, lang='ja')
                                                                                                                                                                                                                                                                          # 英語ニュースは今後追加予定（例：Reuters）

                                                                                                                                                                                                                                                                               # テキスト保存（オプション）
                                                                                                                                                                                                                                                                                   with open(os.path.join(output_dir, "summary.txt"), "w", encoding="utf-8") as f:
                                                                                                                                                                                                                                                                                           f.write("todays news"+"\n")
                                                                                                                                                                                                                                                                                                   f.write(f"date:{today}\n")
                                                                                                                                                                                                                                                                                                           f.write("keywords:"+",".join(keywords)+"\n")
                                                                                                                                                                                                                                                                                                                   f.write("summary:\n")
                                                                                                                                                                                                                                                                                                                           for article in filtered[:8]:
                                                                                                                                                                                                                                                                                                                                       f.write(summarize(article["title"]) + "\n")


                                                                                                                                                                                                                                                                                                                                       if __name__ == "__main__":
                                                                                                                                                                                                                                                                                                                                           main()
                                                                                                                                                                                                                                                                                                                                               print(f"音声ファイルは {output_dir} に保存されました。")