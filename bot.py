from components.configFile import ConfigFile
from components.drivers import Drivers
from datetime import datetime
from time import sleep

# Drivers(Количество ботов, ссылка на соц. сеть, режим без открытия окна браузера(headless))
# Количество ботов зависит от количества аккаунтов, которые прописаны в config.py
# Поддерживается только www.instagram.com
# Режим headless - обеспечивает работу ботов без открытия окна браузера

# loginInfo = ConfigFile("logins.ini").getConfigInfo("instagram")
# print(f"Данные для входа = {loginInfo}")
# parameter = ConfigFile("configfile.ini").getConfigInfo("drivers_settings", ["drivers_amount", "sleep_time", "browser_type", "headless_mode"])
# print(f"Праметры drivers_settings = {parameter}")


browser_drives = Drivers(1, 'https://www.instagram.com/', False)
browser_drives.create_drivers()
browser_drives.start_drivers()
browser_drives.login_drivers()
browser_drives.like_posts()
browser_drives.comment_posts()
print("Драйвера закончили работу, нажмите Enter для выключения")
input()
browser_drives.stop_drivers()

# TODO:
# Проверку на существование комментария под постом от имени драйвера №3
# Нормальное ожидание загрузки страницы и загрузки элементов №1 (ON GOING)
# Запускать каждый драйвер в отдельном потоке №2