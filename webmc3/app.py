import dash

from .components import *
from .layout import get_var_layout


def webmc3_app(trace):
    app = dash.Dash() 
    app.title = "webmc3"
    app.layout = get_var_layout(trace)

    @app.callback(
        dash.dependencies.Output('var-hist', 'figure'),
        [dash.dependencies.Input('var-selector', 'value')]
    )
    def update_var_hist(varname):
        return var_hist_figure(trace, varname)

    @app.callback(
        dash.dependencies.Output('var-lines', 'figure'),
        [dash.dependencies.Input('var-selector', 'value')]
    )
    def update_var_lines(varname):
        return var_lines_figure(trace, varname)
    
    return app
