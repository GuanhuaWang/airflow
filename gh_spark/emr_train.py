# (Guanhua) 
# Simple Neural network training job using EMR (1 master, 2 workers)

from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
import os
from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Load training data.
os.system("hdfs dfs -put /usr/lib/spark/data/mllib/sample_multiclass_classification_data.txt /user/livy/sample_multiclass_classification_data.txt")
data = spark.read.format("libsvm").load("sample_multiclass_classification_data.txt")

# Split data into train and test sets.
splits = data.randomSplit([0.6,0.4], 2333)
train = splits[0]
test = splits[1]

# Define Neural network with input layer with 4 features \
# 2 hidden layers with 5 and 6 neurons \
# output layer with 3 classes.
layers = [4,5,6,3]

# Create trainer.
trainer = MultilayerPerceptronClassifier(maxIter = 100, layers = layers, blockSize = 128, seed = 1234)

# Train model.
model = trainer.fit(train)

# Compute test accuracy.
result = model.transform(test)
predictionAndLabels = result.select("prediction", "label")
evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
print("Accuracy: " + str(evaluator.evaluate(predictionAndLabels)))
