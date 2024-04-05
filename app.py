import streamlit as st
import preproccessor,helper
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Upload WhatsApp chat text file", type=['txt'])
if uploaded_file is not None:
    file_path = "C:/Users/hp/Desktop/SIH/WhatsApp Chat with Oshak Agarwal.txt"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    df = preproccessor.preprocess(file_path)

    # Format 'Year' column to remove commas
    df['Year'] = df['Year'].astype(str).str.replace(',', '')

    st.dataframe(df)

    # fetch unique Sender
    Sender_list = df['Sender'].unique().tolist()
    Sender_list.sort()
    Sender_list.insert(0,"Overall")

    selected_sender = st.sidebar.selectbox("Show Analysis With Respect to",Sender_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_sender,df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # finding the busiest Senders in the group(Group Level)

        if selected_sender == "Overall":
            st.title('Most Busy Senders')
            x, new_df = helper.most_busy_Senders(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_sender,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words :
        most_common_df = helper.most_common_words(selected_sender, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most Commmon Words')
        st.pyplot(fig)





