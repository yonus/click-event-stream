from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, LongType, StringType,TimestampType
from pyspark.sql.functions import udf, col, expr,from_unixtime


import json
import base64



def main():
    a=sc.parallelize([1,2,3,4])
    print(a.collect())


def get_click_event_schema():
    schema = StructType() \
        .add("user_id",IntegerType()) \
        .add("session_id",LongType()) \
        .add("session_start",IntegerType()) \
        .add("click_article_id",IntegerType()) \
        .add("click_timestamp", IntegerType()) \
        .add("click_environment",IntegerType()) \
        .add("click_device_group", IntegerType()) \
        .add("click_os", IntegerType()) \
        .add("click_country", IntegerType())
    
    return schema

def get_article_metadata_file_directory():
    return "/var/data/stream-click-datasource/article/articles_metadata.csv"

def get_sink_prefix_directory():
    return "/var/data/stream-click-datasource/egress/stream/click-event-article"


def read_article_metadata():
    if get_article_metadata_file_directory():
        return spark.read.load(get_article_metadata_file_directory(),format="csv", sep=",", inferSchema="true", header="true")
        

def decode_payload_to_json(payload):
      return json.loads(base64.b64decode(payload).decode('utf-8'))

def get_decoder_udf():
    return udf(lambda x : decode_payload_to_json(x) ,get_click_event_schema())

    



if __name__ == "__main__":
    spark = SparkSession.builder.appName("click-event-stream").getOrCreate()
    sc = spark.sparkContext
    article_metadata_df = read_article_metadata()
    
    
    stream = spark.readStream \
          .format("kafka") \
          .option("kafka.bootstrap.servers", "kafka1:19091") \
          .option("subscribe", "click-stream") \
          .load()

    click_event_stream_df = stream.select("value").select(get_decoder_udf()(col("value")).alias("click_event")) \
       .select("click_event.*")
    
    click_event_stream_df = click_event_stream_df.withColumn('click_timestamp_date',from_unixtime('click_timestamp', 'yyyy-MM-dd'))
    
   
    
    click_event_with_article = click_event_stream_df.join(article_metadata_df, 
        expr("""
        click_article_id = article_id
        """),
        "leftOuter" )
    
    

    click_event_with_article.writeStream \
       .format("parquet")  \
       .option("path", get_sink_prefix_directory()) \
       .option("checkpointLocation", get_sink_prefix_directory()+"/checkpoint") \
       .partitionBy("click_timestamp_date") \
       .start() \
       .awaitTermination()

   
   
  




