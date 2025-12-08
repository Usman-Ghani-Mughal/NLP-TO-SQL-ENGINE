import os
import json
from dotenv import load_dotenv
from nlp_to_sql_engine.backend.agents.GenrateQueryAgent.GenrateQueryAgent import GenrateQueryAgent
from nlp_to_sql_engine.backend.agents.RunQueryAgent.RunQueryAgent import RunQueryAgent


load_dotenv()

def start_agent(frontend_prompt):
    print("Received prompt from frontend:", frontend_prompt)
    genrate_query_agent = GenrateQueryAgent(
        question=frontend_prompt,
        openai_api_key = os.getenv("gpt_4_o_mini_AZURE_OPENAI_KEY"),
        azure_endpoint = os.getenv("gpt_4_o_mini_AZURE_OPENAI_ENDPOINT"),
        deployment_name = os.getenv("gpt_4_o_mini_AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version = os.getenv("gpt_4_o_mini_AZURE_OPENAI_API_VERSION"),
        temperature = 0.7
    )
    response_sql_query = genrate_query_agent.run()
    
    print('<<------STEP 1------>>')
    print("Generated SQL Query:", response_sql_query)
    print('<<----------------->>')
    run_query_agent = RunQueryAgent(
        query=response_sql_query,
        databricks_host=os.getenv("DATABRICKS_HOST"),
        databricks_token=os.getenv("DATABRICKS_TOKEN"),
        sql_http_path=os.getenv("DATABRICKS_SQL_HTTP_PATH"),
        catalog=os.getenv("CATALOG"),
        schema=os.getenv("SCHEMA")
    )
    response_run_query = run_query_agent.run()
    return response_run_query
    # ------------------------------------------------
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # response_sql_query = """
    # SELECT product_id, CAST(price AS FLOAT) as price
    # FROM ecom.brazilian_ecom_olist.orderitems_bronze
    # ORDER BY price DESC
    # LIMIT 3
    # """ 
    # import pandas as pd
    # import numpy as np
    # import random
    # import uuid

    # # reproducibility
    # np.random.seed(42)

    # # 500 rows
    # n = 500

    # def random_product_id():
    #     return uuid.uuid4().hex[:32]

    # def random_customer_id():
    #     return uuid.uuid4().hex[:16]

    # def random_seller_id():
    #     return uuid.uuid4().hex[:16]
    
    # # sample categories
    # categories = [
    #     "beauty", "electronics", "furniture", "sports", "fashion",
    #     "stationery", "health", "pet_shop", "toys", "kitchen"
    # ]

    # # generate dataframe
    # df = pd.DataFrame({
    #     "order_id": [uuid.uuid4().hex[:20] for _ in range(n)],
    #     "customer_id": [random_customer_id() for _ in range(n)],
    #     "seller_id": [random_seller_id() for _ in range(n)],
    #     "product_id": [random_product_id() for _ in range(n)],
    #     "category": np.random.choice(categories, n),
    #     "price": np.round(np.random.uniform(10, 2000, n), 2),
    #     "freight_value": np.round(np.random.uniform(5, 200, n), 2),
    #     "order_purchase_timestamp": pd.to_datetime(
    #         np.random.choice(pd.date_range("2023-01-01", "2023-12-31"), n)
    #     )
    # })
    # return {"query": response_sql_query, "response":df, "success": True}
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
    # return response_run_query