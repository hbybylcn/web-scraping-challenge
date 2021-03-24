from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

import requests
from splinter import Browser

from selenium import webdriver












def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    

def scrape_info():
    browser = init_browser()

    all_data={}

    #for new in news:
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'lxml')

    news = soup.find('div', class_="list_text")
 
    #for new in news:
    
    news_title=news.find('div', class_="content_title").text
    
    news_teaser=news.find('div', class_="article_teaser_body").text

    all_data['News Title']=news_title

    all_data['News Summary']=news_teaser




    # featured images
    url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)

    browser.links.find_by_partial_text('FULL IMAGE').click()


    html = browser.html
    soup = bs(html, 'lxml')
    
    link=soup.find('img',class_='fancybox-image')['src']
    
    featured_image_url=f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{link}'


    all_data['Featured Image']=featured_image_url


    #mars fact table


    url='https://space-facts.com/mars/'

    tables=pd.read_html(url)


    mars_table=tables[0]

    html_mars=mars_table.to_html()

    all_data['Mars Facts']=html_mars

    #hemisphere
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_image_urls={'title':[],'img_url':[] }
    for i in range(4):    
        browser.links.find_by_partial_text('Hemisphere Enhanced')[i].click()
        html = browser.html
        soup = bs(html, 'lxml')
    
        link=soup.find_all('div',class_='downloads')
    
        img = link[0].find_all('a')
        img_url = img[0]['href']
        title=soup.find_all('div', class_='content')

        title=title[0].find('h2').text
        
    
        hemisphere_image_urls['title'].append(title)
        hemisphere_image_urls['img_url'].append(img_url)
    
    
    
        browser.back()



        all_data['Hemisphere Images']=hemisphere_image_urls 


    

    # Quite the browser after scraping
    browser.quit()



    # Return results
    return all_data
