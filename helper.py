from urlextract import URLExtract
from wordcloud import WordCloud
extract = URLExtract()
import pandas as pd
from collections import Counter
def fetch_stats(selected_Sender,df):

    if selected_Sender != "Overall":
        df = df[df["Sender"] == selected_Sender]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['Message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['Message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df["Message"]:
        links.extend(extract.find_urls(message))


    return num_messages, len(words), num_media_messages, len(links)


def most_busy_Senders(df):
    x = df['Sender'].value_counts().head()
    df = round((df['Sender'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'Sender': 'percent'})
    return x,df


def create_wordcloud(selected_Sender,df):
    if selected_Sender != 'Overall':
        df = df[df['Sender'] == selected_Sender]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['Message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_Sender,df):

    f = open('C:/Users/hp/Desktop/SIH/stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_Sender != 'Overall':
        df = df[df['Sender'] == selected_Sender]

    temp = df[df['Sender'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']

    words = []

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

