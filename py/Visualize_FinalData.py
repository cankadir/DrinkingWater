
#%% IMPORT
import pandas as pd
import numpy as np
import plotly.graph_objects as go

df = pd.read_excel( r"C:\Users\csucuogl\Dropbox\CCR_waterQuality_contest\data\Dataset_1_Bad.xlsx" )

df.head(5)

#%%

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

# %%

plot_blue = '#5DA7FF'
plot_red = '#F47A4E'

#%% Simple Bar Chart - VERTICAL

fig = go.Figure()

df_below = df[ df['n_average']<=0 ]
df_above = df[ df['n_average']>0 ]

fig.add_trace( #Below Threshold
    go.Scatter(
        x=df_below['SUBSTANCE '],
        y=df_below['n_average'],
        mode = 'markers',
        marker_symbol= 200,
        text = df_below['source'].replace(' <br> ' , "<br>" , regex = True),
        hovertemplate = '<b>%{x}</b><br>%{text}<extra></extra>',
        error_y=dict(
            type='data',
            symmetric=False,
            array= df_below['n_range_high'] - df_below['n_average'],
            arrayminus = df_below['n_average'] - df_below['n_range_low'],
            color='white',
            thickness=7,
            width=0,
                ),
            marker = dict(
                color='black',
                size = 3,
                line_width=1.4
                )
        )
    )

fig.add_trace( #Above Threshold
    go.Scatter(
        x=df_above['SUBSTANCE '],
        y=df_above['n_average'],
        mode = 'markers',
        marker_symbol= 200,
        text = df_above['source'].replace(' <br> ' , "<br>" , regex = True),
        hovertemplate = '<b>%{x}</b><br>%{text}<extra></extra>',
        error_y=dict(
            type='data',
            symmetric=False,
            array= df_above['n_range_high'] - df_above['n_average'],
            arrayminus = df_above['n_average'] - df_above['n_range_low'] ,
            color= plot_red,
            thickness=7,
            width=0,
                ),
            marker = dict(
                color= 'black',
                size = 3,
                line_width=1.4
                )
        )
    )

fig.update_yaxes(nticks=1)

fig.update_layout(yaxis_tickformat = '%')
fig.update_layout(yaxis=dict(range=[-1,1]))

fig.update_layout(
    xaxis = dict(showticklabels=False),
    yaxis = dict(showticklabels=False)
    ) 

fig.update_layout(
    width=550,
    height=350,
    plot_bgcolor=plot_blue,
    paper_bgcolor=plot_blue ,
    showlegend = False,
    margin = dict(t=0,l=0,r=0,b=0)
    )

fig.update_xaxes(showgrid=True, gridwidth=0.05, gridcolor = '#e4f6f5' )
fig.update_yaxes(showgrid=True, gridwidth=0.05, gridcolor = '#e4f6f5' )

fig.add_annotation(text="Level <b>Above</b><br>EPA Threshold",
                  xref="paper", yref="paper",
                  x=0, y=0.75, showarrow=False,align='right',
                  font=dict(
                    size=12,
                    color="white"
                    ),
                  )

fig.add_annotation(text="Level <b>Below</b><br>EPA Threshold",
                  xref="paper", yref="paper",
                  x=0, y=0.25, showarrow=False, align='right',
                  font=dict(
                    size=12,
                    color="white"
                    ),
                  )

fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=11,
        #bordercolor = 'white'
    )
)
fig.update_xaxes(range=[-4, len(df) ])

#fig.show( config = dict(displayModeBar= False) )
fig.write_html( 
    r"C:\Users\csucuogl\Documents\GitHub\DrinkingWater\visuals\lolli_graph.html" ,
    include_plotlyjs = 'cdn',
    full_html = False
    )
#fig.write_image( r"C:\Users\csucuogl\Documents\GitHub\DrinkingWater\visuals\lolli_graph.pdf" )
fig.show()


# %% BAR CHART - VERTICAL

fig = go.Figure()

df_below = df[ df['n_average']<=0 ]
df_above = df[ df['n_average']>0 ]

fig.add_trace( #Below Threshold - POINT
    go.Scatter(
        y=df_below['SUBSTANCE '],
        x=df_below['n_average'],
        mode = 'markers',
        text = df_below['source'].replace(' <br> ' , "<br>" , regex = True),
        hovertemplate = '<b>%{y}</b><br>%{text}<extra></extra>',
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
        hovertemplate = '<b>%{y}</b><br>%{text}<extra></extra>',
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

fig.add_trace( #EPA Goals
    go.Scatter(
        y=df[~pd.isna(df['PHG [MCLG] Goal'])]['SUBSTANCE '],
        x=df[~pd.isna(df['PHG [MCLG] Goal'])]['n_goal'],
        mode = 'markers',
        marker_symbol = 142,
        text = df['PHG [MCLG] Goal'],
        hovertemplate = "EPA's future goal for<br><b>%{y}</b> is %{text}<extra></extra>",
        marker = dict(
            color= '#F9D812',
            size = 10,
            line = dict(
                width = 3
                )
            )
        )
    )

fig.update_layout( #All Layout
    width=650,
    height=400,
    xaxis = dict(zeroline=False,nticks=1,showgrid=False,showticklabels=False,
        range = [df['n_average'].min() - 0.05 , df['n_average'].max() + 0.05 ]
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

fig.add_annotation(text="EPA Threshold",
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
fig.write_html( 
    r"C:\Users\csucuogl\Documents\GitHub\DrinkingWater\visuals\vBar_graph.html" ,
    include_plotlyjs = 'cdn',
    full_html = False
    )


# %%


# %%
