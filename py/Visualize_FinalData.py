
#%% IMPORT
import pandas as pd
import numpy as np
import plotly.graph_objects as go

#Bad Data
df = pd.read_excel( r"C:\Users\csucuogl\Dropbox\CCR_waterQuality_contest\data\Dataset_1_Bad.xlsx" )
#Good Data
df = pd.read_excel( r"C:\Users\csucuogl\Dropbox\CCR_waterQuality_contest\data\Dataset_2_Good_NYC_2.xlsx" )

df.head(5)


#%%

plot_blue = '#5DA7FF'
plot_red = '#F47A4E'

new_text = []
for i,r in df['TYPICAL SOURCE'].iteritems():

    if not pd.isna( r ):
        t = 5
        text = r.split(' ')
        while t < len( text ):
            text.insert(t, '<br>')
            t += (5+1)
        new_text.append( ' '.join( text ) )
    else:
        new_text.append( None )

df['source'] = new_text

df.head(5)

# %% BAR CHART - VERTICAL

height = 650
width = 400

fig = go.Figure()

df_below = df[ df['n_average']<=0 ]
df_above = df[ df['n_average']>0 ]

fig.add_trace( #Below Threshold - POINT
    go.Scatter(
        y=df_below['SUBSTANCE '],
        x=df_below['n_average'],
        mode = 'markers',
        text = df_below['source'].replace(' <br> ' , "<br>" , regex = True),
        customdata = df_below['Average Level'], 
        hovertemplate = '<b>%{y}</b><br>%{text}<br><b>Current Average Level:</b> %{customdata} <extra></extra>',
            marker = dict(
                color='white',
                size = 10,
                line_width=0
                )
        )
    )

fig.add_trace( #Below Threshold - BAR
    go.Bar(
        y=df_below['SUBSTANCE '],
        x=df_below['n_range_high'] - df_below['n_range_low'],
        base = df_below['n_range_low'],
        orientation = 'h',
        width = 0.75,
        marker_color = 'white',
        opacity= 0.2

        )
    )

fig.add_trace( #Above Threshold - POINT
    go.Scatter(
        y=df_above['SUBSTANCE '],
        x=df_above['n_average'],
        mode = 'markers',
        marker_symbol = 4,
        text = df_above['source'].replace(' <br> ' , "<br>" , regex = True),
        customdata = df_above['Average Level'], 
        hovertemplate = '<b>%{y}</b><br>%{text}<br><b>Current Average Level:</b> %{customdata} <extra></extra>',
        marker = dict(
            color= plot_red,
            size = 14,
            line_width=1,
            line_color='white'

            )
        )
    )

fig.add_trace( #Above Threshold - BAR
    go.Bar(
        y=df_above['SUBSTANCE '],
        x=df_above['n_range_high'] - df_above['n_range_low'],
        base = df_above['n_range_low'],
        orientation = 'h',
        width = 0.75,
        marker_color = plot_red,
        opacity= 0.3

        )
    )

fig.add_shape(type="line", #GRID LINES - ZERO LINE
    x0=0, y0=0, x1=0, y1=len(df)+1,
    opacity = 0.75,
    line=dict(
        color= plot_red,
        width=1.5,
        dash="dash",
        )
    )

for i in range( len(df)): #GRID LINES - GRIDLINE
    fig.add_shape(type="line",
        x0=-1.05, 
        y0=i, 
        x1=1.05,
        y1=i,
        opacity = 0.75,
        line=dict(
            color= 'white',
            width=0.6,
            dash="dot",
        )
    )

fig.add_shape(type="rect", #Violation BG
    x0=1.05, y0=len(df), 
    x1=0, y1=len(df)+1,
    fillcolor=plot_red,
    opacity = 0.5,
    line=dict(width=0),
    )

fig.add_trace( #Goals
    go.Scatter(
        y=df[~pd.isna(df['PHG [MCLG] Goal'])]['SUBSTANCE '],
        x=df[~pd.isna(df['PHG [MCLG] Goal'])]['n_goal'],
        mode = 'markers',
        marker_symbol = 142,
        text = df[~pd.isna(df['PHG [MCLG] Goal'])]['PHG [MCLG] Goal'],
        customdata = df[~pd.isna(df['PHG [MCLG] Goal'])]['Units'],
        hovertemplate = "Goal for<b>%{y}</b>:<br> %{text} %{customdata}<extra></extra>",
        marker = dict(
            color= '#F9D812',
            size = 10,
            line = dict(
                width = 3
                )
            )
        )
    )

if len(df_above) == 0:
    xlim = 0.1
else:
    xlim = df['n_average'].max()

fig.update_layout( #All Layout
    width=width,
    height=height,
    xaxis = dict(zeroline=False,nticks=1,showgrid=False,showticklabels=False,
        range = [df['n_average'].min() - 0.05 , xlim + 0.05 ]
        ),
    xaxis_tickformat = '%',
    yaxis = dict(
        showticklabels=False,zeroline=False,showgrid=False,
        range=[-1,len(df)+1]
        ),
    plot_bgcolor=plot_blue,
    paper_bgcolor=plot_blue ,
    showlegend = False,
    margin = dict(t=5,l=5,r=5,b=5),
    hoverlabel=dict(
        bgcolor="white",
        font_size=11,
        )
    )

ay = 0.99

fig.add_annotation(text="Safe",
                  xref="paper", yref="paper",
                  x=0.025, y=ay, showarrow=False,align='right',
                  font=dict(
                    family= "Open Sans, sans-serif",
                    size=12,
                    color="white"
                    ),
                  )

fig.add_annotation(text="Action Level",
                  xref="paper", yref="paper",
                  x=0.79, y=ay, showarrow=False,align='right',
                  font=dict(
                    family= "Open Sans, sans-serif",
                    size=12,
                    color="white"
                    ),
                  )

fig.add_annotation(text="Violation",
                  xref="paper", yref="paper",
                  x=0.99, y=ay, showarrow=False,align='right',
                  font=dict(
                    family= "Open Sans, sans-serif",
                    size=12,
                    color="white"
                    ),
                  )

config={'modeBarButtonsToRemove': ['toggleSpikelines','hoverCompareCartesian','zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2'],'displayModeBar': False }
fig.show( config = config )

#%%

fig.write_image( r"C:\Users\csucuogl\Dropbox\CCR_waterQuality_contest\visual\good_chart.pdf" )

#%%
fig.write_html( 
    r"C:\Users\csucuogl\Documents\GitHub\DrinkingWater\visuals\vBar_graph.html" ,
    include_plotlyjs = 'cdn',
    full_html = False
    )


# %%

import sys
print( sys.prefix)
# %%
