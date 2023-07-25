# Import required libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import chain

# Function to scrape data from a given URL and extract specified classes
def scrape_data(url, selected_classes):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {}

        for class_name in selected_classes:
            elements = soup.find_all(class_=class_name)
            data[class_name] = [elem.text.strip() for elem in elements]

        return data

    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to get available classes from the provided URL
def get_available_classes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        classes = set(chain.from_iterable(elem.get("class") for elem in soup.find_all(class_=True) if elem.get("class")))
        return list(classes)

    except Exception as e:
        st.error(f"Error fetching available classes: {e}")
        return []

# Introduction section
def introduction():
    st.title("Web Scraping App")
    st.write("Welcome to the Web Scraping App! This app allows you to extract data from web pages "
             "by specifying the URL and selecting HTML classes to scrape. No coding skills required!")

# About section
def about():
    st.header("About")
    st.write("Web scraping is a technique used to extract data from websites. This app simplifies the process "
             "and lets you scrape data easily. It uses the BeautifulSoup library for parsing HTML content and "
             "provides a user-friendly interface powered by Streamlit.")

# How it works section
def how_it_works():
    st.header("How It Works")
    st.write("1. Enter the URL of the website you want to scrape data from in the text box above.")
    st.write("2. The app will fetch the available classes from the provided URL and display them as options.")
    st.write("3. Select the classes you want to scrape data from using the multi-select dropdown.")
    st.write("4. Click the 'Scrape' button to extract the data from the selected classes.")
    st.write("5. The scraped data will be displayed in a table below.")
    st.write("6. You can download the scraped data as a CSV file using the 'Download CSV' button.")

# Tips section
def tips():
    st.header("Tips for Successful Scraping")
    st.write("1. Make sure you have proper permissions to scrape data from the website.")
    st.write("2. Respect the website's terms of service and robots.txt file.")
    st.write("3. Be considerate of the website's resources and avoid aggressive scraping.")
    st.write("4. Test the app with different websites to ensure it works as expected.")
    st.write("5. Regularly check and update the scraping code, as website structures may change.")

# Streamlit web app
def main():
    introduction()
    st.write("----")
    about()
    st.write("----")
    how_it_works()
    st.write("----")
    tips()
    st.write("----")

    # User input: URL and classes to scrape
    st.write("Enter the URL of the website and select the classes to scrape.")
    url = st.text_input("URL:")
    available_classes = get_available_classes(url)
    selected_classes = st.multiselect("Select classes to scrape:", available_classes)

    if st.button("Scrape"):
        if url and selected_classes:
            data = scrape_data(url, selected_classes)

            if data:
                # Convert data to a DataFrame and create a CSV file
                df = pd.DataFrame(data)
                st.dataframe(df)

                # Create and download CSV file
                csv_file = df.to_csv(index=False)
                st.download_button(label="Download CSV", data=csv_file, file_name="scraped_data.csv", mime="text/csv",key="csv-download")
            else:
                st.warning("No data scraped.")
        else:
            st.warning("Please enter a valid URL and select at least one class.")

if __name__ == "__main__":
    main()
