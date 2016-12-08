# Regression
## Linear Regression
## Ridge Regression (L2)
## Lasso Regression (L1)

## Sample code for regression
### Basic Modeling / Transformation
```python
from sklearn.cross_validation import train_test_split ## for train/test data preparation
from sklearn import preprocessing ## for standarizing/scaling the data
from sklearn.linear_model import LinearRegression, Ridge, Lasso ## for regression models
from sklearn.metrics import mean_squared_error ## for regression evaluation

## data preparation
## need x, y
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.15, random_state=319)
scaler = preprocessing.StandardScaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

## modeling
mdl = [LinearRegression(), Ridge(RIDGE_ALPHA), Lasso(LASSO_ALPHA)][0] ## change the index if needed
mdl.fit(x_train, y_train)

## prediction
y_pred = mdl.predict(x_test)

## evaluation
mse_train = mean_squared_error( y_train, mdl.predict(x_train) )
mse_test = mean_squared_error( y_test, mdl.predict(x_test) )
```

### Advanced Modeling / Transformation
#### Polynomial Fit
```python
from sklearn.preprocessing import PolynomialFeatures

## x.shape = (400,2)
## x_poly2.shape = (400, 6). "6" includes 1, x1, x1**2, x_poly2, x_poly2**2, x1*x_poly2
poly = PolynomialFeatures(2)
x_poly2 = poly.fit_transform(x)
mdl.fit(x_poly2, y)

```
