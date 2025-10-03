import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import networkx as nx
from scripts.classes.sig_graph import SigGraph
from scripts.classes.sig_dat import SigDat

class SigVis:
    """
    Handles visualization of SIG network data.
    Uses SigGraph for data loading and graph operations.
    """

    def __init__(self, data_path=None, sheet_id=None):
        """
        Initialize SigVis with a SigGraph instance
        
        Parameters:
        - data_path: Path to data file or URL
        - sheet_id: Google Sheets ID for direct access
        """
        self.sig_graph = SigGraph(data_path=data_path, sheet_id=sheet_id)

        
    @property
    def edges(self):
        """Convenience property to access edges dataframe"""
        return self.sig_graph.get_edges_dataframe()
    
    @property
    def graph(self):
        """Convenience property to access NetworkX graph"""
        return self.sig_graph.get_networkx_graph()
    
    def plot(self, figsize=(12, 8), node_size=1000, with_labels=True, layout='spring'):
        """
        Create a network visualization from the edges data
        Uses 'from' and 'to' columns from your Google template
        """
        if not self.graph or self.graph.number_of_nodes() == 0:
            print("No graph data available for plotting")
            return
        
        # Set up the plot
        plt.figure(figsize=figsize)
        
        # Choose layout
        layout_functions = {
            'spring': lambda g: nx.spring_layout(g, k=1, iterations=50),
            'circular': nx.circular_layout,
            'random': nx.random_layout,
            'shell': nx.shell_layout
        }
        pos = layout_functions.get(layout, nx.spring_layout)(self.graph)
        
        # Draw the network
        nx.draw(
            self.graph, pos,
            node_size=node_size,
            node_color='lightblue',
            edge_color='gray',
            with_labels=with_labels,
            font_size=10,
            font_weight='bold'
        )
        
        plt.title("Network Visualization", size=16)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        
        # Print basic network stats
        print(f"Network has {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")
        if self.graph.number_of_nodes() > 0:
            print(f"Average degree: {sum(dict(self.graph.degree()).values()) / self.graph.number_of_nodes():.2f}")

    def plot_clustered(self, cluster_by='to_parent', figsize=(14, 10), node_size=1500, layout='spring'):
        """
        Create a network visualization with nodes colored by cluster
        Uses your Google template columns: from -> to, clustered by to_parent
        
        Parameters:
        - cluster_by: column to use for clustering ('to_parent', 'from_parent', or 'arrowkeeper')
        - figsize: tuple for figure size
        - node_size: size of nodes in the plot
        - layout: layout algorithm ('spring', 'circular', 'random', 'shell')
        """
        if not self.graph or self.graph.number_of_nodes() == 0:
            print("No graph data available for plotting")
            return
        
        # Get node clusters from SigGraph
        node_clusters = self.sig_graph.get_node_clusters(cluster_by)
        
        if not node_clusters:
            print(f"Cluster column '{cluster_by}' not found or empty")
            return
        
        # Get unique clusters and assign colors
        unique_clusters = list(set(node_clusters.values()))
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_clusters)))
        cluster_colors = dict(zip(unique_clusters, colors))
        
        # Create color list for nodes
        node_colors = [cluster_colors[node_clusters[node]] for node in self.graph.nodes()]
        
        # Set up the plot
        plt.figure(figsize=figsize)
        
        # Choose layout
        layout_functions = {
            'spring': lambda g: nx.spring_layout(g, k=2, iterations=50),
            'circular': nx.circular_layout,
            'random': nx.random_layout,
            'shell': nx.shell_layout
        }
        pos = layout_functions.get(layout, lambda g: nx.spring_layout(g, k=2, iterations=50))(self.graph)
        
        # Draw the network
        nx.draw(
            self.graph, pos,
            node_size=node_size,
            node_color=node_colors,
            edge_color='gray',
            with_labels=True,
            font_size=9,
            font_weight='bold',
            alpha=0.8
        )
        
        # Create legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor=color, markersize=10, 
                      label=f'{cluster}')
            for cluster, color in cluster_colors.items()
        ]
        
        plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))
        plt.title(f"Network Clustered by '{cluster_by}'", size=16)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        
        # Print cluster information
        print(f"\nClustering by '{cluster_by}':")
        for cluster in sorted(unique_clusters):
            nodes_in_cluster = [node for node, c in node_clusters.items() if c == cluster]
            print(f"  {cluster}: {len(nodes_in_cluster)} nodes - {nodes_in_cluster}")

    # Delegate analysis methods to SigGraph
    def get_network_stats(self):
        """Get basic network statistics using your Google template columns"""
        return self.sig_graph.get_network_stats()
    
    def get_cluster_summary(self):
        """Get summary of clusters in your Google template"""
        return self.sig_graph.get_cluster_summary()
    
    def get_role_connections(self):
        """Analyze connections to/from 'roles' node"""
        return self.sig_graph.get_role_connections()
    
    def get_data_source_info(self):
        """Get information about the current data source"""
        return self.sig_graph.get_data_source_info()
    
    def table(self):
        """Return the edges dataframe for display"""
        return self.edges

    def table_min_req(self):
        """Get minimum requirements for the analysis"""
        return self.edges[['from', 'to', 'to_parent', 'from_parent', 'arrowkeeper', "to_minimum_requirements"]]

    def plot_with_role_shapes(self, cluster_by='to_parent', figsize=(14, 10), node_size=1500, layout='spring'):
        """
        Create a network visualization with nodes shaped by role connections
        
        Node shapes:
        - Circle: nodes that connect TO roles
        - Square: nodes that connect FROM roles  
        - Diamond: nodes that connect both ways with roles
        - Triangle: the 'roles' node itself
        - Pentagon: nodes with no role connections
        
        Parameters:
        - cluster_by: column to use for coloring ('to_parent', 'from_parent', or 'arrowkeeper')
        - figsize: tuple for figure size
        - node_size: size of nodes in the plot
        - layout: layout algorithm ('spring', 'circular', 'random', 'shell')
        """
        if not self.graph or self.graph.number_of_nodes() == 0:
            print("No graph data available for plotting")
            return
        
        # Get role indicators and node clusters
        role_indicators = self.sig_graph.get_role_indicators()
        node_clusters = self.sig_graph.get_node_clusters(cluster_by)
        
        if not role_indicators:
            print("No role indicators found")
            return
        
        if not node_clusters:
            print(f"Cluster column '{cluster_by}' not found or empty")
            return
        
        # Get unique clusters and assign colors
        unique_clusters = list(set(node_clusters.values()))
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_clusters)))
        cluster_colors = dict(zip(unique_clusters, colors))
        
        # Define node shapes based on role indicators
        shape_mapping = {
            'to_roles': 'o',      # Circle
            'from_roles': 's',    # Square
            'both': 'D',          # Diamond
            'roles_node': '^',    # Triangle
            'none': 'p'           # Pentagon
        }
        
        # Set up the plot
        plt.figure(figsize=figsize)
        
        # Choose layout
        layout_functions = {
            'spring': lambda g: nx.spring_layout(g, k=2, iterations=50),
            'circular': nx.circular_layout,
            'random': nx.random_layout,
            'shell': nx.shell_layout
        }
        pos = layout_functions.get(layout, lambda g: nx.spring_layout(g, k=2, iterations=50))(self.graph)
        
        # Draw nodes by shape groups
        for role_type, shape in shape_mapping.items():
            # Get nodes of this role type
            nodes_of_type = [node for node in self.graph.nodes() 
                           if role_indicators.get(node) == role_type]
            
            if nodes_of_type:
                # Get colors for these nodes
                node_colors = [cluster_colors[node_clusters[node]] for node in nodes_of_type]
                
                # Draw this group of nodes
                nx.draw_networkx_nodes(
                    self.graph, pos,
                    nodelist=nodes_of_type,
                    node_color=node_colors,
                    node_shape=shape,
                    node_size=node_size,
                    alpha=0.8
                )
        
        # Draw edges
        nx.draw_networkx_edges(self.graph, pos, edge_color='gray', alpha=0.6)
        
        # Draw labels
        nx.draw_networkx_labels(self.graph, pos, font_size=9, font_weight='bold')
        
        # Create legend for shapes
        shape_legend_elements = []
        shape_descriptions = {
            'to_roles': 'Connects TO roles',
            'from_roles': 'Connects FROM roles', 
            'both': 'Bidirectional with roles',
            'roles_node': 'Roles node',
            'none': 'No role connections'
        }
        
        for role_type, shape in shape_mapping.items():
            if any(role_indicators.get(node) == role_type for node in self.graph.nodes()):
                shape_legend_elements.append(
                    plt.Line2D([0], [0], marker=shape, color='w', 
                              markerfacecolor='gray', markersize=10,
                              label=shape_descriptions[role_type], linestyle='None')
                )
        
        # Create legend for colors (clusters)
        color_legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor=color, markersize=10, 
                      label=f'{cluster}')
            for cluster, color in cluster_colors.items()
        ]
        
        # Add both legends
        shape_legend = plt.legend(handles=shape_legend_elements, loc='upper left', 
                                bbox_to_anchor=(1, 1), title='Node Shapes (Role Connections)')
        plt.gca().add_artist(shape_legend)
        
        color_legend = plt.legend(handles=color_legend_elements, loc='upper left', 
                                bbox_to_anchor=(1, 0.6), title=f'Node Colors ({cluster_by})')
        
        plt.title(f"Network: Shapes by Role Connections, Colors by {cluster_by}", size=16)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        
        # Print role connection summary
        print(f"\n🎯 Role Connection Summary:")
        for role_type, description in shape_descriptions.items():
            nodes_of_type = [node for node in role_indicators.keys() 
                           if role_indicators[node] == role_type]
            if nodes_of_type:
                print(f"  {description}: {nodes_of_type}")

    def plot_with_role_shapes_and_arrowkeeper_lines(self, cluster_by='to_parent', figsize=(16, 12), node_size=1500, layout='spring'):
        """
        Create a network visualization with:
        - Node shapes based on role connections
        - Node colors based on cluster_by parameter
        - Edge line styles based on arrowkeeper
        
        Node shapes:
        - Circle: nodes that connect TO roles
        - Square: nodes that connect FROM roles  
        - Diamond: nodes that connect both ways with roles
        - Triangle: the 'roles' node itself
        - Pentagon: nodes with no role connections
        
        Edge line styles by arrowkeeper:
        - Solid: first arrowkeeper
        - Dashed: second arrowkeeper
        - Dotted: third arrowkeeper
        - Dash-dot: fourth arrowkeeper
        
        Parameters:
        - cluster_by: column to use for node coloring ('to_parent', 'from_parent', or 'arrowkeeper')
        - figsize: tuple for figure size
        - node_size: size of nodes in the plot
        - layout: layout algorithm ('spring', 'circular', 'random', 'shell')
        """
        if not self.graph or self.graph.number_of_nodes() == 0:
            print("No graph data available for plotting")
            return
        
        # Get role indicators and node clusters
        role_indicators = self.sig_graph.get_role_indicators()
        node_clusters = self.sig_graph.get_node_clusters(cluster_by)
        
        if not role_indicators:
            print("No role indicators found")
            return
        
        if not node_clusters:
            print(f"Cluster column '{cluster_by}' not found or empty")
            return
        
        # Get edge arrowkeeper data
        edge_arrowkeepers = self.sig_graph.get_edge_arrowkeepers()
        
        # Get unique clusters and assign colors
        unique_clusters = list(set(node_clusters.values()))
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_clusters)))
        cluster_colors = dict(zip(unique_clusters, colors))
        
        # Get unique arrowkeepers and assign line styles
        unique_arrowkeepers = list(set(edge_arrowkeepers.values()))
        line_styles = ['-', '--', ':', '-.']  # solid, dashed, dotted, dash-dot
        # Extend line styles if we have more arrowkeepers
        while len(line_styles) < len(unique_arrowkeepers):
            line_styles.extend(['-', '--', ':', '-.'])
        arrowkeeper_styles = dict(zip(unique_arrowkeepers, line_styles[:len(unique_arrowkeepers)]))
        
        # Define node shapes based on role indicators
        shape_mapping = {
            'to_roles': 'o',      # Circle
            'from_roles': 's',    # Square
            'both': 'D',          # Diamond
            'roles_node': '^',    # Triangle
            'none': 'p'           # Pentagon
        }
        
        # Set up the plot
        plt.figure(figsize=figsize)
        
        # Choose layout
        layout_functions = {
            'spring': lambda g: nx.spring_layout(g, k=2, iterations=50),
            'circular': nx.circular_layout,
            'random': nx.random_layout,
            'shell': nx.shell_layout
        }
        pos = layout_functions.get(layout, lambda g: nx.spring_layout(g, k=2, iterations=50))(self.graph)
        
        # Draw edges grouped by arrowkeeper (line style)
        for arrowkeeper, line_style in arrowkeeper_styles.items():
            # Get edges for this arrowkeeper
            edges_of_type = [(u, v) for u, v in self.graph.edges() 
                           if edge_arrowkeepers.get((u, v)) == arrowkeeper]
            
            if edges_of_type:
                # Draw this group of edges with consistent line style
                nx.draw_networkx_edges(
                    self.graph, pos,
                    edgelist=edges_of_type,
                    style=line_style,
                    edge_color='gray',
                    alpha=0.6,
                    width=1.5
                )
        
        # Draw nodes by shape groups
        for role_type, shape in shape_mapping.items():
            # Get nodes of this role type
            nodes_of_type = [node for node in self.graph.nodes() 
                           if role_indicators.get(node) == role_type]
            
            if nodes_of_type:
                # Get colors for these nodes
                node_colors = [cluster_colors[node_clusters[node]] for node in nodes_of_type]
                
                # Draw this group of nodes
                nx.draw_networkx_nodes(
                    self.graph, pos,
                    nodelist=nodes_of_type,
                    node_color=node_colors,
                    node_shape=shape,
                    node_size=node_size,
                    alpha=0.8
                )
        
        # Draw labels
        nx.draw_networkx_labels(self.graph, pos, font_size=10, font_weight='bold')
        
        # Create legend for shapes
        shape_legend_elements = []
        shape_descriptions = {
            'to_roles': 'Connects TO roles',
            'from_roles': 'Connects FROM roles', 
            'both': 'Bidirectional with roles',
            'roles_node': 'Roles node',
            'none': 'No role connections'
        }
        
        for role_type, shape in shape_mapping.items():
            if any(role_indicators.get(node) == role_type for node in self.graph.nodes()):
                shape_legend_elements.append(
                    plt.Line2D([0], [0], marker=shape, color='w', 
                              markerfacecolor='gray', markersize=10,
                              label=shape_descriptions[role_type], linestyle='None')
                )
        
        # Create legend for colors (clusters)
        color_legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor=color, markersize=10, 
                      label=f'{cluster}')
            for cluster, color in cluster_colors.items()
        ]
        
        # Create legend for line styles (arrowkeepers)
        line_legend_elements = [
            plt.Line2D([0], [0], color='gray', linewidth=2, 
                      linestyle=style, label=f'{arrowkeeper}')
            for arrowkeeper, style in arrowkeeper_styles.items()
        ]
        
        # Add all three legends
        shape_legend = plt.legend(handles=shape_legend_elements, loc='upper left', 
                                bbox_to_anchor=(1, 1), title='Node Shapes (Role Connections)')
        plt.gca().add_artist(shape_legend)
        
        color_legend = plt.legend(handles=color_legend_elements, loc='upper left', 
                                bbox_to_anchor=(1, 0.7), title=f'Node Colors ({cluster_by})')
        plt.gca().add_artist(color_legend)
        
        line_legend = plt.legend(handles=line_legend_elements, loc='upper left', 
                               bbox_to_anchor=(1, 0.4), title='Edge Styles (Arrowkeeper)')
        
        plt.title(f"Network: Shapes by Role, Colors by {cluster_by}, Lines by Arrowkeeper", size=16)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        
        # Print summary
        print(f"\n🎯 Visualization Summary:")
        print(f"  Node shapes: Role connections")
        print(f"  Node colors: {cluster_by}")
        print(f"  Edge styles: Arrowkeeper")
        print(f"\n📊 Arrowkeeper Line Styles:")
        for arrowkeeper, style in arrowkeeper_styles.items():
            style_name = {'−': 'solid', '--': 'dashed', ':': 'dotted', '-.': 'dash-dot'}.get(style, style)
            print(f"  {arrowkeeper}: {style_name}")

    def plot_by_arrowkeeper(self, figsize=(14, 10), node_size=1500):
        """Create visualization clustered by arrowkeeper"""
        return self.plot_clustered(cluster_by='arrowkeeper', figsize=figsize, node_size=node_size)
    
    def plot_role_shapes(self, cluster_by='to_parent', figsize=(14, 10), node_size=1500):
        """Convenience method for role-based shape plotting"""
        return self.plot_with_role_shapes(cluster_by=cluster_by, figsize=figsize, node_size=node_size)