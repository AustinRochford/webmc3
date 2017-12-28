from decorator import decorator

import dash_html_components as html

from .components import *

LOGO = html.Img(
    src="https://camo.githubusercontent.com/2af4bb9d3ff6744a6ad1aab0b2b916b5efee8b49/68747470733a2f2f63646e2e7261776769742e636f6d2f70796d632d646576732f70796d63332f6d61737465722f646f63732f6c6f676f732f7376672f50794d43335f62616e6e65722e737667",
    width=300
)


@decorator
def with_header(layout_func, *args, **kwargs):
    return html.Div([
        LOGO, html.Hr(),
        layout_func(*args, **kwargs)
    ])


@with_header
def var_layout(trace):
    varname = trace.varnames[0]

    return html.Div([
        var_selector(trace, varname),
        var_table(trace, varname)
    ])


def var_table(trace, varname):
    return html.Table([
        html.Tr([
            html.Td(
                [var_hist(trace, varname)],
                style={'width': '40%'}
            ),
            html.Td(
                [var_lines(trace, varname)],
                style={'width': '40%'}
            )
        ]),
        html.Tr([
            html.Td([
                var_gelman_rubin(trace, varname),
                var_effective_n(trace, varname)
            ]),
            html.Td([var_autocorr(trace, varname)])
        ])
    ],
    style={'tableLayout': 'fixed'})
