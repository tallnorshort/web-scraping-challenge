# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time
import requests
import re
from selenium import webdriver
import io

def init_browser():

    executable_path = {"executable_path": "/Users/talln/Desktop/chromedriver"}

    return Browser("chrome", **executable_path, headless=True)



def scrape():

    browser = init_browser()

    mars_data_scrape = {}

    mars_news = 'https://mars.nasa.gov/news/'

    browser.visit(mars_news)

    time.sleep(2)

    html = browser.html

    news_soup = bs(html, 'html.parser')


################################################
                    #Mars News#
################################################
    url = "https://mars.nasa.gov/news/?page=0\&per_page=40\&order=publish_date+desc%2Ccreated_at+desc\&search=\&category=19%2C165%2C184%2C204\&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    
    news_soup = BeautifulSoup(html, "html.parser")
    slide_element = news_soup.select_one("ul.item_list li.slide")
    slide_element
    slide_element.find("div", class_="content_title")

    news_title = slide_element.find("div", class_="content_title").get_text()
    # Scrape the Latest Paragraph Text
    news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    time.sleep(2)

    mars_data_scrape["data1"] = news_title
    mars_data_scrape["data2"] = news_p




#################################################################
                       #JPL Mars Space Images - Featured Image
#################################################################
# Visit the NASA JPL (Jet Propulsion Laboratory) Site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=\&category=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
# Find "More Info" Button and Click It
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    browser.click_link_by_partial_text('.jpg')

    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
    img_url = image_soup.select_one("img").get("src")
    mars_data_scrape["image"]= img_url

# Use Base URL to Create Absolute URL

######################################################################
                     #Mar's Weather
######################################################################
    twitter_response = requests.get("https://twitter.com/marswxreport?lang=en")
    twitter_soup = BeautifulSoup(twitter_response.text, 'html.parser')
    tweet_containers = twitter_soup.find_all('div', class_="js-tweet-text-container")
    for tweets in tweet_containers:
        if tweets.text:
            print(tweets.text)
            break
        
    for i in range(10):
        tweets = tweet_containers[i].text
        if "Sol " in tweets:
            print(tweets)
            break

    mars_weather = 'InSight sol 503 (2020-04-26) low -93.8ºC (-136.8ºF) high -4.9ºC (23.2ºF) winds from the WNW at 4.6 m/s (10.2 mph) gusting to 17.5 m/s (39.1 mph)'
    mars_data_scrape["weather"] = mars_weather
################################################################
                    #Mars Facts
################################################################

    url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(url)
    facts_df = facts_table[0]
    facts_df.columns = ["Category", "Measurement"]
    facts_df = facts_df.set_index("Category")
    facts_df

    str_io = io.StringIO()

    facts_df.to_html(buf=str_io, classes='table table-striped')

    mars_facts = str_io.getvalue()

    mars_data_scrape["table"] = mars_facts
################################################################
                    #Mars HemiSpheres
################################################################

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced\&k1=target\&v1=Mars"

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
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
        soup = BeautifulSoup(html, 'html.parser')
        pic = soup.find("a", target="_blank")
        pic_href = pic['href']
        hemisphere_image_urls.append({"title":title,"img_url":pic_href})
        print(hemisphere_image_urls)

        hemisphere_image_urls
        mars_data_scrape["hemisheres"] = hemisphere_image_urls

        return mars_data_scrape