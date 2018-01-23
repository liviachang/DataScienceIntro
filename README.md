# Livia's Notes for Data Science
Starting from September 2016, I joined the data science immersive program at Galvanize Inc 
(previously known as Zipfian Academy). In this repo, I uploaded my data science-related notes 
and implementation for the machine learning algorithms for future reference.


## Feature Selection
- Why? 
  - Reduce overfitting by reducing # features and improve generalization
  - Easier to interpret
- Univariate Selection via correlation between y and xi
  - Cons: linear only
- Univariate Selection via MIC: bins data and measures dependencies (bin selection is important `minepy`)
  - Pros: able to handle y=x^2
  - Cons: output not comparable acroess datasets. Not for continuous variables
- Regression and Regularization
- Random Forest
- Stability Selection, RFE
- [Reference: datadive](http://blog.datadive.net/category/feature-selection/)

