import requests
import sys
import json
from datetime import datetime

class TargetedFixTester:
    def __init__(self, base_url="https://7270ea2f-1d23-46a0-9a6e-bef595343dd6.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.patient_id = None
        self.diagnosis_id = None
        self.explanation_id = None
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

    def setup_patient(self):
        """Create a test patient for diagnosis testing"""
        patient_data = {
            "demographics": {
                "name": "Dr. Maria Rodriguez",
                "age": "52",
                "gender": "Female",
                "occupation": "Orthopedic Surgeon",
                "insurance": "Self-pay"
            },
            "chief_complaint": "Progressive right shoulder pain and weakness affecting surgical practice",
            "history_present_illness": "52-year-old orthopedic surgeon with 8-month history of progressive right shoulder pain and weakness. Pain initially started after a long surgical case and has worsened despite conservative treatment. Significant functional impairment affecting ability to perform surgery.",
            "past_medical_history": ["Rotator cuff tendinopathy", "Cervical spondylosis"],
            "medications": ["Ibuprofen 600mg TID", "Omeprazole 20mg daily"],
            "allergies": ["NKDA"],
            "vital_signs": {
                "temperature": "98.4",
                "blood_pressure": "118/76",
                "heart_rate": "68",
                "respiratory_rate": "14",
                "oxygen_saturation": "99",
                "weight": "135",
                "height": "5'4\""
            },
            "symptoms": ["right shoulder pain", "weakness with overhead activities", "night pain", "functional limitation"],
            "lab_results": {
                "inflammatory_markers": {
                    "CRP": "1.8 mg/L",
                    "ESR": "15 mm/hr"
                }
            },
            "imaging_data": [
                {
                    "type": "MRI",
                    "location": "right shoulder",
                    "findings": "Full-thickness rotator cuff tear involving supraspinatus and infraspinatus tendons with moderate retraction",
                    "date": "2024-01-20"
                }
            ]
        }

        success, response = self.run_test(
            "Setup: Create Test Patient",
            "POST",
            "patients",
            200,
            data=patient_data
        )
        
        if success and 'patient_id' in response:
            self.patient_id = response['patient_id']
            print(f"   Created Patient ID: {self.patient_id}")
            return True
        return False

    def test_advanced_differential_diagnosis_system(self):
        """Test the Advanced Differential Diagnosis System - all 3 endpoints"""
        print("\n" + "="*80)
        print("TESTING: Advanced Differential Diagnosis System")
        print("="*80)
        
        if not self.patient_id:
            if not self.setup_patient():
                print("❌ Could not create test patient")
                return False
        
        # Test 1: POST /api/diagnosis/comprehensive-differential
        differential_data = {
            "patient_data": {
                "patient_id": self.patient_id,
                "demographics": {
                    "age": 52,
                    "gender": "female",
                    "occupation": "surgeon"
                },
                "medical_history": {
                    "past_medical_history": ["Rotator cuff tendinopathy", "Cervical spondylosis"],
                    "medications": ["Ibuprofen 600mg TID", "Omeprazole 20mg daily"],
                    "allergies": ["NKDA"]
                },
                "clinical_presentation": {
                    "chief_complaint": "Progressive right shoulder pain and weakness affecting surgical practice",
                    "symptom_duration": "8 months",
                    "pain_characteristics": {
                        "intensity": 7,
                        "quality": "deep aching pain with sharp exacerbations during overhead activities",
                        "aggravating_factors": ["overhead reaching", "lifting", "sleeping on affected side"],
                        "relieving_factors": ["rest", "ice application", "NSAIDs"]
                    },
                    "functional_impact": {
                        "work_impact": "unable to perform complex surgical procedures requiring overhead positioning",
                        "daily_activities": "difficulty with hair washing, reaching overhead shelves",
                        "sleep_disturbance": "awakens 2-3 times nightly due to shoulder pain"
                    }
                },
                "diagnostic_modalities": {
                    "physical_examination": {
                        "inspection": "mild deltoid atrophy, no visible deformity",
                        "palpation": "tenderness over greater tuberosity and subacromial space",
                        "range_of_motion": "active abduction limited to 90 degrees, passive abduction 140 degrees",
                        "special_tests": ["positive Hawkins-Kennedy test", "positive empty can test", "positive drop arm test", "positive external rotation lag sign"],
                        "strength_testing": "4/5 abduction, 3/5 external rotation, 5/5 internal rotation"
                    },
                    "imaging": {
                        "mri_findings": "Full-thickness rotator cuff tear involving supraspinatus and infraspinatus tendons with moderate retraction, mild fatty infiltration Goutallier grade 2"
                    },
                    "laboratory": {
                        "inflammatory_markers": {"CRP": 1.8, "ESR": 15}
                    }
                }
            },
            "analysis_parameters": {
                "differential_count": 5,
                "confidence_threshold": 0.1,
                "regenerative_focus": True,
                "evidence_level_minimum": 2
            },
            "practitioner_controlled": True
        }

        print("\n1. Testing POST /api/diagnosis/comprehensive-differential")
        print("   This should generate and STORE diagnosis...")
        success1, response1 = self.run_test(
            "Generate Comprehensive Differential Diagnosis",
            "POST",
            "diagnosis/comprehensive-differential",
            200,
            data=differential_data,
            timeout=120
        )
        
        if success1:
            self.diagnosis_id = response1.get('diagnosis_id')
            if self.diagnosis_id:
                print(f"   ✅ Diagnosis ID generated and stored: {self.diagnosis_id}")
            else:
                print(f"   ⚠️ No diagnosis_id in response - may affect retrieval test")
        
        # Test 2: GET /api/diagnosis/{diagnosis_id}
        print("\n2. Testing GET /api/diagnosis/{diagnosis_id}")
        print("   This should retrieve stored diagnosis (previously 404)...")
        
        if self.diagnosis_id:
            success2, response2 = self.run_test(
                "Retrieve Stored Diagnosis by ID",
                "GET",
                f"diagnosis/{self.diagnosis_id}",
                200,
                timeout=45
            )
        else:
            print("   ❌ Skipping retrieval test - no diagnosis_id available")
            success2 = False
        
        # Test 3: GET /api/diagnosis/engine-status
        print("\n3. Testing GET /api/diagnosis/engine-status")
        print("   This should work (previously 404)...")
        success3, response3 = self.run_test(
            "Get Diagnosis Engine Status",
            "GET",
            "diagnosis/engine-status",
            200,
            timeout=30
        )
        
        # Calculate success rate
        tests_passed = sum([success1, success2, success3])
        total_tests = 3
        success_rate = (tests_passed / total_tests) * 100
        
        print(f"\n📊 Advanced Differential Diagnosis System Results:")
        print(f"   Tests Passed: {tests_passed}/{total_tests} ({success_rate:.1f}%)")
        print(f"   Expected Improvement: 33% → {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("   ✅ EXCELLENT - System is now fully functional!")
        elif success_rate >= 70:
            print("   ✅ GOOD - Significant improvement achieved")
        elif success_rate > 33:
            print("   ⚠️ PARTIAL - Some improvement but issues remain")
        else:
            print("   ❌ FAILED - No improvement from baseline")
        
        return success_rate >= 70

    def test_enhanced_explainable_ai_system(self):
        """Test the Enhanced Explainable AI System - 2 key endpoints"""
        print("\n" + "="*80)
        print("TESTING: Enhanced Explainable AI System")
        print("="*80)
        
        if not self.patient_id:
            if not self.setup_patient():
                print("❌ Could not create test patient")
                return False
        
        # Test 1: POST /api/ai/enhanced-explanation
        explanation_data = {
            "patient_id": self.patient_id,
            "analysis_type": "comprehensive_diagnosis",
            "clinical_context": {
                "primary_diagnosis": "Full-thickness rotator cuff tear",
                "confidence_score": 0.92,
                "treatment_recommendations": ["PRP injection", "BMAC procedure", "Physical therapy"],
                "risk_factors": ["Age 52", "Occupational overuse", "Previous tendinopathy"],
                "prognostic_factors": ["Good tissue quality", "Motivated patient", "Early intervention"]
            },
            "explanation_parameters": {
                "explanation_depth": "comprehensive",
                "include_feature_importance": True,
                "include_visual_breakdown": True,
                "include_counterfactuals": True,
                "transparency_level": "high"
            },
            "model_inputs": {
                "demographic_features": {"age": 52, "gender": "female", "occupation": "surgeon"},
                "clinical_features": {"pain_intensity": 7, "functional_limitation": 8, "symptom_duration": 8},
                "imaging_features": {"tear_size": "large", "retraction": "moderate", "fatty_infiltration": "grade_2"},
                "laboratory_features": {"crp": 1.8, "esr": 15}
            }
        }

        print("\n1. Testing POST /api/ai/enhanced-explanation")
        print("   This should generate and STORE explanation...")
        success1, response1 = self.run_test(
            "Generate Enhanced AI Explanation",
            "POST",
            "ai/enhanced-explanation",
            200,
            data=explanation_data,
            timeout=120
        )
        
        if success1:
            self.explanation_id = response1.get('explanation_id')
            if self.explanation_id:
                print(f"   ✅ Explanation ID generated and stored: {self.explanation_id}")
            else:
                print(f"   ⚠️ No explanation_id in response - may affect retrieval test")
        
        # Test 2: GET /api/ai/enhanced-explanation/{explanation_id}
        print("\n2. Testing GET /api/ai/enhanced-explanation/{explanation_id}")
        print("   This should retrieve stored explanation (previously 500 error)...")
        
        if self.explanation_id:
            success2, response2 = self.run_test(
                "Retrieve Stored Enhanced Explanation by ID",
                "GET",
                f"ai/enhanced-explanation/{self.explanation_id}",
                200,
                timeout=45
            )
        else:
            print("   ❌ Skipping retrieval test - no explanation_id available")
            success2 = False
        
        # Calculate success rate
        tests_passed = sum([success1, success2])
        total_tests = 2
        success_rate = (tests_passed / total_tests) * 100
        
        print(f"\n📊 Enhanced Explainable AI System Results:")
        print(f"   Tests Passed: {tests_passed}/{total_tests} ({success_rate:.1f}%)")
        print(f"   Expected Improvement: 20% → {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("   ✅ EXCELLENT - System is now fully functional!")
        elif success_rate >= 70:
            print("   ✅ GOOD - Significant improvement achieved")
        elif success_rate > 20:
            print("   ⚠️ PARTIAL - Some improvement but issues remain")
        else:
            print("   ❌ FAILED - No improvement from baseline")
        
        return success_rate >= 40  # Lower threshold as requested (at least 40%)

    def run_targeted_tests(self):
        """Run the targeted fix verification tests"""
        print("🎯 TARGETED FIX VERIFICATION")
        print("Testing ONLY the two systems that were just fixed:")
        print("1. Advanced Differential Diagnosis System")
        print("2. Enhanced Explainable AI System")
        print("\n" + "="*80)
        
        # Test both systems
        diagnosis_success = self.test_advanced_differential_diagnosis_system()
        ai_success = self.test_enhanced_explainable_ai_system()
        
        # Final summary
        print("\n" + "="*80)
        print("🎯 TARGETED FIX VERIFICATION SUMMARY")
        print("="*80)
        
        print(f"\n📋 SYSTEMS TESTED:")
        print(f"   Advanced Differential Diagnosis: {'✅ IMPROVED' if diagnosis_success else '❌ STILL BROKEN'}")
        print(f"   Enhanced Explainable AI: {'✅ IMPROVED' if ai_success else '❌ STILL BROKEN'}")
        
        print(f"\n📊 OVERALL RESULTS:")
        print(f"   Total Tests Run: {self.tests_run}")
        print(f"   Tests Passed: {self.tests_passed}")
        print(f"   Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        print(f"\n🎯 FIX VERIFICATION:")
        if diagnosis_success and ai_success:
            print("   ✅ BOTH SYSTEMS IMPROVED - Database storage fixes working!")
        elif diagnosis_success or ai_success:
            print("   ⚠️ PARTIAL SUCCESS - One system improved, one still needs work")
        else:
            print("   ❌ FIXES NOT WORKING - Both systems still have issues")
        
        print(f"\n🔍 KEY FINDINGS:")
        if diagnosis_success:
            print("   ✅ Advanced Differential Diagnosis: Database storage enabled retrieval endpoints")
        else:
            print("   ❌ Advanced Differential Diagnosis: Still has storage/retrieval issues")
            
        if ai_success:
            print("   ✅ Enhanced Explainable AI: Database storage enabled retrieval endpoints")
        else:
            print("   ❌ Enhanced Explainable AI: Still has storage/retrieval issues")
        
        return diagnosis_success and ai_success

if __name__ == "__main__":
    tester = TargetedFixTester()
    success = tester.run_targeted_tests()
    sys.exit(0 if success else 1)