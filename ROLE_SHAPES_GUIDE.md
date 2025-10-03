# Role-Based Node Shaping Guide

## 🎯 New Feature: Node Shapes by Role Connections

The SIG visualization system now supports shaping nodes based on their connection to the central "roles" node.

## 🔍 Role Connection Types

Your data is analyzed to determine how each node relates to the "roles" node:

### Node Shape Mapping:
- **Circle (○)**: Nodes that connect **TO** roles
- **Square (□)**: Nodes that connect **FROM** roles  
- **Diamond (◊)**: Nodes that connect **both ways** with roles
- **Triangle (△)**: The **'roles' node** itself
- **Pentagon (⬟)**: Nodes with **no role connections**

## 📊 Current Data Analysis

Based on your data:
- **TO roles**: `field`, `deciders`, `scientists`, `analytics`
- **Roles node**: `roles` (central hub)
- **No connections**: `tools`, `data`, `reporting`, `projects`, `priorities`

## 🎨 Usage Methods

### Basic Role Shape Plotting
```python
from scripts.classes.sig_vis import SigVis

sig_vis = SigVis()

# Plot with role-based shapes, colored by to_parent
sig_vis.plot_with_role_shapes()

# Convenience method
sig_vis.plot_role_shapes()
```

### Advanced Options
```python
# Shape by role connections, color by arrowkeeper
sig_vis.plot_with_role_shapes(cluster_by='arrowkeeper')

# Shape by role connections, color by from_parent  
sig_vis.plot_with_role_shapes(cluster_by='from_parent')

# Larger plot with custom sizing
sig_vis.plot_with_role_shapes(figsize=(16, 12), node_size=2000)
```

## 🔍 Analysis Benefits

### ✅ **Visual Role Hierarchy**
- Instantly see which nodes are central to the "roles" system
- Identify nodes that feed into vs. receive from roles
- Spot nodes operating independently of the role system

### ✅ **Dual Information Display**
- **Shape** = Role connection type
- **Color** = Cluster/group assignment
- **Position** = Network layout algorithm

### ✅ **Interactive Exploration**
- Combine with different clustering methods
- Adjust layouts for different perspectives
- Easy to identify organizational patterns

## 📋 Example Interpretations

- **Circle nodes (TO roles)**: These feed information or resources to the central role system
- **Square nodes (FROM roles)**: These receive direction or output from roles
- **Pentagon nodes (No connections)**: These operate independently or through other pathways
- **Diamond nodes (Both directions)**: These have bidirectional relationships with roles

## 🔧 Technical Details

The role indicator system:
1. Analyzes your edge data for connections to/from 'roles'
2. Categorizes each node based on connection patterns  
3. Maps categories to distinct matplotlib marker shapes
4. Preserves cluster coloring for dual information display

Perfect for understanding governance and information flow patterns in your structured intelligence system!