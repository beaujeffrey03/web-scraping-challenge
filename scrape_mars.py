from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():

    scrape_dict = {}

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of Red Planet Science
    url_news = 'https://redplanetscience.com/'
    browser.visit(url_news)

    # Set up BS to find first (most recent) news title and paragraph
    html = browser.html
    soup = bs(html, 'html.parser')
    result_news = soup.find('div', class_='list_text')

    scrape_dict['News Title'] = result_news.find('div', class_='content_title').text
    scrape_dict['News Paragraph'] = result_news.find('div', class_='article_teaser_body').text

    # URL of Space Images - Mars
    url_images = 'https://spaceimages-mars.com/'
    browser.visit(url_images)

    # Set up BS to find featured image
    html = browser.html
    soup = bs(html, 'html.parser')
    result_images = soup.find('div', class_='header')

    featured_image_url = result_images.find('img', class_='headerimage fade-in')
    scrape_dict['Featured Image'] = url_images + featured_image_url['src']

    # URL for Mars Facts table
    url_marsfacts = 'https://galaxyfacts-mars.com/'

    # Read table
    table_marsfacts = pd.read_html(url_marsfacts)

    # Convert table to DF
    marsfacts_df = table_marsfacts[0]

    # Transform table to promote first row as header and set new index.
    new_headers = marsfacts_df.iloc[0]
    marsfacts_df = marsfacts_df[1:]
    marsfacts_df.columns = new_headers
    marsfacts_df = marsfacts_df.set_index('Mars - Earth Comparison')

    # Convert back to html
    html_table = marsfacts_df.to_html()
    html_table
    html_table.replace('\n', '')
    marsfacts_df.to_html('table.html')

    # URL for Hemispheres
    url_hemispheres = 'https://marshemispheres.com/'
    browser.visit(url_hemispheres)

    # Set up BS to find routes
    html = browser.html
    soup = bs(html, 'html.parser')
    result_hemispheres = soup.find_all('div', class_='item')

    # create empty lists for gathering hemisphere names and routes to larger images
    route_list = []
    hemisphere_list = []

    # loop through results to make lists of routes and hemisphere names
    for result in result_hemispheres:
        
        route = result.find('a', class_='itemLink product-item')['href']
        route_list.append(route)
        hemisphere = result.find('h3').text
        hemisphere_list.append(hemisphere)

    # create empty list to for gathering image urls
    image_url_list = []

    # loop through route list to make new list of image urls
    for route in route_list:
        
        # attach route to end of base url
        route_url = url_hemispheres + route
        browser.visit(route_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        
        # get route string for image
        big_image = soup.find('img', class_='wide-image')['src']
        
        # attach image route to end of base url
        image_url_list.append(url_hemispheres + str(big_image))

    # make list of dictionaries from lists
    scrape_dict['Hemisphere Images'] = [{ 'title': hemisphere_list[i], 'img_url': image_url_list[i] } for i in range( len(image_url_list) )]

    return scrape_dict