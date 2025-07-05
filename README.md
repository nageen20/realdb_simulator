# 🧪 RealDB Playground

RealDB Playground is an open-source project to help learners, educators, and developers **simulate real-world OLTP databases** — complete with realistic schemas, fake yet meaningful data, and support for multiple database backends.

> Say goodbye to toy datasets with two tables — and hello to full, production-like relational systems you can practice on.

---

## 🚀 Features

- 🏗️ Choose from prebuilt **industry-style database schemas** (supply chain, eCommerce)
- 🤖 Generate **realistic synthetic data** using [Faker](https://faker.readthedocs.io/)
- 🧠 Supports **column relationships**, foreign keys, and dependency-based data generation
- 🧾 Export to **CSV** or insert directly into **PostgreSQL**, **MySQL**
- 🖼️ View **ER diagrams** and business context right in the UI
- 🎛️ Streamlit frontend to select schemas, view info, and simulate data

---

# 🚀 Getting Started with RealDB Simulator

This guide will help you clone, install dependencies, and run the project locally using Streamlit.

---

## 📁 Clone the Repository

```bash
git clone https://github.com/yourusername/realdb-simulator.git
cd realdb-simulator
```

## 🐍 Set Up Your Environment

### Option 1: Using Conda

```
conda create -n realdb python=3.10 -y
conda activate realdb

```

### Option 2: Using venv
```
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

```

## 📦 Install Dependencies
```
pip install -r requirements.txt

```

## 📁 Project Structure (Simplified)
```
realdb-simulator/
├── app/                     # Streamlit UI files
├── core/
│   ├── generators/          # Field & table data generators
│   ├── output_handlers/     # CSV, SQL, and DB writers
│   └── services/            # Coordination logic for data gen
└── utils/                   # Shared utilities
├── schemas/                 # YAML schemas organized by domain
├── context/                 # Markdown files for business context
├── data/                    # Lookup CSVs, hierarchies, etc.
├── requirements.txt
└── README.md
```

## 🖥️ Run the Streamlit App
Use the following command to launch the main Streamlit interface:
```
streamlit run app/🏠 Home.py

```