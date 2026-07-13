from pyspark.sql.functions import sum, count

silver_table = "ecommerce_db.silver_sales"
gold_table = "ecommerce_db.gold_daily_revenue"

# Read from Silver layer
silver_df = spark.read.format("delta").table(silver_table)

# Gold Aggregation (e.g., Daily Revenue and Total Orders by Category)
gold_df = (
    silver_df
    .groupBy("order_date", "product_category")
    .agg(
        sum("total_amount").alias("daily_revenue"),
        count("order_id").alias("total_orders")
    )
)

# Write to Gold layer
gold_df.write.format("delta").mode("overwrite").saveAsTable(gold_table)

print("Aggregated business metrics saved to Gold layer.")