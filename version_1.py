import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Streamlit YouTube Channel Dashboard", layout="wide")

@st.cache_data
def load_data():
    data = pd.read_csv("youtube_channel_data.csv")
    data['DATE'] = pd.to_datetime(data['DATE'])
    data['NET_SUBSCRIBERS'] = data['SUBSCRIBERS_GAINED'] - data['SUBSCRIBERS_LOST']
    return data

def format_with_commas(number):
    return f"{number:,}"

def create_metric_chart(df, column, color, height=150):
    chart_df = df[["DATE", column]].set_index("DATE")
    return st.area_chart(chart_df, color=color, height=height)

def display_metric(col, title, value, df, column, color):
    with col:
        with st.container(border=True):
            st.metric(title, format_with_commas(value))
            create_metric_chart(df, column, color)

# Load data
df = load_data()
df_cumulative = df.copy()
for column in ['NET_SUBSCRIBERS', 'VIEWS', 'WATCH_HOURS', 'LIKES']:
    df_cumulative[column] = df_cumulative[column].cumsum()

# Set up the dashboard
st.title("Streamlit YouTube Channel Dashboard")

logo_icon = "images/streamlit-mark-color.png"
logo_image = "images/streamlit-logo-primary-colormark-lighttext.png"
st.logo(icon_image=logo_icon, image=logo_image)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    start_date = st.date_input("Start date", df['DATE'].min())
    end_date = st.date_input("End date", df['DATE'].max())
    time_frame = st.selectbox("Select time frame", ("Daily", "Cumulative"))

# Key Metrics
st.subheader("Key Metrics")
st.caption("All-Time Statistics")

metrics = [
    ("Total Subscribers", "NET_SUBSCRIBERS", '#29b5e8'),
    ("Total Views", "VIEWS", '#FF9F36'),
    ("Total Watch Hours", "WATCH_HOURS", '#D45B90'),
    ("Total Likes", "LIKES", '#7D44CF')
]

cols = st.columns(4)
for col, (title, column, color) in zip(cols, metrics):
    display_metric(col, title, df[column].sum(), 
                   df_cumulative if time_frame == "Cumulative" else df, 
                   column, color)

# Selected Duration Metrics
st.caption("Selected Duration")
df_filtered = df_cumulative if time_frame == "Cumulative" else df
mask = (df_filtered['DATE'].dt.date >= start_date) & (df_filtered['DATE'].dt.date <= end_date)
df_filtered = df_filtered.loc[mask]

cols = st.columns(4)
for col, (title, column, color) in zip(cols, metrics):
    display_metric(col, title.split()[-1], df_filtered[column].sum(), 
                   df_filtered, column, color)

# DataFrame display
with st.expander("See DataFrame"):
    st.dataframe(df)
