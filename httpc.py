#   python httpc.py get -v 'http://httpbin.org/get?course=networking&assignment=1'
#   python httpc.py post -v -head Accept:application/json -d '{"test":"test"}' 'http://httpbin.org/post'
#   python httpc.py post -v -head Accept:application/json -f 'test.json' 'http://httpbin.org/post'
import sys
from socket import *
import json
import argparse
from http import http

def create_http():
    h = http(args.URL)
    h.setType(args.which)
    if args.verbose:
        h.setVerbosity(True)
    if args.headers:
        header = ""
        if len(args.headers) > 0:
            for head in args.headers:
                split_head = head.split(":")
                if len(split_head) == 2:
                    header = header + "\r\n" + split_head[0] + ": " + split_head[1]
        h.setHeader(header)
    #read the data or file to send it as content in post message and add content-Type of header
    body = ""
    if args.which == "post":
       if args.data:
            body = json.dumps(args.data)
            h.setData(body)
            h.setHeader("\r\n" + "Content-Type:application/json")
            h.setHeader("\r\n" + "Content-Length: "+str(len(body)))
       if args.file:
            with open(args.file, 'r') as f:
                body = f.read()
            h.setFile(body)
            h.setHeader("\r\n" + "Content-Type:application/json")
            h.setHeader("\r\n" + "Content-Length: " + str(len(body)))
    h.constructContent()
    return h

parser = argparse.ArgumentParser(description="httpc is a curl-like application but supports HTTP protocol only.")
# parser.add_argument('request_type', help="type of request, GET or POST", choices=['GET', 'get', 'post', 'POST'])

subparsers = parser.add_subparsers(help='commands')

get_parser = subparsers.add_parser('get', help='executes a HTTP GET request and prints the response.')
get_parser.add_argument("-v", action='store_true', dest="verbose", default=False, help="Prints the detail of the response such as protocol, status, and headers.")
get_parser.add_argument("-head", action="append", dest="headers", default=[], help="Associates headers to HTTP Request with the format 'key:value'.")
get_parser.set_defaults(which='get')

post_parser = subparsers.add_parser('post', help='executes a HTTP POST request and prints the response.')
post_parser.add_argument("-v", action='store_true', dest="verbose", default=False, help="Prints the detail of the response such as protocol, status, and headers.")
post_parser.add_argument("-head", action="append", dest="headers", default=[], help="Associates headers to HTTP Request with the format 'key:value'.")
group = post_parser.add_mutually_exclusive_group(required=False)
group.add_argument("-d", action="store", dest="data", type=json.loads, default='{}', help="Associates an inline data to the body HTTP POST request.")
group.add_argument("-f", action="store", dest="file", default="", help="Associates the content of a file to the body HTTP POST request.")
post_parser.set_defaults(which='post')

help_parser = subparsers.add_parser('help', help='prints this screen.')
help_parser.set_defaults(which='help')

parser.add_argument("URL", help="HTTP URL address")

args = parser.parse_args()
# print(args)
# parser.print_help()
h = create_http()
reply = h.send()
if h.getVerbosity():
    print("Reply:\n" + reply)