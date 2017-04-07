# project-5
Networks Grad project 5

Our code is split into two python projects. One for the DNS server and another for the http server.
The http server runs a socket on the specified port to listen for clients requesting data. When 
it receives a request it checks the cache for a matching path and if it finds one it returns that data.
If not it requests it from the server and adds it to the cache before returning it to the client. If 
the cache is full it deletes the least recently used.

The DNS server also opens a socket and listens in an infinite loop for a client query. When it gets a 
request it encodes the http header info and returns the requested information to the client. The logic 
for picking a server is still pretty basic, we just focused on getting it up and running for the milestone.

Preson: Http server, dns server, caching
Chris: Http server, caching logic
