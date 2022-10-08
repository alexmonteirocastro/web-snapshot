from getopt import getopt
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from time import sleep
import sys, getopt
import re

NEURONS_HOMEPAGE = 'https://www.neuronsinc.com/'

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def get_web_snapshot(webURL):
    try:
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(service=Service('/usr/local/bin/geckodriver'), options=firefox_options)

        print(f'Getting a snapshot from: {webURL}...')

        url_parts = re.search('^https?://(www\.)?([A-Za-z_0-9.-]+).*\.', webURL)
        domain = url_parts.group(2)
        
        driver.get(webURL)
        sleep(1)
        driver.get_screenshot_as_file(f'{domain}_screenshot.png')
    finally:
        try:
            print("end...")
            # driver.close()
            driver.quit()
        except:
            pass

def main(argv):
   urlArg = ''
   try:
      opts, args = getopt.getopt(argv,"y=u:",["url="])
      if(len(opts) ==1):
        for opt, arg in opts:
            if opt in ("-u", "--url"):
                urlArg = arg
                if re.match(regex, urlArg) is not None:
                    get_web_snapshot(urlArg)
                else:
                    print('Please provide a valid URL')
                    sys.exit(2)
      else: 
        print('Sorry, you haven\'t provided a URL. Please use script in following way: args.py -u <url> or: args.py --url <url>')
        sys.exit(2)
   except getopt.GetoptError:
      print('Please use script in following way: args.py -u <url> or: args.py --url <url>')
      sys.exit(2)
    

if __name__ == "__main__":
   main(sys.argv[1:])