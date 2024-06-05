# 186.143 Information visualisation (UE 1,0) 2024S

## Group members 
- Sven Gerloff
- Bakir Bajrovic 

## Project description 
In this project, we created an interactive application using Python and Streamlit. The purpose of our app is to analyze 
hotel reviews using WordClouds to identify differences in the most common words between positive and negative reviews. 
To facilitate deeper analysis, we incorporated two sliders. These sliders allow users to filter hotels based on their 
ratings and the number of reviews. Additionally, users can filter hotels by district.

It consists of two main components:

- Data Preparation: (`data_prep.ipynb`) 
- Application:  (`app.py`) 

Source for the hotel reviews https://www.kaggle.com/datasets/jiashenliu/515k-hotel-reviews-data-in-europe [05.05.2024]

## Project Structure
```ruby
.
├── data 
    ├── hotels.csv         # Original data set
    ├── data_prepared.csv  # Prepared data
├── data_prep.ipynb        # Jupyter Notebook for data preparation
├── app.py                 # Main application
└── requirements.txt       # List of requirements
```

## Installation

1. Recommended: Create and activate a virtual environment
2. Install the necessary Python packages
```ruby
pip install -r requirements.txt
```
3. Start the app via the terminal
```ruby
streamlit run app.py
```

