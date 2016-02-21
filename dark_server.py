#!/usr/bin/python

from darksearch.darkmain import app
from logging.handlers import RotatingFileHandler
import os
import logging


def main():
    app.run(
            host='0.0.0.0',
            port=80,
            threaded=True,
	    debug=True
    )


if __name__ == '__main__':
    main()
