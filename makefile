build:
	chmod a+x ./scripts/*
	cp scripts/* .
	(cd src/httpserver; make build)
	(cd src/dnsserver; make build)
