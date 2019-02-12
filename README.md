# Scrapy---Python
Use Scrapy to scrape restaurant information from www.dianping.com. This program fully utilizes the Scrapy library functionality, mainly the following 7 files:

1. Scrapy.py: performs all scraping actions

2. helper.py: utilizes dynamic IP address to avoid crawler from being blocked

3. items.py: defines the format of data being stored into the database

4. main.py: run this program in any IDE (such as Pycharm)

5. middlewares.py: perform sanity checks immediately before scraping (such as crawler headers and IP address)

6. pipelines.py: perform sanity checks immediately before storing the data into the database (such as duplicate filters)

7. settings.py: sets configurations, such as database address
