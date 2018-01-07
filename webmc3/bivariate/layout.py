import dash_html_components as html

from ..common.components import selector
from .components import scatter_graph


def layout(trace_info):
    untransformed_varnames = trace_info.get_varnames()
    x_varname = untransformed_varnames[0]
    y_varname = untransformed_varnames[1]

    layout = html.Div([
        html.Center([
            selector('bivariate-x', trace_info, x_varname),
            selector('bivariate-y', trace_info, y_varname),
            scatter_graph(trace_info, x_varname, y_varname)
        ])
    ])

    return layout
