# Basics of Client-Server communications Across the Internet
1. Clients and Servers
    1. Computers communicating across the internet
        1. Client: The computer that wants information
        2. Server: The computer that has information that it shares with clients.
        3. Client has to initiate communication to request information
        4. Server constantly stays listening for requests from Clients
        4. More Specifically: All clients can send messages and receive messages to and from the server, but the aren't listening all the time so they aren't capable of reaching each other when one of them wants because the other isn't listening. To connect to each other they could go through a server, since the server is always listening. That way, they could both connect to the server and see that each other are online.
2. Protocols
    1. __TCP__ _Transmission Control Protocol_
        1. Enables information to be broken into small packets, and sent between client and server
        2. If a packet is lost along the way, the send and receiver have a way of figuring out which packet is missing, and request that they be resent
    2. __IP__ _Internet Protocol_
    3. __HTTP__ _Hypertext Transfer Protocol_
