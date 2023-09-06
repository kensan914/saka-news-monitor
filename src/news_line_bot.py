import os

from linebot import LineBotApi
from linebot.models import TextSendMessage

from src.news_item import NewsItem


class NewsLineBot:
    CATEGORY_EMOJI_DICT = {
        "イベント": "🏟️",
        "グッズ": "👕",
        "チケット": "🎟️",
        "ファンクラブ": "⭐",
    }

    @classmethod
    def call_hinata(cls, news_items: list[NewsItem]):
        line_channel_access_token = os.environ.get("HINATA_LINE_CHANNEL_ACCESS_TOKEN")
        return cls()._call(line_channel_access_token, news_items)

    def _call(self, line_channel_access_token: str, news_items: list[NewsItem]):
        line_bot_api = LineBotApi(line_channel_access_token)
        for news_item in news_items:
            line_bot_api.broadcast(self._gene_text_send_message(news_item))

    def _gene_text_send_message(self, news_item: NewsItem):
        category_emoji = (
            self.CATEGORY_EMOJI_DICT.get(news_item.category)
            if news_item.category in self.CATEGORY_EMOJI_DICT
            else ""
        )

        return TextSendMessage(
            text=f"【{category_emoji}{news_item.category}】\n{news_item.title}\n{news_item.url}"
        )
