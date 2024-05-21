import os
from dotenv import load_dotenv  # To load environment variables
import uvicorn  # To run the FastAPI server
from fastapi import FastAPI, File, UploadFile  # FastAPI components
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd  # For data processing
from io import BytesIO  # For handling CSV data
import base64  # For encoding plot images
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import asyncio

# Load environment variables from the .env file
# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

HOST = os.environ["HOST"]
PORT = int(os.environ["PORT"])

# Assuming 'app' is your FastAPI application object, defined in 'my_fastapi_app.py'
app_import_string = "main:app"
# Initialize FastAPI app
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# # Open landing page on startup
# @app.on_event("startup")
# async def open_landing_page():
#     import webbrowser
#     await asyncio.sleep(1)  # Allow server time to start
#     webbrowser.open(f"http://{HOST}:{PORT}/")  # Open the landing page

@app.get('/healthz')
def health():
    return 'OK'

# Serve landing page
@app.get("/", response_class=HTMLResponse)
async def serve_landing_page():
    with open("landingpage.html", "r") as f:
        return f.read()

# Serve CSV upload page
@app.get("/index", response_class=HTMLResponse)
async def serve_upload_page():
    with open("index.html", "r") as f:
        return f.read()

# Function to generate plots and return base64-encoded images
def process_data_and_plot(dataframe):
    plot_images = []

    # Univariate analysis
    for col in ['Age', 'Annual Income (k$)', 'Spending Score (1-100)']:
        fig, ax = plt.subplots(figsize=(6, 5), dpi=100)  # Smaller plot size
        sns.kdeplot(dataframe[col], fill=True, ax=ax)
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.read()
        plot_images.append(base64.b64encode(image_png).decode("utf-8"))

    # Bivariate analysis
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)  # Smaller plot size
    sns.scatterplot(data=dataframe, x='Annual Income (k$)', y='Spending Score (1-100)', ax=ax)
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.read()
    plot_images.append(base64.b64encode(image_png).decode("utf-8"))

# Define a custom color palette
    custom_palette = ["#FF6347", "#4682B4", "#32CD32", "#FFD700", "#9370DB"]

    # Clustering Analysis with Specified Colors
    kmeans = KMeans(n_clusters=3)  # Cluster into 3 groups
    dataframe['Income Cluster'] = kmeans.fit_predict(dataframe[['Annual Income (k$)']])
    
    # Create scatter plot with specified palette
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)  # Smaller plot
    sns.scatterplot(
        data=dataframe,
        x='Annual Income (k$)',
        y='Spending Score (1-100)',
        hue='Income Cluster',
        palette=custom_palette[:3],  # Use first 3 colors from the custom palette
        ax=ax
    )
    
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.read()
    plot_images.append(base64.b64encode(image_png).decode("utf-8"))

    # Multivariate Clustering Analysis with Custom Colors
    kmeans = KMeans(n_clusters=5)
    dataframe['Cluster'] = kmeans.fit_predict(dataframe[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']])
    
    # Create scatter plot with specified palette
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    sns.scatterplot(
        data=dataframe,
        x='Annual Income (k$)',
        y='Spending Score (1-100)',
        hue='Cluster',
        palette=custom_palette[:5],  # Use first 5 colors from the custom palette
        ax=ax
    )
    
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.read()
    plot_images.append(base64.b64encode(image_png).decode("utf-8"))

    return plot_images  # Return list of base64-encoded images

@app.post("/upload", response_class=HTMLResponse)
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return HTMLResponse(content="<p>Invalid file format. Please upload a CSV file.</p>", status_code=400)

    # Read the CSV data
    dataframe = pd.read_csv(BytesIO(await file.read()))

    # Generate plots
    plot_images = process_data_and_plot(dataframe)

    # Create the HTML content with plots in pairs
    plot_content = []
    for i in range(0, len(plot_images), 2):
        # Start a new row for every two plots
        plot_content.append('<div class="row">')
        plot_content.append(f'<img src="data:image/png;base64,{plot_images[i]}">')  # First plot in the row
        if i + 1 < len(plot_images):
            plot_content.append(f'<img src="data:image/png;base64,{plot_images[i + 1]}">')  # Second plot
        plot_content.append('</div>')

    # Load the HTML template
    with open("analysis_results.html", "r") as f:
        html_template = f.read()

    # Replace the placeholder with the correct content
    final_html = html_template.replace("{{ plot_images }}", "".join(plot_content))

    return HTMLResponse(content=final_html)

# Run FastAPI server with uvicorn
if __name__ == "__main__":
    uvicorn.run(app_import_string, host=HOST, port=PORT, reload=True)
