### Basics 

**Feature reduction, extraction, and selection** - all hep to reduce extra computational requirements by focusing on specific features to train model without loss of information. Also depending on the model, helps explainability of model. Ex. pruning decision trees

**Curse of High Dimensionality** - each additional feature to include in training set requires exponentially more data to produce statistical signifiance. 

**Imbalanced Classes** - when the target variable to identify is a minority of the dataset, undersampling of other classes or duplicating minority data points is recommended before training.

**Over fitting / training** - when the model is over fit with training set, it performs poorly against the validation set and novel data. To avoid over fitting randomization, pruning, and other strategies are implemented. 