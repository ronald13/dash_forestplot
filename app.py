import os
import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash_trich_components as dtc
from forestplot import draw_forest_plot, prepare_forest_data


# read data
forestdata = prepare_forest_data("data/forest_data-1.csv", addcategoty=False)
forest_plot = draw_forest_plot(
        forestdata,
        inputheight=500,
        forest_font_size=10,
        annotation_list=["","","","","","","","","" ],
    )

app = Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server




theme_toggle = dtc.ThemeToggle(
        bg_color_dark='#232323',
        # icon_color_dark='#EDC575',
        # bg_color_light='#07484E',
        icon_color_light='#C8DBDC',
        tooltip_text='Toggle light/dark theme'
    )
theme_switch = html.Div(theme_toggle, className='theme__switcher')
header = html.Div([
        html.H1('ForestPlot'),
        html.P('Forest description'),
], className='dash__header')

footer = html.Div([
    html.P('Created by:', style={}),

], className='dash__footer')

app.layout = html.Div([
                    header,
                    theme_switch,
                    html.Div([
                        html.Div([
                            html.Div('ForestPlot - All information ', className="table_name"),
                            dcc.Graph(
                                                    figure=forest_plot,
                                                    config={"displayModeBar": False},
                                                    style={
                                                        "width": "100vw",
                                                        "max-width": "100%",
                                                        "max-height": "100%",
                                                        "margin": "0 auto",
                                                    },
                                                )

                        ], style={'width':'100%'}),
                    ], className='dash__graph_block'),
                    footer

                ], className='dash__wrapper', style={})


# don't run when imported, only when standalone
if __name__ == '__main__':
    port = os.getenv("DASH_PORT", 8053)
    app.run_server(debug=True,  port=port)
