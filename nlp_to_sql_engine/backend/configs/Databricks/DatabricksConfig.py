from databricks.sdk import WorkspaceClient
from databricks import sql
from ..BaseConfig.BaseConfig import BaseConfig
import os


class DatabricksConfig(BaseConfig):
    """
    Central place to manage all Databricks-related configuration and clients.
    """

    def __init__(self, host, token, sql_http_path, catalog, schema) -> None:
        self.host = host
        self.token = token
        self.sql_http_path = sql_http_path

        # Optional defaults for your NLP-to-SQL engine
        self.default_catalog = catalog
        self.default_schema = schema

        # Lazy-initialized clients
        self._workspace_client: WorkspaceClient | None = None
        self._sql_connection = None
        
        super().__init__()

    # ---------- internal helpers ----------

    def validate(self) -> None:
        print("Validating Databricks configuration...")
        missing = []
        if not self.host:
            missing.append("DATABRICKS_HOST")
        if not self.token:
            missing.append("DATABRICKS_TOKEN")
        if not self.sql_http_path:
            missing.append("DATABRICKS_SQL_HTTP_PATH")

        if missing:
            raise RuntimeError(
                f"Missing required Databricks env vars in .env: {', '.join(missing)}"
            )
        print("Databricks configuration is valid.")

    # ---------- public: workspace client ----------

    def get_workspace_client(self) -> WorkspaceClient:
        """
        Returns a singleton WorkspaceClient instance.
        """
        if self._workspace_client is None:
            # SDK reads from env vars, so make sure they’re set
            os.environ["DATABRICKS_HOST"] = self.host
            os.environ["DATABRICKS_TOKEN"] = self.token

            self._workspace_client = WorkspaceClient()
        return self._workspace_client

    # ---------- public: SQL Warehouse connection ----------

    def get_sql_connection(self):
        """
        Returns a singleton SQL connection to your SQL Warehouse.
        """
        if self._sql_connection is None:
            server_hostname = self.host.replace("https://", "").rstrip("/")

            self._sql_connection = sql.connect(
                server_hostname=server_hostname,
                http_path=self.sql_http_path,
                access_token=self.token,
            )
        return self._sql_connection

    def get_sql_cursor(self):
        """
        Convenience helper to get a fresh cursor.
        """
        conn = self.get_sql_connection()
        return conn.cursor()

    def close_sql_connection(self) -> None:
        """
        Cleanly close the SQL connection (e.g. on app shutdown).
        """
        if self._sql_connection is not None:
            self._sql_connection.close()
            self._sql_connection = None
