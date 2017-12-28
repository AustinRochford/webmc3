import dash

from .components import *
from .layout import var_layout


def webmc3_app(trace):
    """
    Generate a Dash/Flask app to visualize the given trace
    """
    app = dash.Dash() 
    app.title = "webmc3"

    app.layout = var_layout(trace)
    add_var_callbacks(app, trace)
    
    return app
