#!/usr/bin/env python3
"""
FOCUSED BACKEND REALITY CHECK
Tests specific areas mentioned in the review request
"""

import requests
import json
import hashlib

def test_literature_reality():
    """Test if literature integration returns real papers or sample data"""
    api_url = "https://7270ea2f-1d23-46a0-9a6e-bef595343dd6.preview.emergentagent.com/api"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer demo-token'}
    
    print("🔍 LITERATURE INTEGRATION REALITY CHECK")
    
    try:
        # Test PubMed search
        response = requests.get(f"{api_url}/literature/search?query=osteoarthritis%20PRP&limit=5", 
                              headers=headers, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            papers = data.get('papers', [])
            
            if papers:
                print(f"✅ Found {len(papers)} papers")
                
                # Check for real PMIDs
                pmids = [p.get('pmid') for p in papers if p.get('pmid')]
                valid_pmids = [pmid for pmid in pmids if pmid.isdigit() and len(pmid) >= 7]
                print(f"   Real PMIDs: {len(valid_pmids)}/{len(pmids)}")
                
                # Check abstract quality
                abstracts = [p.get('abstract', '') for p in papers]
                substantial_abstracts = [abs for abs in abstracts if len(abs) > 200]
                print(f"   Substantial abstracts: {len(substantial_abstracts)}/{len(abstracts)}")
                
                # Show sample paper
                if papers:
                    sample = papers[0]
                    print(f"   Sample: {sample.get('title', 'No title')[:60]}...")
                    print(f"   PMID: {sample.get('pmid', 'No PMID')}")
                    print(f"   Journal: {sample.get('journal', 'No journal')}")
                    
                return len(valid_pmids) >= 1 and len(substantial_abstracts) >= 1
            else:
                print("❌ No papers found")
                return False
        else:
            print(f"❌ Literature search failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Literature test error: {str(e)}")
        return False

def test_database_reality():
    """Test if database contains real data or mock entries"""
    api_url = "https://7270ea2f-1d23-46a0-9a6e-bef595343dd6.preview.emergentagent.com/api"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer demo-token'}
    
    print("\n🔍 DATABASE REALITY CHECK")
    
    try:
        # Check dashboard analytics
        response = requests.get(f"{api_url}/analytics/dashboard", headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            stats = data.get('summary_stats', {})
            
            total_patients = stats.get('total_patients', 0)
            protocols_approved = stats.get('protocols_approved', 0)
            outcomes_tracked = stats.get('outcomes_tracked', 0)
            
            print(f"   Total Patients: {total_patients}")
            print(f"   Protocols Approved: {protocols_approved}")
            print(f"   Outcomes Tracked: {outcomes_tracked}")
            
            # Check for realistic data
            if total_patients > 10:
                print("✅ GENUINE: Substantial patient database")
                return True
            else:
                print("❌ LIMITED: Minimal patient data")
                return False
        else:
            print(f"❌ Dashboard access failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Database test error: {str(e)}")
        return False

def main():
    print("🎯 FOCUSED BACKEND REALITY CHECK")
    print("Testing actual functionality vs claimed features")
    print("=" * 60)
    
    reality_checks = [
        ("Literature Integration", test_literature_reality),
        ("Database Persistence", test_database_reality)
    ]
    
    results = []
    for check_name, check_function in reality_checks:
        try:
            result = check_function()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} test failed: {str(e)}")
            results.append((check_name, False))
    
    # Final assessment
    genuine_count = sum(1 for _, result in results if result)
    total_count = len(results)
    reality_percentage = (genuine_count / total_count * 100) if total_count > 0 else 0
    
    print(f"\n🎯 FINAL REALITY ASSESSMENT")
    print("=" * 60)
    print(f"REALITY SCORE: {genuine_count}/{total_count} ({reality_percentage:.1f}%)")
    
    for check_name, result in results:
        status = "✅ GENUINE" if result else "❌ MOCK/LIMITED"
        print(f"   {status}: {check_name}")

if __name__ == "__main__":
    main()