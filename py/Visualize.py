
#%% IMPORT
import pandas as pd
import numpy as np

df = pd.read_csv( 'https://raw.githubusercontent.com/PrattSAVI/SafeWater/master/data/Seatlle_data.csv')

df
# %% Clean Data

df['range_min'] = [r.split(' to ')[0] if 'to' in r else None for i,r in df['Range'].iteritems() ]
df['range_max'] = [r.split(' to ')[1] if 'to' in r else None for i,r in df['Range'].iteritems()]

df['Average'] = df['Average'].replace('ND',0)
df['Range'] = df['Range'].replace('ND',0)

df
#%% Replace Values

df['mclg'] = df['mclg'].replace('MRDLG=4','4')
df['mcl'] = df['mcl'].replace('MRDL=4','4')
df['Average'] = df['Average'].astype(float)
df['range_min'] = df['range_min'].astype(float)
df['range_max'] = df['range_max'].astype(float)

df
# %% Float

df = df[ df['mcl']!='TT'].copy()
df['mclg'] = df['mclg'].astype(float)
df['mcl'] = df['mcl'].astype(float)
df
# %% Final Value
# Negative values mean the value is below the threshold
df['a1'] = df['Average'] - df['mcl'] 
df['a2'] = (df['a1'] / df['mcl'] ) * 100

df

#%% Graph
import random
df['a3'] = [random.randint(-100,100)/100 for i in range(len(df)) ]

import plotly.graph_objects as go

dfn = df[ df['a3']<0]
dfp = df[ df['a3']>=0]

fig = go.Figure()
fig.add_trace( #Negative
    go.Bar(
        x= dfn['contaminate'],
        y= dfn['a3'],
        text = dfn['Cause'],
        hovertemplate = '<b>%{x}</b><br>%{text}<extra></extra>',
        marker_color='white'
        
        )
    )

fig.add_trace( #Positive
    go.Bar(
        x= dfp['contaminate'],
        y= dfp['a3'],
        text = dfp['Cause'],
        hovertemplate = '<b>%{x}</b><br>%{text}<extra></extra>',
        marker_color='#ED6A5A'
        )
    )

fig.update_layout(
    width=550,
    height=350,
    plot_bgcolor='#BEE9E8',
    paper_bgcolor='#BEE9E8',
    showlegend = False,
    margin = dict(t=5,l=5,r=0,b=0)
    )

fig.update_layout(
    xaxis = dict(
        showticklabels=False),
    yaxis=dict(color="white")
    )   
fig.update_layout(yaxis_tickformat = '%')

fig.write_html( r"C:\Users\csucuogl\Documents\GitHub\SafeWater\visuals\bar_graph.html")
fig.show( config = dict(displayModeBar= False))


# %% Timeline Fake

dft = pd.DataFrame( index = df['contaminate'] )

dft['2000'] = [random.randint(-100,100) for i in range(len(df))]
dft['2005'] = [random.randint(-100,100) for i in range(len(df))]
dft['2010'] = [random.randint(-100,100) for i in range(len(df))]
dft['2015'] = [random.randint(-100,100) for i in range(len(df))]
dft['2020'] = [random.randint(-100,100) for i in range(len(df))]
dft['2025'] = [random.randint(-100,100) for i in range(len(df))]


dft = dft.transpose()
dft

# %%

for c in dft.columns:

    
    fig = go.Figure(
        data=go.Scatter(
            x=dft.index,
            y=dft[c],
            mode='lines'
            )
        )

    fig.update_layout(
    width=350,
    height=250,
    plot_bgcolor='#BEE9E8',
    paper_bgcolor='#BEE9E8',
    showlegend = False,
    margin = dict(t=5,l=5,r=0,b=0)
    )

    fig.update_layout(
        xaxis = dict(showticklabels=False),
        yaxis=dict( showticklabels=False )
        )   

    fig.show()


    break


# %%
