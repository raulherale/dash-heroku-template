app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("Gender Wage Gap study using \n the 2019 General Social Survey")
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
