.phony: all install test

install:
	@ python setup.py install

all: install

test:
	@ python -m unittest discover -s tests/ -v
