#  Data Pipeline
- Torfka checks seedlist for 200 Response, scrapes page, logs date, size, name, link.
- Take log, read it, pipe through Apache Tika, gather Tika metadata and generate 200 word description to Dataframe.
- Ingest DataFrame into Elasticsearch index.
- Use Flask to serve content and elas.py to read index

# Technologies
- Tor and Scrapy for web scraping
- Apache Kafka for streaming messages
- Apache Tika for text translation
- Postgres for the database
- Elasticsearch as an index
- Flask/flask-api/Gunicorn for the server
- Nginx for reverse proxy
