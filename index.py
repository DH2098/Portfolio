import os
 
from dash import html, dcc
from dash.dependencies import Input, Output
import feffery_antd_components as fac

from app import app
server = app.server

from layouts import (
    Navbar,
    main_layout,
    trend_layout,
    revenue_layout,
    keyword_layout,
    corr_layout,
    recommender_layout
)
import callbacks

app_name = os.getenv("DASH_APP_PATH", "/movie-recommender")

nav = Navbar()

content = html.Div([dcc.Location(id="url"), html.Div(id="page-content")])
container = fac.AntdLayout(
    [
        nav,
        fac.AntdContent(content)
    ]
)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname in [app_name, app_name + "/"]:
        return html.Div()
    elif pathname.endswith("/main"):
        return main_layout
    elif pathname.endswith("/trend"):
        return trend_layout
    elif pathname.endswith("/revenue"):
        return revenue_layout
    elif pathname.endswith("/keyword"):
        return keyword_layout
    elif pathname.endswith("/corr"):
        return corr_layout
    elif pathname.endswith("/recommender"):
        return recommender_layout
    else:
        return main_layout

def index():
    layout = html.Div(container)
    return layout

app.layout = index()

if __name__ == "__main__":
    app.run_server()