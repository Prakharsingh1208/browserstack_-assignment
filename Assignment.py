import urllib.request
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from googletrans import  Translator
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


translator = Translator()

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://elpais.com/")

language = driver.find_element(By.TAG_NAME,"html")
lan = language.get_attribute("lang")

try:
    cookie = WebDriverWait(driver,15,0.5).until(EC.visibility_of_element_located((By.XPATH,"//button[@id='didomi-notice-agree-button']")))
    cookie.click()
except Exception as e:
    print("Cookie not found")

if lan == 'es-ES':
    print("Website's text is displayed in Spanish")
else:
    print("Website is not displayed in Spanish")

driver.find_element(By.XPATH,"(//a[@data-mrf-link='https://elpais.com/opinion/'])[1]").click()

articles = driver.find_elements(By.TAG_NAME,"article")[:5]


counter=1
translated_title = []
translated_content = []

for article in articles:
    title_element = article.find_element(By.TAG_NAME,"h2")
    title = title_element.text
    content_element = article.find_element(By.TAG_NAME,'p')
    content = content_element.text
    translated_title.append(translator.translate(title).text)
    translated_content.append(translator.translate(content).text)

    print(f"------------------Aritcle {counter}------------------")
    print(f"Title: {title}")
    print(f"Content: {content}")
    print(f"-----Trying to find the cover images-----")
    try:
        image = article.find_element(By.TAG_NAME,"img")
        image_url=image.get_attribute("src")
        urllib.request.urlretrieve(image_url,f"Cover_image{counter}.jpg")
        print("Cover image saved")
    except Exception:
        print("No cover image found")
    counter += 1



print("----------------------------------English Version----------------------------------")
for i in range(counter-1):
    print(f"------------------Aritcle {i + 1}------------------")
    print(f"Title: {translated_title[i]}")
    print(f"Content: {translated_content[i]}")


all_words = []
repeated_words = []
count_of_repeated_words=[]
for title in translated_title:
    words = title.lower().split()
    all_words.extend(words)

element_count = Counter(all_words)

for word, count in element_count.items():
    if count > 2:
        repeated_words.append(word)
        count_of_repeated_words.append(count)

print("-----------------Finding the repeated words-----------------")
for i in range(len(repeated_words)):
    print(f"Word '{repeated_words[i]}' found {count_of_repeated_words[i]} times")
