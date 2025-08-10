#!/usr/bin/env python3
"""
QUICK BACKEND REALITY CHECK - Core functionality verification
"""

import requests
import json
import sys

def quick_reality_check():
    base_url = "https://099faa9d-49d6-4fd5-979e-df2b63248fdd.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer demo-token'}
    
    results = []
    
    print("🎯 QUICK BACKEND REALITY CHECK")
    print("=" * 50)
    
    # 1. Health Check
    try:
        response = requests.get(f"{api_url}/health", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results.append(f"✅ Health Check: {data.get('status', 'unknown')}")
        else:
            results.append(f"❌ Health Check: Failed ({response.status_code})")
    except Exception as e:
        results.append(f"❌ Health Check: Error - {str(e)}")
    
    # 2. Patient List
    try:
        response = requests.get(f"{api_url}/patients", headers=headers, timeout=10)
        if response.status_code == 200:
            patients = response.json()
            count = len(patients) if isinstance(patients, list) else 0
            results.append(f"✅ Patient Database: {count} patients found")
            
            # Test with existing patient if available
            if patients and count > 0:
                test_patient_id = patients[0].get('patient_id')
                
                # 3. Patient Analysis
                try:
                    response = requests.post(f"{api_url}/patients/{test_patient_id}/analyze", 
                                           json={}, headers=headers, timeout=30)
                    if response.status_code == 200:
                        analysis = response.json()
                        diagnoses = analysis.get('diagnostic_results', [])
                        results.append(f"✅ AI Analysis: {len(diagnoses)} diagnoses generated")
                    else:
                        results.append(f"❌ AI Analysis: Failed ({response.status_code})")
                except Exception as e:
                    results.append(f"❌ AI Analysis: Error - {str(e)}")
                
                # 4. Protocol Generation
                try:
                    protocol_data = {"patient_id": test_patient_id, "school_of_thought": "ai_optimized"}
                    response = requests.post(f"{api_url}/protocols/generate", 
                                           json=protocol_data, headers=headers, timeout=30)
                    if response.status_code == 200:
                        protocol = response.json()
                        steps = protocol.get('protocol_steps', [])
                        results.append(f"✅ Protocol Generation: {len(steps)} steps generated")
                    else:
                        results.append(f"❌ Protocol Generation: Failed ({response.status_code})")
                except Exception as e:
                    results.append(f"❌ Protocol Generation: Error - {str(e)}")
        else:
            results.append(f"❌ Patient Database: Failed ({response.status_code})")
    except Exception as e:
        results.append(f"❌ Patient Database: Error - {str(e)}")
    
    # 5. Literature Search
    try:
        response = requests.get(f"{api_url}/literature/search?query=osteoarthritis&limit=3", 
                              headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            papers = data.get('papers', [])
            results.append(f"✅ Literature Search: {len(papers)} papers found")
        else:
            results.append(f"❌ Literature Search: Failed ({response.status_code})")
    except Exception as e:
        results.append(f"❌ Literature Search: Error - {str(e)}")
    
    # 6. Advanced Services Status
    try:
        response = requests.get(f"{api_url}/advanced/system-status", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            services = data.get('services', {})
            active_count = sum(1 for s in services.values() if s.get('status') == 'active')
            results.append(f"✅ Advanced Services: {active_count}/{len(services)} active")
        else:
            results.append(f"❌ Advanced Services: Failed ({response.status_code})")
    except Exception as e:
        results.append(f"❌ Advanced Services: Error - {str(e)}")
    
    # Print results
    print("\n📊 QUICK REALITY CHECK RESULTS:")
    for result in results:
        print(f"   {result}")
    
    # Count successes
    successes = sum(1 for r in results if r.startswith("✅"))
    total = len(results)
    percentage = (successes / total * 100) if total > 0 else 0
    
    print(f"\n🎯 REALITY SCORE: {successes}/{total} ({percentage:.1f}%)")
    
    if percentage >= 70:
        print("   🟢 ASSESSMENT: Core functionality appears genuine")
    elif percentage >= 50:
        print("   🟡 ASSESSMENT: Mixed genuine and mock features")
    else:
        print("   🔴 ASSESSMENT: Significant functionality gaps")
    
    return percentage >= 70

if __name__ == "__main__":
    success = quick_reality_check()
    sys.exit(0 if success else 1)