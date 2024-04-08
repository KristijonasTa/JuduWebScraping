"""Locators to find web elements"""
from selenium.webdriver.common.by import By

REJECT_COOKIES = (By.XPATH, "(//button[contains(text(),'Atsisakyti slapukų')])[1]")
NAV_BAR_TRANSPORT = (By.XPATH, "(//span[contains(text(),'Viešojo transporto keleiviams')])[1]")
TRANSPORT_TIME_TABLES = (By.XPATH, "//li[contains(@class,'menu-item "
                                   "menu-item-type-post_type menu-item-object-page "
                                   "menu-item-5404 menu-item-has-children')]//li[2]//a[1]")

IFRAME_SCHEDULE = (By.XPATH, "//iframe[@title='Schedules']")
EXPRESS_BUS_TOGGLE = (By.XPATH, "//span[@class='transport-toggle toggle-expressbus']")
BUS_4G = (By.XPATH, "//span[contains(text(),'Pilaitė–Konstitucijos "
                    "pr.–Saulėtekis')]")
BUS_4G_EUROPOS_STATION = (By.XPATH, "//div[@class='trip-table']"
                                    "//span[contains(text(),'Europos aikštė')]")
RADIO_WEEKDAY = (By.XPATH, "//div[@class='workdays-buttons-container']"
                           "//label[contains(text(),'Darbo diena')]")
RADIO_SATURDAY = (By.XPATH, "//div[@class='workdays-buttons-container']"
                            "//label[contains(text(),'Šeštadienis')]")
RADIO_SUNDAY_HOLIDAY = (By.XPATH, "//div[@class='workdays-buttons-container']"
                                  "//label[contains(text(),'Sekmadienis')]")
