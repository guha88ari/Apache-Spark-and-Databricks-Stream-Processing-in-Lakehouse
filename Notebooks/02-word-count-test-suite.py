# Databricks notebook source
# MAGIC %run ./01-streaming-word-count

# COMMAND ----------

class batchWCTestSuite():
    def __init__(self):
        self.base_data_dir = "/Workspace/Users/guha88ari@gmail.com/Apache-Spark-and-Databricks-Stream-Processing-in-Lakehouse/data_spark_streaming_scholarnest"

    def cleanTests(self):
        print(f"Starting Cleanup...", end='')
        spark.sql("drop table if exists word_count_table")
        dbutils.fs.rm("/Volumes/dev/demo_kafka/vol1/word_count_table", True)

        dbutils.fs.rm(f"{self.base_data_dir}/chekpoint", True)
        dbutils.fs.rm(f"{self.base_data_dir}/data/text", True)

        dbutils.fs.mkdirs(f"{self.base_data_dir}/data/text")
        print("Done\n")

    def ingestData(self, itr):
        print(f"\tStarting Ingestion...", end='')
        dbutils.fs.cp(f"{self.base_data_dir}/datasets/text/text_data_{itr}.txt", f"{self.base_data_dir}/data/text/")
        print("Done")

    def assertResult(self, expected_count):
        print(f"\tStarting validation...", end='')
        actual_count = spark.sql("select sum(count) from word_count_table where substr(word, 1, 1) == 's'").collect()[0][0]
        assert expected_count == actual_count, f"Test failed! actual count is {actual_count}"
        print("Done")

    def runTests(self):
        self.cleanTests()
        wc = batchWC()

        print("Testing first iteration of batch word count...") 
        self.ingestData(1)
        wc.wordCount()
        self.assertResult(25)
        print("First iteration of batch word count completed.\n")

        # print("Testing second iteration of batch word count...") 
        # self.ingestData(2)
        # wc.wordCount()
        # self.assertResult(32)
        # print("Second iteration of batch word count completed.\n") 

        # print("Testing third iteration of batch word count...") 
        # self.ingestData(3)
        # wc.wordCount()
        # self.assertResult(37)
        # print("Third iteration of batch word count completed.\n")
    

# COMMAND ----------

bwcTS = batchWCTestSuite()
bwcTS.runTests()

# COMMAND ----------

class streamWCTestSuite():
    def __init__(self):
        self.base_data_dir = "/Volumes/dev/demo_kafka/vol1"

    def cleanTests(self):
        print(f"Starting Cleanup...", end='')
        spark.sql("drop table if exists word_count_table")
        dbutils.fs.rm("/Volumes/dev/demo_kafka/vol1/word_count_table", True)

        dbutils.fs.rm(f"{self.base_data_dir}/chekpoint", True)
        dbutils.fs.rm(f"{self.base_data_dir}/data/text", True)

        dbutils.fs.mkdirs(f"{self.base_data_dir}/data/text")
        print("Done\n")

    def ingestData(self, itr):
        print(f"\tStarting Ingestion...", end='')
        dbutils.fs.cp(f"{self.base_data_dir}/datasets/text/text_data_{itr}.txt", f"{self.base_data_dir}/data/text/")
        print("Done")

    def assertResult(self, expected_count):
        print(f"\tStarting validation...", end='')
        actual_count = spark.sql("select sum(count) from word_count_table where substr(word, 1, 1) == 's'").collect()[0][0]
        assert expected_count == actual_count, f"Test failed! actual count is {actual_count}"
        print("Done")

    def runTests(self):
        import time
        sleepTime = 30

        self.cleanTests()
        wc = streamWC()
        sQuery = wc.wordCount()

        print("Testing first iteration of batch word count...") 
        self.ingestData(1)
        print(f"\tWaiting for {sleepTime} seconds...") 
        time.sleep(sleepTime)
        self.assertResult(37)
        print("First iteration of batch word count completed.\n")

        print("Testing second iteration of batch word count...") 
        self.ingestData(2)
        print(f"\tWaiting for {sleepTime} seconds...") 
        time.sleep(sleepTime)
        self.assertResult(37)
        print("Second iteration of batch word count completed.\n") 

        print("Testing third iteration of batch word count...") 
        self.ingestData(3)
        print(f"\tWaiting for {sleepTime} seconds...") 
        time.sleep(sleepTime)
        self.assertResult(37)
        print("Third iteration of batch word count completed.\n")

        sQuery.stop()
    

# COMMAND ----------

swcTS = streamWCTestSuite()
swcTS.runTests()

# COMMAND ----------

# MAGIC %fs
# MAGIC ls /Volumes/dev/demo_db/files

# COMMAND ----------

# Source - https://stackoverflow.com/a/79693995
# Posted by addicted
# Retrieved 2026-02-05, License - CC BY-SA 4.0

catalog = 'dev'
schema = 'demo_kafka'
volume_name = 'vol1'
spark.sql(f"CREATE VOLUME IF NOT EXISTS {catalog}.{schema}.{volume_name}")


# COMMAND ----------

# MAGIC %sql
# MAGIC select sum(count) from word_count_table where substr(word, 1, 1) == 's'

# COMMAND ----------

# MAGIC %sql
# MAGIC DESC FORMATTED word_count_table

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2021-2023 <a href="https://www.scholarnest.com/">ScholarNest Technologies Pvt. Ltd. </a>All rights reserved.<br/>
# MAGIC <br/>
# MAGIC <a href="https://www.scholarnest.com/privacy/">Privacy Policy</a> | <a href="https://www.scholarnest.com/terms/">Terms of Use</a> | <a href="https://www.scholarnest.com/contact-us/">Contact Us</a>
