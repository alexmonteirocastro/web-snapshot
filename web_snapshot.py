from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from time import sleep
import re
from url_checker import is_request_valid


NEURONS_HOMEPAGE = 'https://www.neuronsinc.com/'
FAULTY_URL = 'neurons'
NON_EXISTENT_URL = 'https://www.neuronsinc.dk/'

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def take_web_snapshot(webURL):
    try:
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(service=Service('/usr/local/bin/geckodriver'), options=firefox_options)

        print(f'Getting a snapshot from: {webURL}...')

        url_parts = re.search('^https?://(www\.)?([A-Za-z_0-9.-]+).*\.', webURL)
        domain = url_parts.group(2)
        snapshot_file = f'{domain}_screenshot.png'

        driver.get(webURL)
        sleep(1)
        driver.get_screenshot_as_file(snapshot_file)
    finally:
        try:
            print("end...")
            # driver.close()
            driver.quit()
        except:
            pass
    return snapshot_file

def get_web_snapshot(url):
    try:
        if re.match(regex, url) is not None:
            if is_request_valid(url) is True:
                return take_web_snapshot(url)
            else:
                err = 'URL does not seem to exist'
                print(err)
                return err
        else:
            err = 'Please provide a valid URL'
            print(err)
            return err
    except:
        pass

def main():
    get_web_snapshot(NON_EXISTENT_URL)

if __name__ == "__main__":
    main()
