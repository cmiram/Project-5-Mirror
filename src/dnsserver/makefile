server_name="cs5700cdnproject.ccs.neu.edu"
# This should be the SAME port as the HTTP server!
port=40000
bin_name=dnsserver
build:
	ln -fs main.py ${bin_name}
	chmod a+x ${bin_name}
run: build
	./${bin_name} -p ${port} -n ${server_name}
