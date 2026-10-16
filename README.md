# Sales Dashboard

## Project Overview

This project analyzes sales data from a CSV file containing the date, product, category, quantity, and unit price of each transaction.

It generates an overview of business performance, including total revenue, total quantity sold, total number of transactions, monthly sales trends, and revenue by product.

The dashboard also identifies the top product by revenue and calculates the combined revenue share of the three products with the highest revenue. This helps highlight potential revenue concentration.

## Key Findings

### In the current dataset:

- Laptops are the top product by revenue, generating 360,000,000 in revenue.
- The top three products account for approximately 97.6% of total revenue, indicating a high concentration of revenue among a small number of products.

## How to Run

Run the Python sales_dashboard.py and enter the CSV filename (in this case "sales") when prompted. The dashboard will process the data and display the sales reports.

## Limitations

The current dashboard does not provide sales reports by category. Although the dataset includes a category column, category-level sales performance is not yet analyzed. One of the limitation has been fixed in the improved version. The dashboard now includes category-level sales analysis. The category report summarizes total revenue, total quantity sold, transaction count, and each category’s percentage share of total revenue.

The analysis is based on the available dataset and does not include profit margins, costs, inventory levels, or future sales forecasts.
