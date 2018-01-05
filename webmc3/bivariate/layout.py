import dash_html_components as html

from ..common.components import selector
from ..utils import get_varnames
from .components import scatter_graph


def layout(trace):
    untransformed_varnames = get_varnames(trace, include_transformed=False)
    x_varname = untransformed_varnames[0]
    y_varname = untransformed_varnames[1]

    layout = html.Div([
        html.Center([
            selector('bivariate-x', trace, x_varname),
            selector('bivariate-y', trace, y_varname),
            scatter_graph(trace, x_varname, y_varname)
        ])
    ])

    return layout
