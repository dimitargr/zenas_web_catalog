import streamlit as st
import snowflake.connector
import pandas

st.title('Zena\'s Amazing Athleisure Catalog')

# connect to snowflake
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()

# run a snowflake query and put it all in a var called my_catalog
my_cur.execute("select color_or_style from catalog_for_website")
my_catalog = my_cur.fetchall()

# put the dafta into a dataframe
df = pd.DataFrame(my_catalog, columns=['color_or_style'])

# temp write the dataframe to the page so I Can see what I am working with
# st.write(df)
# put the first column into a list
color_list = df['color_or_style'].tolist()

# Let's put a pick list here so they can pick the color
if 'choice_key' in st.session_state:
        if st.session_state['choice_key'] not in option_list: st.session_state['choice_key']='default'
        c_ind = plot_list.index(st.session_state['choice_key'])
else: c_ind = 0

option = st.session_state['choice_key'] = st.selectbox('Choice', option_list, index=c_ind)

#option = st.selectbox('Pick a sweatsuit color or style:', color_list)

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
