[![Build Status](https://travis-ci.org/vlall/darksearch.svg?branch=master)](https://travis-ci.org/vlall/darksearch)

## About Darksearch
[Darksearch](http://darksearch.io) allows you to query cached onion sites, irc chatrooms, various pdfs, game chats, blackhat forums etc...
<img src="https://raw.githubusercontent.com/vlall/darksearch/master/darksearch/docs/darksearch.png" width="700">
## API
Darksearch also has an API in the works. Currently you can't scrape specific data for your queries, but you can retrieve metadata on your searches by using a GET request on darksearch.io/api/YOUR_QUERY/PAGE_NUMBER
```
$ curl -XGET darksearch.io/api/spies/1

{
  "duration": "0.038", 
  "query": "spies", 
  "size": "36", 
  "total_pages": "4"
}
```

The Darksearch index is growing as more scrapers get built...
