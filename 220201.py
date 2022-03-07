import streamlit as st
import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


with open("220201.csv", 'r') as f:
    data = f.readlines()
    print(data)
    # with の次には、open によってファイルをオープンする式を書きます。
    # また、as の次には、ファイルのオブジェクトが格納される変数を書きます。
    # with文は処理後にファイルのクローズを自動的にやってくれますので、 ファイルに対して close() を呼び出す必要がありません。

    # f.readlines()はテキストファイルの中身を改行文字で区切って一行ずつに分割して、リストとしてデータを返します。
    # data1 = [data.strip() for x in data.split(',') if not data.strip]

file = io.StringIO()
file.write("水温,X,DO,時間,水温2,X2,DO2,時間2\n")

for log_line in data:
    file.write(log_line)
    file.write("\n")
file.seek(0)

df = pd.read_table(file, sep = ',')
# change1_df = df.drop(columns=['X', 'X2'])


df['DO'] = df['DO'].astype(str).str.replace('D', "")
df['DO2'] = df['DO2'].astype(str).str.replace('D', "")
df['水温'] = df['水温'].astype(str).str.replace('W', "")
df['水温2'] = df['水温2'].astype(str).str.replace('W', "")

df['DO'] = df['DO'].astype(float)
df['DO2'] = df['DO2'].astype(float)
df['水温'] = df['水温'].astype(float)
df['水温2'] = df['水温2'].astype(float)

# fig = ff.create_table(df)
ST = st.dataframe(df)

fig = go.Figure()
layout = go.Layout(showlegend =True)
fig.update_layout(title=dict(text='<b>DOと水温',
                             font=dict(size=26,
                                       color='grey')))

fig.update_layout(yaxis=dict(side='left',title='水温', range=(8.2, 9.6)),
                  yaxis2=dict(side='right', title='DO', range=(0, 50), overlaying='y'))


yaxis = dict(title='normalized stock price')

fig.add_trace(go.Scatter(x=df['時間'],
                         y=df['水温'],
                         mode='lines',
                         name='水温',
                         yaxis = 'y1', line=dict(color="#00008b")),
              )
fig.add_trace(go.Scatter(x=df['時間'],
                         y=df['DO'],
                         mode='lines',
                         name='DO',
                         yaxis = 'y2', line=dict(color="#ffa500")),
              )
fig.add_trace(go.Scatter(x=df['時間'],
                         y=df['DO2'],
                         mode='lines',
                         name='DO2',
                         yaxis = 'y2', line=dict(color="#fffacd")),
              )
fig.add_trace(go.Scatter(x=df['時間'],
                         y=df['水温2'],
                         mode='lines',
                         name='水温2',
                         yaxis = 'y1', line=dict(color="#708090")),
              )

fig.show()
