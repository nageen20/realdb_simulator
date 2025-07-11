# SnapSupply Micro Logistics (Easy Level)

## 🏢 Business Overview

**SnapSupply** is a fictional logistics startup that connects **local retailers** (such as corner stores, pharmacies, and cafes) with **regional suppliers** of fast-moving consumer goods (FMCG), groceries, and essentials. The startup operates a shared logistics platform to streamline procurement, fulfillment, and last-mile delivery for small businesses that can't afford enterprise-scale supply chain systems.

SnapSupply provides:
- A mobile ordering system for small business owners.
- A supplier portal to list available products and prices.
- A warehouse-backed fulfillment and shipment management system.
- A network of gig-economy delivery partners for last-mile delivery.

---

## 🎯 Use Case

This schema is designed to simulate a **real-world transactional OLTP database** behind such a business. It’s suitable for practicing:

- SQL joins across 10+ related tables.
- Handling of **order-to-ship workflows**.
- Modeling relationships between **products, customers, suppliers, shipments, and delivery assignments**.
- Performing beginner-to-intermediate **business intelligence queries** (e.g., average order value, shipment delays, partner delivery performance).
- Testing **data engineering pipelines** using realistic relational data.

---

## 🗃️ Schema Summary

| Entity              | Description |
|---------------------|-------------|
| `customers`         | Local retailers who place orders through SnapSupply. |
| `suppliers`         | Regional product suppliers who sell goods via the platform. |
| `products`          | Items listed in the SnapSupply catalog. |
| `supplier_products` | Join table showing which suppliers stock which products and in what quantity. |
| `orders`            | Purchase orders created by customers. |
| `order_items`       | Individual line items under each order. |
| `warehouses`        | Physical locations where inventory is stored or consolidated before shipping. |
| `shipments`         | Packages prepared and sent out from warehouses for customer orders. |
| `delivery_partners` | Third-party logistics contractors assigned to fulfill shipments. |
| `delivery_assignments` | Tracks who delivered what, and when. |
| `product_reviews`   | Optional feedback left by customers on received products. |

---

## 🧩 Example Workflows

1. **Customer Order Flow**
   - A customer browses products → places an order → SnapSupply routes the order to the nearest warehouse → a shipment is prepared and assigned to a delivery partner → the partner delivers the order → order marked as completed.

2. **Supplier Interaction**
   - Suppliers register their products via `supplier_products`, specifying available stock. SnapSupply uses this to fulfill inventory needs per order.

3. **Fulfillment & Delivery**
   - Orders are split into shipments.
   - Each shipment is handled by a warehouse and a delivery partner.
   - Realistic `shipped_at` and `delivered_at` timestamps simulate fulfillment timelines.

---

## 📊 Suggested Learning Exercises

- **Find the top 5 best-selling products this month.**
- **Which delivery partners have the best on-time rates?**
- **What’s the average time between `order_date` and `delivered_at`?**
- **Which warehouses are handling the most shipments?**
- **Are there any products with unusually high `product_reviews.rating` variance?**

---

## 🔖 Difficulty Level

| Level | Description |
|-------|-------------|
| 🟢 Easy | Designed for learners to explore basic relational models with enough depth to simulate real scenarios. No complex recursive joins or many-to-many edge cases. |

---

## 💡 Future Extensions

This schema could be extended to support:
- Inventory movement between warehouses.
- Dynamic pricing per supplier.
- Geolocation of customers and delivery partners.
- Simulated live order flows (streaming inserts).

---

**License:** MIT — use freely, contribute improvements, and customize for your own use cases.

---

