#!/usr/bin/python

from darksearch.darkmain import app


def main():
    app.run(
            host='0.0.0.0',
            port=80,
            threaded=True
    )


if __name__ == '__main__':
    main()
