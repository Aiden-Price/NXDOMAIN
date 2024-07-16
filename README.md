# NXDOMAIN
Implement a simplified DNS infrastructure that contains a DNS recursor, some DNS servers, a launcher program that generates configurations for the DNS servers and a verifier
that validates the configurations of the DNS servers. When the DNS servers are running, any end user can ask the recursor to resolve a hostname.

Then, the recursor initiates a chain of DNS queries to the DNS servers via TCP connection. Eventually, the recursor shall collect responses from the DNS servers, and resolve the hostname to a valid identifier or NXDOMAIN to the end user.

## On the high level, the DNS server is capable of the following:
1. Start up according to the given command-line arguments.
2. Accept DNS queries from the recursor via TCP.
3. Process the queries and reply to the recursor via TCP.
4. Log the server activities on the standard output.
5. Parse commands sent from the user via TCP and update the server.


## The recursor can:
1. Start up if the root DNS server is specified in command-line argument.
2. Read and validate a domain in the standard input.
3. Query a chain of DNS servers, and receive responses.
4. Resolve the domain and output the response in the standard output.


Note that the DNS infrastructure in this context will be running on the same device and is incapable of running on different physical devices. This is an intentional design and therefore the complexity of communication over the Internet is omitted in the system.


## The five tasks, namely:
1. Implement the simplified DNS recursor program.
2. Implement the simplified DNS server program.
3. Implement the launcher program that generates DNS server configurations.
4. Implement the verifier program that validates the equivalency of configurations.
5. Test whether the DNS server fulfils the implementation requirements and achieve a high coverage.
