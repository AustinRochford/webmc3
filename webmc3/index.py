import dash
from dash import dependencies as dep
import dash_core_components as dcc
import dash_html_components as html

from . import univariate


LOGO = html.Img(
    src="https://camo.githubusercontent.com/2af4bb9d3ff6744a6ad1aab0b2b916b5efee8b49/68747470733a2f2f63646e2e7261776769742e636f6d2f70796d632d646576732f70796d63332f6d61737465722f646f63732f6c6f676f732f7376672f50794d43335f62616e6e65722e737667",
    width=300
)


def add_callbacks(app, trace):
    univariate_layout = univariate.layout(trace)

    @app.callback(
        dep.Output('page-content', 'children'),
        [dep.Input('url', 'pathname')]
    )
    def update_page_content(pathname):
        if pathname in ['/', '/univariate']:
            return univariate_layout
        elif pathname == '/bivariate':
            return html.Div([html.H1("NOT YET IMPLEMENTED")])

    univariate.add_callbacks(app, trace)


def layout(trace):
    layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div([
            LOGO,
            html.P([
                dcc.Link("Univariate", href='/univariate'),
                dcc.Link("Bivariate", href='/bivariate'),
            ]),
            html.Hr()
        ]),
        html.Div(id='page-content')
    ])

    return layout
