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

    def __init__(self, data_path=None):
        """
        Initialize SigVis with a SigGraph instance
                """
        self.sig_graph = SigGraph(data_path=data_path)
    
    @property
    def edges(self):
        """Convenience property to access edges dataframe"""
        return self.sig_graph.edges_df
    
    @property
    def graph(self):
        """Convenience property to access NetworkX graph"""
        return self.sig_graph.graph

    @property
    def nodes(self):
        """Get node attributes for plotting"""
        return self.sig_graph.nodes_df

    def table_min_req(self):
        """Get minimum requirements for the analysis"""
        return self.edges[[
            'from', 
            'to', 
            'arrowkeeper', 
            "to_minimum_requirements",
            "status"]]

    def plot_role_contexts(self):
        G = self.graph
        pos = nx.spring_layout(G)
        node_attrs = self._node_plot_attributes()
        plt.figure(figsize=(12, 8))
        for shape in node_attrs['shape'].unique():
            nodes = node_attrs[node_attrs['shape'] == shape].index
            nx.draw_networkx_nodes(
                G, pos,
                nodelist=nodes,
                node_color=node_attrs.loc[nodes, 'color'],
                node_shape=shape,
                node_size=2000,
                alpha = 0.3
        )       
        nx.draw_networkx_edges(G, 
            pos, 
            edge_color='gray', 
            alpha=0.5, 
            arrows=True,
            connectionstyle='arc3,rad=0.2'
        )
        nx.draw_networkx_labels(G, pos)
        plt.title("structured intelligence governance minimal presentation")
        plt.show()    

    def _node_plot_attributes(self):
        
        # set palette
        color_palette = {
            'reporting': '#268bd2',   # blue
            'humans':    '#b58900',   # yellow
            'data':      '#2aa198',   # cyan
            'tools':     '#839496',   # base1 (light gray)
            'field':     '#859900',   # green
            'projects':  '#d33682',   # magenta
        }        
        
        return self.nodes.assign(
            shape=lambda df: np.where(df['role_context'] == 'humans', 'o', 's'),
            color=lambda df: df['role_context'].map(color_palette)
        ).set_index('node')