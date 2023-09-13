WORKDIR=/app

all: install
	cd $(WORKDIR)
	python3 $(WORKDIR)/zadarma.py

install:
	pip3 install -r $(WORKDIR)/requirements.txt
