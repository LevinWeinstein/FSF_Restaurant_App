# Basics of Client-Server communications Across the Internet
1. Clients and Servers
    1. Computers communicating across the internet
        1. Client: The computer that wants information
        2. Server: The computer that has information that it shares with clients.
        3. Client has to initiate communication to request information
        4. Server constantly stays listening for requests from Clients
        5. More Specifically: All clients can send messages and receive messages to and from the server, but the aren't listening all the time so they aren't capable of reaching each other when one of them wants because the other isn't listening. To connect to each other they could go through a server, since the server is always listening. That way, they could both connect to the server and see that each other are online.
2. Protocols
    1. __TCP__ _Transmission Control Protocol_
        1. Enables information to be broken into small packets, and sent between clients and servers
        2. If a packet is lost along the way, the sender and receiver have a way of figuring out which packet is missing, and request that they be resent
    2. __UDP__ _User Datagram Protocol_
        1. The counterpart to TCP is UDP.
        2. Good for streaming content like music or video.
    2. __IP__ _Internet Protocol_
        1. IP addresses allow messages to be properly router to all participants on the internet.
        2. When you type a domain name into your browser, your browser finds it's corresponding IP in a DNS: a Domain Name Server
        3. Ports:
            1. since multiple applications using the internet can run on one machine, operating systems use ports to designate channels of communication on the same ip address.
            2. Placing a colon after an IP address, followed by another number, indicates that we want to communicate on a specific port on the device using that IP Address.
            3. On most machines, ports range from `0-65,536`
            4. Ports `0-10,000` are reserved by the operation system for specific use.
            5. `Port 80: Http`
            6. `Port 8080: Https`
            7. Client and server on the same machine: IP "localhost", accessed by typing `localhost` or `127.0.0.1`
    3. __HTTP__ _Hypertext Transfer Protocol_
