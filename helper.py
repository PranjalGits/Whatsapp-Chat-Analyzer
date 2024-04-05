from urlextract import URLExtract
from wordcloud import WordCloud
extract = URLExtract()
import pandas as pd
from collections import Counter
import emoji
import emoji_data_python
import regex
import matplotlib.pyplot as plt
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

    f = open('C:/Users/hp/Desktop/SIH/stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_Sender != 'Overall':
        df = df[df['Sender'] == selected_Sender]

    temp = df[df['Sender'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['Message'] = temp['Message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Message'].str.cat(sep=" "))
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

def emoji_analysis(selected_Sender, df):
    if selected_Sender != 'Overall':
        df = df[df['Sender'] == selected_Sender]

    # Extract emojis from messages
    emojis = []
    for message in df['Message']:
        emojis.extend(c for c in message if c in emoji.emoji_count)

    # Count frequency of each emoji
    emoji_counter = Counter(emojis)

    # Convert emoji_counter to DataFrame
    emoji_df = pd.DataFrame.from_dict(emoji_counter, orient='index', columns=['Frequency'])

    # Sort DataFrame by frequency
    emoji_df = emoji_df.sort_values(by='Frequency', ascending=False)

    return emoji_df

def plot_emoji_analysis(emoji_df):
    fig, ax = plt.subplots()
    emoji_df.head(10).plot(kind='bar', ax=ax)
    ax.set_title('Top 10 Most Used Emojis')
    ax.set_xlabel('Emoji')
    ax.set_ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig






