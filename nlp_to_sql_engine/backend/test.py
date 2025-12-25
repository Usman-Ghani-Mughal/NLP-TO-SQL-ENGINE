import os
import json
from dotenv import load_dotenv
# from Configs import AzureOpenAIConfig
#from Configs import DatabricksConfig
from nlp_to_sql_engine.backend.configs.Databricks.DatabricksConfig import DatabricksConfig

load_dotenv()

# Create an instance of AzureOpenAIConfig with environment variables
# test = AzureOpenAIConfig(
#     openai_api_key = os.getenv("gpt_4_o_mini_AZURE_OPENAI_KEY"),
#     azure_endpoint = os.getenv("gpt_4_o_mini_AZURE_OPENAI_ENDPOINT"),
#     deployment_name = os.getenv("gpt_4_o_mini_AZURE_OPENAI_DEPLOYMENT_NAME"),
#     api_version = os.getenv("gpt_4_o_mini_AZURE_OPENAI_API_VERSION"),
#     temperature = 0.7
# )
# llm_model = test.get_ll_model()
# print(llm_model)
# ------------------------------------------------------------------------------

dbx = DatabricksConfig(
    host=os.getenv("DATABRICKS_HOST"), 
    token=os.getenv("DATABRICKS_TOKEN"), 
    sql_http_path=os.getenv("DATABRICKS_SQL_HTTP_PATH"), 
    catalog=os.getenv("CATALOG"), 
    schema=os.getenv("SCHEMA")
)

w = dbx.get_workspace_client()
user = w.current_user.me()
print("Connected as:", user.user_name)
cursor = dbx.get_sql_cursor()

catalog = os.getenv("CATALOG")
schema = os.getenv("SCHEMA")

sql_script = f"""
SELECT table_name, comment
FROM {catalog}.information_schema.tables
WHERE table_schema = '{schema}'
"""
cursor.execute(sql_script)
rows = cursor.fetchall()
meta_data = {
    "catalog": catalog,
    "schema":schema,
    "tables":[]
}
for row in rows:
    print(row.table_name)
    table_meta_daata = {
        "table_name": row.table_name,
        "table_description": row.comment,
        "row_count": 0,
        "sample_3_rows": [],
        "columns": []
    }
    
    # --------------- Get Rows count ---------------------
    row_count_sql_script = f"""
    SELECT COUNT(*) as row_count FROM {catalog}.{schema}.{row.table_name}
    """
    cursor.execute(row_count_sql_script)
    rows_count = cursor.fetchall()
    for rc in rows_count:
        table_meta_daata['row_count'] = rc.row_count
    # --------------------------------------------------
    
    # --------------- Get Sample 3 rows -----------------
    sample_rows_sql_script = f"""
    SELECT * FROM {catalog}.{schema}.{row.table_name} LIMIT 3
    """
    cursor.execute(sample_rows_sql_script)
    sample_rows = cursor.fetchall()
    for sr in sample_rows:
        sample_row_dict = {}
        for idx, col in enumerate(cursor.description):
            sample_row_dict[col[0]] = sr[idx]
        table_meta_daata["sample_3_rows"].append(sample_row_dict)
    # --------------------------------------------------
    
    
    columns_sql_script = f"""
    SELECT column_name, data_type, comment
    FROM {catalog}.information_schema.columns
    WHERE table_schema = '{schema}' AND table_name = '{row.table_name}'
    """
    cursor.execute(columns_sql_script)
    columns = cursor.fetchall()
    for column in columns:
        column_meta_data = {
            "column_name": column.column_name,
            "data_type": column.data_type,
            "column_description": column.comment,
            "distinct_values_count": None,
            "sample_values": []
        }
        # --------------- Get Distinct values count -----------------
        distinct_values_sql_script = f"""
        SELECT COUNT(DISTINCT {column.column_name}) as distinct_count
        FROM {catalog}.{schema}.{row.table_name}
        """
        cursor.execute(distinct_values_sql_script)
        distinct_values_counts = cursor.fetchall()
        sample_values = False
        for dvc in distinct_values_counts:
            column_meta_data["distinct_values_count"] = dvc.distinct_count
            if dvc.distinct_count <= 50:
                sample_values = True
        # --------------------------------------------------
        if sample_values:
            # get all distinct sample values
            sample_values_sql_script = f"""
            SELECT DISTINCT {column.column_name} as sample_value
            FROM {catalog}.{schema}.{row.table_name}
            """
            cursor.execute(sample_values_sql_script)
            all_distinct_values = cursor.fetchall()
            for adv in all_distinct_values:
                column_meta_data["sample_values"].append(adv.sample_value)
        else:
            # get 5 distinct sample values
            sample_values_sql_script_5 = f"""
            SELECT DISTINCT {column.column_name} as sample_value
            FROM {catalog}.{schema}.{row.table_name}
            LIMIT 5
            """
            cursor.execute(sample_values_sql_script_5)
            distinct_values_5 = cursor.fetchall()
            for dv5 in distinct_values_5:
                column_meta_data["sample_values"].append(dv5.sample_value)
        
        table_meta_daata["columns"].append(column_meta_data)
    
    meta_data["tables"].append(table_meta_daata)
    
    
print(meta_data)

import datetime as dt
def datetime_converter(o):
    if isinstance(o, dt.datetime):
        # UTC ISO format with milliseconds: 2025-11-23T00:47:41.843+00:00
        return o.astimezone(dt.timezone.utc).isoformat(timespec="milliseconds")
    return str(o)  # fallback, just in case

with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(meta_data, f, indent=4, default=datetime_converter)
