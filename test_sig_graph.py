#!/usr/bin/env python3
"""
Test script for the modularized SigGraph with SigDat integration
"""

from scripts.classes.sig_graph import SigGraph

def test_sig_graph():
    """Test the SigGraph with SigDat integration"""
    print("🧪 Testing SigGraph with SigDat Integration")
    print("=" * 45)
    
    # Test 1: Basic initialization
    print("\n1️⃣ Testing SigGraph initialization...")
    try:
        sig_graph = SigGraph()
        print("✅ SigGraph initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing SigGraph: {e}")
        return
    
    # Test 2: Data source info (delegated to SigDat)
    print("\n2️⃣ Testing data source info (delegated to SigDat)...")
    try:
        info = sig_graph.get_data_source_info()
        print(f"📊 Data source type: {info['type']}")
        print(f"🔗 Accessible: {info['accessible']}")
        print(f"💡 Instructions: {info['instructions']}")
    except Exception as e:
        print(f"❌ Error getting data source info: {e}")
    
    # Test 3: Network stats
    print("\n3️⃣ Testing network statistics...")
    try:
        stats = sig_graph.get_network_stats()
        print(f"🎯 Nodes: {stats['nodes']}")
        print(f"🔗 Edges: {stats['edges']}")
        print(f"📊 Density: {stats['density']:.3f}")
        print(f"🌐 Connected: {stats['is_connected']}")
        print(f"📋 Unique arrowkeepers: {stats['unique_arrowkeepers']}")
    except Exception as e:
        print(f"❌ Error getting network stats: {e}")
    
    # Test 4: Role indicators
    print("\n4️⃣ Testing role indicators...")
    try:
        role_indicators = sig_graph.get_role_indicators()
        print(f"🎯 Role indicators found: {len(role_indicators)}")
        for node, role in list(role_indicators.items())[:3]:
            print(f"  {node}: {role}")
        print("  ...")
    except Exception as e:
        print(f"❌ Error getting role indicators: {e}")
    
    # Test 5: Edge arrowkeepers
    print("\n5️⃣ Testing edge arrowkeepers...")
    try:
        edge_arrowkeepers = sig_graph.get_edge_arrowkeepers()
        print(f"🏹 Edge arrowkeepers found: {len(edge_arrowkeepers)}")
        for edge, arrowkeeper in list(edge_arrowkeepers.items())[:3]:
            print(f"  {edge[0]} → {edge[1]}: {arrowkeeper}")
        print("  ...")
    except Exception as e:
        print(f"❌ Error getting edge arrowkeepers: {e}")
    
    print("\n✅ SigGraph integration testing completed!")
    return sig_graph

if __name__ == "__main__":
    test_sig_graph()