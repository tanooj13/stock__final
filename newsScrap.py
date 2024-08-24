
import sys
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
from nltk.classify import NaiveBayesClassifier
import streamlit as st
from sklearn.externals import joblib
# To handle utf-8 encoding
sys.stdout.reconfigure(encoding='utf-8')


option = st.selectbox(
    "Select the stock:",
    ("Mobile phone","Google", "Microsoft"),
)
st.write("You selected:", option)

click = st.button("Click", type="primary")
# Initialize the WebDriver (Chrome)
headlines = []
def webscrap():
    driver = webdriver.Chrome()

    # List to store all the scraped headlines
    

    # Number of pages to scrape
    num_pages = 10
    
    # Start the loop for scraping multiple pages
    for i in range(0, num_pages * 10, 10):  
        driver.get(f"https://www.google.com/search?q={option}+stock+price&sca_esv=28194934ae825b70&sca_upv=1&rlz=1C1VDKB_en-GBIN1079IN1079&tbm=nws&ei=E0zJZpm8O8SG4-EP3fHfgQE&start={i}&sa=N&ved=2ahUKEwjZke_o0IyIAxVEwzgGHd34NxA4ChDy0wN6BAgCEAc&biw=1536&bih=776&dpr=1.25")

        try:
            # Wait for headlines to be present
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "n0jPhd"))
            )

            # Find all elements containing headlines
            elems = driver.find_elements(By.CLASS_NAME, "n0jPhd")

            print(f"{len(elems)} headlines found on page {i//10 + 1}")

            # Append each headline to the list
            for elem in elems:
                headline = elem.text
                headlines.append(headline)  
                print(f"Appended headline: {headline}")

        except Exception as e:
        
            # print(f"An error occurred on page {i//10 + 1}: {e}")
            break

    # To avoid bot detection
        time.sleep(4)


    driver.close()

    return headlines

if (click):
    headlines = webscrap()
else:st.write("Select a company")

# for idx, headline in enumerate(headlines, start=1):
#     print(f"{idx}: {headline}")

#Saving the headlines to a file 
# output_file = f"newsData/{query}_headlines.txt"
# os.makedirs("newsData", exist_ok=True)

# with open(output_file, 'w', encoding="utf-8") as f_out:
#     for headline in headlines:
#         f_out.write(headline + "\n")


# df = pd.DataFrame(headlines,columns=['Headlines'])
# df.to_csv(f'{query}.csv')


def preprocess_text(text):
    text=text.lower() #converting into lower case
    tokens=word_tokenize(text) #
    tokens=[word for word in tokens if word.isalpha() and word not in stop_word]
    return ' '.join(tokens)
def extract_features(words):
  return {word:True for word in words}

def modelling(headlines,option):

    with open('sentiment_model.pkl', 'rb') as f:
        classifier = joblib.load(f)

    df1 = pd.DataFrame(headlines,columns=['Headlines'])
    df1.drop('Unnamed: 0',axis = 1,inplace = True)
    preprocessed_texts = [preprocessed_text(text) for text in df1['Headlines']]

    features = [extract_features(text) for text in preprocessed_texts]

    predictions = [classifier.classify(feature) for feature in features]

    df1['predicted_sentiment'] = predictions

    df1['predicted_sentiment'] = df1['predicted_sentiment'].replace(4,1)

    sen = df1['predicted_sentiment'].mode()

    if (sen == 1):st.write('Positive')
    else:st.write('Negative')


# option = st.selectbox(
#     "Select the stock:",
#     ("Apple","Google", "Microsoft"),
# )
# st.write("You selected:", option)
modelling(headlines,option)









