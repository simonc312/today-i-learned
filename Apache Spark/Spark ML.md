# Spark ML

MLlib is Spark’s machine learning (ML) library. Its goal is to make practical machine learning scalable and easy. At a high level, it provides tools such as:

    ML Algorithms: common learning algorithms such as classification, regression, clustering, and collaborative filtering
    Featurization: feature extraction, transformation, dimensionality reduction, and selection
    Pipelines: tools for constructing, evaluating, and tuning ML Pipelines
    Persistence: saving and load algorithms, models, and Pipelines
    Utilities: linear algebra, statistics, data handling, etc.

As of Spark 2.0, Dataframes are primary API instead of RDD for Spark ML

To use MLlib in Python, you will need NumPy version 1.4 or newer.

MLlib standardizes APIs for machine learning algorithms to make it easier to combine multiple algorithms into a single pipeline, or workflow. The Pipelines API is mostly inspired by the scikit-learn project.



    DataFrame: This ML API uses DataFrame from Spark SQL as an ML dataset, which can hold a variety of data types. E.g., a DataFrame could have different columns storing text, feature vectors, true labels, and predictions.

    Transformer: A Transformer is an algorithm which can transform one DataFrame into another DataFrame. E.g., an ML model is a Transformer which transforms a DataFrame with features into a DataFrame with predictions.

    Estimator: An Estimator is an algorithm which can be fit on a DataFrame to produce a Transformer. E.g., a learning algorithm is an Estimator which trains on a DataFrame and produces a model.

    Pipeline: A Pipeline chains multiple Transformers and Estimators together to specify an ML workflow.

    Parameter: All Transformers and Estimators now share a common API for specifying parameters.

Transformer.transform()s and Estimator.fit()s are both stateless. In the future, stateful algorithms may be supported via alternative concepts.

DAG Pipelines: A Pipeline’s stages are specified as an ordered array. The examples given here are all for linear Pipelines, i.e., Pipelines in which each stage uses data produced by the previous stage. It is possible to create non-linear Pipelines as long as the data flow graph forms a Directed Acyclic Graph (DAG). This graph is currently specified implicitly based on the input and output column names of each stage (generally specified as parameters). If the Pipeline forms a DAG, then the stages must be specified in topological order.

Runtime checking: Since Pipelines can operate on DataFrames with varied types, they cannot use compile-time type checking. Pipelines and PipelineModels instead do runtime checking before actually running the Pipeline. This type checking is done using the DataFrame schema, a description of the data types of columns in the DataFrame.

Unique Pipeline stages: A Pipeline’s stages should be unique instances. E.g., the same instance myHashingTF should not be inserted into the Pipeline twice since Pipeline stages must have unique IDs. However, different instances myHashingTF1 and myHashingTF2 (both of type HashingTF) can be put into the same Pipeline since different instances will be created with different IDs.


Example

    from pyspark.ml.linalg import Vectors
    from pyspark.ml.classification import LogisticRegression

    # Prepare training data from a list of (label, features) tuples.
    training = spark.createDataFrame([
        (1.0, Vectors.dense([0.0, 1.1, 0.1])),
        (0.0, Vectors.dense([2.0, 1.0, -1.0])),
        (0.0, Vectors.dense([2.0, 1.3, 1.0])),
        (1.0, Vectors.dense([0.0, 1.2, -0.5]))], ["label", "features"])

    # Create a LogisticRegression Estimator
    lr = LogisticRegression(maxIter=12, regParam=0.01)
    print("LogisticRegression parameters:\n" + lr.explainParams() + "\n")

    # Learn a LogisticRegression model.
    model1 = lr.fit(training)

    # Since model1 is a Model
    # we can view the parameters it used during fit().
    # This prints the parameter (name: value) pairs, where names are unique IDs for this
    # LogisticRegression instance.
    print("Model 1 was fit using parameters: ")
    print(model1.extractParamMap())

    # We may alternatively specify parameters using a Python dictionary as a paramMap
    paramMap = {lr.maxIter: 20}
    paramMap[lr.maxIter] = 30  # Specify 1 Param, overwriting the original maxIter.
    # Specify multiple Params.
    paramMap.update({lr.regParam: 0.1, lr.threshold: 0.55})  # type: ignore

    # You can combine paramMaps, which are python dictionaries.
    # Change output column name
    paramMap2 = {lr.probabilityCol: "myProbability"}
    paramMapCombined = paramMap.copy()
    paramMapCombined.update(paramMap2)  # type: ignore

    # Now learn a new model using the paramMapCombined parameters.
    # paramMapCombined overrides all parameters set earlier via lr.set* methods.
    model2 = lr.fit(training, paramMapCombined)
    print("Model 2 was fit using parameters: ")
    print(model2.extractParamMap())

    # Prepare test data
    test = spark.createDataFrame([
        (1.0, Vectors.dense([-1.0, 1.5, 1.3])),
        (0.0, Vectors.dense([3.0, 2.0, -0.1])),
        (1.0, Vectors.dense([0.0, 2.2, -1.5]))], ["label", "features"])

    # Make predictions on test data using the Transformer.transform() method.
    # LogisticRegression.transform will only use the 'features' column.
    # Note that model2.transform() outputs a "myProbability" column instead of the usual
    # 'probability' column since we renamed the lr.probabilityCol parameter previously.
    prediction = model2.transform(test)
    result = prediction.select("features", "label", "myProbability", "prediction") \
        .collect()

    for row in result:
        print("features=%s, label=%s -> prob=%s, prediction=%s"
            % (row.features, row.label, row.myProbability, row.prediction))