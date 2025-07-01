# 🛒 ShopSwift - Business Context

ShopSwift is a simple eCommerce platform that sells physical goods directly to consumers across the country. It allows customers to browse products, add items to their cart, place orders, and leave reviews after receiving deliveries. This schema simulates the core transactional and operational workflows of a typical online store.

---

## 👤 Customers
Customers sign up with their name, contact info, and address. Each customer can have multiple shipping addresses. Orders are placed by customers and linked to their respective addresses and payment records.

---

## 📦 Products
ShopSwift sells various product categories like electronics, fashion, and household goods. Each product has its own stock count and unit price. Products are referenced in both `order_items` and `cart_items`.

---

## 🛒 Carts and Orders
- **Carts**: Temporary baskets where customers add items before checkout. Cart data is helpful for abandoned cart analysis.
- **Orders**: Finalized purchases with full order metadata including customer, order total, status, and linked payments.

---

## 📄 Order Items
Every order has one or more `order_items`, each referring to a specific product, quantity, and unit price at the time of order.

---

## 💳 Payments
Each order has a payment record detailing payment method, date, amount, and status. Failed or pending payments can be tracked through this table.

---

## 📦 Shipments
Orders that are paid are shipped via third-party carriers. Each shipment has a tracking number and shipping date.

---

## ⭐ Reviews
After delivery, customers can leave product reviews with a star rating and optional text feedback.

---

## 🔄 Relationships Overview

- One customer → many orders, addresses, reviews
- One order → many order_items, one payment, one shipment
- One cart → many cart_items
- One product → many order_items, cart_items, reviews

---

## 📊 What Can You Learn with This Schema?

- SQL joins (1-to-many, many-to-many through junctions)
- Aggregations: revenue, product popularity, cart abandonment
- Payment status monitoring
- Order processing funnel
- Customer behavior and retention
- Time-series analysis (orders over time)

---

This schema strikes a balance between realism and simplicity, making it ideal for:
- Beginner SQL practice
- Analytics pipelines
- BI tool prototyping
- Teaching relational modeling

