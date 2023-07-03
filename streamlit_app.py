import streamlit
import requests
import pandas as pd
import snowflake.connector
from urllib.error import URLError

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

def get_fruitvice_data(fruit):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


streamlit.header("Fruityvice Fruit Advice!")
try: 
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        streamlit.dataframe(get_fruitvice_data(fruit_choice))
except URLError as e:
    streamlit.error()

# streamlit.stop()

snowflake.connector.paramstyle = 'qmark'
conn = snowflake.connector.connect(**streamlit.secrets['snowflake'])

def get_fruit_load_list(conn=None):
    if not conn:
        raise BaseException('snowflake Connection is not provided.')
    with conn.cursor() as cur:
        cur.execute("SELECT * from fruit_load_list")
        return cur.fetchall()

def insert_fruit(fruit, conn=None):
    if not conn:
        raise BaseException('snowflake Connection is not provided.')
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO fruit_load_list VALUES (?)", 
            (add_fruit_choice,)
        )


streamlit.header("Fruit Load List contains:")

data = get_fruit_load_list(conn)
streamlit.dataframe(data)

add_fruit_choice = streamlit.text_input('What fruit would youlike to add?', None)
if streamlit.button('Add a Fruit to the List'):
    if not add_fruit_choice:
        streamlit.error("Please select a fruit to put in the list.")
    else:
        insert_fruit(add_fruit_choice, conn=conn)
        streamlit.write('Thanks for adding ', add_fruit_choice)
    
