import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pyautogui

url = 'https://www.monkeytype.com/'
# Initialize the browser
browser = webdriver.Chrome()
browser.get(url)

# Wait for the initial content to load
time.sleep(10)

# Initialize the last typed word index
last_index = 0

# Function to extract and type new words
def type_new_words():
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    words_div = soup.find('div', id='words')

    if words_div:
        words = words_div.find_all('div', class_='word')  # Adjust this selector as needed
        new_words_to_type = []

        for word in words:
            letter_tags = word.find_all('letter')
            if all('correct' in letter_tag.get('class', []) for letter_tag in letter_tags):
                continue  # Skip words that have been typed correctly

            word_text = ''.join(letter_tag.text.strip() for letter_tag in letter_tags)
            if word_text:
                new_words_to_type.append(word_text)

        if new_words_to_type:
            string_to_type = ' '.join(new_words_to_type)
            pyautogui.write(string_to_type + ' ', interval=0.02)

# Continuously check for new words and type them
try:
    while True:
        type_new_words()
        time.sleep(0.01)  # Adjust the sleep time as needed
except KeyboardInterrupt:
    print("Script stopped by user.")

# Close the browser after the script is stopped
browser.quit()
