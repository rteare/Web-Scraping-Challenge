import pandas as pd
from pprint import pprint
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set browser
def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)
    time.sleep(5)

# time to Scape

def mars_scrape():
    browser = init_browser()

    #set up url for Mars Facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    time.sleep(2)

    tables = pd.read_html(facts_url)
    mars_table = tables[0]

    mars_table.columns = ["Description", "Mars"]
    mars_table = mars_table.set_index("Description")

    html_table = mars_table.to_html()
    html_table = html_table.replace('\n', '')

    #Set up new scrape
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    time.sleep(2)

    news_html = browser.html
    news_soup = bs(news_html, "html.parser")

    all_news_title = news_soup.find_all("div", class_="content_title")
    latest_title = all_news_title[1].find("a").get_text()

    all_news_para = news_soup.find_all("div", class_="article_teaser_body")
    latest_para = all_news_para[0].get_text()

    browser.quit()

    # Mars Feature
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    time.sleep(2)

    browser.find_by_id('full_image').click()

    browser.find_by_text("more info     ").click()

    image_html = browser.html
    image_soup = bs(image_html, "html.parser")

    url = image_soup.find("img", class_="main_image")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + url

    browser.quit()

    #Hemishper Images
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)

    hemi_scrape = []

    for i in range(4):
        hemi_html = browser.html
        hemi_soup = bs(hemi_html, "html.parser")
    
        title = hemi_soup.find_all("h3")[i].get_text()
        browser.find_by_tag('h3')[i].click()
    
        hemi_html = browser.html
        hemi_soup = bs(hemi_html, "html.parser")
    
        hemi_url = hemi_soup.find("a", text="Sample")["href"]
    
        hemi_scrape.append({
            "title": title,
            "image_url": image_url
        })
        browser.back()

    browser.quit()

    ##### FINAL DICTIONARY ######

    mars_scrape_data = {
    "latest_title": latest_title,
    "latest_para" : latest_para,
    "html_table": html_table,
    "featured_image": featured_image_url,
    "hemi_scrape": hemi_scrape
    }


    return mars_scrape_data