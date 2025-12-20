# Databricks notebook source
# Percebemos que para Betelgeuse temos vários nomes, vamos padronizar num estado intermediário
df = spark.table("workspace.default.betelgeuse_2000_2025")
resultado = df.select("Star Name").distinct().limit(5)
resultado.show()

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.functions import lit, col, expr

df_betelgeuse = spark.table("`workspace`.`default`.`betelgeuse_2000_2025`")\
  .withColumn("star_name", lit("Betelgeuse"))\
  .select("star_name", col("JD").alias("jd"), col("Magnitude").alias("magnitude"), col("Observer Code").alias("observer_code"), col("Uncertainty").alias("uncertainty"))

df_eta_carinae = spark.table("`workspace`.`default`.`eta_carinae_2000_2025`")\
  .withColumn("star_name", lit("Eta Carinae"))\
  .select("star_name", col("JD").alias("jd"), col("Magnitude").alias("magnitude"), col("Observer Code").alias("observer_code"), col("Uncertainty").alias("uncertainty"))

df_algol = spark.table("`workspace`.`default`.`algol_2000_2025`")\
  .withColumn("star_name", lit("Algol"))\
  .select("star_name", col("JD").alias("jd"), col("Magnitude").alias("magnitude"), col("Observer Code").alias("observer_code"), col("Uncertainty").alias("uncertainty"))

## Vamos unificar o resultado em uma única tabela na camada prata
df_silver = df_betelgeuse.union(df_eta_carinae).union(df_algol)

# Limpando a coluna magnitude
df_silver = df_silver.withColumn("magnitude_temp", F.regexp_replace(F.col("magnitude"), r"[^\d.]", ""))
df_silver = df_silver.withColumn("magnitude_float", expr("try_cast(magnitude_temp AS FLOAT)"))
df_silver = df_silver.dropna(subset=["magnitude_float"])
df_silver = df_silver.withColumn("magnitude", F.col("magnitude_float")).drop("magnitude_temp", "magnitude_float")
print(df_silver.filter(F.col("magnitude").isNull()).count())

# Limpando a coluna uncertainty
df_silver = df_silver.withColumn("uncertainty_temp", F.regexp_replace(F.col("uncertainty"), r"[^\d.]", ""))
df_silver = df_silver.withColumn("uncertainty", F.col("uncertainty_temp")).drop("magnitude_temp")
df_silver.filter(F.col("uncertainty").isNull()).count()

df_silver.printSchema()

# As outras colunas não possuiam valores nulos
df_silver.filter(F.col("star_name").isNull()).count()
df_silver.filter(F.col("jd").isNull()).count()
df_silver.filter(F.col("observer_code").isNull()).count()


# COMMAND ----------

## Gerando a data no formato gregoriano
from pyspark.sql import functions as F

df_silver = df_silver.withColumn("data_gregoriana", ((F.col("jd") - 2440587.5) * 86400).cast("timestamp"))

# COMMAND ----------

df_silver.write.mode("overwrite").saveAsTable("silver_stars")
