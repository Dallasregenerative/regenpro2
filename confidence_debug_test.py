#!/usr/bin/env python3
"""
Confidence Score Bug Investigation Test
DEBUG TEST: 2% Confidence Score Issue Investigation
Testing POST /api/diagnosis/comprehensive-differential with Robert Chen's data
"""

import requests
import json
import sys
from datetime import datetime

class ConfidenceScoreDebugger:
    def __init__(self, base_url="https://9add4fe9-ec95-4c25-945f-328dd5122e17.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer demo-token'
        }

    def debug_confidence_scores(self):
        """Main debug function for confidence score investigation"""
        
        print("🔍 DEBUGGING 2% CONFIDENCE SCORE ISSUE")
        print("=" * 80)
        print("   Testing POST /api/diagnosis/comprehensive-differential with Robert Chen's data")
        print("   Investigating posterior probability calculations and diagnostic reasoning")
        print("=" * 80)
        
        # Step 1: Create Robert Chen patient
        print("\n📋 Step 1: Creating Robert Chen patient...")
        robert_chen_data = {
            "demographics": {
                "name": "Robert Chen",
                "age": "52",
                "gender": "Male",
                "occupation": "Construction Manager",
                "insurance": "Self-pay"
            },
            "chief_complaint": "Right shoulder pain with decreased range of motion, 8 months duration, seeking alternatives to shoulder surgery",
            "history_present_illness": "52-year-old male construction manager with progressive right shoulder pain over 8 months. Pain worse with overhead activities and at night. Decreased range of motion affecting work performance. Failed conservative management including NSAIDs, physical therapy, and corticosteroid injections. Seeking regenerative medicine alternatives to avoid shoulder surgery.",
            "past_medical_history": ["Rotator cuff tendinopathy", "Hypertension", "Type 2 diabetes"],
            "medications": ["Metformin 1000mg BID", "Lisinopril 10mg daily", "Ibuprofen PRN"],
            "allergies": ["NKDA"],
            "vital_signs": {
                "temperature": "98.4",
                "blood_pressure": "138/88",
                "heart_rate": "78",
                "respiratory_rate": "16",
                "oxygen_saturation": "97",
                "weight": "185",
                "height": "5'10\""
            },
            "symptoms": ["right shoulder pain", "decreased range of motion", "night pain", "overhead activity limitation"],
            "lab_results": {
                "inflammatory_markers": {
                    "CRP": "3.2 mg/L",
                    "ESR": "22 mm/hr"
                },
                "metabolic_panel": {
                    "glucose": "145 mg/dL",
                    "HbA1c": "7.2%"
                }
            },
            "imaging_data": [
                {
                    "type": "X-ray",
                    "location": "right shoulder",
                    "findings": "Mild acromioclavicular joint arthritis, no acute fracture",
                    "date": "2024-01-20"
                },
                {
                    "type": "MRI",
                    "location": "right shoulder",
                    "findings": "Partial thickness rotator cuff tear, subacromial impingement, mild glenohumeral arthritis",
                    "date": "2024-02-15"
                }
            ]
        }

        try:
            response = requests.post(
                f"{self.api_url}/patients",
                json=robert_chen_data,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"❌ Failed to create Robert Chen patient: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
            patient_data = response.json()
            robert_chen_id = patient_data.get('patient_id')
            print(f"✅ Robert Chen created with ID: {robert_chen_id}")
            
        except Exception as e:
            print(f"❌ Error creating patient: {str(e)}")
            return False

        # Step 2: Run comprehensive differential diagnosis using the specific endpoint
        print(f"\n🧠 Step 2: Running comprehensive differential diagnosis...")
        print("   🔍 TESTING: POST /api/diagnosis/comprehensive-differential")
        print("   🔍 ANALYZING: Posterior probability calculations and confidence scores")
        
        # First try the specific endpoint mentioned in the review
        try:
            response = requests.post(
                f"{self.api_url}/diagnosis/comprehensive-differential",
                json={"patient_id": robert_chen_id},
                headers=self.headers,
                timeout=120
            )
            
            if response.status_code == 200:
                analysis_data = response.json()
                print("✅ Comprehensive differential diagnosis completed via /diagnosis/comprehensive-differential")
                
                # Extract diagnostic results from the comprehensive diagnosis response
                comp_diagnosis = analysis_data.get('comprehensive_diagnosis', {})
                differential_diagnoses = comp_diagnosis.get('differential_diagnoses', [])
                
                # Convert to the expected format - EXTRACT POSTERIOR PROBABILITY
                diagnostic_results = []
                for diag in differential_diagnoses:
                    # Extract the actual posterior probability value
                    posterior_prob = diag.get('posterior_probability', 0.0)
                    prior_prob = diag.get('prior_probability', 0.0)
                    likelihood = diag.get('likelihood', 0.0)
                    
                    diagnostic_results.append({
                        'diagnosis': diag.get('diagnosis', 'Unknown'),
                        'confidence_score': posterior_prob,  # Use posterior_probability
                        'reasoning': diag.get('diagnostic_reasoning', 'No reasoning'),
                        'supporting_evidence': diag.get('supporting_evidence', []),
                        'mechanisms_involved': diag.get('mechanisms_involved', []),
                        'regenerative_targets': diag.get('regenerative_targets', []),
                        # Add debug info
                        'debug_prior_probability': prior_prob,
                        'debug_likelihood': likelihood,
                        'debug_posterior_probability': posterior_prob
                    })
                
                analysis_data['diagnostic_results'] = diagnostic_results
                
            else:
                print(f"⚠️  /diagnosis/comprehensive-differential failed: {response.status_code}")
                print("   Falling back to /patients/{id}/analyze endpoint...")
                
                # Fallback to the regular analyze endpoint
                response = requests.post(
                    f"{self.api_url}/patients/{robert_chen_id}/analyze",
                    json={},
                    headers=self.headers,
                    timeout=120
                )
                
                if response.status_code != 200:
                    print(f"❌ Both endpoints failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    return False
                    
                analysis_data = response.json()
                print("✅ Comprehensive differential diagnosis completed via /patients/{id}/analyze")
            
        except Exception as e:
            print(f"❌ Error in differential diagnosis: {str(e)}")
            return False

        # Step 3: DETAILED CONFIDENCE SCORE ANALYSIS
        print(f"\n📊 Step 3: DETAILED CONFIDENCE SCORE ANALYSIS")
        print("   🔍 Investigating diagnostic clues and likelihood calculations")
        
        diagnostic_results = analysis_data.get('diagnostic_results', [])
        print(f"   Total Diagnoses Generated: {len(diagnostic_results)}")
        
        if not diagnostic_results:
            print("   ❌ No diagnostic results returned - this is the bug!")
            return False
        
        # Analyze each diagnosis for confidence score issues
        confidence_scores = []
        for i, diagnosis in enumerate(diagnostic_results, 1):
            confidence = diagnosis.get('confidence_score', 0)
            confidence_scores.append(confidence)
            
            print(f"\n   📋 Diagnosis {i}: {diagnosis.get('diagnosis', 'Unknown')}")
            print(f"   ├── Confidence Score: {confidence:.3f} ({confidence*100:.1f}%)")
            print(f"   ├── Reasoning: {diagnosis.get('reasoning', 'No reasoning')[:100]}...")
            print(f"   ├── Supporting Evidence: {len(diagnosis.get('supporting_evidence', []))} items")
            print(f"   ├── Mechanisms: {len(diagnosis.get('mechanisms_involved', []))} mechanisms")
            print(f"   └── Regenerative Targets: {len(diagnosis.get('regenerative_targets', []))} targets")

        # Step 4: CONFIDENCE SCORE BUG DETECTION
        print(f"\n🚨 Step 4: CONFIDENCE SCORE BUG DETECTION")
        
        # Check for the 2% bug
        two_percent_scores = [score for score in confidence_scores if abs(score - 0.02) < 0.001]
        uniform_low_scores = [score for score in confidence_scores if score < 0.1]
        
        print(f"   🔍 Scores exactly at 2%: {len(two_percent_scores)}/{len(confidence_scores)}")
        print(f"   🔍 Scores below 10%: {len(uniform_low_scores)}/{len(confidence_scores)}")
        print(f"   🔍 Score Range: {min(confidence_scores):.3f} - {max(confidence_scores):.3f}")
        
        # Expected behavior check
        expected_primary_range = (0.70, 0.85)  # 70-85% for primary
        expected_secondary_range = (0.60, 0.75)  # 60-75% for secondary
        expected_tertiary_range = (0.40, 0.60)  # 40-60% for tertiary
        
        if len(confidence_scores) >= 1:
            primary_score = confidence_scores[0]
            primary_in_range = expected_primary_range[0] <= primary_score <= expected_primary_range[1]
            print(f"   🔍 Primary diagnosis confidence in expected range (70-85%): {primary_in_range}")
            
        if len(confidence_scores) >= 2:
            secondary_score = confidence_scores[1]
            secondary_in_range = expected_secondary_range[0] <= secondary_score <= expected_secondary_range[1]
            print(f"   🔍 Secondary diagnosis confidence in expected range (60-75%): {secondary_in_range}")
            
        if len(confidence_scores) >= 3:
            tertiary_score = confidence_scores[2]
            tertiary_in_range = expected_tertiary_range[0] <= tertiary_score <= expected_tertiary_range[1]
            print(f"   🔍 Tertiary diagnosis confidence in expected range (40-60%): {tertiary_in_range}")

        # Step 5: ROOT CAUSE ANALYSIS
        print(f"\n🔧 Step 5: ROOT CAUSE ANALYSIS")
        
        # Check if this is the 2% bug
        if len(two_percent_scores) > 0:
            print("   🚨 BUG CONFIRMED: Found diagnoses with exactly 2% confidence scores")
            print("   🔍 This indicates posterior probability calculation issues")
            
        if len(uniform_low_scores) == len(confidence_scores) and len(confidence_scores) > 0:
            print("   🚨 BUG CONFIRMED: All confidence scores are uniformly low (<10%)")
            print("   🔍 This suggests:")
            print("       - Prior probabilities may be too low")
            print("       - Likelihood calculations defaulting to low values (0.3)")
            print("       - Bayes' theorem calculation errors")
            print("       - Diagnostic clues not matching likelihood patterns")
            
        # Check for realistic clinical probability distribution
        has_realistic_distribution = False
        if len(confidence_scores) >= 3:
            # Check if we have a proper decreasing confidence pattern
            decreasing_pattern = all(confidence_scores[i] >= confidence_scores[i+1] for i in range(len(confidence_scores)-1))
            primary_reasonable = confidence_scores[0] > 0.5  # Primary should be >50%
            has_realistic_distribution = decreasing_pattern and primary_reasonable
            
        print(f"   🔍 Realistic clinical probability distribution: {has_realistic_distribution}")

        # Step 6: DETAILED API RESPONSE ANALYSIS
        print(f"\n📡 Step 6: DETAILED API RESPONSE ANALYSIS")
        
        # Print the full response structure for debugging
        print("   🔍 Full API Response Structure:")
        response_keys = list(analysis_data.keys())
        print(f"   Response Keys: {response_keys}")
        
        # Check for comprehensive diagnosis data
        if 'comprehensive_diagnosis' in analysis_data:
            comp_diagnosis = analysis_data['comprehensive_diagnosis']
            print(f"   🔍 Comprehensive diagnosis available: {type(comp_diagnosis)}")
            if isinstance(comp_diagnosis, dict):
                comp_keys = list(comp_diagnosis.keys())
                print(f"   Comprehensive diagnosis keys: {comp_keys}")
                
                # Look for the original differential diagnoses data
                if 'differential_diagnoses' in comp_diagnosis:
                    original_diagnoses = comp_diagnosis['differential_diagnoses']
                    print(f"   🔍 Original differential diagnoses count: {len(original_diagnoses)}")
                    
                    for i, orig_diag in enumerate(original_diagnoses):
                        print(f"   🔍 Original Diagnosis {i+1}:")
                        print(f"       - Diagnosis: {orig_diag.get('diagnosis', 'Unknown')}")
                        print(f"       - Probability: {orig_diag.get('probability', 'Missing')}")
                        print(f"       - Regenerative Suitability: {orig_diag.get('regenerative_suitability', 'Missing')}")
                        print(f"       - Clinical Reasoning: {orig_diag.get('clinical_reasoning', 'Missing')[:50]}...")
                        print(f"       - All keys: {list(orig_diag.keys())}")
                
        # Check for posterior probability data
        for i, diagnosis in enumerate(diagnostic_results):
            print(f"   🔍 Diagnosis {i+1} full data keys: {list(diagnosis.keys())}")
            
        # Print a sample of the raw response for debugging
        print(f"\n   🔍 RAW RESPONSE SAMPLE (first 500 chars):")
        raw_response = json.dumps(analysis_data, indent=2)
        print(f"   {raw_response[:500]}...")

        # Step 7: SUMMARY AND RECOMMENDATIONS
        print(f"\n📋 Step 7: BUG INVESTIGATION SUMMARY")
        print("=" * 80)
        
        bug_detected = len(two_percent_scores) > 0 or (len(uniform_low_scores) == len(confidence_scores) and len(confidence_scores) > 0)
        
        if bug_detected:
            print("   🚨 CONFIDENCE SCORE BUG CONFIRMED")
            print("   📋 FINDINGS:")
            print(f"       - {len(two_percent_scores)} diagnoses with exactly 2% confidence")
            print(f"       - {len(uniform_low_scores)} diagnoses with <10% confidence")
            if confidence_scores:
                print(f"       - Expected primary range: 70-85%, Actual: {confidence_scores[0]*100:.1f}%")
            print("   🔧 RECOMMENDED FIXES:")
            print("       1. Check posterior_probability calculation in backend")
            print("       2. Verify diagnostic clues are generating proper likelihood values")
            print("       3. Ensure prior probabilities are realistic for clinical conditions")
            print("       4. Verify Bayes' theorem implementation")
            print("       5. Check if likelihood calculations are defaulting to 0.3")
        else:
            print("   ✅ CONFIDENCE SCORES APPEAR NORMAL")
            print("   📋 No 2% confidence score bug detected")
            
        print("=" * 80)
        return True

if __name__ == "__main__":
    debugger = ConfidenceScoreDebugger()
    success = debugger.debug_confidence_scores()
    
    if success:
        print("\n🎉 CONFIDENCE SCORE DEBUG TEST COMPLETE!")
        print("Check the detailed analysis above for bug investigation results")
        sys.exit(0)
    else:
        print("\n❌ CONFIDENCE SCORE DEBUG TEST FAILED")
        sys.exit(1)