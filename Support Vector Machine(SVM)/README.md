# SVM Prediction Project

## Overview
This project implements a Support Vector Machine (SVM) to predict categories based on a given dataset. It uses the SVM model from the scikit-learn library, focusing on the linear kernel for its simplicity and effectiveness in high-dimensional spaces.

## Installation
To run this project, you need Python installed on your system along with the following packages:
- `numpy`
- `pandas`
- `scikit-learn`
- `matplotlib` (optional, for plotting)

You can install these packages using pip:
```bash
pip install numpy pandas scikit-learn matplotlib
```

# Usage
To use this project, load the Jupyter notebook and run the cells sequentially. The main operations include:

Loading the dataset.
Splitting the dataset into training and testing sets.
Creating and training the SVM model with a linear kernel.
Evaluating the model's performance on the test set.
Making predictions with the trained model.

# Example of making a prediction:

python
Copy code
```
# Example input features
features = [6.7, 3.0, 5.2, 2.3]
prediction = model.predict([features])
print("Predicted class:", prediction)
```
