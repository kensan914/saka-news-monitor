from src.news_crawler import NewsCrawler
from src.news_line_bot import NewsLineBot


def main():
    news_items = NewsCrawler.call_sakura()
    NewsLineBot.call_sakura(news_items)


if __name__ == "__main__":
    main()
