import pandas as pd
from nlp_to_sql_engine.backend.configs.Databricks.DatabricksConfig import DatabricksConfig

class RunQueryAgent:
    def __init__(self, query, databricks_host, databricks_token, sql_http_path, catalog, schema):
        print("Initializing RunQueryAgent...")
        self.query = query
        self.dbx_config = DatabricksConfig(
            host=databricks_host,
            token=databricks_token,
            sql_http_path=sql_http_path,
            catalog=catalog,
            schema=schema
        )
        print("RunQueryAgent initialized")

    def run(self):
        try:
            workspace_client = self.dbx_config.get_workspace_client()
            cursor = self.dbx_config.get_sql_cursor()
            cursor.execute(self.query)
            # Get column names from cursor
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            df = pd.DataFrame(rows, columns=columns)
            return {"query": self.query, "response":df, "success": True}
        except Exception as e:
            raise
            #raise(f"Error in RunQueryAgent run method: {e}")
            # raise RuntimeError(f"Failed to execute query: {e}")