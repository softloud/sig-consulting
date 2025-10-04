import pandas as pd
import os
from dotenv import load_dotenv



class SigDat:
    """
    Data preparation layer for SIG (Structured Intelligence Governance).
    Focuses on loading raw data and preparing clean node and edge dataframes.

    This function will not work if client_credentials/.env does not have 
    DATA_ENTRY variable set.
    """
    
    def __init__(self, data_source="template"):
        """
        Initialize SigDat with data loading and preparation
        
        Parameters:
        - data_source: Source of the data (e.g., "template", "custom")

        Attributes:
        - data_source: Source of the data
        - edges_df: DataFrame of edges
        - nodes_df: DataFrame of nodes

        """
        # Load environment variables from client_credentials/.env

        if data_source == "template":
            load_dotenv('client_credentials/.env')
        elif data_source == "client":
            load_dotenv('client_credentials/.env-client', override=True)
        

        self._sheet_id = os.getenv('GS_SHEET_ID') 

        self.edges_df = self._load_data('edges')# .set_index(['from', 'to'])
        self.nodes_df = self._load_data('nodes')# .set_index(['node', 'role_context'])

        # helpers   
    def _load_data(self, sheet_name):

        # set sheet id
        if sheet_name == 'edges':
            GID = os.getenv('GS_GID_EDGES')
        elif sheet_name == 'nodes':
            GID = os.getenv('GS_GID_NODES')
        else:
            raise ValueError("sheet_name must be 'edges' or 'nodes'")
        
        # construct csv url
        csv_url = f"https://docs.google.com/spreadsheets/d/{self._sheet_id}/export?format=csv&gid={GID}"

        # read data from csv url
        return pd.read_csv(csv_url)
