import requests
# from bs4 import BeautifulSoup
import fandom
from timeout_decorator import timeout
import random
import time


@timeout(120)  # Set a timeout seconds
def fandom_page(item):
    p = fandom.page(item).plain_text

    return p


# Replace with your unique_list
unique_list = ["Sayyadina", "Chani", "Gurney Halleck", "Chusuk", "Usul"]

fandom.set_wiki("dune")
fandom.set_rate_limiting(3)
for item in unique_list:
    sleep_duration = random.uniform(1, 5)
    print(
        f'-------------------------------------------------- sleeping for {sleep_duration} seconds')
    time.sleep(sleep_duration)

    try:

        # Call the function
        p = fandom_page(item)
        print(p)

    except TimeoutError:
        print("Function timed out!")


# for item in unique_list:
#     # Construct the URL for each item
#     url = f"https://dune.fandom.com/wiki/{item}"
#     response = requests.get(url)
#     content = response.text

#     soup = BeautifulSoup(content, "html.parser")
#     text = soup.get_text().strip()

#     if text:
#         print(f"Text for {item}: {text}")
#     else:
#         print(f"No text found for {item}")
