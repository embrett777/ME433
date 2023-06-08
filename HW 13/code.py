# website wouldn't pop up, even though it generated IP address
# wasn't able to fix problem, and heard multiple people encountered the same thing
import os
import time
import ipaddress
import wifi
import socketpool
import board
import microcontroller
import terminalio
from digitalio import DigitalInOut, Direction
import adafruit_httpserver
import adafruit_httpserver.methods

HTTPServer = adafruit_httpserver.server.Server
HTTPRequest = adafruit_httpserver.request.Request
HTTPResponse = adafruit_httpserver.response.Response

#  onboard LED setup
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

#  function to convert celcius to fahrenheit
def c_to_f(temp):
    temp_f = (temp * 9/5) + 32
    return temp_f

#  connect to network
print()
print("Connecting to WiFi")

#  connect to your SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

print("Connected to WiFi")
pool = socketpool.SocketPool(wifi.radio)
server = HTTPServer(pool, "/static")

# variables for HTML
unit = "F"
#  font for HTML
font_family = "monospace"

#  the HTML script
#  setup as an f string
#  this way, can insert string variables from code.py directly
#  of note, use {{ and }} if something from html *actually* needs to be in brackets
#  i.e. CSS style formatting
def webpage():
    temp = str(c_to_f(microcontroller.cpu.temperature))

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-type" content="text/html;charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
    <style>
    html{{font-family: {font_family}; background-color: lightgrey;
    display:inline-block; margin: 0px auto; text-align: center;}}
      h1{{color: deeppink; width: 200; word-wrap: break-word; padding: 2vh; font-size: 20px;}}
      p{{font-size: 15px; width: 200; word-wrap: break-word;}}
      .button{{font-family: {font_family};display: inline-block;
      background-color: black; border: none;
      border-radius: 4px; color: white; padding: 5px 5px;
      text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}}
      p.dotted {{margin: auto;
      width: 75%; font-size: 15px; text-align: center;}}
    </style>
    </head>
    <body>
    <title>Pico W HTTP Server</title>
    <h1>Pico W HTTP Server</h1>
    <br>
    <p class="dotted">This is a Pico W running an HTTP server with CircuitPython.</p>
    <br>
    <p class="dotted">The current ambient temperature near the Pico W is
    <span style="color: deeppink;"><span id="temp">{temp}</span>°{unit}</span></p><br>
    <h1>Control the LED on the Pico W with these buttons:</h1><br>
    <p><button class="button" name="LED" value="ON" type="submit">LED ON</button></a></p>
    <p><button class="button" name="LED" value="OFF" type="submit">LED OFF</button></a></p>
    </body>
    <script>
    // LED buttons handler
    $(".button").click((el) => {{ $.post("/led", {{[el.target.name]: el.target.value}}) }});
    // 1 sec temperature refresher
    setInterval(() => {{
        $.get("/temp", (data) => {{
            $("#temp").text(data);
        }});
    }}, 1000);
    </script>
    </html>
    """
    return html

#  route default static IP
@server.route("/")
def base(request: HTTPRequest):
    #  serve the HTML f string
    #  with content type text/html
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send(f"{webpage()}")

# change led state
@server.route("/led", adafruit_httpserver.methods.POST)
def buttonpress(request: HTTPRequest):
    print("button request")
    #  get query params (doesn't handle all cases, use with caution
    query = {x[0] : x[1] for x in [x.split("=") for x in request.body.decode("utf8").split("&")]}
    #  if the led on button was pressed
    if "LED" in query:
        #  turn on or off the onboard LED
        led.value = (query["LED"] == "ON")
    # Acknowledge
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send()

# get temperature
@server.route("/temp")
def temp(request: HTTPRequest):
    print("Temp request")
    # Read temperature
    temp = str(c_to_f(microcontroller.cpu.temperature))

    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send(temp)

print("Starting server..")
# startup the server
try:
    server.start(str(wifi.radio.ipv4_address))
    print("Listening on http://%s:80" % wifi.radio.ipv4_address)
    #  prints MAC address to REPL
    print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
    #  prints IP address to REPL
    print("My IP address is", wifi.radio.ipv4_address)
#  if the server fails to begin, restart the pico w
except OSError:
    time.sleep(5)
    print("Restarting..")
    microcontroller.reset()

while True:
    try:
        #  poll the server for incoming/outgoing requests
        server.poll()
    except Exception as e:
        print(e)
        continue
