# -*- coding: utf-8 -*-
import scrapy
from ..items import SteamItem
from scrapy.loader import ItemLoader


class BestSellingSpider(scrapy.Spider):
    name = 'best_selling'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?filter=topsellers/']

    def get_platforms(self, classes_list):
        """classes_list - list of strings, containing the supported platforms
        as classes of a single item"""
        platforms = {
            'win': 'Windows',
            'mac': 'Mac',
            'linux': 'Linux',
            'vr_supported': 'VR'
        }
        supported_platforms = []

        for class_list in classes_list:
            platform = class_list.split(' ')[-1]
            supported_platforms.append(platforms.get(platform, platform))
        return supported_platforms

    def get_original_price(self, selector_object):
        """Gets the original price, if child nodes is greater than 0,
        it has a discount, so the xpath is different to get it"""
        child_nodes = selector_object.xpath(".//*").getall()
        if len(child_nodes) == 0:
            original_price = selector_object.xpath(
                "normalize-space(./text())"
            ).get()
        else:
            original_price = remove_tags(selector_object.xpath(".//strike").get())
        return original_price

    def parse(self, response):
        games = response.xpath("//div[@id='search_resultsRows']/a")
        for game in games:
            loader = ItemLoader(item=SteamItem(), selector=game,
                                response=response)
            # Locators
            loader.add_xpath('game_url', ".//@href")
            loader.add_xpath('img_url', ".//img/@src")
            loader.add_xpath('game_name', ".//span[@class='title']/text()")
            loader.add_xpath('release_date', ".//div[contains(@class, 'search_released')]/text()")
            loader.add_xpath('platforms', 
                """.//span[contains(@class, 'platform_img') or 
                @class='vr_supported']/@class"""
            )
            loader.add_xpath('reviews', 
                """.//span[contains(@class, 
                'search_review_summary')]/@data-tooltip-html"""
            )
            loader.add_xpath('discount_rate', 
                ".//div[contains(@class, 'search_discount')]/span/text()"
            )
            loader.add_xpath('original_price', 
                """.//div[contains(@class, 'search_price_discount_combined')]
                /div[contains(@class, 'search_price')]"""
            )
            loader.add_xpath('discounted_price', 
                """(.//div[contains(@class, 
                'search_price discounted')]/text())[2]"""
            )
            yield loader.load_item()
        next_page = response.xpath(
            "//a[@class='pagebtn' and contains(text(), '>')]/@href"
        ).get()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse
            )


        
