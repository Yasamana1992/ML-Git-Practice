# Sales Dashboard

## Project Overview

This project analyzes sales data from a CSV file containing the date, product, category, quantity, and unit price of each transaction.

It generates an overview of business performance reports, including total revenue, total quantity sold, total number of transactions, monthly sales trends, and revenue by product, and revenue by category.

The dashboard also identifies the top product by revenue and calculates the combined revenue share of the three products with the highest revenue. This metrics help highlight potential revenue concentration in the dataset.

## Key Findings

### Based on the current dataset:

- Top product: Laptops, generating 360,000,000 in revenue.
- Revenue concentration: The three highest-revenue products account for approximately 97.6% of total revenue.
- Top category: Electronics, generating 388,000,000, or approximately 84.8% of total revenue.
- Monthly trend: Revenue increased by approximately 15.7% in February and decreased by approximately 29.6% in March compared with the previous month.

These findings describe the available dataset and should not be interpreted as definitive conclusions about long-term business performance.

## How to Run

Run "sales_dashboard.py" and enter the CSV filename when prompted. For the included dataset, enter "sales".

The dashboard will process the data and display the monthly, product, and category reports, along with a business summary.

## Limitations

The current analysis focuses on revenue and sales quantities. It does not include profit margins, operating costs, inventory levels, or future sales forecasts.

The dataset covers only three months, so the monthly trends are insufficient to establish long-term patterns. The findings also depend on the quality and representativeness of the available data