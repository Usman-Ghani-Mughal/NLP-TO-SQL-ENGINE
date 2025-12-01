import json
METADATAFILE_PATH = "E:\\Northumbria\\Study\Sem 3\\thesis\\Project\\NLP-TO-SQL-ENGINE\\nlp_to_sql_engine\\metadata\\metadata.json"
class MetaDataManager:
    def __init__(self, metadata_file='metadata.json'):
        self.metadata_file = METADATAFILE_PATH
        self.metadata = self.load_metadata()

    def get_metadata(self):
        return self.metadata
    
    def load_metadata(self):
        try:
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            raise(f"Error loading metadata: {e}")
            # return {"catalog": "", "schema": "", "tables": []}

    def get_tables(self):
        return self.metadata.get("tables", [])

    def get_table_columns(self, table_name):
        for table in self.get_tables():
            if table["table_name"] == table_name:
                return table.get("columns", [])
        return []

    def save_metadata(self):
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=4)