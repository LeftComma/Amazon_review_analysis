import requests
from bs4 import BeautifulSoup
import time


def request_url(url, no_tries=3):
    if no_tries == 0:
        print('URL request has failed 3 times. Moving to next URL')
        return 0

    try:
        time.sleep(2)
        # Having a header helps convince Amazon that we're not a bot
        headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
                    'Accept-Language': 'en-US, en;q=0.5'})

        # Make the request, timeout means it throw an error if it takes longer than 1 sec
        r = requests.get(url=url, headers=headers, timeout=1)

        r.raise_for_status()

        # Create a soup object, lxml is a fast and lenient HTML parser
        soup = BeautifulSoup(r.text, "lxml")

    # This handles all types of error in the requests package
    except requests.exceptions.RequestException as err:
        print('An error has occured when trying to reach the url')
        print(err)
        no_tries -= 1
        request_url(url, no_tries)


request_url('http://www.google.com/nothere')
