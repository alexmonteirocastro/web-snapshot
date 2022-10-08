import requests

NEURONS_HOMEPAGE = 'https://www.neuronsinc.com/'
FAULTY_URL = 'neurons'
NON_EXISTENT_URL = 'https://www.neuronsinc.dk/'


def is_request_valid(url):
    try:
        response = requests.get(url, timeout=10, verify=False)
        return True
    except requests.exceptions.ConnectionError as e:
        # 👇️ handle error here or use a `pass` statement
        print(f'connection error occurred: {e}')
        return False

def main():
    is_request_valid(NEURONS_HOMEPAGE)

if __name__ == "__main__":
    main()