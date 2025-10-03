# SigVis Quick Reference - Google Template

## Your Google Template Structure
Your data should have these columns:
- `from` - source node 
- `to` - target node
- `from_parent` - cluster/parent of source node
- `to_parent` - cluster/parent of target node  
- `to_minimum_requirements` - requirements description
- `arrowkeeper` - oversight/responsibility assignment

## Basic Usage

```python
from scripts.classes.sig_vis import SigVis

# Load data (automatically uses DATA_ENTRY from .env)
sig_vis = SigVis()

# Basic network plot
sig_vis.plot()

# Clustered visualizations
sig_vis.plot_clustered(cluster_by='to_parent')      # Default clustering
sig_vis.plot_clustered(cluster_by='from_parent')    # Alternative clustering  
sig_vis.plot_clustered(cluster_by='arrowkeeper')    # By oversight
# or use shorthand:
sig_vis.plot_by_arrowkeeper()

# Get statistics
stats = sig_vis.get_network_stats()
clusters = sig_vis.get_cluster_summary()
roles = sig_vis.get_role_connections()

# Display data table
sig_vis.table()
```

## Key Simplifications Made

1. **Hardcoded column names** - No more auto-detection, uses your specific template
2. **Template-specific methods** - Added `get_cluster_summary()`, `get_role_connections()`, `plot_by_arrowkeeper()`
3. **Improved clustering logic** - Better handling of your parent/arrowkeeper relationships
4. **Cleaner error handling** - More specific error messages for your template

## Data Source Options

1. **Google Sheets (recommended)**: Set DATA_ENTRY to your sheet URL
2. **Local CSV**: Use `local-data/sample-google-template.csv` for testing
3. **Direct initialization**: `SigVis(data_path='your-file.csv')`

## Layout Options for Plots

- `layout='spring'` - Force-directed (default)
- `layout='circular'` - Nodes in a circle
- `layout='random'` - Random positioning
- `layout='shell'` - Concentric shells