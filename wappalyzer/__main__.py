import argparse
import queue
import re
import sys
import threading
import tldextract

from queue import Queue
from huepy import bold, green

from wappalyzer.core.requester import get_response
from wappalyzer.core.analyzer import http_scan
from wappalyzer.core.utils import pretty_print, write_to_file
from wappalyzer.browser.analyzer import DriverPool, cookie_to_cookies, process_url, merge_technologies


def analyze(url, scan_type='full', threads=3, cookie=None):
    """Analyze a single URL"""
    if scan_type.lower() == 'full':
        driver_pool = None
        try:
            driver_pool = DriverPool(size=1, max_retries=6)  # Single driver for one URL
            with driver_pool.get_driver() as driver:
                if cookie:
                    for cookie_dict in cookie_to_cookies(cookie):
                        driver.add_cookie(cookie_dict)
                url, detections = process_url(driver, url)
                return {url: merge_technologies(detections)}
        finally:
            if driver_pool:
                try:
                    driver_pool.cleanup()
                except Exception as e:
                    print(f"Error during final cleanup: {str(e)}")
    return {url: http_scan(url, scan_type, cookie)}


def main():
    return

if __name__ == '__main__':
    main()
