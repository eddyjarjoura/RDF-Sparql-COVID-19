import dash_table

filename = "rows.rdf"  # replace with something interesting
import rdflib
import rdfextras
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import plotly.graph_objects as go
from datetime import datetime

from matplotlib import pyplot as plt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

rdfextras.registerplugins()  # so we can Graph.query()
Case_total = []
total_pop = []
death = []
hisp_race = []
dateupdated = []
g = rdflib.Graph()
g.parse(filename)
qres = g.query("""
SELECT ?case_tot ?total_pop   ?deaths ?hisp_race ?dateupdated
Where{
  ?label ds:case_tot  ?case_tot.
  ?label ds:total_pop  ?total_pop.
  ?label ds:deaths  ?deaths.
  ?label ds:hisp_race ?hisp_race.
  ?label ds:dateupdated ?dateupdated.
}ORDER BY ?label
""")
AllRaces = []
results = g.query("""
SELECT DISTINCT  ?hisp_race
Where{
  ?label ds:hisp_race ?hisp_race.
}
""")
for row in results:
    AllRaces.append(row[0])
print(AllRaces)
data = pd.DataFrame(columns=['hisp_race', 'Case_total', 'deaths', 'dateupdated', 'total_pop'])
for row in qres:
    Case_total.append(row[0])
    total_pop.append(row[1])  # total_pop
    death.append(row[2])
    hisp_race.append(row[3])
    dateupdated.append(row[4])

df = data.append(pd.DataFrame(
    {'hisp_race': hisp_race, 'Case_total': Case_total, 'deaths': death, 'dateupdated': dateupdated,
     'total_pop': total_pop}))
df['Case_total'] = pd.to_numeric(df['Case_total'])
df['deaths'] = pd.to_numeric(df['deaths'])
df = df.sort_values(by='dateupdated')
GroupbyMonths = df.groupby(['dateupdated'], as_index=False)['Case_total'].sum()
GroupbyMonths2 = df.groupby(['dateupdated'], as_index=False)['deaths'].sum()
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=total_pop, y=Case_total, name="Case_total", stackgroup='one'))  # fill down to xaxis
fig1.add_trace(go.Scatter(x=total_pop, y=death, name="death", stackgroup='one'))
fig1.update_layout(
    title="<b>Population-Cases-Death<b>",
    title_x=0.5,
    xaxis_title="",
    yaxis_title="Cases and Death",
    legend_title="Total_population",
    plot_bgcolor='#e6e6e6',
    paper_bgcolor='#e6e6e6',
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="RebeccaPurple"
    )
)
fig2 = px.bar(df, x='hisp_race', y='Case_total')
fig2.update_layout(
    title="<b>Cases Per Race<b>",
    title_x=0.5,
    xaxis_title="",
    yaxis_title="Number of Cases",
    legend_title="Cases Per Case",
    plot_bgcolor='#e6e6e6',
    paper_bgcolor='#e6e6e6',
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="RebeccaPurple"
    )
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    'Filter by Date:', className="Titre1 Categorization D1 B"
                                ),
                                dcc.RangeSlider(
                                    id='my-range-slider',
                                    min=0,
                                    max=1,
                                    step=1,
                                    vertical=False,
                                    verticalHeight=600,
                                    value=[],
                                    className="dcc_control",

                                ),
                                html.Div(id='output-container-range-slider', className="Colorr", children=[]),

                                html.P("Choose Race ", className="Sentiment-x Ja"),
                                dcc.Dropdown(id="slct-sentiment",
                                             options=[
                                                 {"label": "Black", "value": "Black"},
                                                 {"label": "Hispanic", "value": "Hispanic"},
                                                 {"label": "American Indian or Alaskan Native",
                                                  "value": "American Indian or Alaskan Native"},
                                                 {"label": "Asian or Pacific Islander",
                                                  "value": "Asian or Pacific Islander"},
                                                 {"label": "White", "value": "White"},
                                             ],
                                             placeholder="Select a city",

                                             multi=False),

                            ], className="pretty_container5 ", ),
                        html.Div(
                            dash_table.DataTable(
                                id='review_table',

                                columns=[{"name": i, "id": i} for i in
                                         ['hisp_race', 'case_tot', 'deaths', 'dateupdated']],
                                style_cell={
                                    'color': 'Black',
                                    'font_size': '16px',
                                    'backgroundColor': '#bfbfbf',
                                    'textAlign': 'left',
                                    'whiteSpace': 'normal',
                                }, style_header={
                                    'font_size': '20px',
                                    'text-align': ' left',
                                    'fontWeight': 'bold',
                                },
                                tooltip_data=[],

                                tooltip_duration=None,
                                # sort_action='native',
                                data=[],
                            ),
                            className="pretty_container12",
                        ),
                    ],
                ),
                html.Div(
                    className="one columns"
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6("Date", className="Titre3"),
                                     html.P(datetime.now().strftime('%Y-%m-%d'), className=" P  B"),
                                     ],
                                    id="wells",
                                    className="mini_container three columns ",
                                ),
                                html.Div(
                                    [html.H6("# of population", className="Titre D1"),
                                     html.P(id="Nmbreofreviews", children=[], className="P B")
                                     ],
                                    id="gas",
                                    className="mini_container three columns",
                                ),
                                html.Div(
                                    [html.H6("# of Cases", className="Titre D1"),
                                     html.P(id="Positive", children=[], className="P D1 B")],
                                    id="oil",
                                    className="mini_container three columns",
                                ),
                                html.Div(
                                    [html.H6("# of Death", className="Titre D1"),
                                     html.P(id="Negative", children=[], className="P D1 B")],
                                    id="water",
                                    className="mini_container three columns",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [dcc.Graph(id='FIG3')],
                                    className="pretty_container4 six columns",
                                ),
                                html.Div(
                                    [dcc.Graph(id='FIG4')],
                                    className="pretty_container4 six columns",
                                ),
                            ],
                            className="row flex-display Piechart",

                        ),

                        html.Div(
                            [
                                html.Div(
                                    [dcc.Graph(figure=fig2)],
                                    className="pretty_container4 six columns",
                                ),
                                html.Div(
                                    [dcc.Graph(figure=fig1)],
                                    className="pretty_container4 six columns",
                                ),
                            ],
                            className="row flex-display Piechart",

                        ),
                    ],
                    id="right-column ",
                    className="eight columns ",

                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


