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


class exploratoryCrawler:
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
        sleep(0.1)
        with open("ExploredChannels.tsv", "a", encoding="utf-8") as f:
            self.iterateOverRecommendationsFunctionUntilSuccess(ch, i, f)

    def iterateOverRecommendationsFunctionUntilSuccess(self, ch, i, f):
        attempt = 1
        while not self.getRecommededChannels_FromRecommendedVideos(ch, f):
            print(
                "CHANNEL No. "
                + str(i + 1)
                + " Attempt "
                + str(attempt)
                + " failed, retrying..."
            )
            attempt += 1
        return

    def getRecommededChannels_FromRecommendedVideos(self, ch, f):
        try:
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=self.chrome_options,
            )
            body = driver.find_element(By.CSS_SELECTOR, "body")
            body.send_keys(Keys.PAGE_DOWN)
            stealth(
                driver,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36",
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=False,
                run_on_insecure_origins=False,
            )
            driver.delete_all_cookies()
            driver.get("https://youtube.com/")
            sleep(5)

            try:
                window = driver.find_element(
                    "xpath",
                    "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]",
                )
                scroll = 0
                while scroll < 5:  # this will scroll 3 times
                    driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;",
                        window,
                    )
                    scroll += 1
                driver.find_element(
                    "xpath",
                    "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]",
                ).click()
            except Exception as e:
                try:
                    window = driver.find_element(
                        "xpath",
                        "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]",
                    )
                    scroll = 0
                    while scroll < 5:  # this will scroll 3 times
                        driver.execute_script(
                            "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;",
                            window,
                        )
                        scroll += 1
                    driver.find_element(
                        "xpath",
                        "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/a/tp-yt-paper-button/yt-formatted-string",
                    ).click()
                except Exception as e:
                    print(str(e))

            sleep(5)
            attempt = 1
            while not self.getIndividualChannelInfo(driver, ch, f) and attempt <= 5:
                print("Attempt " + str(attempt) + " failed, retrying...")
                attempt += 1

            driver.quit()
            return True
        except Exception as e:
            print(e)
            return False

    def getIndividualChannelInfo(self, driver, ch, f):
        try:
            driver.get(ch[1])
            sleep(1)
            if (
                len(
                    driver.find_elements(
                        "xpath",
                        "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse[1]/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[1]/div[3]/ytd-channel-video-player-renderer/div[2]/div/yt-formatted-string/a",
                    )
                )
                != 0
            ):
                vlink = driver.find_element(
                    "xpath",
                    "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse[1]/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[1]/div[3]/ytd-channel-video-player-renderer/div[2]/div/yt-formatted-string/a",
                ).get_attribute("href")
            else:
                vlink = driver.find_element(
                    "xpath",
                    "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[1]/div[3]/ytd-shelf-renderer/div[1]/div[2]/yt-horizontal-list-renderer/div[2]/div/ytd-grid-video-renderer[1]/div[1]/ytd-thumbnail/a",
                ).get_attribute("href")
            driver.get(vlink)
            driver.maximize_window()
            sleep(1)

            # with Controller.from_port(port=9051) as controller:
            #     controller.authenticate()
            #     # print("successful authenticate")
            #     controller.signal(Signal.NEWNYM)

            # recommended channel from video
            ch_names = []
            i = 1
            print("here1")
            while len(ch_names) <= 20:
                try:
                    temp = driver.find_element(
                        "xpath",
                        "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[3]/ytd-watch-next-secondary-results-renderer/div[2]/ytd-compact-video-renderer["
                        + str(i)
                        + "]/div[1]/div/div[1]/a/div/ytd-video-meta-block/div[1]/div[1]/ytd-channel-name/div/div/yt-formatted-string",
                    ).text
                    if temp not in ch_names:
                        ch_names.append(temp)
                        print(temp)
                    i += 1
                    body = driver.find_element(By.CSS_SELECTOR, "body")
                    body.send_keys(Keys.PAGE_DOWN)
                except Exception as e:
                    # print(e)
                    break
            print("here2")
            for x in ch_names:
                f.write(x + "\n")
            return True
        except Exception as e:
            print(e)
            return False


with open(
    "iteration1_complete/joined_distinct.tsv",
    "r",
    encoding="utf-8",
) as file:
    text = [x.split("\t") for x in file.read().split("\n")]
    with mp.Pool(mp.cpu_count()) as pool:
        pool.starmap(
            exploratoryCrawler,
            [(ch, i) for i, ch in enumerate(text)],
        )

# with mp.Pool(mp.cpu_count()) as pool:
#     out = pool.map(channelCrawler, [i for i in range(15)])
# Parallel(n_jobs=1)(delayed(channelCrawler)(i) for i in range(15))
# my_bot = channelCrawler(1)
# my_bot.build_name_and_Couple_Database()
