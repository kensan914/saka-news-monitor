import urllib.parse
import certifi
import urllib3
from bs4 import BeautifulSoup, Tag
from urllib3 import BaseHTTPResponse
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime, timedelta
from pytz import timezone

from src.news_item import NewsItem


class NewsCrawler:
    CATEGORY_FILTERS = ["イベント", "グッズ", "チケット", "ファンクラブ"]

    @classmethod
    def call_hinata(cls):
        base_url = "https://www.hinatazaka46.com"
        news_url = f"https://www.hinatazaka46.com/s/official/news/list?ima=0000&dy={cls.format_yesterday()}"
        news_item_tags_selector = "li.p-news__item > a"
        category_selector = "div.c-news__category"
        title_selector = "p.c-news__text"

        return cls()._call(
            base_url,
            news_url,
            news_item_tags_selector,
            category_selector,
            title_selector,
        )

    @classmethod
    def call_sakura(cls):
        base_url = "https://sakurazaka46.com"
        news_url = f"https://sakurazaka46.com/s/s46/news/list?ima=0000&dy={cls.format_yesterday()}"
        news_item_tags_selector = "ul.com-news-part a"
        category_selector = "p.type"
        title_selector = "p.lead"

        return cls()._call(
            base_url,
            news_url,
            news_item_tags_selector,
            category_selector,
            title_selector,
        )

    def __init__(self):
        ...

    def _call(
        self,
        base_url: str,
        news_url: str,
        news_item_tags_selector: str,
        category_selector: str,
        title_selector: str,
    ):
        response = self._request_news(news_url)
        return self._parse(
            response,
            base_url,
            news_item_tags_selector,
            category_selector,
            title_selector,
        )

    @staticmethod
    def format_yesterday():
        """0時に定期実行して前日のニュースを取得して通知するため、1日前の日付を指定する"""
        yesterday = datetime.now() - timedelta(days=1)
        ja_yesterday = yesterday.astimezone(timezone("Asia/Tokyo"))
        return ja_yesterday.strftime("%Y%m%d")

    @staticmethod
    def _request_news(url: str) -> BaseHTTPResponse:
        urllib3.disable_warnings(InsecureRequestWarning)
        http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
        return http.request("GET", url)

    def _parse(
        self,
        response: BaseHTTPResponse,
        base_url: str,
        news_item_tags_selector: str,
        category_selector: str,
        title_selector: str,
    ) -> list[NewsItem]:
        soup = BeautifulSoup(response.data, "lxml")
        news_item_a_tags = soup.select(news_item_tags_selector)

        def init_news_item(news_item_a_tag: Tag) -> NewsItem | None:
            category = news_item_a_tag.select_one(category_selector).text.strip()
            if category not in self.CATEGORY_FILTERS:
                return

            title = news_item_a_tag.select_one(title_selector).text.strip()
            news_detail_path = news_item_a_tag.get("href")
            news_detail_url = urllib.parse.urljoin(base_url, news_detail_path)
            return NewsItem(title=title, url=news_detail_url, category=category)

        news_items_nullable = list(map(init_news_item, news_item_a_tags))
        return [news_item for news_item in news_items_nullable if news_item is not None]
