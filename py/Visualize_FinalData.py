
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

plot_blue = '#BEE9E8'
plot_red = '#ED6A5A'

#%% Simple Bar Chart

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
# %%

fig.write_image( r"C:\Users\csucuogl\Documents\GitHub\DrinkingWater\visuals\chart.pdf")
# %%
