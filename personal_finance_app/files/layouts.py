import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
# Define Page Layouts
def home_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to the Personal Finance App", className="text-center my-4")),
        ]),
        dbc.Row([
            dbc.Col(html.P("Navigate to different sections using the links below:", className="text-center")),
        ]),
        dbc.Row([
            dbc.Col(dbc.Nav([
                dbc.NavLink("Dashboard", href="/dashboard", className="btn btn-primary mx-2"),
                dbc.NavLink("About", href="/about", className="btn btn-secondary mx-2"),
            ], className="justify-content-center")),
        ]),
    ])

def dashboard_layout(df):
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Personal Finance Dashboard", className="text-center my-4")),
        ]),
        dbc.Row([
            dbc.Col(dbc.Button("Go to Home", href="/", color="primary", className="mb-4")),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id="category-filter",
                    options=[{"label": cat, "value": cat} for cat in df["Category"].unique()],
                    placeholder="Select a Category",
                    multi=True,
                ),
                html.Div(className="my-2"),
                dcc.DatePickerRange(
                    id="date-range-filter",
                    start_date=df["Date"].min(),
                    end_date=df["Date"].max(),
                ),
            ], width=6),
        ]),
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id="data-table",
                    columns=[{"name": col, "id": col} for col in df.columns],
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "left"},
                    style_header={"fontWeight": "bold"},
                ),
            ], width=12, className="my-4"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="spending-chart"), width=12),
        ]),
    ])

def about_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("About the Personal Finance App", className="text-center my-4")),
        ]),
        dbc.Row([
            dbc.Col(html.P(
                "This app helps you track your spending and visualize your expenses in an intuitive way.",
                className="text-center"
            )),
        ]),
        dbc.Row([
            dbc.Col(dbc.Button("Go to Home", href="/", color="primary", className="my-4 text-center")),
        ]),
    ])