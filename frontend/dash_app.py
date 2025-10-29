from dash import Dash, html
import dash
import dash_bootstrap_components as dbc
import components_.header as header

app = Dash(__name__, use_pages= True, external_stylesheets=[dbc.themes.LUX])

header = header.create_header()

app.layout = html.Div([
    header,
    dash.page_container
])


if __name__ == '__main__':
    print("Registered pages/routes:")
    for p in dash.page_registry.values():
        print(f"- {p['name']} -> {p['path']}")
    app.run(debug=True)