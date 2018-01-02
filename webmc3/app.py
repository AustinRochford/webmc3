import dash

from . import index


def webmc3_app(trace):
    """
    Generate a Dash/Flask app to visualize the given trace
    """
    app = dash.Dash() 
    app.title = "webmc3"
    app.layout = index.layout(trace)

    app.config.suppress_callback_exceptions = True
    index.add_callbacks(app, trace)

    return app
