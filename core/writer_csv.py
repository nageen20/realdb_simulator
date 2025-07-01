import os

def write_csvs(dataframes: dict, output_dir="output/csv"):
    os.makedirs(output_dir, exist_ok=True)
    for table, df in dataframes.items():
        df.to_csv(f"{output_dir}/{table}.csv", index=False)
