from selenium import webdriver
import os
from time import sleep
from collections import defaultdict
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import multiprocessing as mp
import tqdm

# from joblib import Parallel, delayed
import multiprocessing as mp
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


class channelInfoFromName:
    def __init__(self, ch, i):
        print("starting ...")
        PROXY = "socks5://127.0.0.1:9050"  # IP:PORT or HOST:PORT
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")  # linux only
        self.chrome_options.add_argument("--proxy-server=%s" % PROXY)
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        self.chrome_options.add_experimental_option("useAutomationExtension", False)
        self.chrome_options.add_argument("--headless")
        # chrome_options.headless = True # also works
        with open(
            "ExploredChannelsDistinct_CompleteInfo.tsv", "a", encoding="utf-8"
        ) as f:
            self.getChannelInfo(ch, i, f)

    def getChannelInfo(self, ch, i, f):
        attempt = 1
        while not self.getChannelInfoFunc(ch, f):
            print(
                "CHANNEL No. "
                + str(i + 1)
                + " Attempt "
                + str(attempt)
                + " failed, retrying..."
            )
            attempt += 1
        return

    def getChannelInfoFunc(self, ch, file):
        try:
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=self.chrome_options,
            )
            driver.delete_all_cookies()
            driver.get("https://channelcrawler.com/eng")

            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                # print("successful authenticate")
                controller.signal(Signal.NEWNYM)

            driver.maximize_window()
            # Category
            driver.find_element(
                "xpath",
                "/html/body/div[1]/div[3]/div/form/div[2]/div[1]/div[2]/div/div/div[1]/div[1]/div/input",
            ).send_keys(ch)
            # Country
            driver.find_element(
                "xpath",
                "/html/body/div[1]/div[3]/div/form/div[2]/div[1]/div[2]/div/div/div[1]/div[4]/div/div/div[1]/div/span/input",
            ).click()
            # India
            driver.find_element(
                "xpath",
                "/html/body/div[1]/div[3]/div/form/div[2]/div[1]/div[2]/div/div/div[1]/div[4]/div/div/div[2]/ul/li[103]",
            ).click()
            #Submit button
            driver.find_element(
                "xpath", "/html/body/div[1]/div[3]/div/form/div[3]/div/button"
            ).click()

            data = []
            for i in range(20):
                temp = self.channelInfo(
                    driver,
                    "/html/body/div[1]/div[1]/div/div[2]/div[" + str(i + 1) + "]",
                )
                if temp != []:
                    data.append("\t".join(temp))

            data = list(set(data))

            for x in data:
                file.write(x + "\n")

            driver.quit()
            return True

        except Exception as e:
            print(str(e))
            return False

    def channelInfo(self, driver, path):
        try:
            name = driver.find_element("xpath", path + "/h4/a").get_attribute("title")
            link = driver.find_element("xpath", path + "/h4/a").get_attribute("href")
            category = driver.find_element("xpath", path + "/small/b").text
            description = driver.find_element("xpath", path + "/a").get_attribute(
                "title"
            )
            subCount = driver.find_element("xpath", path + "/p[1]/small").text.split(
                "\n"
            )[0]
            totalVideos = driver.find_element("xpath", path + "/p[1]/small").text.split(
                "\n"
            )[1]
            totalViews = driver.find_element("xpath", path + "/p[1]/small").text.split(
                "\n"
            )[2]
            return [
                name,
                link,
                category,
                description.replace("\n", " ").replace("\t", " "),
                subCount,
                totalVideos,
                totalViews,
            ]
        except Exception as e:
            return []

with open(
    "ExploredChannelsDistinct.tsv",
    "r",
    encoding="utf-8",
) as file:
    text = file.read().split("\n")
    with mp.Pool(1) as pool:
        pool.starmap(
            channelInfoFromName,
            [(ch, i) for i, ch in enumerate(tqdm.tqdm(text))],
        )

# with mp.Pool(mp.cpu_count()) as pool:
#     out = pool.map(channelCrawler, [i for i in range(15)])
# Parallel(n_jobs=1)(delayed(channelCrawler)(i) for i in range(15))
# my_bot = channelCrawler(1)
# my_bot.build_name_and_Couple_Database()
