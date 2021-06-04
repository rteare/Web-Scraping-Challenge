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

    # set up url for Mars News
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(2)
    news_html = browser.html

    # parse with BeautifulSoup
    news_soup = bs(news_html, 'html.parser')

    # find the latest news article
    all_news_title = news_soup.find_all("div", class_="content_title")
    latest_title = all_news_title[1].find("a").get_text()

    # latest article paragraph text
    all_news_para = news_soup.find_all("div", class_="article_teaser_body")
    latest_para = all_news_para[0].get_text()

    # print article title and  paragraph text
    pprint(latest_title)
    pprint(latest_para)

    # set up url for Mars Facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    time.sleep(2)

    # Parse facts url to find tables
    facts_tables = pd.read_html(facts_url)
    mars_table = facts_tables[0]    

    # rename columns
    mars_table.columns = ["Description", "Mars"]
    mars_table = mars_table.set_index("Description")

    # convert data to html
    html_table = mars_table.to_html()
    html_table = html_table.replace('\n', '')
    
    # print table
    pprint(html_table)

    # Set up url for Mars Image
    image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(image_url)
    time.sleep(2)

    # Set new browser link
    browser.links.find_by_partial_text('FULL IMAGE').first.click()
    time.sleep(2) 
    full_image_html = browser.html

    # parse with BeautifulSoup
    image_soup = bs(full_image_html, "html.parser")

    # scrape the URL
    feature_url = image_soup.find('img')['src']

    # print the url for the full image version of the Featured Mars Image
    base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    featured_image_url = f'{base_url}{feature_url}'

    # print url
    pprint(featured_image_url)

    # Set up url for Mars Hemisphere
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    time.sleep(2)
    hemi_html = browser.html

    # list for titles and image urls
    hemi_scrape = []

    # Loop for hemisphere info
    for i in range(4):
        hemi_html = browser.html
        hemi_soup = bs(hemi_html, "html.parser")

        title = hemi_soup.find_all("h3")[i].get_text()
        browser.find_by_tag('h3')[i].click()

        hemi_html = browser.html
        hemi_soup = bs(hemi_html, "html.parser")

        hemi_url = hemi_soup.find("a", text="Sample")["href"]

        # append title and image url to dictionary
        hemi_scrape.append({
            "Title": title,
            "Link to image": hemi_url
        })
    
    # print the hemispheres images
    pprint(hemi_scrape)

    # close the browser
    browser.quit()

    # Scraped Dictionary

    mars_scrape_data = {
        'latest_title': latest_title,
        'latest_para' : latest_para,
        'html_table': html_table,
        'featured_image': featured_image_url,
        'hemi_scrape': hemi_scrape
    }

    return mars_scrape_data