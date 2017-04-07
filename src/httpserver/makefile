origin="ec2-54-166-234-74.compute-1.amazonaws.com"
port=40000
build:
	ln -fs main.py httpserver
	chmod a+x httpserver
run: build
	./httpserver -p ${port} -o ${origin}
