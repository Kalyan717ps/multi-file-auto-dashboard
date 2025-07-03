import plotly.express as px

def generate_chart_options(df):
    options = ["Bar Chart", "Line Chart", "Pie Chart", "Map (Lat/Lon)", "Scatter Plot", "Histogram", "Heatmap"]
    return options

def create_chart(df, config):
    chart_type = config["type"]
    x = config["x"]
    y = config["y"]
    color = config["color"]
    colors = ['#F2C811', '#01B8AA', '#FD625E', '#8AD4EB', '#A66999', '#3599B8', '#B6B6B6']

    if chart_type == "Bar Chart":
        return px.bar(df, x=x, y=y, color=color, color_discrete_sequence=colors)
    elif chart_type == "Line Chart":
        return px.line(df, x=x, y=y, color=color, color_discrete_sequence=colors)
    elif chart_type == "Pie Chart":
        return px.pie(df, names=x, color=color, color_discrete_sequence=colors)
    elif chart_type == "Map (Lat/Lon)" and 'latitude' in df.columns and 'longitude' in df.columns:
        return px.scatter_mapbox(df, lat='latitude', lon='longitude', color=color, zoom=3,
                                 mapbox_style="carto-positron", color_discrete_sequence=colors)
    elif chart_type == "Scatter Plot":
        return px.scatter(df, x=x, y=y, color=color, color_discrete_sequence=colors)
    elif chart_type == "Histogram":
        return px.histogram(df, x=x, color=color, color_discrete_sequence=colors)
    elif chart_type == "Heatmap":
        corr = df.select_dtypes(include='number').corr()
        return px.imshow(corr, color_continuous_scale='YlGnBu')
    else:
        return px.scatter(df, x=x, y=y, color=color)
