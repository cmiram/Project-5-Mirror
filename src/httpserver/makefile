origin="ec2-54-166-234-74.compute-1.amazonaws.com"
port=8080
build:
	ln -fs main.py httpserver
	chmod a+x httpserver
run: build
	./httpserver -p ${port} -o ${origin}
