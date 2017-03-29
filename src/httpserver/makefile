origin="ec2-54-166-234-74.compute-1.amazonaws.com"
build:
	ln -fs main.py httpserver
	chmod a+x httpserver
run: build
	./httpserver -p 40000 -o ${origin}
