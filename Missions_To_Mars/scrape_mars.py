# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from selenium import webdriver


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# create scrape function
def scrape():
    browser = init_browser()

    # use browser to open the url 
    url = "https://mars.nasa.gov/news/"

    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # get the latest news
    data = soup.find("li", class_="slide")
    news_title = data.find("div", class_="content_title").a.text
    paragraph = data.find("div", class_="article_teaser_body").text
    

    # for Mars latest image visit the url and get the full image url
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # use browser to open the url for image
    browser.visit(img_url) 

    # create html to parse
    html = browser.html

    # create soup object to parse html
    soup = bs(html, "html.parser")

    # use beautifulsoup to navigate to the image
    image = soup.find("li", class_="slide").a["data-fancybox-href"]

    # create the url for the image
    featured_image_url = "https://www.jpl.nasa.gov" + image
    
    # get the Mars tweet info
    # get the url and perform get requests
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(tweet_url)

    # create beautifulsoup object 
    soup = bs(response.text, "html.parser")

    # get the weather tweet with beautiful soup
    mars_weather = soup.find("div", class_="js-tweet-text-container").p.get_text(strip=True)

    # strip unnecessary strings
    mars_weather = mars_weather.strip("InSight")
    mars_weather = mars_weather.split("pic",1)[0]

    # replace newline characters with ",", and manipulate the string 
    mars_weather = mars_weather.replace("\n", ", ")
    mars_weather = mars_weather.capitalize()
    mars_weather = mars_weather.strip()
    mars_weather = mars_weather.capitalize()
   
    # Mars facts
    # get the url for Mars's facts 
    facts_url = "https://space-facts.com/mars/"

    # Use panda's `read_html` to parse the url
    table = pd.read_html(facts_url)

    # convert table to pandas dataframe
    facts_df = table[0]

    #rename the columns
    facts_df.columns=["description", "value"]

    # reset the index for the df
    facts_df.set_index("description", inplace=True)
    # convert dataframe to an html table string
    facts_html = facts_df.to_html()

    # Mars hemisphere
    # get the url and open it with browser
    h_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(h_url)
    # cerate html 
    html = browser.html

    # use beautiful soup to create soup object
    soup = bs(html, "html.parser")

    data = soup.find_all("div", class_="item")
    
    # cretae a list to hold data for hemispheres
    hemisphere_img_urls = []

    # loop the data list to find titles and img urls for hemispheres
    for d in data:
    
        title = d.find("h3").text

        img_url = d.a["href"]
    
        url = "https://astrogeology.usgs.gov" + img_url
    
        # use requests to get full images url 
        response = requests.get(url)
    
        # create soup object
        soup = bs(response.text,"html.parser")
    
        # find full image url
        new_url = soup.find("img", class_="wide-image")["src"]
    
        # create full image url
        full_url = "https://astrogeology.usgs.gov" + new_url
        
        #make a dict and append to the list
        hemisphere_img_urls.append({"title": title, "img_url": full_url})
        
    # create mars data dictionary to hold data
    mars_data = {
        "news_title": news_title,
        "paragraph" : paragraph,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "html_table": facts_html,
        "hemisphere_img_urls": hemisphere_img_urls
    }

    # close the browser after scraping
    browser.quit()

    # return results
    return mars_data