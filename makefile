build:
	chmod a+x ./scripts/*
	(cd src/httpserver; make build)
	(cd src/dnsserver; make build)