#
#
@app.callback(
    Output('Nmbreofreviews', 'children'),
    [
        Input("my-range-slider", "value"), Input("slct-sentiment", "value")
    ])
def update_nbr_review(value, value2):
    if value2 is None:
        qrs = g.query("""
        SELECT ?total_pop ?dateupdated
        Where{
        ?label ds:total_pop ?total_pop.
        ?label ds:hisp_race ?hisp_race.
        ?label ds:dateupdated ?dateupdated.
        }
        """)
        death1 = []
        data12 = pd.DataFrame(columns=['total_pop'])
        for row in qrs:
            death1.append(row[0])
        dt = data12.append(pd.DataFrame(
            {'total_pop': death1}))
        dt['total_pop'] = pd.to_numeric(dt['total_pop'])
        Total = dt['total_pop'].unique().sum()
        Total = human_format(Total)
        return Total
    else:
        y1 = value2
        qrs = g.query("""
        SELECT  ?total_pop ?dateupdated
        Where{
        ?label ds:total_pop ?total_pop.
        ?label ds:hisp_race ?hisp_race.
        ?label ds:dateupdated ?dateupdated.FILTER(?hisp_race="%s")
        }
        """ % y1)
        death1 = []
        data12 = pd.DataFrame(columns=['total_pop'])
        for row in qrs:
            death1.append(row[0])
        dt = data12.append(pd.DataFrame(
            {'total_pop': death1}))
        dt['total_pop'] = pd.to_numeric(dt['total_pop'])
        Total = dt['total_pop'].unique().sum()
        Total = human_format(Total)
        return Total


@app.callback(
    Output('Positive', 'children'),
    [
        Input("my-range-slider", "value"), Input("slct-sentiment", "value")
    ])
