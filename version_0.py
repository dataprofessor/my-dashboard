import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Streamlit YouTube Channel Dashboard", layout="wide")

def load_data():
    data = pd.read_csv("youtube_channel_data.csv")
    data['DATE'] = pd.to_datetime(data['DATE'])
    data['NET_SUBSCRIBERS'] = data['SUBSCRIBERS_GAINED'] - data['SUBSCRIBERS_LOST']
    return data

df = load_data()

# Original
df1 = df[['DATE', 'NET_SUBSCRIBERS', 'VIEWS', 'WATCH_HOURS', 'LIKES']]

# Calculate row-wise cumulative sum
df2 = df1.copy()

for column in ['NET_SUBSCRIBERS', 'VIEWS', 'WATCH_HOURS', 'LIKES']:
    df2[column] = df2[column].cumsum()

def format_with_commas(number):
    return f"{number:,}"
    

st.title("Streamlit YouTube Channel Dashboard")

logo_icon = "images/streamlit-mark-color.png"
logo_image = "images/streamlit-logo-primary-colormark-lighttext.png"
st.logo(icon_image=logo_icon, image=logo_image)

with st.sidebar:
    st.header("⚙️ Settings")
    start_date = st.date_input("Start date", df['DATE'].min())
    end_date = st.date_input("End date", df['DATE'].max())

    time_frame = st.selectbox(
        "Select time frame",
        ("Daily", "Cumulative"),
    )


# Display key metrics (Total)
st.subheader("Key Metrics")

st.caption("All-Time Statistics")


col = st.columns(4)
with col[0]:
    with st.container(border=True):
        st.metric("Total Subscribers", format_with_commas((df['SUBSCRIBERS_GAINED'].sum() - df['SUBSCRIBERS_LOST'].sum())))
        if time_frame == 'Daily':
            df_subscribers = df1[["DATE", "NET_SUBSCRIBERS"]].set_index(df1.columns[0])
            st.area_chart(df_subscribers, color='#29b5e8', height=150)
            
        if time_frame == 'Cumulative':
            df_subscribers = df2[["DATE", "NET_SUBSCRIBERS"]].set_index(df2.columns[0])
            st.area_chart(df_subscribers, color='#29b5e8', height=150)

with col[1]:
    with st.container(border=True):
        st.metric("Total Views", format_with_commas(df['VIEWS'].sum()))

        if time_frame == 'Daily':
            df_views = df1[["DATE", "VIEWS"]].set_index(df1.columns[0])
            st.area_chart(df_views, color='#FF9F36', height=150)

        if time_frame == 'Cumulative':
            df_views = df2[["DATE", "VIEWS"]].set_index(df2.columns[0])
            st.area_chart(df_views, color='#FF9F36', height=150)

with col[2]:
    with st.container(border=True):
        st.metric("Total Watch Hours", format_with_commas((df['WATCH_HOURS'].sum())))

        if time_frame == 'Daily':
            df_views = df1[["DATE", "WATCH_HOURS"]].set_index(df1.columns[0])
            st.area_chart(df_views, color='#D45B90', height=150)

        if time_frame == 'Cumulative':
            df_views = df2[["DATE", "WATCH_HOURS"]].set_index(df2.columns[0])
            st.area_chart(df_views, color='#D45B90', height=150)
        
with col[3]:
    with st.container(border=True):
        st.metric("Total Likes", format_with_commas(df['LIKES'].sum()))

        if time_frame == 'Daily':
            df_views = df1[["DATE", "LIKES"]].set_index(df1.columns[0])
            st.area_chart(df_views, color='#7D44CF', height=150)
            
        if time_frame == 'Cumulative':
            df_views = df2[["DATE", "LIKES"]].set_index(df2.columns[0])
            st.area_chart(df_views, color='#7D44CF', height=150)


# Display key metrics (Selected Duration)
st.caption("Selected Duration")

if time_frame == 'Daily':
    mask = (df1['DATE'].dt.date >= start_date) & (df1['DATE'].dt.date <= end_date)
    filtered_df = df1.loc[mask]
    
if time_frame == 'Cumulative':
    mask = (df2['DATE'].dt.date >= start_date) & (df2['DATE'].dt.date <= end_date)
    filtered_df = df2.loc[mask]

cols = st.columns(4)
with cols[0]:
    with st.container(border=True):
        st.metric("Subscribers", format_with_commas(filtered_df['NET_SUBSCRIBERS'].sum()))

        df_subscribers_duration = filtered_df[["DATE", "NET_SUBSCRIBERS"]].set_index(filtered_df.columns[0])
        st.area_chart(df_subscribers_duration, color='#7D44CF', height=150)

with cols[1]:
    with st.container(border=True):
        st.metric("Views", format_with_commas(filtered_df['VIEWS'].sum()))

        df_views_duration = filtered_df[["DATE", "VIEWS"]].set_index(filtered_df.columns[0])
        st.area_chart(df_views_duration, color='#D45B90', height=150)

with cols[2]:
    with st.container(border=True):
        st.metric("Watch Hours", format_with_commas(round(filtered_df['WATCH_HOURS'].sum(), 2)))

        df_watch_hours_duration = filtered_df[["DATE", "WATCH_HOURS"]].set_index(filtered_df.columns[0])
        st.area_chart(df_watch_hours_duration, color='#FF9F36', height=150)

with cols[3]:
    with st.container(border=True):
        st.metric("Likes", format_with_commas(filtered_df['LIKES'].sum()))

        df_likes_duration = filtered_df[["DATE", "LIKES"]].set_index(filtered_df.columns[0])
        st.area_chart(df_likes_duration, color='#29b5e8', height=150)


with st.expander("See DataFrame"):
    st.dataframe(df)
