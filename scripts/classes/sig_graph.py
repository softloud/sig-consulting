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
    
    def __init__(self, data_path=None, sheet_id=None):
        """
        Initialize SigGraph with NetworkX graph creation
        
        Parameters:
        - data_path: Path to data file or URL
        - sheet_id: Google Sheets ID for direct access
        """
        self.sig_dat = SigDat(data_path, sheet_id)
        self.edges_df = self.sig_dat.get_edges_dataframe()
        self.nodes_df = self.sig_dat.get_nodes_dataframe()
        self.graph = None
        self._create_graph()
    
    def _create_graph(self):
        """Create NetworkX graph object from prepared dataframes"""
        if self.edges_df is None or self.edges_df.empty:
            print("❌ No edge data available for graph creation")
            self.graph = nx.Graph()
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
    
    def get_network_stats(self):
        """Get basic network statistics"""
        if not self.graph:
            return {'error': 'No graph available'}
        
        stats = {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'is_connected': nx.is_connected(self.graph),
            'unique_from_nodes': self.edges_df['from'].nunique() if 'from' in self.edges_df.columns else 'N/A',
            'unique_to_nodes': self.edges_df['to'].nunique() if 'to' in self.edges_df.columns else 'N/A',
            'unique_clusters_to_parent': self.edges_df['to_parent'].nunique() if 'to_parent' in self.edges_df.columns else 'N/A',
            'unique_clusters_from_parent': self.edges_df['from_parent'].nunique() if 'from_parent' in self.edges_df.columns else 'N/A',
            'unique_arrowkeepers': self.edges_df['arrowkeeper'].nunique() if 'arrowkeeper' in self.edges_df.columns else 'N/A'
        }
        
        if self.graph.number_of_nodes() > 0:
            stats['average_degree'] = sum(dict(self.graph.degree()).values()) / self.graph.number_of_nodes()
            
        return stats
    
    def get_cluster_summary(self):
        """Get summary of clusters in your Google template"""
        summary = {}
        
        if 'to_parent' in self.edges_df.columns:
            summary['to_parent_clusters'] = self.edges_df['to_parent'].value_counts().to_dict()
            
        if 'from_parent' in self.edges_df.columns:
            summary['from_parent_clusters'] = self.edges_df['from_parent'].value_counts().to_dict()
            
        if 'arrowkeeper' in self.edges_df.columns:
            summary['arrowkeeper_distribution'] = self.edges_df['arrowkeeper'].value_counts().to_dict()
            
        return summary
    
    def get_role_connections(self):
        """Analyze connections to/from 'roles' node"""
        if 'from' not in self.edges_df.columns or 'to' not in self.edges_df.columns:
            return "Missing required columns"
            
        # Find all connections involving 'roles'
        from_roles = self.edges_df[self.edges_df['from'] == 'roles']['to'].tolist()
        to_roles = self.edges_df[self.edges_df['to'] == 'roles']['from'].tolist()
        
        return {
            'nodes_connected_from_roles': from_roles,
            'nodes_connected_to_roles': to_roles,
            'total_roles_connections': len(from_roles) + len(to_roles)
        }
    
    def get_node_clusters(self, cluster_by='to_parent'):
        """
        Create node-to-cluster mapping based on the selected cluster column
        
        Parameters:
        - cluster_by: column to use for clustering ('to_parent', 'from_parent', or 'arrowkeeper')
        
        Returns:
        - dict: mapping of nodes to their clusters
        """
        if cluster_by not in self.edges_df.columns:
            return {}
        
        node_clusters = {}
        
        # Map nodes to their clusters based on the selected cluster column
        for _, row in self.edges_df.iterrows():
            source_node = row['from']
            target_node = row['to']
            cluster_value = row[cluster_by]
            
            # Assign cluster based on the clustering column
            if pd.notna(cluster_value):
                if cluster_by == 'to_parent':
                    # Target node belongs to the cluster
                    node_clusters[target_node] = cluster_value
                elif cluster_by == 'from_parent':
                    # Source node belongs to the cluster  
                    node_clusters[source_node] = cluster_value
                elif cluster_by == 'arrowkeeper':
                    # Both nodes can be influenced by arrowkeeper
                    node_clusters[source_node] = cluster_value
                    node_clusters[target_node] = cluster_value
        
        # Fill in missing nodes with 'unassigned'
        for node in self.graph.nodes():
            if node not in node_clusters:
                node_clusters[node] = 'unassigned'
        
        return node_clusters
    
    def get_data_source_info(self):
        """Get information about the current data source (delegates to SigDat)"""
        return self.sig_dat.get_data_source_info()
    
    def get_edges_dataframe(self):
        """Return the edges dataframe"""
        return self.edges_df
    
    def get_nodes_dataframe(self):
        """Return the nodes dataframe"""
        return self.nodes_df
    
    def get_networkx_graph(self):
        """Return the NetworkX graph object"""
        return self.graph
    
    def get_role_indicators(self):
        """
        Create mapping of nodes to their role connection status
        
        Returns:
        - dict: mapping of nodes to role indicator ('to_roles', 'from_roles', 'both', 'none')
        """
        if 'from' not in self.edges_df.columns or 'to' not in self.edges_df.columns:
            return {}
        
        role_indicators = {}
        all_nodes = set(self.edges_df['from'].unique()) | set(self.edges_df['to'].unique())
        
        # Find nodes that connect to roles
        to_roles = set(self.edges_df[self.edges_df['to'] == 'roles']['from'].unique())
        # Find nodes that connect from roles  
        from_roles = set(self.edges_df[self.edges_df['from'] == 'roles']['to'].unique())
        
        for node in all_nodes:
            if node == 'roles':
                role_indicators[node] = 'roles_node'
            elif node in to_roles and node in from_roles:
                role_indicators[node] = 'both'
            elif node in to_roles:
                role_indicators[node] = 'to_roles'
            elif node in from_roles:
                role_indicators[node] = 'from_roles'
            else:
                role_indicators[node] = 'none'
        
        return role_indicators

    def get_edge_arrowkeepers(self):
        """
        Create mapping of edges to their arrowkeeper values
        
        Returns:
        - dict: mapping of (from_node, to_node) tuples to arrowkeeper values
        """
        if 'from' not in self.edges_df.columns or 'to' not in self.edges_df.columns or 'arrowkeeper' not in self.edges_df.columns:
            return {}
        
        edge_arrowkeepers = {}
        
        for _, row in self.edges_df.iterrows():
            edge = (row['from'], row['to'])
            edge_arrowkeepers[edge] = row['arrowkeeper']
        
        return edge_arrowkeepers

    def get_networkx_graph(self):
        """Return the NetworkX graph object"""
        return self.graph