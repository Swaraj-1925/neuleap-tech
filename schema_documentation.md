
# Database Schema Documentation

---

## Entity Relationship Summary

| Entity      | Description                                   |
| ----------- | --------------------------------------------- |
| customers   | Stores customer profile and registration data |
| products    | Stores product catalog information            |
| orders      | Stores purchase orders made by customers      |
| order_items | Stores individual products within an order    |
| payments    | Stores payment transactions for orders        |

---

## Table: `customers`

### Description

Stores personal and account-related information for customers registered on the platform.

### Columns

| Column Name    | Data Type | Constraints | Description                             |
| -------------- | --------- | ----------- | --------------------------------------- |
| customer_id    | Integer   | Primary Key | Unique identifier for each customer     |
| full_name      | String    | —           | Customer’s full name                    |
| email          | String    | —           | Customer’s email address                |
| phone          | String    | —           | Customer’s contact number               |
| country        | String    | —           | Country of residence                    |
| signup_date    | Date      | —           | Date the customer registered            |
| signup_channel | String    | —           | Registration source (e.g., web, mobile) |
| loyalty_points | Integer   | —           | Accumulated loyalty or reward points    |

### Relationships

* One customer can place **multiple orders**
* Referenced by `orders.customer_id`

---

## Table: `products`

### Description

Contains the product catalog, including pricing and classification details.

### Columns

| Column Name  | Data Type | Constraints | Description               |
| ------------ | --------- | ----------- | ------------------------- |
| product_id   | Integer   | Primary Key | Unique product identifier |
| product_name | String    | —           | Name of the product       |
| price        | Numeric   | —           | Base price of the product |
| category     | String    | —           | Product category          |
| brand        | String    | —           | Product brand             |
| created_at   | TIMESTAMP | —           | Record creation timestamp |
| updated_at   | TIMESTAMP | —           | Last update timestamp     |

### Relationships

* A product can appear in **multiple order items**
* Referenced by `order_items.product_id`

---

## Table: `orders`

### Description

Stores order-level transaction information for customer purchases.

### Columns

| Column Name      | Data Type | Constraints                         | Description                               |
| ---------------- | --------- | ----------------------------------- | ----------------------------------------- |
| order_id         | Integer   | Primary Key                         | Unique order identifier                   |
| customer_id      | Integer   | Foreign Key → customers.customer_id | Customer who placed the order             |
| order_date       | Date      | —                                   | Date the order was placed                 |
| status           | String    | —                                   | Order status (e.g., completed, cancelled) |
| discount_amount  | Numeric   | —                                   | Discount applied to the order             |
| tax_amount       | Numeric   | —                                   | Tax charged on the order                  |
| payment_method   | String    | —                                   | Payment method used                       |
| shipping_address | Text      | —                                   | Shipping destination address              |

### Relationships

* Each order belongs to **one customer**
* An order can contain **multiple order items**
* An order can have **multiple payments**

---

## Table: `order_items`

### Description

Represents individual product line items within an order.

### Columns

| Column Name   | Data Type | Constraints                       | Description                     |
| ------------- | --------- | --------------------------------- | ------------------------------- |
| order_item_id | Integer   | Primary Key                       | Unique order item identifier    |
| order_id      | Integer   | Foreign Key → orders.order_id     | Associated order                |
| product_id    | Integer   | Foreign Key → products.product_id | Associated product              |
| quantity      | Integer   | —                                 | Quantity ordered                |
| unit_price    | Numeric   | —                                 | Price per unit at time of order |

### Relationships

* Each order item belongs to **one order**
* Each order item references **one product**
* Serves as a junction table between orders and products

---

## Table: `payments`

### Description

Stores payment transactions associated with customer orders.

### Columns

| Column Name    | Data Type | Constraints                   | Description                               |
| -------------- | --------- | ----------------------------- | ----------------------------------------- |
| payment_id     | Integer   | Primary Key                   | Unique payment identifier                 |
| order_id       | Integer   | Foreign Key → orders.order_id | Associated order                          |
| payment_date   | Date      | —                             | Date of payment                           |
| payment_amount | Numeric   | —                             | Amount paid                               |
| payment_status | String    | —                             | Payment status (e.g., successful, failed) |
| payment_type   | String    | —                             | Type of payment (e.g., credit card, UPI)  |

### Relationships

* Each payment is linked to **one order**
* An order may have **one or multiple payments**
---

