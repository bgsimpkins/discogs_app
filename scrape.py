from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from time import sleep
import re

from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import dbUtils
from discogs_data_classes import RecordItem, RecordMaster
from dotenv import load_dotenv

def get_records_for_release(driver, conn, type, format, id, cookies=True):

    if format.lower() == 'cd':
        format = 'CD'
    elif format.lower() == 'vinyl':
        format = 'Vinyl'

    if type == 'release':
        url = 'https://www.discogs.com/sell/release/{release_id}?format={format}&price%2Casc'.format(format=format, release_id=id)
    elif type == 'master':
        url = 'https://www.discogs.com/sell/list?master_id={master_id}&format={format}&sort=price%2Casc'.format(format=format, master_id=id)
    else:
        print('Type not supported. Exiting!')
        exit(1)

    driver.get(url)

    if cookies:
        accept_cookies(driver)

    ## Don't need to click header. Sort can be set in URL
    #table = driver.find_element_by_class_name('table_block')
    #price_header = table.find_element_by_class_name('price_header')
    #price_header.click()
    #sleep(1)
    #price_header.click()

    try:

        table = driver.find_element(By.CLASS_NAME, 'table_block')
        rows = table.find_elements(By.CLASS_NAME,'shortcut_navigable ')
    except Exception:
        print('No items found!')
        dbUtils.update_scrape_date_in_watchlist(conn, id, datetime.now())
        return

    dollar_regex = '\d+(?:\.\d+)?'
    dollar_pattern = re.compile(dollar_regex)

    comma_sep_int_regex = '\d+(?:,\d+)?'
    comma_sep_int_pattern = re.compile(comma_sep_int_regex)

    dbUtils.delete_release(conn, id)

    for r in rows:

        # See if unavailable in US
        uv = r.get_attribute('class').find('unavailable')
        available_us = 1 if uv == -1 else 0

        # Item description (contains link, condition, and details)
        description = r.find_element(By.CLASS_NAME,'item_description')
        item_link = description.find_element(By.CLASS_NAME,'item_description_title').get_property('href')

        # Get <p>s in item_description
        ps = description.find_elements(By.TAG_NAME,'p')

        # condition = ps[1].text
        condition = description.find_element(By.CLASS_NAME,'item_condition').text
        # print('Condition={}'.format(condition))

        media_condition, sleeve_condition = parse_condition(condition)

        # There can be additional <p> tags but last always seems to be description/details
        # TODO: Add try/catch. This is risky business
        description = ps[-1].text
        #print('Description={}'.format(description))

        seller_info = r.find_element(By.CLASS_NAME,'seller_info')
        seller_list = seller_info.find_elements(By.TAG_NAME,'li')

        # TODO: Using indexes here. Brittle.
        rating = None
        num_ratings = 0
        try:
            rating = seller_list[1].find_element(By.TAG_NAME,'strong').text
            rating = rating.replace('%', '')
            num_ratings_str = seller_list[1].find_element(By.CLASS_NAME,'section_link').text
            num_ratings_parsed: str = comma_sep_int_pattern.findall(num_ratings_str)
            num_ratings = int(num_ratings_parsed[0].replace(',', ''))
        except NoSuchElementException:
            print('Rating missing')


        country_span = seller_list[2]
        country = country_span.text.replace('Ships From:','')

        price = None
        try:
            price = r.find_element(By.CLASS_NAME,'item_price').find_element(By.CLASS_NAME,'converted_price').text
        except Exception as e:
            print('No coverted price found!')

        price_parsed = None
        if price is not None:
            try:
                price_parsed = dollar_pattern.findall(price)
                price_parsed = price_parsed[0]
            except Exception as e:
                print('Couldn''t parse coverted price: {}'.format(price))

        item_id = item_link.split('/')[-1]

        print('Link={link} Converted Price={price} Available={avail}'
              .format(link=item_link,
                      price=price_parsed,
                      avail=available_us)
              )

        ri = RecordItem(
            release_id=id,
            item_id=item_id,
            available=available_us,
            url=item_link,
            adjusted_price=price_parsed,
            media_condition=media_condition,
            sleeve_condition=sleeve_condition,
            details=description,
            avg_rating=rating,
            num_ratings=num_ratings,
            country=country,
            date_created=datetime.now(),
            date_updated=None
        )

        dbUtils.insert_record_item(conn, ri)

        dbUtils.update_scrape_date_in_watchlist(conn, id, datetime.now())

    # print(table)


def parse_condition(condition: str):
    # TODO: Should probably drill into <span>s instead, but this seems to work
    str_len = len('Media Condition: ')
    media_cond_start = condition.find('Media Condition') + str_len

    str_len = len('Sleeve Condition: ')
    sleeve_cond_start = condition.find('Sleeve Condition')
    media_cond = condition[media_cond_start:sleeve_cond_start-1]
    #print('Media Condition={}'.format(media_cond))

    sleeve_cond_start += str_len
    sleeve_cond = condition[sleeve_cond_start:len(condition)]
    #print('Sleeve Condition={}'.format(sleeve_cond))
    return media_cond, sleeve_cond


def accept_cookies(driver):
    # Click on button to accept cookies
    print('Accepting cookies...')

    ps = driver.page_source

    tries = 0
    while True:
        try:
            #main_wrapper = driver.find_element_by_id('main_wrapper')
            #accept_button = driver.find_element_by_id('onetrust-accept-btn-handler')
            accept_button = driver.find_element(By.ID,"onetrust-accept-btn-handler")
            accept_button.click()
            sleep(3)
            break
        except Exception:
            tries += 1
            if tries > 5:
                print('Exceeded max tries for cookie accept. Exiting..')
                exit(1)
            sleep(3)
            print('Cookie accept try #{}'.format(tries))




def create_driver(headless=False):
    # ff_options = Options()
    # ff_options.headless = headless
    opts = FirefoxOptions()
    if headless:
        opts.add_argument("--headless")
    return webdriver.Firefox(options=opts)


def scrape_for_master(driver, conn, id, format, accept_cookies=True):
    print(f'Accepting friggen cookies {accept_cookies}')
    dbUtils.delete_release(conn, id)
    get_records_for_release(driver, conn, 'master', format, id, accept_cookies)


def scrape_watchlist(conn):
    print('Scraping watchlist..')
    wl = dbUtils.get_watchlist(conn)
    driver = create_driver(True)

    i: int = 0
    for rec in wl:
        cookies = True if i == 0 else False
        #cookies = False
        scrape_for_master(driver, conn, rec.master_id, rec.formats, cookies)
        i += 1

    driver.close()
    driver.quit()


def scrape_queue(conn):
    print('Scraping scrape queue')
    batch_id = 1            ##TODO: Hard-coded. Need to tweak if wanting to scrape multiple batchs (sync or async)
    q, historical = dbUtils.get_scrape_queue(conn, batch_id)
    driver = create_driver(True)

    i: int = 0
    for rec in q:
        cookies = True if i == 0 else False
        # cookies = False
        dbUtils.update_scrape_status(conn, rec.row_id, "RUNNING")
        scrape_for_master(driver, conn, rec.master_id, rec.formats, cookies)
        dbUtils.update_scrape_status(conn, rec.row_id, "COMPLETE")
        i += 1

    driver.close()
    driver.quit()

if __name__ == '__main__':
    load_dotenv()
    conn = dbUtils.connect_to_db()
    wl = dbUtils.get_watchlist(conn)
    driver = create_driver(False)
    scrape_for_master(driver, conn, 274115, 'cd')
