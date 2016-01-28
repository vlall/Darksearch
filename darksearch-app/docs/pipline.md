#  Data Pipeline
- Torfka checks seedlist for 200 Response, scrapes page, logs date, size, name, link.
- Take log, read it, pipe through Apache Tika, gather Tika metadata and generate 200 word description to Dataframe.
- Turn DataFrame into Elastic Search index.
- Use flask to serve content and Engine.py to read index   