"""Main for scrap data from Judu"""
import argparse

from functions.drivers import Drivers
from functions.extract_data_and_get_times import ExtractDataAndGetTimes
from functions.find_4g import Find4g
from utils.logs_class import LogsClass


def main():
    """Scrap data from judu web page, insert it into MongoDB, and generate JSON if needed."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-log",
        default="info",
        help=(
            "Provide logging level. "
            "Example -log 'debug', default='info'"),
    )
    args = parser.parse_args()

    logs = LogsClass(log_level=args.log)
    logger = logs.logger

    browsers = ["chrome", "firefox", "edge"]
    for browser in browsers:
        driver = Drivers(browser, logger)
        driver.start_browser()
        find_4g = Find4g(driver.driver, logger)
        find_4g.find_4g_timetable()
        extract_data = ExtractDataAndGetTimes(driver.driver, logger)
        extract_data.extract_data()
        driver.close_browser()


if __name__ == "__main__":
    main()
