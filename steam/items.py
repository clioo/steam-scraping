# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.selector import Selector
from w3lib.html import remove_tags


def remove_html(review_summary):
    return remove_tags(review_summary) if review_summary != None else 'No reviews'


def get_platforms(one_class):
    """one_class - strings, containing the supported platform"""
    platforms = []

    platform = one_class.split(' ')[-1]
    if platform == 'win':
        platforms.append('Windows')
    if platform == 'mac':
        platforms.append('Mac os')
    if platform == 'linux':
        platforms.append('Linux')
    if platform == 'vr_supported':
        platforms.append('VR Supported')

    return platforms


def get_original_price(html_markup):
    """Gets the original price, if child nodes is greater than 0,
    it has a discount, so the xpath is different to get it"""
    original_price = ''
    selector_obj = Selector(text=html_markup)
    div_with_discount = selector_obj.xpath(
        ".//div[contains(@class, 'search_price discounted')]")
    if len(div_with_discount) > 0:
        original_price = div_with_discount.xpath(".//span/strike/text()").get()
    else:
        original_price = selector_obj.xpath(
            ".//div[contains(@class, 'search_price')]/text()").getall()

    return original_price


def clean_discount_rate(discount_rate):
    if discount_rate:
        return discount_rate.lstrip('-')
    return discount_rate


def clean_discounted_price(discounted_price):
    if discounted_price:
        return discounted_price.strip()

    return discounted_price


class SteamItem(scrapy.Item):
    game_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    img_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    game_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    release_date = scrapy.Field(
        output_processor=TakeFirst()
    )
    # This one returns more than 1
    platforms = scrapy.Field(
        input_processor=MapCompose(get_platforms),
    )

    reviews = scrapy.Field(
        input_processor=MapCompose(remove_html),
        output_processor=TakeFirst()
    )
    original_price = scrapy.Field(
        input_processor=MapCompose(get_original_price, str.strip),
        output_processor=Join('')
    )
    discounted_price = scrapy.Field(
        input_processor=MapCompose(clean_discounted_price),
        output_processor=TakeFirst()
    )
    discount_rate = scrapy.Field(
        input_processor=MapCompose(clean_discount_rate),
        output_processor=TakeFirst()
    )
