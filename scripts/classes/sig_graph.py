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
    Handles graph data loading, processing, and analysis logic.
    Separated from visualization concerns.
    """
    
    def __init__(self, data_path=None, sheet_id=None):
        """
        Initialize SigGraph with data loading
        
        Parameters:
        - data_path: Path to data file or URL
        - sheet_id: Google Sheets ID for direct access
        """
        self.sig_dat = SigDat(data_path, sheet_id)
        self.edges =  self.sig_dat.edges
        self.graph = None
        self._create_graph()
    
    
    def _create_graph(self):
        """Create NetworkX graph from edge data"""
        source_col = 'from'
        target_col = 'to'
        
        if source_col in self.edges.columns and target_col in self.edges.columns:
            self.graph = nx.from_pandas_edgelist(
                self.edges, 
                source=source_col, 
                target=target_col, 
                create_using=nx.Graph()
            )
        else:
            print(f"Required columns not found. Available: {list(self.edges.columns)}")
            self.graph = nx.Graph()
    
    def get_network_stats(self):
        """Get basic network statistics"""
        if not self.graph:
            return {'error': 'No graph available'}
        
        stats = {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'is_connected': nx.is_connected(self.graph),
            'unique_from_nodes': self.edges['from'].nunique() if 'from' in self.edges.columns else 'N/A',
            'unique_to_nodes': self.edges['to'].nunique() if 'to' in self.edges.columns else 'N/A',
            'unique_clusters_to_parent': self.edges['to_parent'].nunique() if 'to_parent' in self.edges.columns else 'N/A',
            'unique_clusters_from_parent': self.edges['from_parent'].nunique() if 'from_parent' in self.edges.columns else 'N/A',
            'unique_arrowkeepers': self.edges['arrowkeeper'].nunique() if 'arrowkeeper' in self.edges.columns else 'N/A'
        }
        
        if self.graph.number_of_nodes() > 0:
            stats['average_degree'] = sum(dict(self.graph.degree()).values()) / self.graph.number_of_nodes()
            
        return stats
    
    def get_cluster_summary(self):
        """Get summary of clusters in your Google template"""
        summary = {}
        
        if 'to_parent' in self.edges.columns:
            summary['to_parent_clusters'] = self.edges['to_parent'].value_counts().to_dict()
        
        if 'from_parent' in self.edges.columns:
            summary['from_parent_clusters'] = self.edges['from_parent'].value_counts().to_dict()
            
        if 'arrowkeeper' in self.edges.columns:
            summary['arrowkeeper_distribution'] = self.edges['arrowkeeper'].value_counts().to_dict()
            
        return summary
    
    def get_role_connections(self):
        """Analyze connections to/from 'roles' node"""
        if 'from' not in self.edges.columns or 'to' not in self.edges.columns:
            return "Missing required columns"
            
        # Find all connections involving 'roles'
        from_roles = self.edges[self.edges['from'] == 'roles']['to'].tolist()
        to_roles = self.edges[self.edges['to'] == 'roles']['from'].tolist()
        
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
        if cluster_by not in self.edges.columns:
            return {}
        
        node_clusters = {}
        
        # Map nodes to their clusters based on the selected cluster column
        for _, row in self.edges.iterrows():
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
        return self.edges
    
    def get_role_indicators(self):
        """
        Create mapping of nodes to their role connection status
        
        Returns:
        - dict: mapping of nodes to role indicator ('to_roles', 'from_roles', 'both', 'none')
        """
        if 'from' not in self.edges.columns or 'to' not in self.edges.columns:
            return {}
        
        role_indicators = {}
        all_nodes = set(self.edges['from'].unique()) | set(self.edges['to'].unique())
        
        # Find nodes that connect to roles
        to_roles = set(self.edges[self.edges['to'] == 'roles']['from'].unique())
        # Find nodes that connect from roles  
        from_roles = set(self.edges[self.edges['from'] == 'roles']['to'].unique())
        
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
        if 'from' not in self.edges.columns or 'to' not in self.edges.columns or 'arrowkeeper' not in self.edges.columns:
            return {}
        
        edge_arrowkeepers = {}
        
        for _, row in self.edges.iterrows():
            edge = (row['from'], row['to'])
            edge_arrowkeepers[edge] = row['arrowkeeper']
        
        return edge_arrowkeepers

    def get_networkx_graph(self):
        """Return the NetworkX graph object"""
        return self.graph