import dash
import dash_core_components as dcc
import dash_html_components as html

from . import univariate

LOGO = html.Img(
    src="https://camo.githubusercontent.com/2af4bb9d3ff6744a6ad1aab0b2b916b5efee8b49/68747470733a2f2f63646e2e7261776769742e636f6d2f70796d632d646576732f70796d63332f6d61737465722f646f63732f6c6f676f732f7376672f50794d43335f62616e6e65722e737667",
    width=300
)



def webmc3_app(trace):
    """
    Generate a Dash/Flask app to visualize the given trace
    """
    app = dash.Dash() 
    app.title = "webmc3"

    app.config.suppress_callback_exceptions = True

    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div([LOGO, html.Hr()]),
        html.Div(id='page-content')
    ])

    univariate_layout = univariate.layout(app, trace)

    @app.callback(
        dash.dependencies.Output('page-content', 'children'),
        [dash.dependencies.Input('url', 'pathname')]
    )
    def update_page_content(pathname):
        if pathname in ['/', '/univariate']:
            return univariate_layout
    
    
    return app
