import inspect

from flask import Flask
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
from layouts import *

# Sample DataFrame
data = {
    "Date": ["2024-12-01", "2024-12-02", "2024-12-03", "2024-12-04"],
    "Category": ["Food", "Transport", "Shopping", "Food"],
    "Amount": [20, 15, 40, 30],
    "Payment Method": ["Card", "Cash", "Card", "Card"],
}
df = pd.DataFrame(data)

# Flask app
server = Flask(__name__)

# Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],  # Using Bootstrap theme
    suppress_callback_exceptions=True,
)

# Main layout with dynamic content
app.layout = dbc.Container([
    dcc.Location(id="url", refresh=False),  # Tracks the URL
    html.Div(id="page-content"),  # Container for page content
])

# Callbacks to update page content
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/dashboard":
        return dashboard_layout(df)
    elif pathname == "/about":
        return about_layout()
    else:
        return home_layout()


# Dashboard Callbacks
@app.callback(
    [Output("data-table", "data"),
     Output("spending-chart", "figure")],
    [Input("category-filter", "value"),
     Input("date-range-filter", "start_date"),
     Input("date-range-filter", "end_date")]
)
def update_dashboard(selected_categories, start_date, end_date):
    # Filter data based on inputs
    filtered_df = df.copy()
    if selected_categories:
        filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df["Date"] >= start_date) & (filtered_df["Date"] <= end_date)
        ]

    # Create a bar chart of spending by category
    fig = px.bar(
        filtered_df,
        x="Category",
        y="Amount",
        color="Payment Method",
        title="Spending by Category",
    )

    return filtered_df.to_dict("records"), fig

if __name__ == "__main__":
    server.run(debug=True)
