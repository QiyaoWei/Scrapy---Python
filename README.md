# Scrapy---Python
Use Scrapy to scrape restaurant information from www.dianping.com

Scrapy.py: performs all scraping actions

settings.py: sets configurations, such as database address

middlewares.py: perform sanity checks immediately before scraping, and immediately before storing the data into the database (such as duplicate filters)

helper.py: utilizes dynamic IP address to avoid crawler from being blocked

main.py: run this program in any IDE (such as Pycharm)
