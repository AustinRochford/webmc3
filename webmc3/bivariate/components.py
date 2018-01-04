from dash import dependencies as dep
import dash_core_components as dcc
from plotly import graph_objs as go

from ..common.components import add_include_transformed_callback


def add_callbacks(app, trace):
    add_include_transformed_callback(app, 'bivariate-x', trace)
    add_include_transformed_callback(app, 'bivariate-y', trace)

    @app.callback(
        dep.Output('bivariate-scatter', 'figure'),
        [
            dep.Input('bivariate-x-selector', 'value'),
            dep.Input('bivariate-y-selector', 'value')
        ]
    )
    def update_bivariate_scatter(x_varname, y_varname):
        return scatter_figure(trace, x_varname, y_varname)


def scatter_figure(trace, x_varname, y_varname):
    return {
        'data': [
            go.Scatter(
                x=trace[x_varname],
                y=trace[y_varname],
                mode='markers'
            )
        ],
        'layout': go.Layout(
            xaxis={'title': x_varname},
            yaxis={'title': y_varname}
        )
    }


def scatter_graph(trace, x_varname, y_varname):
    return dcc.Graph(
        id='bivariate-scatter',
        figure=scatter_figure(trace, x_varname, y_varname)
    )
