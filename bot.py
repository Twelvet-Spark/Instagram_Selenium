from components.drivers import Drivers

browser_drives = Drivers(False)
browser_drives.create_driver()
browser_drives.start_driver()
browser_drives.login_driver()
browser_drives.start_scraping()
print("The driver have finished working, press Enter to turn off")
input()
browser_drives.stop_driver()