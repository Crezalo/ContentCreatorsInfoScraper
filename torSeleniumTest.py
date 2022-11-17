from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
from stem.control import Controller
from stem import Signal
from stem import process

# To use Tor's SOCKS proxy server with chrome, include the socks protocol in the scheme with the --proxy-server option
# PROXY = "socks5://127.0.0.1:9150" # IP:PORT or HOST:PORT
try:
    os.system("sudo fuser -k 9050/tcp")
    tor_launcher = process.launch_tor_with_config(
        config={
            "ControlPort": "9051",
        },
    )
except OSError:
    print(
        "Please terminate the running tor process in task manager(optional), Press Ctrl+C to stop the program"
    )
    raise

# torexe = os.popen(r'C:\Users\Kuski\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe')
PROXY = "socks5://127.0.0.1:9050"  # IP:PORT or HOST:PORT
print("reached")
options = Options()
options.add_argument("--proxy-server=%s" % PROXY)
for i in range(50):
    driver = webdriver.Chrome(options=options)
    driver.get("http://www.icanhazip.com")

    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        print("successful authenticate")
        controller.signal(Signal.NEWNYM)

    driver.get("https://channelcrawler.com/eng")
    time.sleep(1)
tor_launcher.terminate()
driver.quit()
