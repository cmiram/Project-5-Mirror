# To build and run
First, run "make build" in the project root. This will set all the necessary scripts to be executable.
To deploy to the servers with pre-configured defaults, change the current directory to `./scripts/` using `cd scripts`, and then run the `./startCDN` script.
ALL of the scripts should be ran in the `scripts/` directory
`deployCDN` will deploy with the given arguments to all the replica servers and the DNS server.
`runCDN` will run with the given arguments on all the replica servers and the dns server
`stopCDN` will stop them all (including the DNS server)

# Technical Details
## Overview
Our code is split into two python projects. One for the DNS server and another for the http server.
The http server runs a socket on the specified port to listen for clients requesting data. When 
it receives a request it checks the cache for a matching path and if it finds one it returns that data.
The server keeps track of two caches, one static containing the most popular zipf pages and a second 
runtime cache that adds items as they're requested, but all this data is lost on a server restart.
If not it requests it from the server and adds it to the runtime cache before returning it to the client. 
If the cache is full it deletes items in the cache until it stays within the memory limits.

The DNS server also opens a socket and listens in an infinite loop for a client query. When it gets a 
request it encodes the http header info and returns the requested information to the client. If the 
client is new the DNS server picks a replica that is the closest geographically to the client.


## DNS Server
The DNS server pre-computes the coordinates of the replica servers. Using that information, it intelligently chooses the closest server when a new client is connected to the DNS server. Because we know nothing about the new client, except their IP address, the only information we can use to find them the best server is to get their rough GPS coordinates and locate the closest one using a fast distance function.

We set the TTL to be low, so that we can easily do measurements to determine the best server to choose from. We have a list of latencies per client, so that other active measurements can be taken to determine if there is a better server to send to them. If we find a lower latency, we send them to that server. Choosing based only on GPS coordinates is not sufficient, because though they might be geographically close the connection may not be the best topographically.

### Possible Improvements
Compared to the HTTP server, the code is much messier in the DNS server than we would have liked. Given more time, it would have been nice to clean it up, and perhaps provide cleverer checks.

## HTTP Server
### Static Cache
The HTTP server employs two kinds of caches: one static, the other dynamic. The static is based on a pre-selected list of high ranking pages that are commonly hit. Once the server starts, a thread is spawned that will go through the list and fetch the content to be cached at the replica. Since this can easily lock up the server with multiple requests, a lock is employed that will stop all cache building the moment any uncached content is requested. In general, this shouldn't have too much effect since most requests are fast, but it is done so that the cache doesn't burden any early users in any way.

### Dynamic Cache
The second cache we have is a dynamic, in-memory cache. Unlike the first cache, this cache is not fixed and will change as more requests are made. Though over time the zipf distribution should give a nice user experience, the dynamic cache will smooth out the rougher edges when multiple users are hitting a page that we may not have cached. The cache is set so that if it was to ever go above the 10MB limit, old pages ares removed until the cache is small enough to fit within the 10MB limit. The most gains we have seen from this are for the small elements that are present in each page, and usually require lots of small, latency filled trips to the origin server.

In order to optimize the amount of space used in the dynamic cache, we employed the `pickle` python library to compress the data. The amount of CPU cycles spent uncompressing the data is trivial compared to the gains we get in memory storage.

The dynamic cache also helps the static cache: we only statically cache the pages of the popular content, but popular content often has other resources that need to be fetched from the server. By having them cached in the dynamic cache, it allows them to not take up our very important hard-disk storage cache, but also removes the usual penalty that we had to endure even when using a static cache.

### Possible Improvements
One thing that would have been nice to fix is the lock. Since it is an atomic lock, there is a performance penalty to setting and clearing it even after the cache building is complete. If given more time, i would have added checks to not do this expensive operation once the child thread had completed. Since the network latency is so much higher than anything else however, I thought it best not to complicate the code since it doesn't seem to have that large of an effect.


# Authors
Preston: 
* Most of HTTP server, including the static cache.
* DNS server
* README

Chris: 
* HTTP server dynamic caching logic
* README