def update_nmbrofcases(value, value2):
    if value2 is None:
        dates = list(df['dateupdated'].unique())[::-1]
        dates = [" ".join(i.split()) for i in dates]
        date_value = [dates[value[0]], dates[value[1]]]
        D1 = str(dates[value[0]])
        D2 = str(dates[value[1]])
        qres12 = g.query("""
            SELECT ?case_tot ?dateupdated
            Where{
            ?label ds:case_tot ?case_tot.
            ?label ds:hisp_race ?hisp_race.
            ?label ds:dateupdated ?dateupdated.
            }
            """)
        death1 = []
        data12 = pd.DataFrame(columns=['case_tot'])
        for row in qres12:
            death1.append(row[0])
        dt = data12.append(pd.DataFrame(
            {'case_tot': death1}))
        dt['case_tot'] = pd.to_numeric(dt['case_tot'])
        Total = dt['case_tot'].sum()
        Total = human_format(Total)
        return Total

    else:
        y1 = str(value2)
        dates = list(df['dateupdated'].unique())[::-1]
        dates = [" ".join(i.split()) for i in dates]
        date_value = [dates[value[0]], dates[value[1]]]
        D1 = str(dates[value[0]])
        D2 = str(dates[value[1]])
        qres12 = g.query("""
        SELECT ?case_tot ?dateupdated
        Where{
        ?label ds:case_tot ?case_tot.
        ?label ds:hisp_race ?hisp_race.
        ?label ds:dateupdated ?dateupdated.FILTER(?hisp_race="%s"&&?dateupdated<="%s" && ?dateupdated>="%s")
        }
        """ % (y1, D1, D2))
        death1 = []
        data12 = pd.DataFrame(columns=['case_tot'])
        for row in qres12:
            death1.append(row[0])
        dt = data12.append(pd.DataFrame(
            {'case_tot': death1}))
        dt['case_tot'] = pd.to_numeric(dt['case_tot'])
        Total = dt['case_tot'].sum()
        Total = human_format(Total)
        return Total


@app.callback(
    Output('Negative', 'children'),
    [
        Input("my-range-slider", "value"), Input("slct-sentiment", "value")
    ])
def update_nmbrofcases1(value, value2):
    if value2 is None:
        dates = list(df['dateupdated'].unique())[::-1]
        dates = [" ".join(i.split()) for i in dates]
        date_value = [dates[value[0]], dates[value[1]]]
        D1 = str(dates[value[0]])
        D2 = str(dates[value[1]])
        qres1 = g.query("""
        SELECT ?deaths ?dateupdated
        Where{
        ?label ds:deaths ?deaths.
        ?label ds:hisp_race ?hisp_race.
        ?label ds:dateupdated ?dateupdated.
        }
        """)
        death = []
        data1 = pd.DataFrame(columns=['deaths'])
        for row in qres1:
            death.append(row[0])
        ef = data1.append(pd.DataFrame(
            {'deaths': death}))
        ef['deaths'] = pd.to_numeric(ef['deaths'])
        Total = ef['deaths'].sum()
        Total = human_format(Total)
        return Total
    else:
        y1 = value2
        dates = list(df['dateupdated'].unique())[::-1]
        dates = [" ".join(i.split()) for i in dates]
        date_value = [dates[value[0]], dates[value[1]]]
        D1 = str(dates[value[0]])
        D2 = str(dates[value[1]])
        qres1 = g.query("""
        SELECT ?deaths ?dateupdated
        Where{
        ?label ds:deaths ?deaths.
        ?label ds:hisp_race ?hisp_race.
        ?label ds:dateupdated ?dateupdated.FILTER(?hisp_race="%s"&&?dateupdated<="%s" && ?dateupdated>="%s")
        }
        """ % (y1, D1, D2))
        death = []
        data1 = pd.DataFrame(columns=['deaths'])
        for row in qres1:
            death.append(row[0])
        ef = data1.append(pd.DataFrame(
            {'deaths': death}))
        ef['deaths'] = pd.to_numeric(ef['deaths'])
        Total = ef['deaths'].sum()
        Total = human_format(Total)
        return Total


@app.callback(
    [Output('my-range-slider', 'value'), Output('my-range-slider', 'max')],
    [Input('Nmbreofreviews', 'value')])
def update_output(value):
    dates = list(df['dateupdated'].unique())[::-1]
    dates = [" ".join(i.split()) for i in dates]
    return [0, len(dates) - 1], len(dates) - 1


@app.callback(
    Output('output-container-range-slider', 'children'),
    [Input('my-range-slider', 'value')])
