
# 📘 How to Add a New Schema

This guide explains how to define and integrate a new schema into the RealDB Simulator project using YAML. Schemas define the structure, metadata, relationships, and data generation logic for your domain-specific datasets.

---

## 📂 Folder Structure

Place your new schema files in a folder under the `schemas/` directory organized by domain.

```
schemas/
└── ecommerce/
    └── shopshift_easy_v1.yaml
└── supply_chain/
    └── snapsupply_easy_v2.yaml
```

Each schema YAML file should be accompanied by:
- A `context/` Markdown file (`.md`) describing the business case.
- Any necessary CSV lookup files inside the global `data/` directory.

---

## 🧾 YAML File Template Explained

Below is an annotated breakdown of a schema YAML file:

```yaml
name: ShopSwift (Easy)      # Project name
tag: ecommerce              # Project domain
difficulty: easy            # Project difficulty

tables:                                     # Start adding tables below
    customers:                        
        rows: 100                           # Default number of rows to be generated in the table
        columns:                            # Start adding columns below
            id:
                type: int                   # Data generation type. Reference below for available types
                data_type: int              # SQL Data type

            name:
                type: name
                data_type: VARCHAR(200)

            email:
                type: email
                data_type: VARCHAR(300)

        primary_key: [id]                   # Primary keys in the table. List all the columns that are part of the primary key here

    supplier_products:                      # Adding second table
    rows: 200
    columns:
      id:
        type: int
        data_type: INT
        
      supplier_id:
        type: int
        data_type: INT
        
      product_id:
        type: int
        data_type: INT
        
      stock_quantity:
        type: random_int
        data_type: INT
        min: 50
        max: 500
    primary_key: [id]
    foreign_keys:                           # Adding foreign keys. List the foreign key columns in the table below
      supplier_id: suppliers.id             # Map the foreign key to the referencing table and column using the table_name.column_name syntax
      product_id: products.id

```

---

## 🔑 Column Fields Reference

| Field          | Description |
|----------------|-------------|
| `type`         | Faker or custom generator function (e.g., `name`, `email`, `fetch_from_file`, `date_between`) |
| `data_type`    | SQL data type (e.g., `VARCHAR(100)`, `INT`, `DECIMAL(10,2)`) |
| `values`       | Enum values (used in `weighted_enum`) |
| `weights`      | Probabilities for each enum value |
| `min`/`max`    | Range for integers, floats, or dates |
| `start_date`/`end_date` | For date generators like `date_between` |
| `depends_on`   | Specify another column (same or different table) this field depends on |
| `dependent_formula` | Type of logic (`equals`, `hierarchy`, `conditional`, `pandas`) |
| `conditions`   | Mapping for conditional logic (typically used with `dependent_formula: conditional`) |
| `source_file`  | Path to external CSV file for value lookup |
| `group`        | Used for grouped fields like locations |
| `primary_key`  | Used for generating primary key columns |
| `foreign_key`  | Used for generating foreign key columns |

---

## 📚 Common Generators

| Generator             | Description |
|-----------------------|-------------|
| `random_int`          | Generates random integers (with optional min/max) |
| `pydecimal`           | Decimal with optional distribution |
| `date_between`        | Random date between two dates |
| `fetch_from_file`     | Load value from CSV column |
| `dependent_column`    | Set value based on another column |
| `weighted_enum`       | Random choice with weighted probabilities |
| `review_text`         | Sentiment-based review generator |

---

## 🧠 Advanced Use Cases

- **Hierarchical Lookup**:
  ```yaml
  product_name:
    type: fetch_from_file
    depends_on: product_category
    dependent_formula: hierarchy
    source_file: product_hierarchy.csv
  ```

- **Conditional Mapping**:
  ```yaml
  status:
    type: dependent_column
    depends_on: order_status
    dependent_formula: conditional
    conditions:
      cancelled: [refunded]
      placed: [paid]
  ```

- **Cross-table Dependency**:
  ```yaml
  order_date:
    type: date_time_between
    min: customers.signup_date
    max: now
  ```

---

## ➕ Steps to Add a New Schema

1. **Create a YAML file** under the correct domain folder (`schemas/supply_chain/my_schema.yaml`)
2. **Write a context file** in `context/domain/` folder explaining the business case
3. **Add any required CSV lookup files** in `data/`
4. **Add entry to the project index JSON file**:
    ```json
    {
        "name": "ShopShift",
        "emoji": "🛒",
        "path": "ecommerce/shopshift_easy_v2.yaml",
        "context": "ecommerce/shopshift_easy_v1.md",
        "data": "ecommerce/",
        "tag": "ecommerce",
        "difficulty": "easy"
    }
    ```
5. Run the app using:
    ```bash
    streamlit run app/🏠 Home.py
    ```

---

## 🧪 Tips for Designing Realistic Schemas

- Add real-world constraints: foreign keys, dependencies, enums
- Include numerical ranges and weights for more realistic distributions
- Use `depends_on` and `dependent_formula` for logic-heavy relationships
- Use separate CSVs for scalable value lookups (e.g., product catalog)
