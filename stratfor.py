import requests
from bs4 import BeautifulSoup
import argparse

# Define the base URL and topics URL
base_url = 'https://worldview.stratfor.com'
topics_url = base_url + '/topic/'
topics = {
    "isr": "israel-hamas-conflict",
    "ukr": "russia-ukraine-conflict",
    "nvy": "tracking-us-naval-power",
    "soc": "social-issues",
    "tec": "environment-science-technology",
    "mil": "military-security",
    "cyb": "cyber-security",
    "pol": "politics",
    "ecn": "economics",
    "eng": "energy",
    "m": "main page"  # Special case for the main page
}

# Setup command line argument parsing
parser = argparse.ArgumentParser(description='Fetch information about specific topics or the main page.')
parser.add_argument('topic', type=str, nargs='?', help='Three-letter reference to a topic or "m" for the main page')

# Function to display available topics
def display_help():
    print("Available topics and their codes:")
    for key, value in topics.items():
        print(f"{key}: {value} ({topics_url}{value} for topics, {base_url} for the main page)")

# Function to fetch and display topic information
def fetch_topic_data(topic_key):
    if topic_key == 'm':  # Special handling for the main page
        response = requests.get(base_url)
        print("\nFetching headlines from the main page...\n")
    elif topic_key in topics:
        topic_url = topics_url + topics[topic_key]
        response = requests.get(topic_url)
        print(f"\nFetching information about {topics[topic_key]}...\n")
    else:
        print("\nTopic not found. Use the following command for help: python script_name.py help\n")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    if topic_key == 'm':
        headlines = soup.find('body').find_all('li', class_='headline')
    else:
        headlines = soup.find('body').find_all('div', class_='ContentTemplate_title__sBxv9')
    
    line_number = 1
    for headline in headlines:
        print(f"{line_number}. {headline.text.strip()}")
        line_number += 1

args = parser.parse_args()

if args.topic:
    if args.topic == 'help':
        display_help()
    else:
        fetch_topic_data(args.topic)
else:
    display_help()