def update_output(value):
    dates = list(df['dateupdated'].unique())[::-1]
    dates = [" ".join(i.split()) for i in dates]
    value = [dates[value[1]], dates[value[0]]]
    return 'Date Range: [{}, {}]'.format(value[1], value[0])


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


# Update figure
@app.callback(
    Output("FIG3", "figure"),
    [
        Input("my-range-slider", "value"), Input("slct-sentiment", "value")
    ],
)
def update_figure2(value, value2):
    if value2 is None:
        dates = list(df['dateupdated'].unique())[::-1]
        dates = [" ".join(i.split()) for i in dates]
        date_value = [dates[value[0]], dates[value[1]]]
        D1 = str(dates[value[0]])
        D2 = str(dates[value[1]])
        qres123 = g.query("""
        SELECT ?case_tot ?dateupdated
        Where{
        ?label ds:case_tot ?case_tot.
        ?label ds:hisp_race ?hisp_race.
        ?label ds:dateupdated ?dateupdated.
        }
        """)
        death12 = []
        dateupdated2 = []
        data123 = pd.DataFrame(columns=['case_tot', 'dateupdated'])
        for row in qres123:
            death12.append(row[0])
            dateupdated2.append(row[1])
        dte = data123.append(pd.DataFrame(
            {'case_tot': death12, 'dateupdated': dateupdated2}))
        dte['case_tot'] = pd.to_numeric(dte['case_tot'])
        GroupbyMonths = dte.groupby(['dateupdated'], as_index=False)['case_tot'].sum()
        fig3 = px.bar(GroupbyMonths, x='dateupdated', y='case_tot')
        fig3.update_layout(
            title="<b>Cases Per Date<b>",
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Case",
            legend_title="Cases Per Date",
            plot_bgcolor='#e6e6e6',
            paper_bgcolor='#e6e6e6',
            font=dict(
                family="Courier New, monospace",
                size=12,
                color="RebeccaPurple"
            )
        )
        return fig3

    else:
        y1 = value2
        dates = list(df['dateupdated'].unique())[::-1]
        dates = [" ".join(i.split()) for i in dates]
        date_value = [dates[value[0]], dates[value[1]]]
        D1 = str(dates[value[0]])
        D2 = str(dates[value[1]])
        qres123 = g.query("""
        SELECT ?case_tot ?dateupdated
        Where{
        ?label ds:case_tot ?case_tot.
        ?label ds:hisp_race ?hisp_race.
        ?label ds:dateupdated ?dateupdated.FILTER(?hisp_race="%s"&&?dateupdated<="%s" && ?dateupdated>="%s")
        }
        """ % (y1, D1, D2))
        death12 = []
        dateupdated2 = []
        data123 = pd.DataFrame(columns=['case_tot', 'dateupdated'])
        for row in qres123:
            death12.append(row[0])
            dateupdated2.append(row[1])
        dte = data123.append(pd.DataFrame(
            {'case_tot': death12, 'dateupdated': dateupdated2}))
        dte['case_tot'] = pd.to_numeric(dte['case_tot'])
        GroupbyMonths = dte.groupby(['dateupdated'], as_index=False)['case_tot'].sum()
        fig3 = px.bar(GroupbyMonths, x='dateupdated', y='case_tot')
        fig3.update_layout(
            title="<b>Cases Per Date<b>",
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Case",
            legend_title="Cases Per Date",
            plot_bgcolor='#e6e6e6',
            paper_bgcolor='#e6e6e6',
            font=dict(
                family="Courier New, monospace",
                size=12,
                color="RebeccaPurple"
            )
        )
        return fig3


