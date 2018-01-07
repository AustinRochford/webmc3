import dash

from . import index
from .traceinfo import TraceInfo


def webmc3_app(trace):
    """
    Generate a Dash/Flask app to visualize the given trace
    """
    trace_info = TraceInfo(trace)

    app = dash.Dash() 
    app.title = "webmc3"
    app.layout = index.LAYOUT

    app.config.suppress_callback_exceptions = True
    index.add_callbacks(app, trace_info)

    return app
