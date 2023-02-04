from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import components.settings as settings
import time

# TODO: Instead of checking media height only in carousel, check it also for single media post
# TODO: Change all to one element in multiple media posts
# TODO: line 77 hardcoded url https://www.instagram.com/

class PostPage:
    def __init__(self, driver: Chrome):
        self.driver = driver
        self.posts_to_scrape = settings.posts_to_scrape
        self.postsURLs = []
        self.mediaType = ""
        self.postType = ""
        self.isStories = False
        self.isMultipleMedia = False
        self.timeToFindVideo = 1
        self.carouselMedia = []
        self.carouselTimeToWaitNextButtonAppear = 1 # SECONDS How long bot will wait until Next button appear or not. (Slightly make script faster, but i don't recommend changing this)
        self.carouselTimeBetweenSlides = 1 # SECONDS How fast slides will be chaged, less > faster. (Could make script lot faster, just make sure all media is loaded in this time)

    def scrape_links(self):
        if len(self.posts_to_scrape) == 0:
            print(f"[Driver] The list of posts is empty!")
            return 0
        else:
            self.postsURLs = self.posts_to_scrape.copy()
        # Main cycle for posts scraping.
        for url in self.postsURLs:
            self.carouselMedia.clear()
            self.driver.get(url)
            try:
                if WebDriverWait(self.driver, 1).until(EC.url_contains("stories")):
                    try:
                        viewStoryTextBool = WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "button[type=\"button\"]"), "View story"))
                        if viewStoryTextBool:
                            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type=\"button\"]"))).click()
                            self.isStories = True
                    except TimeoutException:
                        pass
                    except Exception as e:
                        raise(e)
            except TimeoutException:
                pass
            except Exception as e:
                raise(e)
            if not self.isStories:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[style=\"position: relative; display: flex; flex-direction: column; padding-bottom: 0px; padding-top: 0px;\"]")))
            try:
                # Search for next media button in post to check if it is carousel.
                self.driver.find_element(by=By.CSS_SELECTOR, value="button[aria-label=\"Next\"]")
                print(f"[Driver] Multiple media post {url}:")
                self.isMultipleMedia = True
            except NoSuchElementException:
                print(f"[Driver] Single media post {url}:")
                self.isMultipleMedia = False
            except Exception as e:
                raise(e)
            # If post contains carousel
            if self.isMultipleMedia == True:
                maxSizeImageHeight = 0 # I think in all cases main post media has the biggest height and width. Using this we can sort out any other media on page.
                while True:
                    time.sleep(self.carouselTimeBetweenSlides)
                    try:
                        medias = WebDriverWait(self.driver, self.timeToFindVideo).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "video")))
                        self.postType = "Video"
                    except TimeoutException:
                        medias = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img[crossorigin=\"anonymous\"]:not([draggable=\"false\"])")))
                        self.postType = "Image"
                    except Exception as e:
                        raise(e)
                    for media in medias:
                        if media.size["height"] > maxSizeImageHeight:
                            maxSizeImageHeight = media.size["height"]
                        if {"src": media.get_attribute('src'), "height": media.size["height"], "type": self.postType} not in self.carouselMedia:
                            self.carouselMedia.append({"src": media.get_attribute('src'), "height": media.size["height"], "type": self.postType})
                    try:
                        # Check if we are ended watching stories
                        if self.isStories:
                            if self.driver.current_url == "https://www.instagram.com/":
                                break
                        WebDriverWait(self.driver, self.carouselTimeToWaitNextButtonAppear).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label=\"Next\"]"))).click()
                    except TimeoutException:
                        break
                    except Exception as e:
                        raise(e)
                for url in self.carouselMedia:
                    if url['height'] == maxSizeImageHeight: # Filter media by comaring their height to height of the main post media.
                        print(f"--{url['type']}\n{url['src']}\n")
            # If post is single media file.
            # WARNING: Possible media mismatched delivered.
            elif self.isMultipleMedia == False:
                media = WebDriverWait(self.driver, 10).until(EC.any_of(EC.presence_of_element_located((By.CSS_SELECTOR, "img[crossorigin=\"anonymous\"]:not([draggable=\"false\"])")), EC.presence_of_element_located((By.CSS_SELECTOR, "video"))))
                if media.tag_name == "img":
                    self.postType = "Image"
                elif media.tag_name == "video":
                    self.postType = "Video"
                else:
                    self.postType = "Other"
                print(f"--{self.postType}\n{media.get_attribute('src')}\n")