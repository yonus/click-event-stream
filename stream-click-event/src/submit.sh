spark-submit \
  --master spark://spark:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 \
  click_event_stream_job.py