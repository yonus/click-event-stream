from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, LongType, StringType,TimestampType
from pyspark.sql.functions import udf, col, expr,from_unixtime


import json
import base64



def get_click_event_data_file_directory():
    return "/var/data/stream-click-datasource/egress/stream/click-event-article/*/*.parquet"

def get_sink_directory():
     return "/var/data/stream-click-datasource/egress/batch_analyze"


 

def write_click_event_count_by_environment(click_event_df):
   click_event_df.groupBy("click_environment").count().coalesce(1)  \
       .write \
        .mode('overwrite') \
        .option('header', 'true') \
        .csv(get_sink_directory()+'/click_event_count_by_environment')

def write_click_event_count_by_device_group(click_event_df):
   click_event_df.groupBy("click_device_group").count().coalesce(1)  \
       .write \
        .mode('overwrite') \
        .option('header', 'true') \
        .csv(get_sink_directory()+'/click_event_count_by_device_group')
    
def write_click_event_count_by_os(click_event_df):
   click_event_df.groupBy("click_os").count().coalesce(1)  \
       .write \
        .mode('overwrite') \
        .option('header', 'true') \
        .csv(get_sink_directory()+'/click_event_count_by_os')

def write_most_and_least_popular_articles():
    most_and_least_popular_article =spark.sql("select article_id, count(article_id) as count_article_id FROM click_event_with_article GROUP BY article_id ORDER BY count_article_id DESC")
    most_and_least_popular_article.coalesce(1).write \
        .mode('overwrite') \
        .option('header', 'true') \
        .csv(get_sink_directory()+'/most_and_least_popular_article')

def write_most_and_least_popular_categories():
    most_and_least_popular_article =spark.sql("select category_id, count(category_id) as count_category_id FROM click_event_with_article GROUP BY category_id ORDER BY count_category_id DESC")
    most_and_least_popular_article.coalesce(1).write \
        .mode('overwrite') \
        .option('header', 'true') \
        .csv(get_sink_directory()+'/most_and_least_popular_categories')


def write_avarage_count_by_categories_and_article(click_event_with_article):
    click_event_with_article.groupBy("article_id","category_id").avg("words_count").coalesce(1).write \
        .mode('overwrite') \
        .option('header', 'true') \
        .csv(get_sink_directory()+'/avarage_count_by_categories_and_article')

def write_avarage_time_to_click_on_article_by_categories():
    avarage_time_to_click_on_article_by_categories = spark.sql("""SELECT category_id, CAST(avg((click_timestamp -session_start)/1000) as int) as avarge_time_in_second 
                                                                    FROM click_event_with_article 
                                                                    GROUP BY category_id""")
    avarage_time_to_click_on_article_by_categories.coalesce(1).write \
        .mode('overwrite') \
        .option('header', 'true') \
        .csv(get_sink_directory()+'/avarage_time_to_click_on_article_by_categories')



if __name__ == "__main__":
    spark = SparkSession.builder.appName("click-event-batch").getOrCreate()
     


    click_event_with_article = spark.read.parquet(get_click_event_data_file_directory())
    click_event_with_article.cache()
    click_event_with_article.createOrReplaceTempView("click_event_with_article")

    write_click_event_count_by_device_group(click_event_df=click_event_with_article)
    write_click_event_count_by_os(click_event_df=click_event_with_article)
    write_click_event_count_by_environment(click_event_df=click_event_with_article)

    write_most_and_least_popular_articles()
    write_most_and_least_popular_categories()
    write_avarage_count_by_categories_and_article(click_event_with_article=click_event_with_article)
    write_avarage_time_to_click_on_article_by_categories()
   




   

     
   
   
  




