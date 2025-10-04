# SIG Architecture: Three-Tier Modular Design

## Overview

The SIG (Structured Intelligence Governance) system follows a modular three-tier architecture with clear separation of concerns:

- **`SigDat`**: Pure data layer - loading, validation, and source management
- **`SigGraph`**: Analysis layer - graph creation, network analysis, and statistics
- **`SigVis`**: Presentation layer - visualization, plotting, and user interface

## Class Responsibilities

### � SigDat (`scripts/classes/sig_dat.py`)

**Purpose**: Pure data preparation layer - transforms raw data into clean node and edge dataframes

**Responsibilities**:
- Raw data loading from multiple sources (Google Sheets, CSV, URLs)
- Data validation and integrity checking
- **Edge dataframe preparation**: Clean, standardized edge data with IDs
- **Node dataframe creation**: Extract nodes with attributes and degree metrics
- Source configuration and environment management
- Fallback data source handling

**Key Methods**:
```python
# Core data access
.get_edges()                    # Returns edge dataframe
.get_nodes()                    # Extract unique nodes from edges
.load_data()                    # Reload data from source
.refresh_data()                 # Refresh from current source

# Data validation and info
.validate_data()                # Check data integrity
.get_data_summary()             # Summary statistics
.get_data_source_info()         # Source type and metadata
```

### 🔧 SigGraph (`scripts/classes/sig_graph.py`)

**Purpose**: Graph object creation and network analysis using prepared dataframes

**Responsibilities**:
- **NetworkX graph creation** from clean dataframes (with node and edge attributes)
- Network analysis and statistics computation
- Cluster analysis and node grouping algorithms
- Graph algorithms and centrality metrics
- Uses SigDat for dataframe preparation

**Key Methods**:
```python
# Graph object access
.get_networkx_graph()           # Returns NetworkX graph with attributes
.get_edges_dataframe()          # Access to edges dataframe (from SigDat)
.get_nodes_dataframe()          # Access to nodes dataframe (from SigDat)

# Network analysis
.get_network_stats()            # Network metrics (nodes, edges, density, etc.)
.get_cluster_summary()          # Cluster distribution analysis
.get_role_connections()         # Analysis for 'roles' node connections
.get_node_clusters(cluster_by)  # Node-to-cluster mapping
.get_role_indicators()          # Role-based node classification
.get_edge_arrowkeepers()        # Arrowkeeper assignments for edges

# Advanced analysis
.get_centrality_measures()      # Node centrality metrics
.get_community_detection()      # Community structure analysis
```

### 🎨 SigVis (`scripts/classes/sig_vis.py`)

**Purpose**: Visualization layer that uses NetworkX graph objects for plotting

**Responsibilities**:
- Matplotlib-based network plotting using graph objects
- Cluster visualization with colors and legends  
- Advanced multi-dimensional visual encoding (shapes, colors, line styles)
- Layout algorithms (spring, circular, etc.)
- Plot formatting and styling
- User interface for analysis results
- Uses SigGraph for graph objects and analysis

**Key Methods**:
```python
# Advanced visualization methods
.plot()                                    # Basic network plot using graph object
.plot_clustered(cluster_by)                # Colored cluster visualization  
.plot_by_arrowkeeper()                     # Arrowkeeper-based clustering
.plot_with_role_shapes()                   # Node shapes by role connections
.plot_with_role_shapes_and_arrowkeeper_lines()  # Triple visual encoding

# Data presentation
.table()                                   # Interactive edge data display
.table_min_req()                          # Minimum requirements table

# Convenience methods (delegates to SigGraph)
.get_network_stats()                      # Network statistics
.get_cluster_summary()                    # Cluster analysis
.get_role_connections()                   # Role connection analysis
.get_data_source_info()                   # Data source information
```

## Architecture Benefits

### ✅ **Clear Separation of Concerns**
- **Data layer (SigDat)**: Pure data loading and source management
- **Analysis layer (SigGraph)**: Graph algorithms and network analysis  
- **Presentation layer (SigVis)**: Visualization and user interface
- Each layer has a single, focused responsibility

### ✅ **Enhanced Testability**
- Can test data loading independently of analysis or visualization
- Can test graph algorithms independently of data sources
- Can test plotting independently of data loading and analysis
- Isolated unit testing for each component

