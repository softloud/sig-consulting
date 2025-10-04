import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from client_credentials/.env
load_dotenv('client_credentials/.env')

class SigDat:
    """
    Data preparation layer for SIG (Structured Intelligence Governance).
    Focuses on loading raw data and preparing clean node and edge dataframes.
    """
    
    def __init__(self, data_path=None, sheet_id=None):
        """
        Initialize SigDat with data loading and preparation
        
        Parameters:
        - data_path: Path to data file or URL
        - sheet_id: Google Sheets ID for direct access
        """
        self.data_path = data_path
        self.sheet_id = sheet_id
        self.raw_data = None
        self.edges_df = None
        self.nodes_df = None
        self.load_and_prepare_data()

    def load_and_prepare_data(self):
        """Load raw data and prepare edge and node dataframes"""
        self.raw_data = self._load_data(self.data_path, self.sheet_id)
        if self.raw_data is not None:
            self.edges_df = self._prepare_edges_dataframe()
            self.nodes_df = self._prepare_nodes_dataframe()
            print(f"✅ Data prepared: {len(self.edges_df)} edges, {len(self.nodes_df)} nodes")
        else:
            print("❌ Failed to load and prepare data")

    def get_edges_dataframe(self):
        """Return the prepared edges dataframe"""
        return self.edges_df

    def get_nodes_dataframe(self):
        """Return the prepared nodes dataframe"""
        return self.nodes_df

    def get_edges(self):
        """Return the edges dataframe (legacy compatibility)"""
        return self.edges_df

    def get_nodes(self):
        """Extract unique nodes as list (legacy compatibility)"""
        if self.nodes_df is not None:
            return self.nodes_df['node'].tolist()
        return []

    def _prepare_edges_dataframe(self):
        """Prepare clean edges dataframe from raw data"""
        if self.raw_data is None:
            return pd.DataFrame()
        
        # Ensure required columns exist
        edges_df = self.raw_data.copy()
        
        # Standardize column names and clean data
        if 'from' in edges_df.columns and 'to' in edges_df.columns:
            # Remove any rows with missing source or target
            edges_df = edges_df.dropna(subset=['from', 'to'])
            
            # Clean whitespace
            edges_df['from'] = edges_df['from'].astype(str).str.strip()
            edges_df['to'] = edges_df['to'].astype(str).str.strip()
            
            # Add edge IDs if not present
            if 'edge_id' not in edges_df.columns:
                edges_df['edge_id'] = range(len(edges_df))
                
            return edges_df
        else:
            print(f"❌ Required 'from' and 'to' columns not found. Available: {list(edges_df.columns)}")
            return pd.DataFrame()

    def _prepare_nodes_dataframe(self):
        """Prepare clean nodes dataframe from edge data"""
        if self.edges_df is None or self.edges_df.empty:
            return pd.DataFrame()
            
        # Extract unique nodes from edges
        from_nodes = set(self.edges_df['from'].unique())
        to_nodes = set(self.edges_df['to'].unique())
        all_nodes = from_nodes.union(to_nodes)
        
        # Create nodes dataframe
        nodes_df = pd.DataFrame({'node': list(all_nodes)})
        
        # Add node attributes by aggregating from edges
        node_attributes = {}
        
        for node in all_nodes:
            # Get attributes from edges where this node appears
            from_edges = self.edges_df[self.edges_df['from'] == node]
            to_edges = self.edges_df[self.edges_df['to'] == node]
            
            # Aggregate attributes (take first non-null value)
            attrs = {}
            
            # From 'from_parent' when node is source
            if 'from_parent' in self.edges_df.columns and not from_edges.empty:
                parent_vals = from_edges['from_parent'].dropna()
                if not parent_vals.empty:
                    attrs['parent'] = parent_vals.iloc[0]
                    
            # From 'to_parent' when node is target (if no parent found yet)
            if 'parent' not in attrs and 'to_parent' in self.edges_df.columns and not to_edges.empty:
                parent_vals = to_edges['to_parent'].dropna()
                if not parent_vals.empty:
                    attrs['parent'] = parent_vals.iloc[0]
            
            # Count connections
            attrs['in_degree'] = len(to_edges)
            attrs['out_degree'] = len(from_edges)
            attrs['total_degree'] = attrs['in_degree'] + attrs['out_degree']
            
            node_attributes[node] = attrs
        
        # Add attributes to nodes dataframe
        for attr in ['parent', 'in_degree', 'out_degree', 'total_degree']:
            nodes_df[attr] = nodes_df['node'].map(lambda x: node_attributes[x].get(attr, None))
            
        return nodes_df

    def _load_data(self, data_path=None, sheet_id=None):
        """Load edge data from various sources"""
        if sheet_id:
            # Read from Google Sheet using CSV export
            return self._read_public_google_sheet(sheet_id)
        elif data_path:
            # Read from file path
            if data_path.startswith('http') and 'docs.google.com' in data_path:
                # Extract sheet ID from Google Sheets URL and read as CSV
                sheet_id = self._extract_sheet_id(data_path)
                return self._read_public_google_sheet(sheet_id)
            elif data_path.startswith('http'):
                # Direct CSV URL
                return pd.read_csv(data_path)
            else:
                # Local file
                return pd.read_csv(data_path)
        else:
            # Check environment variable
            data_entry_url = os.getenv('DATA_ENTRY')
            if data_entry_url:
                if 'docs.google.com' in data_entry_url:
                    sheet_id = self._extract_sheet_id(data_entry_url)
                    return self._read_public_google_sheet(sheet_id)
                elif data_entry_url.startswith('http'):
                    return pd.read_csv(data_entry_url)
                else:
                    return pd.read_csv(data_entry_url)
            else:
                # Create sample data if no path provided
                print("Using sample data - configure your data source or pass data_path/sheet_id")
                return pd.DataFrame({
                    'from': ['A', 'B', 'C'],
                    'to': ['B', 'C', 'A'],
                    'from_parent': ['group1', 'group2', 'group1'],
                    'to_parent': ['group2', 'group1', 'group1'],
                    'arrowkeeper': ['keeper1', 'keeper2', 'keeper1']
                })
    
    def _extract_sheet_id(self, url):
        """Extract Google Sheet ID from URL"""
        if '/d/' in url:
            return url.split('/d/')[1].split('/')[0]
        else:
            raise ValueError("Invalid Google Sheets URL")
    
    def _read_public_google_sheet(self, sheet_id, gid=0):
        """Read data from a public Google Sheet using CSV export URL"""
        try:
            # Construct the CSV export URL
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
            # Note: Reading from Google Sheets CSV export
            
            # Read directly with pandas
            return pd.read_csv(csv_url)
            
        except Exception as e:
            print(f"Error reading Google Sheet data")
            print("Make sure the sheet is publicly viewable (shared with 'Anyone with the link')")
            print("Falling back to sample data")
            return pd.DataFrame({
                'from': ['A', 'B', 'C'],
                'to': ['B', 'C', 'A'],
                'from_parent': ['group1', 'group2', 'group1'],
                'to_parent': ['group2', 'group1', 'group1'],
                'arrowkeeper': ['keeper1', 'keeper2', 'keeper1']
            })
    
    def get_data_source_info(self):
        """Get information about the current data source"""
        info = {
            'type': 'unknown',
            'accessible': False,
            'instructions': 'No data source configured'
        }
        
        if self.sheet_id:
            info['type'] = 'google_sheet'
            info['sheet_id'] = self.sheet_id
            info['accessible'] = self.edges is not None and len(self.edges) > 0
            info['instructions'] = 'Using direct Google Sheets ID'
        elif self.data_path:
            if self.data_path.startswith('http') and 'docs.google.com' in self.data_path:
                info['type'] = 'google_sheet_url'
                info['accessible'] = self.edges is not None and len(self.edges) > 0
                info['instructions'] = 'Using Google Sheets URL'
            elif self.data_path.startswith('http'):
                info['type'] = 'web_csv'
                info['accessible'] = self.edges is not None and len(self.edges) > 0
                info['instructions'] = 'Using web CSV URL'
            else:
                info['type'] = 'local_file'
                info['accessible'] = os.path.exists(self.data_path) if self.data_path else False
                info['instructions'] = f"Local file: {self.data_path}"
        else:
            # Check environment variable
            data_entry_url = os.getenv('DATA_ENTRY')
            if data_entry_url:
                if 'docs.google.com' in data_entry_url:
                    info['type'] = 'google_sheet_env'
                    info['accessible'] = self.edges is not None and len(self.edges) > 0
                    info['instructions'] = 'Using DATA_ENTRY environment variable (Google Sheets)'
                elif data_entry_url.startswith('http'):
                    info['type'] = 'web_csv_env'
                    info['accessible'] = self.edges is not None and len(self.edges) > 0
                    info['instructions'] = 'Using DATA_ENTRY environment variable (Web CSV)'
                else:
                    info['type'] = 'local_file_env'
                    info['accessible'] = os.path.exists(data_entry_url)
                    info['instructions'] = f"Using DATA_ENTRY environment variable: {data_entry_url}"
            else:
                info['type'] = 'sample_data'
                info['accessible'] = True
                info['instructions'] = 'Using sample data - configure DATA_ENTRY environment variable'
            
        return info
    
    def validate_data(self):
        """Validate that the loaded data has required columns"""
        if self.edges is None:
            return {'valid': False, 'message': 'No data loaded'}
        
        required_columns = ['from', 'to']
        missing_columns = [col for col in required_columns if col not in self.edges.columns]
        
        if missing_columns:
            return {
                'valid': False, 
                'message': f'Missing required columns: {missing_columns}',
                'available_columns': list(self.edges.columns)
            }
        
        return {
            'valid': True,
            'message': 'Data validation passed',
            'rows': len(self.edges),
            'columns': list(self.edges.columns)
        }
    
    def get_data_summary(self):
        """Get summary statistics about the loaded data"""
        if self.edges is None:
            return {'error': 'No data loaded'}
        
        summary = {
            'total_edges': len(self.edges),
            'unique_from_nodes': self.edges['from'].nunique() if 'from' in self.edges.columns else 0,
            'unique_to_nodes': self.edges['to'].nunique() if 'to' in self.edges.columns else 0,
            'columns': list(self.edges.columns)
        }
        
        # Add column-specific summaries
        for col in ['from_parent', 'to_parent', 'arrowkeeper']:
            if col in self.edges.columns:
                summary[f'unique_{col}'] = self.edges[col].nunique()
                summary[f'{col}_values'] = list(self.edges[col].unique())
        
        return summary
    
    def refresh_data(self):
        """Reload data from source"""
        print("🔄 Refreshing data...")
        self.load_data()
        
    def export_data(self, output_path):
        """Export the loaded data to a CSV file"""
        if self.edges is not None:
            self.edges.to_csv(output_path, index=False)
            print(f"📁 Data exported to: {output_path}")
        else:
            print("❌ No data to export")
