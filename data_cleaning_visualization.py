"""
Data Cleaning & Visualization Project
Dataset: raw_ecommerce_sales.csv

Run:
    pip install pandas matplotlib
    python data_cleaning_visualization.py
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
RAW_FILE = BASE / "raw_ecommerce_sales.csv"
OUTPUT_FILE = BASE / "cleaned_ecommerce_sales.csv"
CHARTS = BASE / "charts"
CHARTS.mkdir(exist_ok=True)

df = pd.read_csv(RAW_FILE)
print("Raw shape:", df.shape)
print("\nMissing values before cleaning:\n", df.isna().sum())
print("\nDuplicate rows:", df.duplicated().sum())

# 1. Remove duplicates
df = df.drop_duplicates().copy()

# 2. Standardize text
df["City"] = df["City"].astype("string").str.strip().str.title()
df["City"] = df["City"].replace({"New Delhi": "Delhi", "Bangalore": "Bengaluru"})
df["Category"] = df["Category"].astype("string").str.strip().str.title()
df["Category"] = df["Category"].replace({"Electronic": "Electronics", "Clothes": "Clothing"})
df["Payment_Method"] = df["Payment_Method"].astype("string").str.strip().str.title()
df["Payment_Method"] = df["Payment_Method"].replace({"Upi": "UPI"})

# 3. Convert data types
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
for column in ["Customer_Age", "Unit_Price", "Customer_Rating"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# 4. Handle missing values
df["City"] = df["City"].fillna("Unknown")
df["Customer_Age"] = df["Customer_Age"].fillna(df["Customer_Age"].median())
df["Customer_Rating"] = df["Customer_Rating"].fillna(df["Customer_Rating"].median())
df["Unit_Price"] = df.groupby("Category")["Unit_Price"].transform(
    lambda series: series.fillna(series.median())
)
df["Unit_Price"] = df["Unit_Price"].fillna(df["Unit_Price"].median())

# 5. Fix impossible age values
valid_age_median = df.loc[df["Customer_Age"].between(15, 80), "Customer_Age"].median()
df.loc[~df["Customer_Age"].between(15, 80), "Customer_Age"] = valid_age_median

# 6. Cap numerical outliers using the IQR method
def cap_outliers(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return series.clip(lower, upper)

df["Unit_Price"] = cap_outliers(df["Unit_Price"])
df["Quantity"] = cap_outliers(df["Quantity"])

# 7. Create useful features
df["Gross_Sales"] = df["Quantity"] * df["Unit_Price"]
df["Net_Sales"] = df["Gross_Sales"] * (1 - df["Discount_Percent"] / 100)
df["Order_Month"] = df["Order_Date"].dt.to_period("M").astype(str)
df["Age_Group"] = pd.cut(
    df["Customer_Age"],
    bins=[14, 20, 30, 40, 50, 80],
    labels=["15-20", "21-30", "31-40", "41-50", "51+"],
    include_lowest=True
)

df.to_csv(OUTPUT_FILE, index=False)

# 8. Visualize insights
category_sales = df.groupby("Category")["Net_Sales"].sum().sort_values(ascending=False)
monthly_sales = df.groupby("Order_Month")["Net_Sales"].sum()
city_sales = df.groupby("City")["Net_Sales"].sum().sort_values(ascending=False)

plt.figure(figsize=(9, 5))
category_sales.plot(kind="bar")
plt.title("Net Sales by Product Category")
plt.xlabel("Category")
plt.ylabel("Net Sales")
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig(CHARTS / "sales_by_category.png", dpi=180)
plt.close()

plt.figure(figsize=(10, 5))
monthly_sales.plot(marker="o")
plt.title("Monthly Net Sales Trend")
plt.xlabel("Month")
plt.ylabel("Net Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(CHARTS / "monthly_sales_trend.png", dpi=180)
plt.close()

plt.figure(figsize=(9, 5))
city_sales.plot(kind="bar")
plt.title("Net Sales by City")
plt.xlabel("City")
plt.ylabel("Net Sales")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(CHARTS / "sales_by_city.png", dpi=180)
plt.close()

print("\nClean shape:", df.shape)
print("Total net sales:", round(df["Net_Sales"].sum(), 2))
print("Average order value:", round(df["Net_Sales"].mean(), 2))
print("Top category:", category_sales.index[0])
print("Top city:", city_sales.index[0])
print("\nSaved:", OUTPUT_FILE)
