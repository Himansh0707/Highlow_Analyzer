import streamlit as st
import pandas as pd
import io

# Title
st.title("📈 Daily & Weekly High/Low Session Analyzer")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Clean & prepare dataframe
    df = df[['time', 'open', 'high', 'low', 'close']].copy()
    df['time'] = pd.to_datetime(df['time'])
    df['date'] = df['time'].dt.date
    df['hour'] = df['time'].dt.hour
    df['weekday'] = df['time'].dt.day_name()

    def get_session(hour):
        if 3 <= hour < 9:
            return 'Asia'
        elif 9 <= hour < 15:
            return 'London'
        elif 15 <= hour < 21:
            return 'New York'
        else:
            return 'Off Hours'

    df['session'] = df['hour'].apply(get_session)

    st.subheader("Data Preview")
    st.dataframe(df.head(20))

    # ----------- DAILY HIGH/LOW SESSION DISTRIBUTION -----------
    st.header("📊 Daily High/Low Session Distribution")

    daily_highs = df.loc[df.groupby('date')['high'].idxmax()]
    daily_lows = df.loc[df.groupby('date')['low'].idxmin()]

    high_session_counts = daily_highs['session'].value_counts()
    low_session_counts = daily_lows['session'].value_counts()

    st.subheader("High Made in Session")
    st.bar_chart(high_session_counts)

    st.subheader("Low Made in Session")
    st.bar_chart(low_session_counts)

    # ----------- WEEKLY HIGH/LOW WEEKDAY DISTRIBUTION -----------
    st.header("🗓️ Weekly High/Low Weekday Distribution")

    df['week'] = df['time'].dt.to_period('W').apply(lambda r: r.start_time)

    weekly_highs = df.loc[df.groupby('week')['high'].idxmax()]
    weekly_lows = df.loc[df.groupby('week')['low'].idxmin()]

    high_weekday_counts = weekly_highs['weekday'].value_counts()
    low_weekday_counts = weekly_lows['weekday'].value_counts()

    st.subheader("Weekly High Made on Day")
    st.bar_chart(high_weekday_counts)

    st.subheader("Weekly Low Made on Day")
    st.bar_chart(low_weekday_counts)

    # Optional: Show raw weekly high/low rows
    with st.expander("See raw weekly high/low rows"):
        st.write("Weekly Highs")
        st.dataframe(weekly_highs[['time', 'high', 'weekday']])
        st.write("Weekly Lows")
        st.dataframe(weekly_lows[['time', 'low', 'weekday']])
