# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

conn = st.connection("snowflake")
session = conn.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

ingredients_list = st.multiselect("Choose up to 5 ingredients:", my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = " ".join(ingredients_list)
    #my_insert_stmt = """ insert into smoothies.public.orders(name_on_order, ingredients)
    #        values ('""" + name_on_order + "','" + ingredients_string + """')"""

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        #session.sql(my_insert_stmt).collect()
        session.sql("insert into smoothies.public.orders(name_on_order, ingredients) values (?, ?)", params=[name_on_order, ingredients_string]).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon='✅')
