# Import required libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

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
        classes = set(elem.get("class") for elem in soup.find_all(class_=True))
        return [cls for cls in classes if cls]

    except Exception as e:
        st.error(f"Error fetching available classes: {e}")
        return []




# Streamlit web app
def main():
    st.title("Web Scraping App")
    st.write("Enter the URL of the website and select the classes to scrape.")

    # User input: URL and classes to scrape
    url = st.text_input("Enter the URL")
    selected_classes = st.multiselect("Select classes to scrape", [])

    if st.button("Scrape"):
        if url and selected_classes:
            data = scrape_data(url, selected_classes)

            if data:
                # Convert data to a DataFrame and create a CSV file
                df = pd.DataFrame(data)
                st.dataframe(df)

                # Create and download CSV file
                csv_file = df.to_csv(index=False)
                st.download_button(label="Download CSV", data=csv_file, file_name="scraped_data.csv", mime="text/csv")
            else:
                st.warning("No data scraped.")
        else:
            st.warning("Please enter a valid URL and select at least one class.")

if __name__ == "__main__":
    main()
