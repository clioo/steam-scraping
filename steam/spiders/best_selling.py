# -*- coding: utf-8 -*-
import scrapy
from ..items import SteamItem


class BestSellingSpider(scrapy.Spider):
    name = 'best_selling'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?filter=topsellers/']

    def parse(self, response):
        steam_item = SteamItem()
        games = response.xpath("//div[@id='search_resultsRows']/a")
        for game in games:
            game_url = game.xpath(".//@href").get()
            img_url = game.xpath(".//img/@src")
            game_name = game.xpath(".//span[@class='title']/text()")
            release_date = game.xpath(".//div[contains(@class, 'search_released')]/text()")
            platforms = game.xpath(
                """.//span[contains(@class, 'platform_img') or 
                @class='vr_supported']/@class"""
            )
            steam_item['game_url'] = game_url.get()
            steam_item['img_url'] = img_url.get()
            steam_item['game_name'] = game_name.get()
            steam_item['release_date'] = release_date.get()
            steam_item['platforms'] = platforms.getall()


        