# Update figure
@app.callback(
    Output("FIG4", "figure"),
    [
        Input("my-range-slider", "value"), Input("slct-sentiment", "value")
    ],
)
def update_figure21(value, value2):
    if value2 is None:
        dates = list(df['dateupdated'].unique())[::-1]
        dates = [" ".join(i.split()) for i in dates]
        date_value = [dates[value[0]], dates[value[1]]]
        D1 = str(dates[value[0]])
        D2 = str(dates[value[1]])
        qres1253 = g.query("""
        SELECT ?deaths ?dateupdated ?hisp_race
        Where{
        ?label ds:hisp_race ?hisp_race.
        ?label ds:deaths ?deaths.
        ?label ds:dateupdated ?dateupdated.
        }
        """)
        deatha = []
        dateupdated21 = []
        Deathdata = pd.DataFrame(columns=['deaths', 'dateupdated'])
        for row in qres1253:
            deatha.append(row[0])
            dateupdated21.append(row[1])
        dtef = Deathdata.append(pd.DataFrame(
            {'deaths': deatha, 'dateupdated': dateupdated21}))
        dtef['deaths'] = pd.to_numeric(dtef['deaths'])
        GroupbyMonths2 = dtef.groupby(['dateupdated'], as_index=False)['deaths'].sum()
        fig4 = px.bar(GroupbyMonths2, x='dateupdated', y='deaths')
        fig4.update_layout(
            title="<b>Death per date<b>",
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Death",
            legend_title="Death  Per Date",
            plot_bgcolor='#e6e6e6',
            paper_bgcolor='#e6e6e6',
            font=dict(
                family="Courier New, monospace",
                size=12,
                color="RebeccaPurple"
            )
        )
        return fig4

    else:
        y1 = value2
        dates = list(df['dateupdated'].unique())[::-1]
        dates = [" ".join(i.split()) for i in dates]
        date_value = [dates[value[0]], dates[value[1]]]
        D1 = str(dates[value[0]])
        D2 = str(dates[value[1]])
        qres1253 = g.query("""
        SELECT ?deaths ?dateupdated ?hisp_race
        Where{
        ?label ds:hisp_race ?hisp_race.
        ?label ds:deaths ?deaths.
        ?label ds:dateupdated ?dateupdated.FILTER(?hisp_race="%s"&&?dateupdated<="%s" && ?dateupdated>="%s")
        }
        """ % (y1, D1, D2))
        deatha = []
        dateupdated21 = []
        Deathdata = pd.DataFrame(columns=['deaths', 'dateupdated'])
        for row in qres1253:
            deatha.append(row[0])
            dateupdated21.append(row[1])
        dtef = Deathdata.append(pd.DataFrame(
            {'deaths': deatha, 'dateupdated': dateupdated21}))
        dtef['deaths'] = pd.to_numeric(dtef['deaths'])
        GroupbyMonths2 = dtef.groupby(['dateupdated'], as_index=False)['deaths'].sum()
        fig4 = px.bar(GroupbyMonths2, x='dateupdated', y='deaths')
        fig4.update_layout(
            title="<b>Death per date<b>",
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Death",
            legend_title="Death  Per Date",
            plot_bgcolor='#e6e6e6',
            paper_bgcolor='#e6e6e6',
            font=dict(
                family="Courier New, monospace",
                size=12,
                color="RebeccaPurple"
            )
        )
        return fig4


