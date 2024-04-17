# ChartCraft Insights

## Overview
ChartCraft Insights is an advanced analytics tool designed to offer deep insights into customer segmentation using machine learning techniques. It provides a web-based interface for uploading customer data, visualizing segments, and deriving actionable insights to optimize business strategies.

## Features
- **Data Upload**: Users can upload their customer data through a simple CSV file format.
- **Interactive Visualization**: The tool generates interactive plots that provide a visual representation of the different customer segments.
- **Segmentation Analysis**: Utilizes clustering algorithms to segment the customer data effectively.
- **Optimization Insights**: Offers recommendations for targeting specific customer segments based on the analysis.

## How to Use
1. **Start the Application**: Run the `main.py` file to launch the server.
2. **Access the Web Interface**: Open a browser and go to `localhost:8000` to access the GraphGrid Insights landing page.
3. **Upload Data**: Use the upload section to submit your CSV file containing customer data.
4. **View Results**: After uploading the data, the tool processes it and displays the segmentation results in the form of plots and insights.

## Technologies Used
- **FastAPI**: For backend server operations.
- **Pandas and Scikit-Learn**: For data manipulation and running clustering algorithms.
- **Matplotlib and Seaborn**: For generating static plots of the data.
- **HTML/CSS**: For frontend presentation.

## Project Structure
- `main.py`: The main server file that handles web requests and integrates all components.
- `styles.css` and `styles1.css`: CSS files for styling the web interface.
- `index.html` and `landingpage.html`: HTML files for the web interface.
- `Mall_Customers.csv`: Example dataset for testing and demonstration.

## Setup and Installation
1. **Clone the Repository**: Clone this repository to your local machine.
2. **Install Dependencies**: Run `pip install -r requirements.txt` to install required Python libraries. Ensure FastAPI and Uvicorn (an ASGI server for FastAPI) are included in the requirements.
3. **Run the Server**: Execute `uvicorn main:app --reload` to start the FastAPI server. This command assumes that `main.py` contains a FastAPI application instance named `app`.
4. **Open the Web Interface**: Navigate to `http://localhost:8000` in your web browser to access the GraphGrid Insights interface.




