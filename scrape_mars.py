from splinter import Browser
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import time


def scrape():
    mars_dictionary={}

    #get_ipython().system('which chromedriver')
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Find latest mars headline and paragraph
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    mars_dictionary['news_title']=news_title
    mars_dictionary['news_p']=news_p

    # Scrape image url for featured image
    url_nasa_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_nasa_image)
    nasa_image_html = browser.html
    nasa_image_soup = BeautifulSoup(nasa_image_html, "lxml")
    featured_image = nasa_image_soup.find('div', class_='default floating_text_area ms-layer').footer
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image.find('a')['data-fancybox-href']
    mars_dictionary['featured_image_url']= featured_image_url

    # Scrape latest mars weather tweet
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    mars_twitter_html = browser.html
    mars_twitter_soup = BeautifulSoup(mars_twitter_html, 'lxml')
    mars_weather_div = mars_twitter_soup.find('div', class_='js-tweet-text-container')
    mars_weather = mars_weather_div.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    mars_dictionary['mars_weather']= mars_weather

    # Scrape data about mars
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    mars_data  = pd.read_html(mars_facts_url)
    mars_data_df=mars_data[0]
    mars_data_df.columns = ['Description', 'Value']
    mars_data_html=mars_data_df.to_html(escape=True,index=False,header=False)
    mars_dictionary['mars_facts']= mars_data_html

    # Scrape high resolution mars images and titles
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = BeautifulSoup(hemispheres_html, 'lxml')
    image_list_of_dicts = []
    base_url = "https://astrogeology.usgs.gov"
    images = hemispheres_soup.find_all('div', class_='item')
    for image in images:
        href = image.find('a', class_='itemLink product-item')['href']
        link = base_url + href
        browser.visit(link)
        high_res_html = browser.html
        high_res_soup = BeautifulSoup(high_res_html, 'lxml')
        img_url = high_res_soup.find('div', class_='downloads').find('a')['href']
        title = high_res_soup.find('div', class_='content').find('h2', class_='title').text
        image_list_of_dicts.append({'img_url': img_url, 'title': title})
    mars_dictionary['image_list_of_dicts']= image_list_of_dicts

    return mars_dictionary


    