# Update table
@app.callback(
    [Output("review_table", "tooltip_data"), Output("review_table", "data")],
    [Input("slct-sentiment", "value")]
)
def updateTable2(value):
    global data
    if value is None:
        Cases = []
        total_pop1 = []
        death1 = []
        hisp_race1 = []
        d = []
        qres11 = g.query("""
        SELECT ?case_tot ?total_pop   ?deaths ?hisp_race  ?dateupdated
        Where{
          ?label ds:case_tot  ?case_tot.
          ?label ds:total_pop  ?total_pop.
          ?label ds:deaths  ?deaths.
          ?label ds:hisp_race ?hisp_race.
          ?label ds:dateupdated ?dateupdated.

        }ORDER BY ?label
        """)
        data = pd.DataFrame(columns=['hisp_race', 'case_tot', 'deaths', 'dateupdated'])
        for row1 in qres11:
            Cases.append(row1[0])
            total_pop1.append(row1[1])  # total_pop
            death1.append(row1[2])
            hisp_race1.append(row1[3])
            d.append(row1[4])

        df23 = data.append(pd.DataFrame(
            {'hisp_race': hisp_race1, 'case_tot': Cases,
             'deaths': death1, 'dateupdated': d}))
        df23 = df23.head(7)

        data = [{'hisp_race': i['hisp_race'], 'case_tot': i['case_tot'],
                 'deaths': i['deaths'], 'dateupdated': i['dateupdated']}
                for i in df23.to_dict('records')]
        label_data = [{column: {'value': str(value)} for column, value in row.items()}
                      for row in df23.to_dict('records')]
        df23 = pd.DataFrame(data)
        df23 = df23.fillna(' ')
        return label_data, df23.to_dict('records')

    elif 'Hispanic' in value:
        Cases = []
        total_pop1 = []
        death1 = []
        hisp_race1 = []
        d = []
        qres1122 = g.query("""
        SELECT ?case_tot ?total_pop   ?deaths  ?hisp_race ?dateupdated
        Where{
          ?label ds:case_tot  ?case_tot.
          ?label ds:total_pop  ?total_pop.
          ?label ds:deaths  ?deaths.
          ?label ds:hisp_race ?hisp_race.FILTER(?hisp_race="Hispanic")
          ?label ds:dateupdated ?dateupdated.
        }ORDER BY ?label
        """)
        data = pd.DataFrame(columns=['hisp_race', 'case_tot', 'deaths', 'dateupdated'])
        for row1 in qres1122:
            Cases.append(row1[0])
            total_pop1.append(row1[1])  # total_pop
            death1.append(row1[2])
            hisp_race1.append(row1[3])
            d.append(row1[4])
        df23 = data.append(pd.DataFrame(
            {'hisp_race': hisp_race1, 'case_tot': Cases,
             'deaths': death1, 'dateupdated': d}))
        df23 = df23.head(13)
        print(df23)
        data = [{'hisp_race': i['hisp_race'], 'case_tot': i['case_tot'],
                 'deaths': i['deaths'], 'dateupdated': i['dateupdated']}
                for i in df23.to_dict('records')]
        label_data = [{column: {'value': str(value)} for column, value in row.items()}
                      for row in df23.to_dict('records')]
        df23 = pd.DataFrame(data)
        df23 = df23.fillna(' ')
        return label_data, df23.to_dict('records')
    elif 'Black' in value:
        Cases = []
        total_pop1 = []
        death1 = []
        hisp_race1 = []
        d = []
        qres112x2 = g.query("""
        SELECT ?case_tot ?total_pop   ?deaths ?hisp_race ?dateupdated
        Where{
          ?label ds:case_tot  ?case_tot.
          ?label ds:total_pop  ?total_pop.
          ?label ds:deaths  ?deaths.
          ?label ds:hisp_race ?hisp_race.FILTER(?hisp_race="Black")
          ?label ds:dateupdated ?dateupdated.

        }ORDER BY ?label
        """)
        data = pd.DataFrame(columns=['hisp_race', 'case_tot', 'deaths', 'dateupdated'])
        for row1 in qres112x2:
            Cases.append(row1[0])
            total_pop1.append(row1[1])  # total_pop
            death1.append(row1[2])
            hisp_race1.append(row1[3])
            d.append(row1[4])
        df23 = data.append(pd.DataFrame(
            {'hisp_race': hisp_race1, 'case_tot': Cases,
             'deaths': death1, 'dateupdated': d}))
        df23 = df23.head(13)

        data = [{'hisp_race': i['hisp_race'], 'case_tot': i['case_tot'],
                 'deaths': i['deaths'], 'dateupdated': i['dateupdated']}
                for i in df23.to_dict('records')]
        label_data1 = [{column: {'value': str(value)} for column, value in row.items()}
                       for row in df23.to_dict('records')]
        df23 = pd.DataFrame(data)
        df23 = df23.fillna(' ')
        return label_data1, df23.to_dict('records')
    elif 'American Indian or Alaskan Native' in value:
        Cases = []
        total_pop1 = []
        death1 = []
        hisp_race1 = []
        d = []
        qres1122as = g.query("""
            SELECT ?case_tot ?total_pop   ?deaths ?hisp_race ?dateupdated
        Where{
          ?label ds:case_tot  ?case_tot.
          ?label ds:total_pop  ?total_pop.
          ?label ds:deaths  ?deaths.
          ?label ds:hisp_race ?hisp_race.FILTER(?hisp_race="American Indian or Alaskan Native")
          ?label ds:dateupdated ?dateupdated.

        }ORDER BY ?label
        """)
        data = pd.DataFrame(columns=['hisp_race', 'case_tot', 'deaths', 'dateupdated'])
        for row1 in qres1122as:
            Cases.append(row1[0])
            total_pop1.append(row1[1])  # total_pop
            death1.append(row1[2])
            hisp_race1.append(row1[3])
            d.append(row1[4])

        df23 = data.append(pd.DataFrame(
            {'hisp_race': hisp_race1, 'case_tot': Cases,
             'deaths': death1, 'dateupdated': d}))
        df23 = df23.head(3)

        data = [{'hisp_race': i['hisp_race'], 'case_tot': i['case_tot'],
                 'deaths': i['deaths'], 'dateupdated': i['dateupdated']}
                for i in df23.to_dict('records')]
        label_data = [{column: {'value': str(value)} for column, value in row.items()}
                      for row in df23.to_dict('records')]
        df23 = pd.DataFrame(data)
        df23 = df23.fillna(' ')
        return label_data, df23.to_dict('records')
    elif 'Asian or Pacific Islander' in value:
        Cases = []
        total_pop1 = []
        death1 = []
        hisp_race1 = []
        d = []
        qres112212 = g.query("""
        SELECT ?case_tot ?total_pop   ?deaths ?hisp_race ?dateupdated
        Where{
          ?label ds:case_tot  ?case_tot.
          ?label ds:total_pop  ?total_pop.
          ?label ds:deaths  ?deaths.
          ?label ds:hisp_race ?hisp_race.FILTER(?hisp_race="Asian or Pacific Islander")
          ?label ds:dateupdated ?dateupdated.

        }ORDER BY ?label
        """)
        data = pd.DataFrame(columns=['hisp_race', 'case_tot', 'deaths', 'dateupdated'])
        for row1 in qres112212:
            Cases.append(row1[0])
            total_pop1.append(row1[1])  # total_pop
            death1.append(row1[2])
            hisp_race1.append(row1[3])
            d.append(row1[4])

        df23 = data.append(pd.DataFrame(
            {'hisp_race': hisp_race1, 'case_tot': Cases,
             'deaths': death1, 'dateupdated': d}))
        df23 = df23.head(4)

        data = [{'hisp_race': i['hisp_race'], 'case_tot': i['case_tot'],
                 'deaths': i['deaths'], 'dateupdated': i['dateupdated']}
                for i in df23.to_dict('records')]
        label_data = [{column: {'value': str(value)} for column, value in row.items()}
                      for row in df23.to_dict('records')]
        df23 = pd.DataFrame(data)
        df23 = df23.fillna(' ')
        return label_data, df23.to_dict('records')
    elif 'White' in value:
        Cases = []
        total_pop1 = []
        death1 = []
        hisp_race1 = []
        d = []
        qres11222 = g.query("""
        SELECT ?case_tot ?total_pop   ?deaths ?hisp_race ?dateupdated
        Where{
          ?label ds:case_tot  ?case_tot.
          ?label ds:total_pop  ?total_pop.
          ?label ds:deaths  ?deaths.
          ?label ds:hisp_race ?hisp_race.FILTER(?hisp_race="White")
          ?label ds:dateupdated ?dateupdated.
        }ORDER BY ?label
        """)
        data = pd.DataFrame(columns=['hisp_race', 'case_tot', 'deaths', 'dateupdated'])
        for row1 in qres11222:
            Cases.append(row1[0])
            total_pop1.append(row1[1])  # total_pop
            death1.append(row1[2])
            hisp_race1.append(row1[3])
            d.append(row1[4])
        df23 = data.append(pd.DataFrame(
            {'hisp_race': hisp_race1, 'case_tot': Cases,
             'deaths': death1, 'dateupdated': d}))
        df23 = df23.head(13)

        data = [{'hisp_race': i['hisp_race'], 'case_tot': i['case_tot'],
                 'deaths': i['deaths'], 'dateupdated': i['dateupdated']}
                for i in df23.to_dict('records')]
        label_data = [{column: {'value': str(value)} for column, value in row.items()}
                      for row in df23.to_dict('records')]
        df23 = pd.DataFrame(data)
        df23 = df23.fillna(' ')
        return label_data, df23.to_dict('records')



if __name__ == '__main__':
    app.run_server(debug=False, port=9127)
