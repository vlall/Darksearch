[![Build Status](https://travis-ci.org/vlall/darksearch.svg?branch=master)](https://travis-ci.org/vlall/darksearch)

## About Darksearch
Darksearch is a search engine that allows you to query cached onion sites, irc chatrooms, various pdfs, game chats, blackhat forums etc...  
<img src="https://raw.githubusercontent.com/vlall/darksearch/master/darksearch/docs/darksearch.png" width="700">


## Technologies
- Tor and Scrapy for web scraping
- Apache Kafka for streaming messages
- Apache Tika for text translation
- Postgres for the database
- Elasticsearch as an index
- Flask/flask-api/Gunicorn for the server
- Nginx for reverse proxy

The Darksearch index is growing as more scrapers get built...
