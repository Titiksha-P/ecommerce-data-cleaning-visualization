# Data Cleaning & Visualization Project

## Project Summary
This portfolio project analyses a deliberately messy e-commerce sales dataset. The raw data contains missing values, duplicate rows, inconsistent category names, impossible ages, and extreme numerical outliers.

## Dataset
- Raw rows: **332**
- Clean rows: **320**
- Duplicate rows removed: **12**
- Final columns: **14**

## Cleaning Performed
- Removed exact duplicate records.
- Standardized inconsistent city, category, and payment labels.
- Filled missing ages and ratings with median values.
- Filled missing prices using category medians.
- Replaced impossible ages with the median valid age.
- Capped price and quantity outliers using the IQR method.
- Converted order dates to datetime.
- Created Gross Sales, Net Sales, Order Month, and Age Group features.

## Main Findings
- **Total net sales:** ₹237,342.47
- **Average order value:** ₹741.70
- **Average rating:** 3.72/5
- **Highest-sales category:** Clothing
- **Highest-sales city:** Pune
- **Highest-sales month:** 2025-06

## Data Story
The cleaned dataset shows that **Clothing** generated the greatest net sales, while **Pune** was the strongest city market. Ratings were generally positive, with the average customer rating remaining above 3.7. The monthly chart also reveals seasonal variation in sales, which could support inventory and marketing planning.

## Files
- `raw_ecommerce_sales.csv` — messy input data
- `cleaned_ecommerce_sales.csv` — cleaned and enriched output data
- `Data_Cleaning_Visualization_Project.ipynb` — step-by-step notebook
- `data_cleaning_visualization.py` — reusable Python script
- `ecommerce_data_project.xlsx` — raw data, cleaned data and dashboard tables
- `charts/` — exported visualization images

## Skills Demonstrated
Python, Pandas, missing-value treatment, duplicate removal, text standardization, IQR outlier handling, feature engineering, data aggregation, Matplotlib visualization, and data storytelling.
