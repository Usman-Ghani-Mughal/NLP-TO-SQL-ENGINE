import os
import json
from dotenv import load_dotenv
from Configs import AzureOpenAIConfig
from Configs import DatabricksConfig

load_dotenv()

# Create an instance of AzureOpenAIConfig with environment variables
test = AzureOpenAIConfig(
    openai_api_key = os.getenv("gpt_4_o_mini_AZURE_OPENAI_KEY"),
    azure_endpoint = os.getenv("gpt_4_o_mini_AZURE_OPENAI_ENDPOINT"),
    deployment_name = os.getenv("gpt_4_o_mini_AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_version = os.getenv("gpt_4_o_mini_AZURE_OPENAI_API_VERSION"),
    temperature = 0.7
)
llm_model = test.get_ll_model()
print(llm_model)
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
        "columns": []
    }
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
            "column_description": column.comment
        }
        table_meta_daata["columns"].append(column_meta_data)
    
    meta_data["tables"].append(table_meta_daata)
    
print(meta_data)

with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(meta_data, f, indent=4)
