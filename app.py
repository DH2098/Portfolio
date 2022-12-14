import dash
import dash_bootstrap_components as dbc


# set app variable with dash, set external style to bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

# set app callback exceptions to true
app.config.suppress_callback_exceptions = True
 
app.title = "영화 추천 시스템"