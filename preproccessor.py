import re
import pandas as pd

def preprocess(file_path):
    dates = []
    names = []
    messages = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Regex pattern to match the date-time format and sender's name
            pattern = r'^(\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\s[AP]M)\s-\s(.+?):\s(.*)$'
            match = re.match(pattern, line)
            if match:
                dates.append(pd.to_datetime(match.group(1), format='%m/%d/%y, %I:%M %p'))
                names.append(match.group(2))
                messages.append(match.group(3))
    data = {'Date': dates, 'Sender': names, 'Message': messages}
    df = pd.DataFrame(data)

    df['Year'] = df['Date'].dt.year  # Extract year component
    df["Month"] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    return df
