from pyspark.sql.functions import col, round

bronze_table = "ecommerce_db.bronze_sales"
silver_table = "ecommerce_db.silver_sales"

# Read from Bronze layer
bronze_df = spark.read.format("delta").table(bronze_table)

# Silver Transformations
silver_df = (
    bronze_df
    # 1. Drop rows where critical columns are null
    .dropna(subset=["order_id", "customer_id", "product_price"])
    
    # 2. Filter out invalid quantities (e.g., negative values)
    .filter(col("quantity") > 0)
    
    # 3. Create a derived column for total amount
    .withColumn("total_amount", round(col("quantity") * col("product_price"), 2))
    
    # 4. Standardize string formats (e.g., uppercase status)
    .withColumn("order_status", col("order_status"))
)

# Write to Silver layer
silver_df.write.format("delta").mode("overwrite").saveAsTable(silver_table)

print("Transformations applied and data saved to Silver layer.")