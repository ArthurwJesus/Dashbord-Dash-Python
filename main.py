
from dash import dash, html, dcc, Output, Input
import plotly.express as px
from formatDataset import *
import dash_bootstrap_components as dbc


def generate_table(dataframe, max_rows=15):
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
    fig = px.pie(bestTeams().head(100), values="Overall", names='League', color='League',title="Beast Teams (Top 100)")
    return fig


def grafic_static_players():
    fig = px.bar(bestPlayers().head(11), x="Name", y="Overall", color="Club", barmode="group",
                 title="Beast Players(Top 11)")
    return fig


def grafic_stats_player_select(playerSelect):
    Pace = (str(playerSelect.PaceTotal).split(" ")[4].split("\n")[0])
    Shoot = (str(playerSelect.ShootingTotal).split(" ")[4].split("\n")[0])
    Passing = (str(playerSelect.PassingTotal).split(" ")[4].split("\n")[0])
    Dribling = (str(playerSelect.DribblingTotal).split(" ")[4].split("\n")[0])
    Defend = (str(playerSelect.DefendingTotal).split(" ")[4].split("\n")[0])

    fig = px.pie(playerSelect, values=[Pace,Shoot,Passing,Dribling,Defend], names=["PaceTotal","ShootingTotal","PassingTotal","DribblingTotal","DefendingTotal"],title="Beast Teams (Top 100)")

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

    if input_value != None:
        return html.Br(), \
               html.Div(children=[
                   html.Div(children=[
                       html.Img(src=str(imgSelect).split(" ")[4].split("\n")[0], alt=str(imgSelect),className="img"),
                       html.P(playerSelect.FullName),  # Name
                   ], className="playerTop"),
                   html.P(playerSelect.Overall, className="infos"),  # Overall
                   html.P(playerSelect.Positions, className="infos"),  # Position
                   html.P(playerSelect.Nationality, className="infos"),  # Nationality
                   dbc.Row(
                       [
                           dbc.Col(children=[html.P("Age: "),html.P(playerSelect.Age)]),  # Age
                           dbc.Col(children=[html.P("Height: "),html.P(playerSelect.Height)]),  # Height
                           dbc.Col(children=[html.P("Weight: "),html.P(playerSelect.Weight)]), # Weight
                       ],className="infos"),
                   # Grafico das stats
                   dbc.CardBody([
                       dcc.Graph(
                           id='graph-status-player',
                           figure=grafic_stats_player_select(playerSelect),
                           # figure = donut_top,
                           style={'height': 580}
                       ),
                   ])
               ]
               )
    else:
        return ""


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Br(),
                html.H1(
                    children="FIFA 23 Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze of Teams and Player"
                             " for the FIFA 23 stats",
                    className="header-description",
                ),
                html.Br(),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Br(),
                html.Br(),
                html.Div(
                    dbc.Row(
                        [
                            dbc.Col(html.Div(children="Select player to get stats", className="text-menu")),
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

        #Grafics
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Div(dbc.Card(children=[
                            dbc.CardBody([
                                dcc.Graph(
                                    id='graph-static-teams',
                                    figure=grafic_static_teams(),
                                    # figure = donut_top,
                                    style={'height': 580}
                                ),
                            ])
                        ]))),
                        dbc.Col(html.Div(dbc.Card(children=[
                            dbc.CardBody([
                                dcc.Graph(
                                    id='graph-static-player',
                                    figure=grafic_static_players(),
                                    # figure = donut_top,
                                    style={'height': 580}
                                ),
                            ])
                        ]))),
                    ]
                ),
            ]
        ),
        html.Br(),
        dbc.Card(children=[
            html.H4(children='',
                    style={'textAlign': 'center', 'color': 'white', 'background': 'rgba(0, 0, 0, 0.93)'}),

            dbc.CardBody([
                html.H4(children=''),
                generate_table(team())
            ]),
        ]),
        html.Br()
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
