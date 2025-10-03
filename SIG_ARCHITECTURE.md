# SIG Architecture: Separated Graph and Visualization Logic

## Overview

The SIG (Structured Intelligence Governance) system has been refactored into two distinct classes to separate concerns:

- **`SigGraph`**: Handles data loading, graph creation, and analysis logic
- **`SigVis`**: Handles visualization and presentation logic

## Class Responsibilities

### 🔧 SigGraph (`scripts/classes/sig_graph.py`)

**Purpose**: Core graph data and analysis operations

**Responsibilities**:
- Data loading from various sources (Google Sheets, CSV, local files)
- NetworkX graph creation and management
- Network analysis and statistics
- Cluster analysis and node grouping
- Data source configuration and validation

**Key Methods**:
```python
# Data and graph access
.get_edges_dataframe()          # Raw edge data
.get_networkx_graph()           # NetworkX graph object

# Analysis methods
.get_network_stats()            # Basic network statistics
.get_cluster_summary()          # Cluster distribution analysis
.get_role_connections()         # Special analysis for 'roles' node
.get_node_clusters(cluster_by)  # Node-to-cluster mapping

# Configuration
.get_data_source_info()         # Data source type and status
```

### 🎨 SigVis (`scripts/classes/sig_vis.py`)

**Purpose**: Visualization and presentation layer

**Responsibilities**:
- matplotlib-based network plotting
- Cluster visualization with colors and legends
- Layout algorithms (spring, circular, etc.)
- Plot formatting and styling
- User interface for analysis results

**Key Methods**:
```python
# Visualization methods
.plot()                         # Basic network plot
.plot_clustered(cluster_by)     # Colored cluster visualization
.plot_by_arrowkeeper()          # Shorthand for arrowkeeper clustering

# Convenience methods (delegates to SigGraph)
.get_network_stats()           # Network statistics
.get_cluster_summary()         # Cluster analysis
.table()                       # Display edge data
```

## Architecture Benefits

### ✅ **Separation of Concerns**
- **Data logic** is isolated in SigGraph
- **Visualization logic** is isolated in SigVis
- Each class has a single, clear responsibility

### ✅ **Testability**
- Can test graph analysis independently of visualization
- Can test plotting independently of data loading
- Easier to write unit tests for each component

### ✅ **Reusability**
- SigGraph can be used in non-visual contexts (APIs, batch processing)
- SigVis can be extended with different plot types
- Other visualization libraries could use SigGraph

### ✅ **Maintainability**
- Changes to data loading don't affect visualization
- Changes to plotting don't affect analysis
- Easier to debug issues in specific areas

## Usage Patterns

### Direct SigGraph Usage
```python
from scripts.classes.sig_graph import SigGraph

# For analysis-only applications
graph = SigGraph()
stats = graph.get_network_stats()
clusters = graph.get_cluster_summary()
networkx_graph = graph.get_networkx_graph()
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

# These properties provide direct access to SigGraph data
edges_df = vis.edges      # Same as vis.sig_graph.get_edges_dataframe()
nx_graph = vis.graph      # Same as vis.sig_graph.get_networkx_graph()
```

## Migration Notes

- **Existing code**: No changes needed! SigVis maintains the same API
- **New features**: Add analysis methods to SigGraph, visualization to SigVis
- **Data access**: Use `.edges` and `.graph` properties for direct access
- **Extensibility**: Inherit from SigGraph for new analysis, SigVis for new plots

## File Structure

```
scripts/classes/
├── __init__.py
├── sig_graph.py          # 🔧 Data and analysis logic
├── sig_vis.py            # 🎨 Visualization logic  
└── sig_vis_backup.py     # Backup of original combined class
```

This separation makes the codebase more modular, testable, and maintainable while preserving the existing user interface.