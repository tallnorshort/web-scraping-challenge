# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time
import requests
import re
import pymongo
from selenium import webdriver
import io
   
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    #init browser
    browser = init_browser()
    
# Visit Nasa news url.
    url = "https://mars.nasa.gov/news/?page=0\&per_page=40&order=publish_date+desc%2Ccreated_at+desc\&search=\&category=19%2C165%2C184%2C204\&blank_scope=Latest"

    browser.visit(url)
    
# HTML Object.
    html = browser.html
# Parse HTML with Beautiful Soup
    news_soup = BeautifulSoup(html, "html.parser")

    news_title = news_soup.find("div",class_="content_title").text
    news_paragraph = news_soup.find("div", class_="article_teaser_body").text
    browser.quit()
    print(f"Title: {news_title}")
    print(f"Para: {news_paragraph}")
    
    # JPL Mars Space Images - Featured Image
    #init browser
    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=\&category=Mars"
    browser.visit(url)

    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

# Find "More Info" Button and Click It
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    img_url = image_soup.select_one("figure.lede a img").get("src")
    featured_image_url = f"https://www.jpl.nasa.gov{img_url}"
    browser.quit()
    print(featured_image_url)
    # Mars Weather
    browser = init_browser()
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    response = requests.get(url)
    browser.visit(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find('div', class_="js-tweet-text-container")
    tweet = results.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    tweet_split = tweet.rsplit("pic")
    mars_weather = tweet_split[0]
    browser.quit()
    print(mars_weather)
    #Mars Table
    browser = init_browser()
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    facts_table = pd.read_html(url)
    facts_df = facts_table[0]
    facts_df.columns = ["Category", "Measurement"]
    facts_df = facts_df.set_index("Category")
    str_io = io.StringIO()

    facts_df.to_html(buf=str_io, classes='table table-striped')

    html_str = str_io.getvalue()
    mars_table_facts = html_str
    browser.quit()
    ##Hemispheres
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    titles = soup.find_all("h3")
    for title in titles:
        browser.click_link_by_partial_text("Hemisphere")
        
    print(titles)

    results = soup.find_all("div", class_="description")
    mars_dict={}
    hemisphere_image_urls=[]
    for result in results:
        link = result.find('a')
        href = link['href']
        title = link.find('h3').text
        url2 = "https://astrogeology.usgs.gov" + href
        browser.visit(url2)
        html = browser.html
        soup = bs(html, 'html.parser')
        pic = soup.find("a", target="_blank")
        pic_href = pic['href']
        hemisphere_image_urls.append({"title":title,"img_url":pic_href})
        print(hemisphere_image_urls)
    browser.quit()
#######MONGODB
    
    mars_data = {'News_title': news_title, 'News_paragraph': news_paragraph,
                  'Featured_Img': featured_image_url,'Mars_Weather': mars_weather,   
                  'Mars_facts_table': mars_table_facts, 'hemisphere_image_urls': hemisphere_image_urls}
    print("Scrape Complete!!!")
    
    return mars_data

   
   

