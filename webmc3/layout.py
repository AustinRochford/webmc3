import dash_html_components as html

from .components import *


def get_var_layout(trace):
    varname = trace.varnames[0]

    return html.Div([
        var_selector(trace, varname),
        get_var_table(trace, varname)
    ])


def get_var_table(trace, varname):
    return html.Table([
        html.Tr([
            html.Td([var_hist(trace, varname)]),
            html.Td([var_lines(trace, varname)])
        ])
    ])
