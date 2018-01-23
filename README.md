# Livia's Notes for Data Science
Starting from September 2016, I joined the data science immersive program at Galvanize Inc 
(previously known as Zipfian Academy). In this repo, I uploaded my data science-related notes 
and implementation for the machine learning algorithms for future reference.


## Feature Selection
- Why? 
  - Reduce overfitting by reducing # features and improve generalization
  - Easier to interpret
- Univariate Selection
  - correlation between y and xi (can't work for non-linear relation)
  - MIC: bins data and measures dependencies between y_bins and x_bins (bin selection is important `minepy`, can work for non-linear relation)
- Regression
  - Linear Regression (multi-collinearity problem, unstable coefs)
  - L1/Lasso: loss function + alpha * sigma (|beta|), to force cofficients for weak features as 0. The higher the alpha, the less the selected features. (multi-collinearity problem, unstable coefs)
  - L2/Ridge: loss function + alpha * sigma (beta^2), tend to spread out feature importances. (stable and likely nonzero coefs, but not good at feature selection)
- Random Forest
- Stability Selection, RFE
- [Reference: datadive](http://blog.datadive.net/category/feature-selection/)

