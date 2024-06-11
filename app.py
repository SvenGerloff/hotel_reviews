import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# set page configuration to wide
st.set_page_config(layout="wide")


# put title at the top
st.title('Vienna Hotel Map')

# define columns on the screen to put map and word clouds in
col1, col2 = st.columns([2,1])


# read the preprocessed data
df = pd.read_csv('./data/data_prepared.csv')




# sidebar for filters
st.sidebar.title('Filters')
search_hotel = st.sidebar.text_input('Search for a hotel by name')
districts = sorted(df['District'].dropna().unique())
selected_district = st.sidebar.selectbox('Select a district', ['All'] + [str(d) for d in districts])
selected_max_words = st.sidebar.selectbox('Select maximum number of words', [10, 15, 30, 50, 100])
min_score, max_score = st.sidebar.slider(
    'Select the rating range',
    min_value=0.0,
    max_value=10.0,
    value=(0.0, 10.0)
)
min_reviews, max_reviews = st.sidebar.slider(
    'Select the review count range',
    min_value=int(df['Total_Number_of_Reviews'].min()),
    max_value=int(df['Total_Number_of_Reviews'].max()),
    value=(int(df['Total_Number_of_Reviews'].min()), int(df['Total_Number_of_Reviews'].max()))
)

# applying selected filters
filtered_df = df

if search_hotel:
    filtered_df = filtered_df[filtered_df['Hotel_Name'].str.contains(search_hotel, case=False, na=False)]

if selected_district != 'All':
    filtered_df = filtered_df[filtered_df['District'] == int(selected_district)]

filtered_df = filtered_df[
    (filtered_df['Average_Score'] >= min_score) &
    (filtered_df['Average_Score'] <= max_score) &
    (filtered_df['Total_Number_of_Reviews'] >= min_reviews) &
    (filtered_df['Total_Number_of_Reviews'] <= max_reviews)
]

center_lat = df['lat'].mean()
center_lng = df['lng'].mean()

# drawing map
m = folium.Map(location=[center_lat, center_lng], zoom_start=12, tiles='CartoDB positron', attr='Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.')

# hotel info
for idx, row in filtered_df.iterrows():
    popup_content = f"""
    <div style="font-size: 16px;">
        <strong>Hotel:</strong> {row['Hotel_Name']}<br>
        <strong>District:</strong> {row['District']} <br>
        <strong>Average Score:</strong> {row['Average_Score']}<br>
        <strong>Number of Reviews:</strong> {row['Total_Number_of_Reviews']}
    </div>
    """
    tooltip_content = f"""
    <div style="font-size: 14px;">
        {row['Hotel_Name']}
    </div>
    """

    folium.Marker(
        location=[row['lat'], row['lng']],
        popup=folium.Popup(popup_content, max_width=300),
        tooltip=tooltip_content,
        icon=folium.Icon(color='blue') 
    ).add_to(m)

# putting map in column 1 on the screen
with col1:
    st_folium(m, width=1000, height=700)

# putting word clouds on the right side of the map
with col2:
    if filtered_df.empty:
        positive_reviews_text = "Empty"
        negative_reviews_text = "Empty"
    else:
        positive_reviews_text = str(filtered_df['Positive_Review'])
        negative_reviews_text = str(filtered_df['Negative_Review'])

    wordcloud_positive = WordCloud(background_color='white', colormap='Greens', max_words=selected_max_words).generate(positive_reviews_text)
    plt.figure()
    plt.imshow(wordcloud_positive, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud for Positive Reviews', fontsize=20, color='#283c5f', fontweight='bold')
    st.pyplot(plt)

    wordcloud_negative = WordCloud(background_color='white', colormap='Reds', max_words=selected_max_words).generate(negative_reviews_text)
    plt.figure()
    plt.imshow(wordcloud_negative, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud for Negative Reviews', fontsize=20, color='#283c5f', fontweight='bold')
    st.pyplot(plt)

