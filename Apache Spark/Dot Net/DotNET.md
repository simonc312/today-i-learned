# Spark for Dot Net Developers

## Pre-requisites

- Java 8 
- .Net 6
- Spark 2.4.4
- Microsoft.Spark.Worker from Git
- Microsoft.Spark from Nuget
- necessary env variables updated like SPARK_HOME, PATH, DOTNET_WORKER_DIR

https://github.com/dotnet/spark

## Application

Initialize project

    dotnet compile console -o HelloSpark


Main program file

    using Microsoft.Spark.Sql;

    namespace HelloSpark
    {
        class Program
        {
            static void Main(string[] args)
            {
                var spark = SparkSession.Builder().GetOrCreate();
                var df = spark.Read().Json("people.json");
                df.Show();
            }
        }
    }

Build application

    dotnet build

Run application

    spark-submit \
    --class org.apache.spark.deploy.dotnet.DotnetRunner \
    --master local \
    microsoft-spark-<version>.jar \
    dotnet HelloSpark.dll