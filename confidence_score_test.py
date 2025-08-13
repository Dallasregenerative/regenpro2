#!/usr/bin/env python3
"""
CONFIDENCE SCORE BUG FIX VALIDATION TEST
Testing Robert Chen case for realistic clinical probability distributions
"""

import requests
import json
import sys
from datetime import datetime

class ConfidenceScoreBugTest:
    def __init__(self, base_url="https://9add4fe9-ec95-4c25-945f-328dd5122e17.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer demo-token'
        }
        self.robert_chen_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=60):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if endpoint else self.api_url
        
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=self.headers, timeout=timeout)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=self.headers, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
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

    def test_confidence_score_bug_fix_validation(self):
        """CONFIDENCE SCORE BUG FIX VALIDATION - Test Robert Chen case for realistic clinical distributions"""
        
        print("🎯 CONFIDENCE SCORE BUG FIX VALIDATION")
        print("   Objective: Verify 2% confidence score bug is fixed with realistic clinical probability distributions")
        print("   Expected: Primary 70-85%, Secondary 60-75%, Tertiary 40-60% confidence scores")
        
        # Create Robert Chen patient (52-year-old construction manager with shoulder pain)
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

        # Step 1: Create Robert Chen patient
        print("   Step 1: Creating Robert Chen patient...")
        create_success, create_response = self.run_test(
            "CONFIDENCE FIX - Create Robert Chen Patient",
            "POST",
            "patients",
            200,
            data=robert_chen_data,
            timeout=30
        )
        
        if not create_success:
            print("   ❌ Failed to create Robert Chen patient")
            return False
            
        self.robert_chen_id = create_response.get('patient_id')
        print(f"   ✅ Robert Chen created with ID: {self.robert_chen_id}")

        # Step 2: Run comprehensive differential diagnosis
        print("   Step 2: Running comprehensive differential diagnosis...")
        print("   🔍 CRITICAL VALIDATION: Checking for realistic clinical probability distributions")
        
        analysis_success, analysis_response = self.run_test(
            "CONFIDENCE FIX - Robert Chen Differential Diagnosis",
            "POST",
            f"patients/{self.robert_chen_id}/analyze",
            200,
            data={},
            timeout=120
        )
        
        if not analysis_success:
            print("   ❌ Comprehensive differential diagnosis failed")
            return False

        # Step 3: CONFIDENCE SCORE VALIDATION
        print("   Step 3: CONFIDENCE SCORE VALIDATION")
        
        diagnostic_results = analysis_response.get('diagnostic_results', [])
        print(f"   Total Diagnoses Generated: {len(diagnostic_results)}")
        
        if not diagnostic_results:
            print("   ❌ No diagnostic results returned")
            return False
        
        # Extract confidence scores
        confidence_scores = []
        diagnoses_info = []
        
        for i, diagnosis in enumerate(diagnostic_results, 1):
            confidence = diagnosis.get('confidence_score', 0)
            confidence_scores.append(confidence)
            diagnoses_info.append({
                'rank': i,
                'diagnosis': diagnosis.get('diagnosis', 'Unknown'),
                'confidence': confidence,
                'confidence_percent': confidence * 100
            })
            
            print(f"   Diagnosis {i}: {diagnosis.get('diagnosis', 'Unknown')}")
            print(f"   ├── Confidence Score: {confidence:.3f} ({confidence*100:.1f}%)")
            print(f"   ├── Reasoning: {diagnosis.get('reasoning', 'No reasoning')[:80]}...")
            print(f"   └── Regenerative Targets: {len(diagnosis.get('regenerative_targets', []))} targets")

        # Step 4: BUG FIX VALIDATION CRITERIA
        print("   Step 4: BUG FIX VALIDATION CRITERIA")
        
        validation_results = {
            'no_uniform_2_percent': True,
            'primary_confidence_realistic': False,
            'proper_distribution': False,
            'clinical_logic_evident': False,
            'varied_confidence_scores': False
        }
        
        # Check 1: No more uniform 2% confidence scores
        two_percent_scores = [score for score in confidence_scores if abs(score - 0.02) < 0.001]
        uniform_low_scores = [score for score in confidence_scores if score < 0.05]
        
        validation_results['no_uniform_2_percent'] = len(two_percent_scores) == 0
        print(f"   ✅ No uniform 2% scores: {validation_results['no_uniform_2_percent']} (Found {len(two_percent_scores)} at 2%)")
        
        # Check 2: Primary diagnosis confidence ≥60% (realistic for clear clinical presentation)
        if len(confidence_scores) >= 1:
            primary_confidence = confidence_scores[0]
            validation_results['primary_confidence_realistic'] = primary_confidence >= 0.60
            print(f"   ✅ Primary confidence ≥60%: {validation_results['primary_confidence_realistic']} ({primary_confidence*100:.1f}%)")
        
        # Check 3: Proper probability distribution with decreasing confidence scores
        if len(confidence_scores) >= 2:
            decreasing_pattern = all(confidence_scores[i] >= confidence_scores[i+1] for i in range(len(confidence_scores)-1))
            validation_results['proper_distribution'] = decreasing_pattern
            print(f"   ✅ Proper decreasing distribution: {validation_results['proper_distribution']}")
        
        # Check 4: Clinical logic evident (shoulder-specific diagnoses higher for shoulder pain)
        shoulder_related_diagnoses = [d for d in diagnoses_info if any(term in d['diagnosis'].lower() for term in ['shoulder', 'rotator', 'cuff', 'glenohumeral', 'subacromial'])]
        if shoulder_related_diagnoses:
            highest_shoulder_confidence = max(d['confidence'] for d in shoulder_related_diagnoses)
            validation_results['clinical_logic_evident'] = highest_shoulder_confidence >= 0.50
            print(f"   ✅ Clinical logic evident: {validation_results['clinical_logic_evident']} (Shoulder diagnoses max: {highest_shoulder_confidence*100:.1f}%)")
        
        # Check 5: Varied confidence scores (not all the same value)
        unique_scores = len(set(confidence_scores))
        validation_results['varied_confidence_scores'] = unique_scores > 1
        print(f"   ✅ Varied confidence scores: {validation_results['varied_confidence_scores']} ({unique_scores} unique values)")

        # Step 5: OVERALL VALIDATION RESULT
        print("   Step 5: OVERALL VALIDATION RESULT")
        
        passed_criteria = sum(validation_results.values())
        total_criteria = len(validation_results)
        
        print(f"   📊 Validation Criteria Passed: {passed_criteria}/{total_criteria}")
        
        # Expected ranges validation
        expected_ranges = {
            'primary': (0.70, 0.85),
            'secondary': (0.60, 0.75),
            'tertiary': (0.40, 0.60)
        }
        
        range_validations = {}
        for i, (range_name, (min_val, max_val)) in enumerate(expected_ranges.items()):
            if i < len(confidence_scores):
                score = confidence_scores[i]
                in_range = min_val <= score <= max_val
                range_validations[range_name] = in_range
                print(f"   📈 {range_name.title()} diagnosis in expected range ({min_val*100:.0f}-{max_val*100:.0f}%): {in_range} ({score*100:.1f}%)")
        
        # Final assessment
        bug_fix_successful = passed_criteria >= 4  # At least 4/5 criteria must pass
        realistic_distributions = any(range_validations.values()) if range_validations else False
        
        print("   🎯 CONFIDENCE SCORE BUG FIX ASSESSMENT:")
        if bug_fix_successful and realistic_distributions:
            print("   ✅ BUG FIX SUCCESSFUL - Confidence scores now show realistic clinical distributions")
            print("   ✅ No more uniform 2% confidence scores across all diagnoses")
            print("   ✅ AI recommendations now clinically actionable based on confidence levels")
        elif bug_fix_successful:
            print("   ⚠️  PARTIAL SUCCESS - Most criteria passed but confidence ranges need adjustment")
        else:
            print("   ❌ BUG FIX INCOMPLETE - Confidence score issues persist")
            print("   🔧 Root cause fixes still needed:")
            print("       - Prior probabilities may still be too low")
            print("       - Likelihood calculations may need enhancement")
            print("       - Bayes' theorem inputs require realistic clinical values")
        
        return bug_fix_successful and realistic_distributions

def main():
    print("🚀 CONFIDENCE SCORE BUG FIX VALIDATION TEST")
    print("=" * 80)
    
    tester = ConfidenceScoreBugTest()
    
    # Run the confidence score bug fix validation
    success = tester.test_confidence_score_bug_fix_validation()
    
    print("\n" + "=" * 80)
    print("🏁 CONFIDENCE SCORE BUG FIX TEST COMPLETE")
    
    if success:
        print("✅ CONFIDENCE SCORE BUG FIX VALIDATED - Realistic clinical distributions confirmed")
        print("✅ System now provides clinically meaningful diagnostic probabilities")
        sys.exit(0)
    else:
        print("❌ CONFIDENCE SCORE BUG FIX NEEDS ATTENTION - Issues persist")
        print("❌ System still shows unrealistic confidence score distributions")
        sys.exit(1)

if __name__ == "__main__":
    main()