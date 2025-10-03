# 🌐 SIG Consulting - Structured Intelligence Governance

> A comprehensive Quarto-based platform for network analysis and visualization of intelligence governance structures.

[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-blue?logo=github)](https://softloud.github.io/sig-consulting)
[![Python](https://img.shields.io/badge/Python-3.11+-green?logo=python)](https://python.org)
[![Quarto](https://img.shields.io/badge/Quarto-Documentation-orange?logo=quarto)](https://quarto.org)

## 🚀 Quick Start

### 🌐 **View Live Site**
Visit the deployed site: **[softloud.github.io/sig-consulting](https://softloud.github.io/sig-consulting)**

### 💻 **Local Development**
```bash
# Clone and setup
git clone [your-repo-url]
cd sig-consulting

# Install dependencies (requires UV)
uv sync

# Start development server
./dev-server.sh
```

Visit: http://localhost:4200

## 📋 What This Platform Does

### 🎯 **Core Capabilities**
- **Network Analysis**: Visualize complex organizational relationships
- **Role Mapping**: Different node shapes for different role types
- **Google Sheets Integration**: Pull data directly from spreadsheets
- **Interactive Dashboards**: Quarto-powered analysis documents
- **Automated Deployment**: GitHub Pages with CI/CD

### 📊 **Analysis Features**
- **Centrality Metrics**: Identify key players and connection hubs
- **Community Detection**: Find clusters and organizational groups
- **Role Classification**: Categorize nodes by connection patterns
- **Network Statistics**: Comprehensive graph metrics and insights

## 🏗️ **Project Architecture**

```
sig-consulting/
├── 📄 sig.qmd                    # Main analysis dashboard
├── 📄 index.qmd                  # Landing page
├── ⚙️ _quarto.yml                # Site configuration
├── 🐍 scripts/classes/
│   ├── sig_graph.py              # Data & analysis logic
│   └── sig_vis.py                # Visualization layer
├── 📊 local-data/                # Sample data for testing
├── 🔐 client_credentials/        # Google API credentials
├── 🚀 .github/workflows/         # GitHub Actions deployment
├── 📝 templates/                 # Configuration templates
└── 📖 docs/                      # Built site (GitHub Pages)
```

## 🛠️ **Technology Stack**

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Quarto + HTML/CSS | Interactive documentation |
| **Backend** | Python 3.11+ | Data analysis and visualization |
| **Graphs** | NetworkX + Matplotlib | Network analysis and plotting |
| **Data** | Google Sheets API | Dynamic data integration |
| **Deployment** | GitHub Pages | Automated web hosting |
| **Package Management** | UV | Fast Python dependency management |

## 📚 **Documentation Structure**

Visit the deployed site for comprehensive guides:

- 🏠 **[Home](https://softloud.github.io/sig-consulting)** - Project overview and navigation
- 📊 **[SIG Analysis](https://softloud.github.io/sig-consulting/sig.html)** - Main dashboard with interactive analysis
- 🎨 **[Visualization Guide](https://softloud.github.io/sig-consulting/SIGVIS_GUIDE.html)** - How to use the visualization tools
- 🏗️ **[Architecture Guide](https://softloud.github.io/sig-consulting/SIG_ARCHITECTURE.html)** - Technical implementation details
- 🔍 **[Role Shapes Guide](https://softloud.github.io/sig-consulting/ROLE_SHAPES_GUIDE.html)** - Understanding role-based visualizations

## ⚡ **Getting Started**

### 🔧 **Prerequisites**
- **Python 3.11+** - For analysis and visualization
- **UV Package Manager** - Fast dependency management
- **Quarto CLI** - Documentation framework
- **Google Sheets Access** - Optional for real data

### 📦 **Installation**

1. **Install UV** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and setup**:
   ```bash
   git clone [your-repo-url]
   cd sig-consulting
   uv sync
   ```

3. **Configure environment** (optional):
   ```bash
   cp templates/.env-template client_credentials/.env
   # Edit client_credentials/.env with your Google Sheets config
   ```

### 🚀 **Development Workflow**

#### **Local Development**
```bash
# Start dev server with hot reload
./dev-server.sh

# Or manually:
quarto preview --port 4200
```

#### **Test GitHub Pages Build**
```bash
# Test production build locally
./build-pages.sh

# Serve built site
cd docs && python -m http.server 8000
```

#### **Deploy to GitHub Pages**
```bash
# Automatic deployment (push to main)
git add .
git commit -m "Update site"
git push origin main

# Manual deployment
./build-pages.sh
git add docs/
git commit -m "Build site"
git push origin main
```

## 🔒 **Security & Data**

### ✅ **Safe for Public Deployment**
- **No credentials exposed**: All sensitive data excluded from builds
- **Sample data included**: Public demos use anonymized sample data
- **Environment isolation**: Development vs production data sources
- **Secure GitHub Actions**: Proper secrets and environment handling

### 🔧 **Data Sources**
- **Development**: Uses your real Google Sheets data
- **Production**: Uses sample data for public deployment
- **Flexible**: Easy to switch between data sources

## 📖 **Usage Examples**

### **Basic Network Analysis**
```python
from scripts.classes.sig_graph import SigGraph

# Load and analyze network
graph = SigGraph()
stats = graph.get_network_stats()
print(f"Network has {stats['nodes']} nodes and {stats['edges']} edges")
```

### **Role-Based Visualization**
```python
from scripts.classes.sig_vis import SigVis

# Create visualization with role shapes
vis = SigVis()
vis.plot_with_role_shapes(title="Network with Role Indicators")
```

### **Custom Analysis**
```python
# Get role indicators
roles = graph.get_role_indicators()
high_centrality = [node for node, score in roles['centrality'].items() if score > 0.1]
```

## 🤝 **Contributing**

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test locally
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 **Support**

- 📖 **Documentation**: [softloud.github.io/sig-consulting](https://softloud.github.io/sig-consulting)
- 🐛 **Issues**: [GitHub Issues](../../issues)
- 💬 **Discussions**: [GitHub Discussions](../../discussions)

---

**🎉 Ready to explore intelligence governance networks?** [Visit the live site →](https://softloud.github.io/sig-consulting)

### Workspace Settings:
The project includes workspace-specific settings for:
- Python path configuration
- Quarto integration
- Code formatting preferences

If you encounter Python import issues, ensure VS Code is using the correct Python interpreter from your UV virtual environment.
