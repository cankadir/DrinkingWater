#%%
import pandas as pd
import numpy as np
import plotly.graph_objects as go

df = pd.read_excel( r"C:\Users\csucuogl\Dropbox\CCR_waterQuality_contest\data\Dataset_1_Bad.xlsx" )

df.head(5)

#%%

plot_blue = '#5DA7FF'
plot_red = '#F47A4E'

#%%
import os

for i,r in df.iterrows():

    cont = r['SUBSTANCE ']
    treshold = r['MCL [MRDL] Action level']
    goal = r['PHG [MCLG] Goal']

    
    level = r[r.index[ r.index.str.contains('average ')] ]

    level = level.to_frame()
    level.columns = ['value']
    level['date'] = [n.split(' ')[1] for n,row in level.iterrows()]

    fig = go.Figure()

    fig.add_trace( #Line Chart
        go.Scatter(
            x = level['date'],
            y = level['value'],
            mode = 'markers+lines',
            hovertemplate = 'Average <b>' + cont + '</b> level<br>in %{x} was %{y}<extra></extra>',
            marker = dict(
                color=plot_blue,
                size = 7
                ),
            line = dict(
                color=plot_blue,
                width = 2
            )
        )
    )

    fig.add_trace( #Treshold
        go.Scatter(
            x = level['date'],
            y = [treshold for m in range(len(level))],
            mode = 'lines',
            line = dict(
                color= '#878787',
                width = 3,
                dash='dash'
            )
        )
    )

    fig.add_trace( #Goal
        go.Scatter(
            x = level['date'],
            y = [goal for m in range(len(level))],
            mode = 'lines',
            line = dict(
                color= '#B7B4AC',
                width = 3,
                dash='dash'
            )
        )
    )

    fig.update_layout(
        width=550,
        height=350,
        plot_bgcolor='white',
        paper_bgcolor='white' ,
        showlegend = False,
        margin = dict(t=5,l=5,r=5,b=5),
        hoverlabel=dict(
            bgcolor="white",
            font_size=11,
            ),
        xaxis = dict(
            nticks=4
            ),
    ) 

    fig.add_annotation(text="EPA Standard",
                  x=2018.7, y=treshold+0.5, showarrow=False,align='left',
                  font=dict(
                    size=12,
                    color="#F47A4E"
                    ),
                  )
    fig.add_annotation(text="EPA Goals",
                x=2018.75, y=goal+0.5, showarrow=False,align='left',
                font=dict(
                size=12,
                color=" #F4A74E"
                ),
                )

    fig.update_yaxes(showgrid=True, gridwidth=0.05, gridcolor = '#e2e1dd' )
    fig.update_xaxes(showgrid=False)

    folder = 'C:/Users/csucuogl/Documents/GitHub/DrinkingWater/visuals/materials/'
    fig.write_html( os.path.join(folder , cont+'.html') )

    fig.show()


# %%
