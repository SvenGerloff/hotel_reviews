import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from wordcloud import WordCloud
import matplotlib.pyplot as plt


st.set_page_config(layout="wide")
col1, col2, col3 = st.columns([2,4,2])

df = pd.read_csv('./data/data_prepared.csv')


with col1:
    st.title('Vienna Hotel Map')
    districts = sorted(df['District'].dropna().unique())
    selected_district = st.selectbox('Select a district', ['All'] + [str(d) for d in districts])
    selected_max_words = st.selectbox('Select maximum number of words', [10, 15, 30, 50, 100])
    min_score, max_score = st.slider(
        'Select the rating range',
        min_value=0.0,
        max_value=10.0,
        value=(0.0, 10.0)
    )

    min_reviews, max_reviews = st.slider(
        'Select the review count range',
        min_value=int(df['Total_Number_of_Reviews'].min()),
        max_value=int(df['Total_Number_of_Reviews'].max()),
        value=(int(df['Total_Number_of_Reviews'].min()), int(df['Total_Number_of_Reviews'].max()))
    )

if selected_district != 'All':
    filtered_df = df[(df['Average_Score'] >= min_score) &
                             (df['Average_Score'] <= max_score) &
                             (df['Total_Number_of_Reviews'] >= min_reviews) &
                             (df['Total_Number_of_Reviews'] <= max_reviews) &
                             (df['District'] == int(selected_district))
                     ]
else:
    filtered_df = df[(df['Average_Score'] >= min_score) &
                             (df['Average_Score'] <= max_score)&
                             (df['Total_Number_of_Reviews'] >= min_reviews) &
                             (df['Total_Number_of_Reviews'] <= max_reviews)
                     ]

center_lat = df['lat'].mean()
center_lng = df['lng'].mean()

m = folium.Map(location=[center_lat, center_lng], zoom_start=12)

color_scale = folium.LinearColormap(['red', 'yellow', 'green'], vmin=min_score, vmax=max_score)

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
    color = color_scale(row['Average_Score'])

    folium.Marker(
        location=[row['lat'], row['lng']],
        popup=folium.Popup(popup_content, max_width=300),
        tooltip=tooltip_content,
        color=color
    ).add_to(m)

with col2:
    st_folium(m, width=1000, height=700)



with col3:
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
    plt.title('Word Cloud for Positive Reviews', fontsize=20,fontweight='bold')
    st.pyplot(plt)

    wordcloud_negative = WordCloud(background_color='white', colormap='Reds',max_words=selected_max_words).generate(negative_reviews_text)
    plt.figure()
    plt.imshow(wordcloud_negative, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud for Negative Reviews', fontsize=20,fontweight='bold')
    st.pyplot(plt)

