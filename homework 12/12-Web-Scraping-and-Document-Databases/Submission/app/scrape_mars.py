from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime

class ScrapingHelper():
    def __init__(self):
        #using place holder due to no base url. We are visiting multiple sites
        pass

    def getData(self):
        # Setup splinter
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)

        #Scrape the Mars News Site and collect the latest News Title and Paragraph Text.
        url = "https://redplanetscience.com/"
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html)

        #news title
        news_title = soup.find("div", {"class":"content_title"}).text
        #paragraph text
        news_p = soup.find("div", {"class":"article_teaser_body"}).text

        #Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
        url = "https://spaceimages-mars.com/"
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html)

        jpls = soup.find("img", {"class":"headerimage"})["src"]
        featured_image_url = url + jpls

        # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
        url = "https://galaxyfacts-mars.com/"
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html)

        # Visit the Mars Facts Site Using Pandas to Read
        mars_facts = pd.read_html("https://galaxyfacts-mars.com/")[1]
        mars_facts.columns=["Planet Profile", "Mars"]

        # Visit the astrogeology site here to obtain high resolution images for each of Mar's hemispheres
        # Mars Hemispheres
        url = 'https://marshemispheres.com/'
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html)

        infos = soup.find_all("div", {"class": "item"})

        hemisphere_image_urls = []


        for info in infos:
                
                hemisphere = {}
                
                #get my titles
                titles = info.find("h3").text.strip("Enhanced")
                #print(titles)
                
                #have to click into each one to get the high res
                item_link = info.find("div", {"class", "description"}).find("a")
                item_url = url + item_link["href"]
                browser.visit(item_url)
                html2 = browser.html
                soup2 = BeautifulSoup(html2)
                
                image_end_url = soup2.find("img", {"class": "wide-image"})["src"]
                image_url = url + image_end_url
                #print(image_link)
                
                hemisphere['title']= titles
                hemisphere['img_url']= image_url
                
                hemisphere_image_urls.append(hemisphere)

        alldata_scraped = {}
        # alldata_scraped["news_p"] = news_p
        # alldata_scraped["news_title"] = news_title
        alldata_scraped["featured_image_url"] = featured_image_url
        alldata_scraped["mars_facts"] = mars_facts.to_html(header=False)
        alldata_scraped["hemispheres"] = hemisphere_image_urls
        alldata_scraped["last_update"] = datetime.now()

        #closebrowser
        browser.quit()

        return(alldata_scraped)


