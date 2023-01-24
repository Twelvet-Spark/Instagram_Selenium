import secrets
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import components.settings as settings

class PostPage:
    def __init__(self, driver: webdriver, id):
        self.driver = driver
        self.id = id
        self.posts_to_like = settings.posts_to_like
        self.posts_to_comment = settings.posts_to_comment
        self.comments_good = settings.comments_good
        self.comments_bad = settings.comments_bad
        self.postUrl = []
        self.likeStatusSvg = ""
        self.likeButton = ""
        self.textArea = ""
        self.sendTextButton = ""
        self.nicknameInComment = ""
        self.commentText = ""
    
    def likePost(self, url="from list"):
        # Проверка списка постов для лайков или замена его на единичный пост переданный параметром
        if url == "from list":
            if len(self.posts_to_like) == 0:
                print(f"[Драйвер - {self.id}] Список постов для лайков пуст!")
                return 0
            self.postUrl = self.posts_to_like.copy()
        else:
            self.postUrl.append(url)
        # Начало поставления лайка
        for i in range(0, len(self.postUrl)):
            self.driver.get(self.postUrl[i])
            try:
                WebDriverWait(self.driver, 10).until(EC.url_matches(self.postUrl[i])) # Проверяем перешли ли мы по ссылке на пост
            except Exception as e:
                print(f"[Драйвер - {self.id}] Не получилось перейти по ссылке {self.postUrl[i]}")
                continue # Переходим к следующему посту TODO: Посты с ошибками добавлять в отдельный массив, чтобы позже их исправить
            else:
                print(f"[Драйвер - {self.id}] Успешный переход по ссылке {self.postUrl[i]}")
            # Проверка на наличие лайка, после чего ставится сам лайк
            try:
                self.likeStatusSvg = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label=\"Like\"][height=\"24\"],[aria-label=\"Unlike\"][height=\"24\"]"))).get_attribute("aria-label") # Если не лайкнут
            except Exception as e:
                print(f"[Драйвер - {self.id}] Не получилось найти состояние кнопки лайка")
                continue # Загружаем другой пост
            try:
                if self.likeStatusSvg == "Like":
                    self.driver.find_element(by=By.CSS_SELECTOR, value=f"svg[aria-label=\"{self.likeStatusSvg}\"]").find_element(by=By.XPATH, value="..").find_element(by=By.XPATH, value="..").click()
                elif self.likeStatusSvg == "Unlike":
                    print(f"[Драйвер - {self.id}] Пост уже лайкнут {self.postUrl[i]}")
                    continue # Следующий пост
            except Exception as e:
                print(f"[Драйвер - {self.id}] Не смог лайкнуть пост {self.postUrl[i]}")
            else:    
                print(f"[Драйвер - {self.id}] Пост успешно лайкнут {self.postUrl[i]}")

    def commentPosts(self, comment="good", url="from list"):
        # Проверка списка постов для комментариев или замена его на единичный пост переданный параметром
        if url == "from list":
            if len(self.posts_to_comment) == 0:
                print(f"[Драйвер - {self.id}] Список постов для комментариев пуст!")
                return 0
            self.postUrl = self.posts_to_comment.copy()
        else:
            self.postUrl.append(url)
        # Определение характера комментария и его текста или замена его на переданный из параметра
        if comment == "good":
            self.commentText = secrets.choice(settings.comments_good)
        elif comment == "bad":
            self.commentText = secrets.choice(settings.comments_bad)
        else:
            self.commentText = comment
        # Начало поставления комментария
        for i in range(0, len(self.postUrl)):
            self.driver.get(self.postUrl[i])
            try:
                WebDriverWait(self.driver, 10).until(EC.url_matches(self.postUrl[i])) # Проверяем перешли ли мы по ссылке на пост
            except Exception as e:
                print(f"[Драйвер - {self.id}] Не получилось перейти по ссылке {self.postUrl[i]}")
                continue # Переходим к следующему посту TODO: Посты с ошибками добавлять в отдельный массив, чтобы позже их исправить
            else:
                print(f"[Драйвер - {self.id}] Успешный переход по ссылке {self.postUrl[i]}")
            # Проверяем есть ли наш никнейм в коммантариях (Он обычно стоит в определённом месте)
            try:
                self.nicknameInComment = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul._a9ym:nth-child(2) > div:nth-child(1) > li:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > h3:nth-child(1) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1)"))).text
                if self.nicknameInComment == settings.login_data[self.id]["username"]:
                    print(f"[Драйвер - {self.id}] Пост уже был прокомментирован {self.postUrl[i]}")
                    continue # Продолжаем, если пост уже прокомментирован
                else:
                    try:
                        self.textArea = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[aria-label=\"Add a comment…\"]")))
                    except Exception:
                        print(f"[Драйвер - {self.id}] Не смог найти поле ввода комментария")
                    else:
                        try:
                            self.sendTextButton = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role=\"button\"]")))
                            for button in self.sendTextButton:
                                if button.text == "Post":
                                    self.sendTextButton = button
                            self.textArea.send_keys(self.commentText)
                            self.sendTextButton.click()
                        except Exception as e:
                            print(f"[Драйвер - {self.id}] Не смог получить состояние или кликнуть на кнопку отправки комментария")
                        try:
                            WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "svg[aria-label=\"Loading...\"]")))
                            self.nicknameInComment = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul._a9ym:nth-child(2) > div:nth-child(1) > li:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > h3:nth-child(1) > div:nth-child(1) > span:nth-child(1) > a:nth-child(1)"))).text
                            if self.nicknameInComment == settings.login_data[self.id]["username"]:
                                print(f"[Драйвер - {self.id}] Пост успешно прокомментирован {self.postUrl[i]}")
                                continue                                
                        except Exception as e:
                            print(f"[Драйвер - {self.id}] Не удалось удостовериться в отправке комментария к посту {self.postUrl[i]}")
            except Exception as e:
                print(f"[Драйвер - {self.id}] Не смог найти никнейм комментария")