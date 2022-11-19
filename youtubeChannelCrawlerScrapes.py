from selenium import webdriver
import os
from time import sleep
from collections import defaultdict
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# from joblib import Parallel, delayed
import multiprocessing as mp
from stem.control import Controller
from stem import Signal
from stem import process

# To use Tor's SOCKS proxy server with chrome, include the socks protocol in the scheme with the --proxy-server option
# PROXY = "socks5://127.0.0.1:9150" # IP:PORT or HOST:PORT
try:
    print("sdsdsd")
    os.system("sudo fuser -k 9050/tcp")
    print("sdsdsd")
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


class channelCrawler:
    def __init__(self, category_ind):
        PROXY = "socks5://127.0.0.1:9050"  # IP:PORT or HOST:PORT
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")  # linux only
        self.chrome_options.add_argument("--proxy-server=%s" % PROXY)
        self.chrome_options.add_argument("--headless")
        # chrome_options.headless = True # also works
        sleep(0.1)
        self.categories = [
            "Autos&Vehicles",
            "Comedy",
            "Education",
            "Entertainment",
            "Film&Animation",
            "Gaming",
            "Howto&Style",
            "Music",
            "News&Politics",
            "Nonprofits&Activism",
            "People&Blogs",
            "Pets&Animals",
            "Science&Technology",
            "Sports",
            "Travel&Events",
        ]
        with open(
            "youtubeChannelData_" + self.categories[category_ind] + ".tsv",
            "a",
            encoding="utf-8",
        ) as file:
            self.searchByCategory(category_ind + 1, file)

        # self.searchQuery(1, 1, 1)

    def searchByCategory(self, i, f):
        for j in range(1, 18):
            for k in range(j, 18):
                self.searchQuery(i, j, k, f)
                print("Percent completion: " + str((j * k - j + k) * 100 / 153) + " %")
                print("Category: " + self.categories[i-1])
                print("Min No. : " + str(j))
                print("Max No.: " + str(k))
        return

    def searchQuery(self, category, minsub, maxsub, file):
        print("sdsdsd")
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
            "/html/body/div[1]/div[3]/div/form/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/div/div/div[1]/div/span/input",
        ).click()
        sleep(0.1)
        # Auto & Vehicle (1-15)
        driver.find_element(
            "xpath",
            "/html/body/div[1]/div[3]/div/form/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/div/div/div[2]/ul/li["
            + str(category)
            + "]",
        ).click()
        sleep(0.1)
        driver.find_element(
            "xpath",
            "/html/body/div[1]/div[3]/div/form/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/label",
        ).click()
        sleep(0.1)
        # Country
        driver.find_element(
            "xpath",
            "/html/body/div[1]/div[3]/div/form/div[2]/div[1]/div[2]/div/div/div[1]/div[4]/div/div/div[1]/div/span/input",
        ).click()
        sleep(0.1)
        # India
        driver.find_element(
            "xpath",
            "/html/body/div[1]/div[3]/div/form/div[2]/div[1]/div[2]/div/div/div[1]/div[4]/div/div/div[2]/ul/li[103]",
        ).click()
        sleep(0.1)
        driver.find_element(
            "xpath",
            "/html/body/div[1]/div[3]/div/form/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/label",
        ).click()
        sleep(0.1)
        # Min Subscribers
        driver.find_element(
            "xpath",
            "/html/body/div[1]/div[3]/div/form/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div/div[1]/div/select",
        ).click()
        sleep(0.1)
        # 1000 (1-17)
        driver.find_element(
            "xpath",
            "/html/body/div[1]/div[3]/div/form/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div/div[1]/div/select/option["
            + str(minsub)
            + "]",
        ).click()
        sleep(0.1)
        driver.find_element(
            "xpath",
            "/html/body/div[1]/div[3]/div/form/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/label",
        ).click()
        # Max Subscribers
        driver.find_element(
            "xpath",
            "/html/body/div[1]/div[3]/div/form/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div/div[2]/div/select",
        ).click()
        sleep(0.1)
        # 2000 (1-17)
        driver.find_element(
            "xpath",
            "/html/body/div[1]/div[3]/div/form/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/div/div[2]/div/select/option["
            + str(maxsub)
            + "]",
        ).click()
        sleep(0.1)
        driver.find_element(
            "xpath",
            "/html/body/div[1]/div[3]/div/form/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/label",
        ).click()
        sleep(0.1)
        driver.find_element(
            "xpath", "/html/body/div[1]/div[3]/div/form/div[3]/div/button"
        ).click()
        sleep(0.1)

        data = []

        mainUrl = driver.current_url

        for j in range(5):
            for i in range(20):
                temp = self.channelInfo(
                    driver,
                    "/html/body/div[1]/div[1]/div/div[2]/div[" + str(i + 1) + "]",
                )
                if temp != []:
                    data.append("\t".join(temp))
            driver.get(mainUrl + "/page:" + str(j + 2))

        data = list(set(data))

        for x in data:
            file.write(x + "\n")

        driver.quit()

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


print("sdsdsd")
with mp.Pool(mp.cpu_count()) as pool:
    out = pool.map(channelCrawler,[i for i in range(15)])
# Parallel(n_jobs=1)(delayed(channelCrawler)(i) for i in range(15))
# my_bot = channelCrawler(1)
# my_bot.build_name_and_Couple_Database()
