'''Filename: webserver.py'''

# Playthrough of the "Building a Server with HTTPBaseServer"
# tutorial with notes


from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

# main, handler


SIMPLE_FORM_HTML = """
<form method='POST' enctype='multipart/form-data' action='/hello'>
<h2>What would you like me to say?</h2>
<input name="message" type="text">
<input type="submit" value="Submit">
</form>"""

def main():
    # Try to connect to localhost port 8080, using my own webserverHandler class
    try:

        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    # handle KeyboardInterrupt to be sure to close the socket so it doesn't get stuck open
    # when I try to close and rerun the program
    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()



class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<html><body>"
                output += "Hello!"
                output += SIMPLE_FORM_HTML
                output += "</body></html>"

                # In Python 3, we can't just write a string to HTTP.
                # This is because Python 3 has allowed for multiple different types of
                # Encodings to be transmitted. We need to specify one. We will choose utf-8
                self.wfile.write(bytes(output, "utf-8"))
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<html><body>"
                output += "&#161Hola"
                output += SIMPLE_FORM_HTML
                output += "<a href = '\hello'>Back to Hello</a>\n\t</body>\n</html>"
                self.wfile.write(bytes(output, "utf-8"))
                print(output)
                return
            raise Exception("File not found")
        except:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # getheader deprecated in python3. use get.
            #ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
            ctype, pdict = cgi.parse_header(self.headers.get('Content-type'))
            

            #workaround for not being able to concat string to bytes in parse_multipart
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
   

            else:
                raise Exception("Weird lookin' form")
            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"

            # messagecontent[0] is the utf-8 data. We want the string version of b'{Message}'
            # So we trim the first two and last characters.
            message = str(messagecontent[0])[2:-1]
            output += "<h1> %s </h1>" % message
            output += SIMPLE_FORM_HTML
            output += "</body></html>"
            self.wfile.write(bytes(output, "utf-8"))
            print(output)
        except:
            print("ERROR")


if __name__ == '__main__':
    main()
