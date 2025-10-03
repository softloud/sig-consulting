#!/usr/bin/env python3
"""
Test script for the modularized SigDat data scraper
"""

from scripts.classes.sig_dat import SigDat

def test_sig_dat():
    """Test the SigDat data scraper"""
    print("🧪 Testing SigDat Data Scraper")
    print("=" * 40)
    
    # Test 1: Basic initialization
    print("\n1️⃣ Testing basic initialization...")
    try:
        sig_dat = SigDat()
        print("✅ SigDat initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing SigDat: {e}")
        return
    
    # Test 2: Data source info
    print("\n2️⃣ Testing data source info...")
    try:
        info = sig_dat.get_data_source_info()
        print(f"📊 Data source type: {info['type']}")
        print(f"🔗 Accessible: {info['accessible']}")
        print(f"💡 Instructions: {info['instructions']}")
    except Exception as e:
        print(f"❌ Error getting data source info: {e}")
    
    # Test 3: Data validation
    print("\n3️⃣ Testing data validation...")
    try:
        validation = sig_dat.validate_data()
        print(f"✅ Validation result: {validation['valid']}")
        print(f"📝 Message: {validation['message']}")
        if 'rows' in validation:
            print(f"📊 Rows: {validation['rows']}")
            print(f"📋 Columns: {validation['columns']}")
    except Exception as e:
        print(f"❌ Error validating data: {e}")
    
    # Test 4: Data summary
    print("\n4️⃣ Testing data summary...")
    try:
        summary = sig_dat.get_data_summary()
        if 'error' in summary:
            print(f"❌ {summary['error']}")
        else:
            print(f"📊 Total edges: {summary['total_edges']}")
            print(f"🔗 Unique from nodes: {summary['unique_from_nodes']}")
            print(f"🎯 Unique to nodes: {summary['unique_to_nodes']}")
            print(f"📋 Columns: {summary['columns']}")
    except Exception as e:
        print(f"❌ Error getting data summary: {e}")
    
    # Test 5: Get nodes and edges
    print("\n5️⃣ Testing node and edge extraction...")
    try:
        edges = sig_dat.get_edges()
        nodes = sig_dat.get_nodes()
        print(f"📊 Edges dataframe shape: {edges.shape if edges is not None else 'None'}")
        print(f"🎯 Number of nodes: {len(nodes)}")
        print(f"🔗 Sample nodes: {nodes[:3] if len(nodes) > 0 else 'None'}")
    except Exception as e:
        print(f"❌ Error getting nodes and edges: {e}")
    
    print("\n✅ SigDat testing completed!")
    return sig_dat

if __name__ == "__main__":
    test_sig_dat()