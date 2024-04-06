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

    df['Sender'] = names
    df['Message'] = messages

    df['Only_Date'] = df['Date'].dt.date
    df['Year'] = df['Date'].dt.year  # Extract year component
    df['Month_num'] = df['Date'].dt.month
    df["Month"] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day
    df['Day_Name'] = df['Date'].dt.day_name()
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    period = []
    for hour in df[['Day_Name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
