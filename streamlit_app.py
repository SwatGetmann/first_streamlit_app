import streamlit
import requests
import pandas as pd

streamlit.title("My Mom's New Healthy Diner")

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Bluberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.text_input(label="Enter your Healthy Food:", value="Kinky Carrot")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
fruit_list = fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits", 
                      options=fruit_list.index,
                      default=['Avocado', 'Strawberries'])
streamlit.dataframe(fruit_list.loc[fruits_selected])

streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)