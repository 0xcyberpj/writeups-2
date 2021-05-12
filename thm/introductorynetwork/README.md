# Introductory Network


### Ping

- What command would you use to ping the bbc.co.uk website?

`ping bbc.co.uk`

- ping muirlandoracle.co.uk
- What is the IPv4 address?

```bash
# soln 1
ping -4 muirlandoracle.co.uk
# output
#PING  (217.160.0.152) 56(84) bytes of data.
#64 bytes from 217-160-0-152.elastic-ssl.ui-r.com (217.160.0.152): icmp_seq=1 ttl=47 time=307 ms
#64 bytes from 217-160-0-152.elastic-ssl.ui-r.com (217.160.0.152): icmp_seq=2 ttl=47 time=267 ms

# soln 2
dig muirlandoracle.co.uk a
[..snip..]
;; ANSWER SECTION:
muirlandoracle.co.uk.	3599	IN	A	217.160.0.152
[..snip..]
```

`217.160.0.152`

- What switch lets you change the interval of sent ping requests?

`-i`

- What switch would allow you to restrict requests to IPv4?

`-4`

- What switch would give you a more verbose output?

`-v`


### Traceroute

- What switch would you use to specify an interface when using Traceroute?

`-i`

- What switch would you use if you wanted to use TCP SYN requests when tracing the route?

`-T`

- [Lateral Thinking] Which layer of the TCP/IP model will traceroute run on by default (Windows)?

`Intrenet`


### WhoIs

- What is the registrant postal code for facebook.com?

```bash
#soln
whois facebook.com
[..snip..]
Admin Postal Code: 94025
[..snip..]
```


- When was the facebook.com domain first registered?
```bash
# Creation Date: 1997-03-29T05:00:00Z
29/03/1997
```

- Which city is the registrant based in?

```bash
# soln
whois microsoft.com
[..snip]
Registrant City: Redmond
[..snip..]
```

- [OSINT] What is the name of the golf course that is near the registrant address for microsoft.com?

```bash
# https://www.yelp.com/search?cflt=golf&find_loc=One+Microsoft+Way%2C+Redmond%2C+WA+98052
Bellevue Golf Course
```

- What is the registered Tech Email for microsoft.com?

```bash
Tech Email: msnhst@microsoft.com
```

### Dig

- What is DNS short for?
`Domain Name System`

- What is the first type of DNS server your computer would query when you search for a domain?
`Recursive`

- What type of DNS server contains records specific to domain extensions (i.e. .com, .co.uk*, etc)*? Use the long version of the name.
`Top-Level Domain`

- Where is the very first place your computer would look to find the IP address of a domain?
`Local Cache`


- [Research] Google runs two public DNS servers. One of them can be queried with the IP 8.8.8.8, what is the IP address of the other one?
`8.8.4.4` (google search)

- If a DNS query has a TTL of 24 hours, what number would the dig query show?
`86400`