### ✅ **Maximum Reusability**
- SigDat can be used by other analysis tools needing the same data
- SigGraph can be used in non-visual contexts (APIs, batch processing, web services)
- SigVis can be extended with different plot types and visualization libraries
- Any layer can be replaced or extended without affecting others

### ✅ **Superior Maintainability**
- Changes to data sources only affect SigDat
- Changes to analysis algorithms only affect SigGraph
- Changes to visualization only affect SigVis
- Easier debugging with clear error isolation
- Modular development allows specialized focus

### ✅ **Scalability and Performance**
- Data loading can be optimized independently
- Analysis can be cached or distributed without affecting visualization
- Visualizations can be rendered separately from data processing
- Memory management can be optimized per layer

## Usage Patterns

### Direct SigDat Usage
```python
from scripts.classes.sig_dat import SigDat

# For data-only applications
data = SigDat()
edges = data.get_edges()
nodes = data.get_nodes()
info = data.get_data_source_info()
summary = data.get_data_summary()
```

### Direct SigGraph Usage
```python
from scripts.classes.sig_graph import SigGraph

# For analysis-only applications
graph = SigGraph()
stats = graph.get_network_stats()
clusters = graph.get_cluster_summary()
networkx_graph = graph.get_networkx_graph()
role_analysis = graph.get_role_connections()
```

### SigVis Usage (Recommended)
```python
from scripts.classes.sig_vis import SigVis

# For interactive analysis and visualization
vis = SigVis()
vis.plot_clustered(cluster_by='to_parent')
stats = vis.get_network_stats()  # Delegates to SigGraph
```

### Property Access
```python
vis = SigVis()

# Direct access to underlying layers
edges_df = vis.edges          # Same as vis.sig_graph.sig_dat.get_edges()
nx_graph = vis.graph          # Same as vis.sig_graph.get_networkx_graph()

# Multi-layer delegation examples
data_info = vis.get_data_source_info()  # SigVis → SigGraph → SigDat
network_stats = vis.get_network_stats() # SigVis → SigGraph
```

## Data Flow Architecture

```
📊 Data Sources (Google Sheets, CSV, URLs)
           ↓
📋 SigDat: Raw data → Clean Node DF & Edge DF
           ↓  
🔧 SigGraph: Dataframes → NetworkX graph object + analysis
           ↓
🎨 SigVis: Graph object → Matplotlib visualizations
           ↓
📈 Output: Interactive plots, statistics, tables
```

## Layer Dependencies & Focus

- **SigDat** (Data Preparation): No dependencies → **Node DF & Edge DF**
- **SigGraph** (Graph Creation): Uses SigDat → **NetworkX graph object**  
- **SigVis** (Visualization): Uses SigGraph → **Matplotlib plots**
- Each layer can be used independently for its specific purpose

## Migration Notes

- **Existing code**: No changes needed! SigVis maintains the same public API
- **New data features**: Add methods to SigDat for new data sources
- **New analysis features**: Add methods to SigGraph for new algorithms  
- **New visualization features**: Add methods to SigVis for new plot types
- **Data access**: Use `.edges` and `.graph` properties for direct access
- **Layer access**: Access `vis.sig_graph.sig_dat` for direct data layer interaction
- **Extensibility**: Inherit from appropriate layer for new functionality

## File Structure

```
scripts/classes/
├── __init__.py
├── sig_dat.py            # � Data loading and source management
├── sig_graph.py          # 🔧 Graph analysis and network logic  
├── sig_vis.py            # 🎨 Visualization and presentation
└── __pycache__/          # Python bytecode cache
```

## Environment Configuration

The system supports multiple data source configurations:

```python
# Environment-based data loading (production)
SIG_DATA_SOURCE=google_sheet_env    # Uses Google Sheets API
SIG_DATA_SOURCE=local_csv          # Uses local CSV file
SIG_DATA_SOURCE=sample_data        # Uses built-in sample data

# Direct specification (development)  
sig_dat = SigDat(data_path="path/to/data.csv")
sig_dat = SigDat(sheet_id="1ABC...XYZ")
```

This three-tier architecture provides maximum flexibility, maintainability, and extensibility while preserving the simplicity of the original single-class interface.