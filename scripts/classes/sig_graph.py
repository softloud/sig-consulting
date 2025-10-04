import pandas as pd
import os
import gspread
from google.auth import default
from dotenv import load_dotenv
import networkx as nx
from scripts.classes.sig_dat import SigDat

# Load environment variables from client_credentials/.env
load_dotenv('client_credentials/.env')

class SigGraph:
    """
    Graph object creation and network analysis layer.
    Uses prepared dataframes from SigDat to create NetworkX graph objects and perform analysis.
    """
    
    def __init__(self, data_path=None):
        """
        Initialize SigGraph with NetworkX graph creation
        
        Parameters:
        - data_path: Path to data file or URL
        - sheet_id: Google Sheets ID for direct access
        """
        self.sig_dat = SigDat(data_path)
        self.edges_df = self.sig_dat.edges_df
        self.nodes_df = self.sig_dat.nodes_df
        self.graph = None
        self._create_graph()
    
    def _create_graph(self):
        """Create NetworkX graph object from prepared dataframes"""
        if self.edges_df is None or self.edges_df.empty:
            print("❌ No edge data available for graph creation")
            self.graph = nx.DiGraph()
            return
            
        # Create graph from edges dataframe
        self.graph = nx.from_pandas_edgelist(
            self.edges_df, 
            source='from', 
            target='to', 
            edge_attr=True,  # Include all edge attributes
            create_using=nx.Graph()
        )
        
        # Add node attributes from nodes dataframe
        if self.nodes_df is not None and not self.nodes_df.empty:
            node_attrs = self.nodes_df.set_index('node').to_dict('index')
            nx.set_node_attributes(self.graph, node_attrs)
        
        print(f"✅ Graph created: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")
    

    def get_networkx_graph(self):
        """Return the NetworkX graph object"""
        return self.graph