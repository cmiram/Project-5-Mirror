build:
	chmod a+x ./scripts/*
	(cd src/httpserver; rm -rf cache; make build)
	(cd src/dnsserver; make build)
