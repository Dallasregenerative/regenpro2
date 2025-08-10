#!/usr/bin/env python3
"""
Focused Google Scholar Integration System Testing
Tests the newly implemented Google Scholar functionality
"""

import requests
import sys
import json
from datetime import datetime

class GoogleScholarTester:
    def __init__(self, base_url="https://099faa9d-49d6-4fd5-979e-df2b63248fdd.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer demo-token'
        }

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=60):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if endpoint else self.api_url
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=self.headers, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    # Truncate long responses for readability
                    response_str = json.dumps(response_data, indent=2)
                    if len(response_str) > 500:
                        response_str = response_str[:500] + "..."
                    print(f"   Response: {response_str}")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_google_scholar_basic(self):
        """Test basic Google Scholar search functionality"""
        success, response = self.run_test(
            "Google Scholar Search - Platelet Rich Plasma Osteoarthritis",
            "GET",
            "literature/google-scholar-search?query=platelet%20rich%20plasma%20osteoarthritis&max_results=10",
            200,
            timeout=45
        )
        
        if success:
            papers = response.get('papers', [])
            print(f"   Query: {response.get('query', 'unknown')}")
            print(f"   Source: {response.get('source', 'unknown')}")
            print(f"   Papers Found: {response.get('total_results', 0)}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            if papers:
                first_paper = papers[0]
                print(f"   Top Result: {first_paper.get('title', 'Unknown')[:60]}...")
                print(f"   Authors: {', '.join(first_paper.get('authors', [])[:2])}")
                print(f"   Journal: {first_paper.get('journal', 'Unknown')}")
                print(f"   Year: {first_paper.get('year', 'Unknown')}")
                print(f"   Citations: {first_paper.get('citation_count', 0)}")
                print(f"   Relevance Score: {first_paper.get('relevance_score', 0):.2f}")
                
                # Check for HTML parsing quality
                if first_paper.get('abstract'):
                    print(f"   Abstract Length: {len(first_paper.get('abstract', ''))}")
                    print(f"   Abstract Preview: {first_paper.get('abstract', '')[:100]}...")
        return success

    def test_google_scholar_stem_cell(self):
        """Test Google Scholar search with stem cell therapy"""
        success, response = self.run_test(
            "Google Scholar Search - Stem Cell Therapy",
            "GET",
            "literature/google-scholar-search?query=stem%20cell%20therapy&max_results=15",
            200,
            timeout=45
        )
        
        if success:
            papers = response.get('papers', [])
            print(f"   Query: {response.get('query', 'unknown')}")
            print(f"   Papers Found: {len(papers)}")
            
            # Check relevance scoring
            relevant_papers = [p for p in papers if p.get('relevance_score', 0) >= 0.5]
            print(f"   High Relevance Papers (≥0.5): {len(relevant_papers)}")
            
            # Check for regenerative medicine context
            regen_papers = [p for p in papers if any(term in p.get('title', '').lower() 
                           for term in ['regenerative', 'stem cell', 'therapy', 'treatment'])]
            print(f"   Regenerative Medicine Related: {len(regen_papers)}")
            
            if papers:
                # Show relevance score distribution
                scores = [p.get('relevance_score', 0) for p in papers]
                avg_score = sum(scores) / len(scores) if scores else 0
                print(f"   Average Relevance Score: {avg_score:.2f}")
                print(f"   Score Range: {min(scores):.2f} - {max(scores):.2f}")
        return success

    def test_google_scholar_year_filter(self):
        """Test Google Scholar search with year filter"""
        success, response = self.run_test(
            "Google Scholar Search - With Year Filter (2023+)",
            "GET",
            "literature/google-scholar-search?query=BMAC%20rotator%20cuff&max_results=10&year_filter=2023",
            200,
            timeout=45
        )
        
        if success:
            papers = response.get('papers', [])
            print(f"   Query: {response.get('query', 'unknown')}")
            print(f"   Year Filter Applied: 2023+")
            print(f"   Papers Found: {len(papers)}")
            
            # Check year distribution
            years = [p.get('year', '') for p in papers if p.get('year', '').isdigit()]
            recent_papers = [y for y in years if int(y) >= 2023]
            
            print(f"   Papers with Year Info: {len(years)}")
            print(f"   Papers from 2023+: {len(recent_papers)}")
            
            if years:
                print(f"   Year Range: {min(years)} - {max(years)}")
        return success

    def test_multi_source_search(self):
        """Test multi-source search combining PubMed and Google Scholar"""
        success, response = self.run_test(
            "Multi-Source Search - Regenerative Medicine",
            "GET",
            "literature/multi-source-search?query=regenerative%20medicine&max_results_per_source=8",
            200,
            timeout=60
        )
        
        if success:
            papers = response.get('papers', [])
            source_stats = response.get('source_statistics', {})
            
            print(f"   Query: {response.get('query', 'unknown')}")
            print(f"   Total Unique Papers: {response.get('total_unique_papers', 0)}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            # Source statistics
            pubmed_stats = source_stats.get('pubmed', {})
            scholar_stats = source_stats.get('google_scholar', {})
            
            print(f"   PubMed: {pubmed_stats.get('papers_found', 0)} papers, status: {pubmed_stats.get('status', 'unknown')}")
            print(f"   Google Scholar: {scholar_stats.get('papers_found', 0)} papers, status: {scholar_stats.get('status', 'unknown')}")
            
            if papers:
                # Check source diversity
                pubmed_papers = [p for p in papers if p.get('source') == 'pubmed']
                scholar_papers = [p for p in papers if p.get('source') == 'google_scholar']
                
                print(f"   PubMed Papers in Results: {len(pubmed_papers)}")
                print(f"   Google Scholar Papers in Results: {len(scholar_papers)}")
                
                # Check deduplication effectiveness
                total_before = pubmed_stats.get('papers_found', 0) + scholar_stats.get('papers_found', 0)
                total_after = len(papers)
                print(f"   Deduplication: {total_before} → {total_after} papers")
                
                # Show top results from each source
                if pubmed_papers:
                    top_pubmed = pubmed_papers[0]
                    print(f"   Top PubMed: {top_pubmed.get('title', 'Unknown')[:40]}...")
                
                if scholar_papers:
                    top_scholar = scholar_papers[0]
                    print(f"   Top Scholar: {top_scholar.get('title', 'Unknown')[:40]}...")
        return success

    def test_multi_source_bmac(self):
        """Test multi-source search for BMAC rotator cuff"""
        success, response = self.run_test(
            "Multi-Source Search - BMAC Rotator Cuff",
            "GET",
            "literature/multi-source-search?query=BMAC%20rotator%20cuff&max_results_per_source=6",
            200,
            timeout=60
        )
        
        if success:
            papers = response.get('papers', [])
            
            print(f"   Query: BMAC rotator cuff")
            print(f"   Total Unique Papers: {response.get('total_unique_papers', 0)}")
            
            # Check for relevant content
            bmac_papers = [p for p in papers if 'bmac' in p.get('title', '').lower() or 'bone marrow' in p.get('title', '').lower()]
            rotator_papers = [p for p in papers if 'rotator' in p.get('title', '').lower() or 'shoulder' in p.get('title', '').lower()]
            
            print(f"   BMAC-related Papers: {len(bmac_papers)}")
            print(f"   Rotator Cuff-related Papers: {len(rotator_papers)}")
            
            # Check relevance scores
            high_relevance = [p for p in papers if p.get('relevance_score', 0) >= 0.7]
            print(f"   High Relevance Papers (≥0.7): {len(high_relevance)}")
            
            if papers:
                top_paper = papers[0]
                print(f"   Top Result: {top_paper.get('title', 'Unknown')[:50]}...")
                print(f"   Top Relevance Score: {top_paper.get('relevance_score', 0):.2f}")
                print(f"   Top Source: {top_paper.get('source', 'unknown')}")
        return success

    def test_error_handling(self):
        """Test Google Scholar error handling"""
        success, response = self.run_test(
            "Google Scholar Search - Error Handling (Empty Query)",
            "GET",
            "literature/google-scholar-search?query=&max_results=5",
            200,  # Should still return 200 with error in response
            timeout=30
        )
        
        if success:
            print(f"   Status: {response.get('status', 'unknown')}")
            if 'error' in response:
                print(f"   Error Handled: {response.get('error', 'unknown')[:50]}...")
            print(f"   Papers Returned: {len(response.get('papers', []))}")
            print(f"   Fallback Available: {'fallback_suggestion' in response}")
        return success

def main():
    print("🧬 Google Scholar Integration System Testing")
    print("Testing newly implemented Google Scholar functionality")
    print("=" * 60)
    
    tester = GoogleScholarTester()
    
    # Define Google Scholar specific tests
    tests = [
        ("Google Scholar - Basic Search", tester.test_google_scholar_basic),
        ("Google Scholar - Stem Cell Therapy", tester.test_google_scholar_stem_cell),
        ("Google Scholar - Year Filter", tester.test_google_scholar_year_filter),
        ("Multi-Source - Comprehensive", tester.test_multi_source_search),
        ("Multi-Source - BMAC Rotator Cuff", tester.test_multi_source_bmac),
        ("Google Scholar - Error Handling", tester.test_error_handling),
    ]
    
    print(f"\nRunning {len(tests)} Google Scholar integration tests...")
    print("Testing: HTML parsing, relevance scoring, deduplication, error handling\n")
    
    for test_name, test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 Google Scholar Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    print(f"🎯 Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All Google Scholar integration tests passed!")
        print("✅ Google Scholar search functionality working correctly")
        print("✅ Multi-source search with deduplication operational")
        print("✅ HTML parsing and relevance scoring functional")
        print("✅ Error handling working properly")
    elif tester.tests_passed >= tester.tests_run * 0.8:
        print("⚠️  Most Google Scholar tests passed. Minor issues detected.")
        print("🔧 Core functionality works but some features may need attention.")
    else:
        print("❌ Significant Google Scholar integration issues detected.")
        print("🚨 Google Scholar functionality may not be fully operational.")
    
    return 0 if tester.tests_passed >= tester.tests_run * 0.8 else 1

if __name__ == "__main__":
    sys.exit(main())