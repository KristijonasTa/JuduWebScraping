"""Get timetable from web"""
import datetime
import holidays
from selenium.common import TimeoutException, NoSuchElementException

from utils.base_class import BaseClass
from utils.locators import REJECT_COOKIES, NAV_BAR_TRANSPORT, TRANSPORT_TIME_TABLES, \
    IFRAME_SCHEDULE, EXPRESS_BUS_TOGGLE, BUS_4G, BUS_4G_EUROPOS_STATION, RADIO_WEEKDAY, \
    RADIO_SUNDAY_HOLIDAY, RADIO_SATURDAY


class Find4g:
    """Get timetable from web"""
    def __init__(self, driver, logger):
        self.driver = driver
        self.base_class = BaseClass(self.driver)
        self.lt_holiday = holidays.country_holidays("LT")
        self.logger = logger

    def find_4g_timetable(self):
        """Full steps to find timetables"""
        self.navigate_to_time_tables()
        self.open_4g_timetable()
        self.select_today()

    def navigate_to_time_tables(self):
        """Navigate to the whole timetable"""
        self.base_class.click(REJECT_COOKIES)
        self.base_class.wait_element_visibility(NAV_BAR_TRANSPORT)
        self.base_class.hover(NAV_BAR_TRANSPORT)
        self.base_class.click(TRANSPORT_TIME_TABLES)

    def open_4g_timetable(self):
        """Open timetable of 4G "Europos aikštė" station"""
        try:
            self.base_class.wait_element_visibility(IFRAME_SCHEDULE)
            self.base_class.switch_to_iframe(IFRAME_SCHEDULE)

            self.base_class.wait_element_clickable(EXPRESS_BUS_TOGGLE)
            self.base_class.click(EXPRESS_BUS_TOGGLE)

            # This part was added because when the script tried to select the BUS_4G
            # locator, connection loss occurred and the script broke.
            self.base_class.switch_to_default_content()
            self.base_class.switch_to_iframe(IFRAME_SCHEDULE)

            self.base_class.wait_element_clickable(BUS_4G)
            self.base_class.click(BUS_4G)

            self.base_class.wait_element_clickable(BUS_4G_EUROPOS_STATION)
            self.base_class.click(BUS_4G_EUROPOS_STATION)
            self.logger.info("4G bus time tables opened")
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.critical(f"4g bus time tables failed to be opened: {e}")

    def select_today(self, date=None):
        """Check by date and select radio button"""
        # Define a dictionary to map weekday numbers to their names
        weekday_names = {
            0: "Weekday",
            1: "Weekday",
            2: "Weekday",
            3: "Weekday",
            4: "Weekday",
            5: "Saturday",
            6: "Sunday or Holiday"
        }

        self.base_class.wait_element_visibility(RADIO_WEEKDAY)
        self.base_class.find_element(*RADIO_WEEKDAY).is_displayed()
        if date is None:
            date = datetime.date.today()
            self.logger.info(f"Date selected: {date} {date.strftime('%A')}")

        try:
            if date.weekday() == 6 or date in self.lt_holiday:
                self.base_class.click(RADIO_SUNDAY_HOLIDAY)
            elif date.weekday() == 5:
                self.base_class.click(RADIO_SATURDAY)
            else:
                self.base_class.click(RADIO_WEEKDAY)
            select_weekday = weekday_names[date.weekday()]
            self.logger.info(f"Radio button selected: {select_weekday}")
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.critical(f"The radio button was not selected: {e}")
