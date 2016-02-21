#!/usr/bin/python

from darksearch.darkmain import app

if __name__ == "__main__":
    app.run(
            host='0.0.0.0',
            port=80,
            debug=True,
            threaded=True
    )
    print "Test Success..."
