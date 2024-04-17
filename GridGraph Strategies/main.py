from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from io import BytesIO
import base64

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def main():
    with open("index.html", "r") as f:
        return f.read()

@app.post("/upload/", response_class=HTMLResponse)
async def handle_upload(file: UploadFile = File(...)):
    if file.filename.endswith('.csv'):
        dataframe = pd.read_csv(BytesIO(await file.read()))
        
        # Process data and generate plots
        plot_images = process_data_and_plot(dataframe)
        
        # Convert plots to inline HTML images and wrap every two plots side by side
        html_images = []
        for i, img in enumerate(plot_images):
            buffer = BytesIO()
            img.savefig(buffer, format="png")
            buffer.seek(0)
            image_png = buffer.getvalue()
            encoded = base64.b64encode(image_png).decode('utf-8')
            html_img = f'<img src="data:image/png;base64,{encoded}" class="plot">'
            if i % 2 == 0 and i != 0:
                html_images.append('</div>')
            if i % 2 == 0:
                html_images.append('<div class="row">')  # Start a new row every two plots
            html_images.append(html_img)
        if len(html_images) % 2 != 0:
            html_images.append('</div>')  # Close the last row if there's an odd number of plots
        
        # Create an enhanced HTML page to display the images
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Analysis Results</title>
            <link rel="stylesheet" href="styles.css">
        </head>
        <body>
            <header>
                    <h1 style="text-align: center;">Data Analysis Dashboard</h1>
            </header>
            <div class="dashboard">
                <section class="content">
                    """ + "".join(html_images) + """
                </section>
            </div>
            <footer>
                <p>© 2024 Data Analysis App</p>
            </footer>
        </body>
        </html>
        """
        return html_content
    return HTMLResponse(content="<html><body><p>Invalid file format. Please upload a CSV file.</p></body></html>", status_code=400)

def process_data_and_plot(df):
    figs = []

    # # Univariate Analysis Plots
    # fig, ax = plt.subplots()
    # sns.displot(df['Annual Income (k$)'])
    # figs.append(fig)
    
    # More Univariate Plots
    columns = ['Age', 'Annual Income (k$)', 'Spending Score (1-100)']
    for col in columns:
        fig, ax = plt.subplots()
        sns.kdeplot(df[col], shade=True, ax=ax)
        figs.append(fig)
    
    # Bivariate Analysis Plots
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x='Annual Income (k$)', y='Spending Score (1-100)', ax=ax)
    figs.append(fig)

    # Clustering - KMeans for Annual Income
    kmeans = KMeans(n_clusters=3)
    df['Income Cluster'] = kmeans.fit_predict(df[['Annual Income (k$)']])
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x='Annual Income (k$)', y='Spending Score (1-100)', hue='Income Cluster', palette='viridis', ax=ax)
    figs.append(fig)

    # Prepare and fit model for multivariate clustering
    df_numeric = df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']]
    kmeans = KMeans(n_clusters=5)
    df['Cluster'] = kmeans.fit_predict(df_numeric)
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x='Annual Income (k$)', y='Spending Score (1-100)', hue='Cluster', palette='viridis', ax=ax)
    figs.append(fig)

    return figs