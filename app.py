import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a File ")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocess(data)
    # st.dataframe(df)
    st.title("Top Statistics")
    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show Analysis wrt ", user_list)
    if st.sidebar.button("Show Analysis "):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(
            selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.subheader("Total Messages")
            st.title(num_messages)
        with col2:
            st.subheader("Total Words")
            st.title(words)
        with col3:
            st.subheader("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.subheader("Total Links")
            st.title(num_links)
    # Monthly timeline
    st.title("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'], color='green')
    plt.xticks(rotation="vertical")
    st.pyplot(fig)

    # Daily Timeline
    st.title("Daily Timeline")
    dailytimeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(dailytimeline['only_date'],
            dailytimeline['message'], color='green')
    plt.xticks(rotation="vertical")
    st.pyplot(fig)

    # Activity Map
    st.title("Activity Map")
    col1, col2 = st.columns(2)
    with col1:
        st.header("Most Busy Day")
        busy_day = helper.week_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values)
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
    with col2:
        st.header("Most Busy Month")
        busy_month = helper.month_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values, color='orange')
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
    # Heat Map
    st.title("Weekly Activity Map ")
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig, ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)

    # finding the Busy Users in the group("Group Level")
    if(selected_user == "Overall"):
        st.title("Most Busy Users")
        x, new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    # WordCloud

    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.title("Word Cloud")
    st.pyplot(fig)

    # Most Common Words
    most_common_df = helper.most_common_words(selected_user, df)
    fig, ax = plt.subplots()
    ax.barh(most_common_df[0], most_common_df[1])
    plt.xticks(rotation='vertical')
    st.title("Most Common Words")
    st.pyplot(fig)

    # emoji Analysis

    emoji_df = helper.emoji_helper(selected_user, df)
    st.title("Emoji Analysis")
    try:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(),
                   labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
    except:
        pass
