from sklearn.linear_model import LinearRegression
import numpy as np

def linear_regression_line(X_values, y_values):
    X = X_values.values[:, np.newaxis]
    y = y_values.values[:, np.newaxis]
    # Fit linear regression model using scikit-learn
    lin_reg = LinearRegression()
    lin_reg.fit(X, y)
    # Make predictions w.r.t. 'x' and store it in a column called 'y_pred'
    return { 'prediction': lin_reg.predict(X_values.values[:, np.newaxis]),
             'X': X,
             'y': y,
             'intercept': lin_reg.intercept_,
             'slope': lin_reg.coef_}
