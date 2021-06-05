# Set up dependencies
import pandas as pd
from pprint import pprint 
import time
import requests as req
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

# Set browser
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

mars_info = {}

# Mars News
# ----------------------------------------
def scrape_mars_news():

    # initiaslize browser
    browser = init_browser()

    # set up url for Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)
    html = browser.html

    # BeautifulSoup
    soup = bs(html, 'html.parser')

    # find the latest news article
    slides = soup.find_all('li', class_='slide')
    content_title = slides[0].find('div', class_ = 'content_title')
    news_title = content_title.text.strip()
    article_teaser_body = slides[0].find('div', class_ = 'article_teaser_body')
    news_article = article_teaser_body.text.strip()
    
    # print article title and paragraph text
    #pprint(news_title)
    #pprint(news_article)

    # Add to scrape dictionary
    mars_info['news_title'] = news_title
    mars_info['news_article'] = news_article

    return mars_info
    
    # close the browser
    browser.quit()


# Mars Facts
# ---------------------------------------
def scrape_mars_facts():

    # initiaslize browser
    browser = init_browser()

    # set up url for Mars Facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    
    # Parse facts url to find tables
    facts_table = pd.read_html(facts_url)
    mars_table = facts_table[0]    

    # rename columns
    mars_table = mars_table.rename(columns = {0:'Description', 1:'Mars'})
    mars_table = mars_table
    mars_table['Description'] = mars_table['Description'].str.replace(':','')
    mars_table
   
    # convert data to html
    html_table = mars_table.to_html(table_id="html_tbl_css",justify='left',index=False)
    
    # print table
    #pprint(html_table)
    
    # Add to dictionary
    mars_info['mars_tables'] = html_table

    return mars_info

    # close the browser
    browser.quit

# Mars Image
# ----------------------------------------

def scrape_mars_images():

    # Initialize browser
    browser = init_browser()

    # Set up url for Mars Image
    base_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    url = base_url + "index.html"
    browser.visit(url)
    time.sleep(3)
    html = browser.html

    # parse with BeautifulSoup
    soup = bs(html, "html.parser")

    # scrape for image URL
    image_url = soup.find('a', class_='showimg fancybox-thumbs')['href']
    featured_image_url = base_url + image_url

    # print url
    # pprint(feature_image_url)

    # Add to dictionary
    mars_info['image_url'] = featured_image_url

    return mars_info
    
    # close the browser
    browser.quit

# Mars Hemisphere
# ----------------------------------------
def scrape_mars_hemi():

    # Initialize browser
    browser = init_browser()

    # Set up url for Mars Hemisphere
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    html = browser.html
    
    # beautifulSoup
    soup = bs(html, "html.parser")

    # retrievethe hemi info
    hemi_items = soup.find_all('div', class_='item')
    
    # set base url
    hemi_base = 'https://astrogeology.usgs.gov'

    # List for hemi info storage
    hemi_image_urls = []

    # Loop for hemisphere info
    for item in hemi_items:
        
        # store items
        title = item.find('h3').text

        # link to hemi image
        hemi_full = item.find('a', class_='itemLink product-item')['href']

        # Set browser link
        browser.visit(hemi_base + hemi_full)
               
        # Set up url for Mars hemi image
        res_html = browser.html
        hemi_soup = bs(res_html, 'html.parser')

        # path to the hemi images
        image_path = hemi_soup.find('img', class_='wide-image')['src']

        # URL for hemi images
        res_hemi_url = f'{hemi_base}{image_path}'

        # append title and image url to dictionary
        hemi_image_urls.append({
            "title": title, 
            "img_url": res_hemi_url
            })

    # print the hemispheres images
    # pprint(hemi_image_urls)

    mars_info['hemi_image_urls'] = hemi_image_urls

    return mars_info
    
    # close the browser
    browser.quit()

print("Data Uploaded!")