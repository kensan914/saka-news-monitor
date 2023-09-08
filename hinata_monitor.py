from src.news_crawler import NewsCrawler
from src.news_line_bot import NewsLineBot


def main():
    news_items = NewsCrawler.call_hinata()
    NewsLineBot.call_hinata(news_items)


if __name__ == "__main__":
    main()
