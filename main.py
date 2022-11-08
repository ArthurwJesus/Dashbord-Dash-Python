##https://dash.plotly.com/datatable/callbacks


from dash import dash, html, dcc, Output, Input, dash_table
import plotly.express as px
import plotly.graph_objects as go
from formatDataset import *
import dash_bootstrap_components as dbc


def generate_table(dataframe, max_rows=20):
    return dbc.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns],
                    style={'textAlign': 'center', 'color': 'white', 'background': ' rgba(0, 0, 0, 0.93)'})
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ], style={'textAlign': 'center'}) for i in range(min(len(dataframe), max_rows))
        ])
    ])


def grafic_static_teams():
    fig = px.pie(bestTeams(), values="LeagueId", names='League', color='League', title="Melhores times disponiveis (Top 100)")
    return fig


def grafic_static_players():
    fig = px.bar(bestPlayers().head(11), x="Overall", y="Name", color="Club",
                 title="Onze melhores jogadores base disponivel")  # COMERÇAR DO 80 ATE O 90

    return fig


def grafic_stats_player_select(Pace, Shoot, Passing, Dribling, Defend):
    fig = go.Figure(data=go.Scatterpolar(
        r=[int(float(Defend)), int(float(Pace)), int(float(Shoot)), int(float(Passing)), int(float(Dribling))],
        theta=["DefendingTotal", "PaceTotal", "ShootingTotal", "PassingTotal", "DribblingTotal"],
        fill='toself'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            ),
        ),
        showlegend=False
    )

    return fig


external_stylesheets = [{
    "rel": "stylesheet",
    "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css"
}]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


@app.callback(
    Output(component_id='title-player', component_property='children'),
    Input(component_id='type-filter', component_property='value')
)
def update_output_div(input_value):
    playerSelect = selectPlayer(input_value)

    imgSelect = playerSelect.PhotoUrl

    Pace = (str(playerSelect.PaceTotal).split(" ")[4].split("\n")[0])
    Shoot = (str(playerSelect.ShootingTotal).split(" ")[4].split("\n")[0])
    Passing = (str(playerSelect.PassingTotal).split(" ")[4].split("\n")[0])
    Dribling = (str(playerSelect.DribblingTotal).split(" ")[4].split("\n")[0])
    Defend = (str(playerSelect.DefendingTotal).split(" ")[4].split("\n")[0])

    if input_value != None:
        return html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.Div(
                                            children=[
                                                html.P(children=playerSelect.Overall, className="span")
                                            ],
                                            className="player-rating"
                                        ),
                                        html.Div(
                                            children=[
                                                html.P(children=playerSelect.Positions, className="span")
                                            ], className="player-position"
                                        ),
                                        html.Div(
                                            children=[
                                                html.P(children=playerSelect.Nationality, className="span")
                                            ], className="player-nation"
                                        ),
                                    ],
                                    className="player-master-info"
                                ),
                                html.Div(
                                    children=[
                                        html.Img(
                                            src=str(imgSelect).split(" ")[4].split("\n")[0],
                                            alt="player", draggable="false", className="img")
                                    ], className="player-picture"
                                )
                            ],
                            className="player-card-top"
                        ),

                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.Div(children=[
                                            html.P(children=playerSelect.FullName, className="SpanName")
                                        ], className="player-name"),

                                        html.Div(
                                            children=[
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.P(children=playerSelect.Age,
                                                                       className="player-feature-value"),
                                                                html.P(children="Age",
                                                                       className="player-feature-title"),
                                                            ], className="Span"
                                                        ),
                                                        html.Div(
                                                            children=[
                                                                html.P(children=playerSelect.Height,
                                                                       className="player-feature-value"),
                                                                html.P(children="Height",
                                                                       className="player-feature-title"),
                                                            ], className="Span"
                                                        ),

                                                    ], className="player-features-col"
                                                ),
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.P(children=playerSelect.Weight,
                                                                       className="player-feature-value"),
                                                                html.P(children="Weight",
                                                                       className="player-feature-title"),
                                                            ], className="Span"
                                                        ),
                                                        html.Div(
                                                            children=[
                                                                html.P(children=playerSelect.Weight,
                                                                       className="player-feature-value"),
                                                                html.P(children="ID",
                                                                       className="player-feature-title"),
                                                            ], className="Span"
                                                        )
                                                    ], className="player-features-col"
                                                )
                                            ], className="player-features"
                                        )
                                    ], className="player-info"
                                )
                            ], className="player-card-bottom"
                        )
                    ],
                    className="fut-player-card"
                ),
            ],
            className="wrapper"
        ), \
               html.Div(children=[
                   dcc.Graph(
                       id='graph-status-player',
                       figure=grafic_stats_player_select(Pace, Shoot, Passing, Dribling, Defend),
                       # figure = donut_top,
                       style={'height': 580}
                   ),
               ])
    else:
        return ""


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Br(),
                html.H1(
                    children="Analise sobre times e jogadores de futebol", className="header-title"
                ),
                html.P(
                    children="Dataset utilizado é sobre os jogadores e times disponiveis no FIFA 23!",
                    className="header-description",
                ),
                html.Br(),
            ],
            className="header",
        ),

        html.Div(
            children=[
                html.Br(),
                html.Div(
                    dbc.Row(
                        [
                            dbc.Col(html.Div(children="Selecione o jogador para obter suas estatisticas",
                                             className="text-menu")),
                            dbc.Col(children=[
                                dcc.Dropdown(
                                    id="type-filter",
                                    options=[
                                        {"label": avocado_type, "value": avocado_type}
                                        for avocado_type in players().Name
                                    ],
                                    value="",
                                    clearable=False,
                                    searchable=False,
                                    className="dropdown",
                                ),
                            ])
                        ]),
                ),
                html.Div(html.P(id="title-player")),
                html.Br()
            ],
            className="menu",
        ),
        html.Br(),

        html.Div(
            children=[
                html.Div(
                    dbc.Row(
                        [
                            dbc.Col(html.Div(children=[

                                dcc.Graph(
                                    id='graph-static-teams',
                                    figure=grafic_static_teams(),
                                    # figure = donut_top,
                                    style={'height': 580}
                                ),

                            ])),
                        ]),
                ),
            ],
            className="cards",
        ),

        html.Br(),

        html.Div(
            children=[
                html.Div(
                    dbc.Row(
                        [
                            dbc.Col(html.Div(children=[

                                dcc.Graph(
                                    id='graph-static-player',
                                    figure=grafic_static_players(),
                                    # figure = donut_top,
                                    style={'height': 580}
                                ),

                            ])),
                        ]),
                ),
            ],
            className="cards",
        ),

        html.Br(),

        html.Br(),
        dbc.Card(children=[
            dbc.CardBody([
                html.H4(children='',
                        style={'textAlign': 'center', 'color': 'white', 'background': 'rgba(0, 0, 0, 0.93)'}),
                html.H4(children=''),
                generate_table(team())
            ]),
        ]),
        html.Br()
    ])

if __name__ == '__main__':
    app.run_server(debug=False)
