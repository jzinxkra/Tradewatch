import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import requests

app = dash.Dash(__name__)
app.title = "TradeWatch Dashboard"

API_BASE = "http://localhost:8000"
symbols = ['btcusdt', 'ethusdt', 'bnbusdt', 'solusdt', 'xrpusdt', 'lrcusdt']

app.layout = html.Div([
    html.H1("📈 TradeWatch - Live Market Monitor"),
    dcc.Dropdown(
        id='symbol-dropdown',
        options=[{'label': sym.upper(), 'value': sym} for sym in symbols],
        value='btcusdt'
    ),
    html.Div(id='stats-output'),
    dcc.Graph(id='price-graph', config={'displayModeBar': False}),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0)
])

@app.callback(
    Output('stats-output', 'children'),
    Output('price-graph', 'figure'),
    Input('interval-component', 'n_intervals'),
    Input('symbol-dropdown', 'value')
)
def update_dashboard(n, symbol):
    try:
        response = requests.get(f"{API_BASE}/summary/{symbol}")
        if response.status_code != 200:
            return "No data available.", go.Figure()

        data = response.json()[symbol]
        prices = [data['avg_price']] * 20

        stats = html.Div([
            html.H3(f"{symbol.upper()} Summary"),
            html.P(f"% Change: {data['price_change_pct']}%"),
            html.P(f"Avg Price: {data['avg_price']}$"),
            html.P(f"Total Volume: {data['total_volume']}")
        ])

        fig = go.Figure()
        fig.add_trace(go.Scatter(y=prices, mode='lines+markers', name='Price'))
        fig.update_layout(title=f"Live Avg Price - {symbol.upper()}", xaxis_title='Time', yaxis_title='Price')

        return stats, fig

    except Exception as e:
        return f"Error fetching data: {e}", go.Figure()

if __name__ == '__main__':
    app.run_server(debug=True)
