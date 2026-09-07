# Predictive-model notes

The original predictive-model notebook trains four classifiers—Logistic Regression, SVM, Decision Tree and KNN—using standardized features and an 80/20 train/test split with `random_state=2`.

Reported cross-validation scores in the supplied notebook:

| Model | Reported CV score |
|---|---:|
| Logistic Regression | 84.64% |
| SVM | 84.82% |
| Decision Tree | 87.50% |
| KNN | 84.82% |

The notebook reports **83.33% test accuracy for each of the four models**. Its final cell therefore labels Logistic Regression as the “best” only because `max()` returns the first model among tied values. For a professional report, the safer conclusion is: **the four models tie on the recorded test accuracy, while Decision Tree has the highest recorded cross-validation score**.

The supplied notebook also contains a Decision Tree grid-search warning because the `max_features='auto'` option is invalid in the installed scikit-learn version. The GitHub version keeps the original notebook for traceability rather than silently changing its historical results.
