# Databricks notebook source
# MAGIC %scala
# MAGIC 
# MAGIC var dataset = Seq(
# MAGIC   ("Thin",       "cell phone", 6000),
# MAGIC   ("Normal",     "tablet",     1500),
# MAGIC   ("Mini",       "tablet",     5500),
# MAGIC   ("Ultra thin", "cell phone", 5000),
# MAGIC   ("Very thin",  "cell phone", 6000),
# MAGIC   ("Big",        "tablet",     2500),
# MAGIC   ("Bendable",   "cell phone", 3000),
# MAGIC   ("Foldable",   "cell phone", 3000),
# MAGIC   ("Pro",        "tablet",     4500),
# MAGIC   ("Pro2",       "tablet",     6500))
# MAGIC   .toDF("product", "category", "revenue")