import streamlit
import snowflake.connector
import pandas

streamlit.title('Zena\'s Amazing Athleisure Catalog')

# connect to snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

# run a snowflake query and put it all in a var called my_catalog
my_cur.execute("select color_or_style from catalog_for_website")
my_catalog = my_cur.fetchall()

# put the dafta into a dataframe
df = pandas.DataFrame(my_catalog)

# temp write the dataframe to the page so I Can see what I am working with
# streamlit.write(df)
# put the first column into a list
color_list = df[0].values.tolist()

# Let's put a pick list here so they can pick the color
option = streamlit.selectbox('Pick a sweatsuit color or style:', color_list)

# We'll build the image caption now, since we can
product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'

# Use the option selected to go back and get all the info from the database
query = """
SELECT direct_url, price, size_list, upsell_product_desc 
FROM catalog_for_website 
WHERE color_or_style = '{}';
""".format(option)
my_cur.execute(query)
df2 = my_cur.fetchone()

if df2:
    st.image(df2[0], width=400, caption=product_caption)
    st.write('Price: ', df2[1])
    st.write('Sizes Available: ', df2[2])
    st.write(df2[3])
else:
    st.write("No details found for the selected option.")
