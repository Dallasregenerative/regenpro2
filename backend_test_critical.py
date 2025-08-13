import requests
import sys
import json
from datetime import datetime, timedelta

class CriticalPriorityTester:
    def __init__(self, base_url="https://medprotocol-3.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.patient_id = None
        self.protocol_id = None
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
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=self.headers, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    # Truncate long responses for readability
                    response_str = json.dumps(response_data, indent=2)
                    if len(response_str) > 300:
                        response_str = response_str[:300] + "..."
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

    def setup_test_data(self):
        """Create patient and protocol for testing"""
        print("\n📋 SETUP PHASE - Creating Test Data")
        print("-" * 50)
        
        # Create patient
        patient_data = {
            "demographics": {
                "name": "Dr. Sarah Mitchell",
                "age": "58",
                "gender": "Female",
                "occupation": "Physician"
            },
            "chief_complaint": "Bilateral knee osteoarthritis seeking regenerative alternatives",
            "history_present_illness": "58-year-old female physician with progressive bilateral knee pain over 3 years. Pain worse with activity, morning stiffness lasting 30 minutes. Failed conservative management including NSAIDs, physical therapy, and corticosteroid injections. Seeking regenerative medicine options to avoid knee replacement surgery.",
            "past_medical_history": ["Osteoarthritis", "Hypertension", "Hypothyroidism"],
            "medications": ["Lisinopril 10mg daily", "Levothyroxine 75mcg daily", "Ibuprofen PRN"],
            "allergies": ["NKDA"],
            "vital_signs": {
                "temperature": "98.6",
                "blood_pressure": "128/82",
                "heart_rate": "72"
            },
            "symptoms": ["bilateral knee pain", "morning stiffness", "decreased mobility"]
        }

        success, response = self.run_test(
            "Create Test Patient",
            "POST",
            "patients",
            200,
            data=patient_data
        )
        
        if success and 'patient_id' in response:
            self.patient_id = response['patient_id']
            print(f"   ✅ Created Patient ID: {self.patient_id}")
        else:
            print("   ❌ Failed to create patient")
            return False

        # Generate protocol
        protocol_data = {
            "patient_id": self.patient_id,
            "school_of_thought": "ai_optimized"
        }

        success, response = self.run_test(
            "Generate Test Protocol",
            "POST",
            "protocols/generate",
            200,
            data=protocol_data,
            timeout=90
        )
        
        if success and 'protocol_id' in response:
            self.protocol_id = response['protocol_id']
            print(f"   ✅ Created Protocol ID: {self.protocol_id}")
            return True
        else:
            print("   ❌ Failed to create protocol")
            return False

    # ========== LIVING EVIDENCE ENGINE TESTS ==========

    def test_living_evidence_protocol_mapping(self):
        """Test POST /api/evidence/protocol-evidence-mapping"""
        if not self.protocol_id:
            print("❌ No protocol ID available")
            return False

        mapping_data = {
            "protocol_id": self.protocol_id,
            "condition": "osteoarthritis",
            "therapies": ["PRP", "BMAC"],
            "patient_factors": {
                "age": 58,
                "severity": "moderate",
                "previous_treatments": ["NSAIDs", "physical_therapy"]
            }
        }

        success, response = self.run_test(
            "CRITICAL: Living Evidence Engine - Protocol Evidence Mapping",
            "POST",
            "evidence/protocol-evidence-mapping",
            200,
            data=mapping_data,
            timeout=90
        )
        
        if success:
            print(f"   Protocol ID: {response.get('protocol_id', 'Unknown')}")
            print(f"   Status: {response.get('status', 'Unknown')}")
            evidence_mapping = response.get('evidence_mapping', {})
            if evidence_mapping:
                print(f"   Evidence Sources: {evidence_mapping.get('total_sources', 0)}")
                print(f"   Evidence Strength: {evidence_mapping.get('evidence_strength_score', 0):.2f}")
        return success

    def test_living_evidence_reviews(self):
        """Test GET /api/evidence/living-reviews/{condition}"""
        success, response = self.run_test(
            "CRITICAL: Living Evidence Engine - Living Reviews",
            "GET",
            "evidence/living-reviews/osteoarthritis",
            200,
            timeout=60
        )
        
        if success:
            print(f"   Condition: {response.get('condition', 'Unknown')}")
            print(f"   Status: {response.get('status', 'Unknown')}")
            living_review = response.get('living_review', {})
            if living_review:
                print(f"   Review Quality: {living_review.get('review_quality_score', 0):.2f}")
                print(f"   Evidence Count: {living_review.get('recent_evidence_count', 0)}")
        return success

    def test_living_evidence_mapping_retrieval(self):
        """Test GET /api/evidence/protocol/{protocol_id}/evidence-mapping"""
        if not self.protocol_id:
            print("❌ No protocol ID available")
            return False

        success, response = self.run_test(
            "CRITICAL: Living Evidence Engine - Get Protocol Mapping",
            "GET",
            f"evidence/protocol/{self.protocol_id}/evidence-mapping",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Protocol ID: {response.get('protocol_id', 'Unknown')}")
            print(f"   Status: {response.get('status', 'Unknown')}")
            evidence_mapping = response.get('evidence_mapping', {})
            if evidence_mapping:
                print(f"   Mapping Quality: {evidence_mapping.get('mapping_quality', 0):.2f}")
        return success

    def test_living_evidence_alerts(self):
        """Test GET /api/evidence/alerts/{protocol_id}"""
        if not self.protocol_id:
            print("❌ No protocol ID available")
            return False

        success, response = self.run_test(
            "CRITICAL: Living Evidence Engine - Evidence Alerts",
            "GET",
            f"evidence/alerts/{self.protocol_id}",
            200,
            timeout=60
        )
        
        if success:
            print(f"   Protocol ID: {response.get('protocol_id', 'Unknown')}")
            print(f"   Status: {response.get('status', 'Unknown')}")
            alerts = response.get('evidence_alerts', [])
            print(f"   Active Alerts: {len(alerts)}")
        return success

    # ========== ADVANCED DIFFERENTIAL DIAGNOSIS TESTS ==========

    def test_differential_diagnosis_comprehensive(self):
        """Test POST /api/diagnosis/comprehensive-differential"""
        if not self.patient_id:
            print("❌ No patient ID available")
            return False

        diagnosis_data = {
            "patient_id": self.patient_id,
            "clinical_presentation": {
                "chief_complaint": "Bilateral knee pain and stiffness",
                "symptom_duration": "3 years",
                "pain_characteristics": {
                    "intensity": 6,
                    "quality": "aching with morning stiffness"
                }
            },
            "analysis_parameters": {
                "differential_count": 5,
                "regenerative_focus": True
            }
        }

        success, response = self.run_test(
            "CRITICAL: Advanced Differential Diagnosis - Comprehensive Analysis",
            "POST",
            "diagnosis/comprehensive-differential",
            200,
            data=diagnosis_data,
            timeout=120
        )
        
        if success:
            print(f"   Patient ID: {response.get('patient_id', 'Unknown')}")
            print(f"   Status: {response.get('status', 'Unknown')}")
            diagnoses = response.get('differential_diagnoses', [])
            print(f"   Diagnoses Generated: {len(diagnoses)}")
            if diagnoses:
                top_diagnosis = diagnoses[0]
                print(f"   Top Diagnosis: {top_diagnosis.get('diagnosis', 'Unknown')}")
                print(f"   Confidence: {top_diagnosis.get('confidence_score', 0):.2f}")
        return success

    def test_differential_diagnosis_retrieval(self):
        """Test GET /api/diagnosis/{diagnosis_id}"""
        # First create a diagnosis
        if not self.patient_id:
            print("❌ No patient ID available")
            return False

        diagnosis_data = {
            "patient_id": self.patient_id,
            "clinical_presentation": {
                "chief_complaint": "Bilateral knee pain",
                "symptom_duration": "3 years"
            },
            "analysis_parameters": {
                "differential_count": 3,
                "regenerative_focus": True
            }
        }

        create_success, create_response = self.run_test(
            "Setup: Create Diagnosis",
            "POST",
            "diagnosis/comprehensive-differential",
            200,
            data=diagnosis_data,
            timeout=90
        )
        
        if not create_success:
            print("❌ Could not create diagnosis")
            return False
        
        diagnosis_id = create_response.get('diagnosis_id')
        if not diagnosis_id:
            print("❌ No diagnosis ID returned")
            return False

        success, response = self.run_test(
            "CRITICAL: Advanced Differential Diagnosis - Get Diagnosis",
            "GET",
            f"diagnosis/{diagnosis_id}",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Diagnosis ID: {response.get('diagnosis_id', 'Unknown')}")
            print(f"   Status: {response.get('status', 'Unknown')}")
            diagnoses = response.get('differential_diagnoses', [])
            print(f"   Retrieved Diagnoses: {len(diagnoses)}")
        return success

    def test_differential_diagnosis_engine_status(self):
        """Test GET /api/diagnosis/engine-status"""
        success, response = self.run_test(
            "CRITICAL: Advanced Differential Diagnosis - Engine Status",
            "GET",
            "diagnosis/engine-status",
            200,
            timeout=60
        )
        
        if success:
            print(f"   Engine Status: {response.get('status', 'Unknown')}")
            print(f"   Version: {response.get('version', 'Unknown')}")
            capabilities = response.get('capabilities', {})
            if capabilities:
                print(f"   Multi-Modal Integration: {capabilities.get('multi_modal_integration', False)}")
                print(f"   Explainable AI: {capabilities.get('explainable_ai', False)}")
        return success

    # ========== ENHANCED EXPLAINABLE AI TESTS ==========

    def test_enhanced_explainable_ai_explanation(self):
        """Test POST /api/ai/enhanced-explanation"""
        if not self.patient_id:
            print("❌ No patient ID available")
            return False

        explanation_data = {
            "patient_id": self.patient_id,
            "demographics": {
                "age": 58,
                "gender": "Female",
                "occupation": "Physician"
            },
            "medical_history": [
                "Osteoarthritis bilateral knees",
                "Hypertension controlled"
            ],
            "symptoms": [
                "bilateral knee pain",
                "morning stiffness",
                "decreased mobility"
            ]
        }

        success, response = self.run_test(
            "CRITICAL: Enhanced Explainable AI - Generate Explanation",
            "POST",
            "ai/enhanced-explanation",
            200,
            data=explanation_data,
            timeout=90
        )
        
        if success:
            print(f"   Patient ID: {response.get('patient_id', 'Unknown')}")
            print(f"   Status: {response.get('status', 'Unknown')}")
            explanation = response.get('enhanced_explanation', {})
            if explanation:
                print(f"   Explanation ID: {explanation.get('explanation_id', 'Unknown')}")
                print(f"   Transparency Score: {explanation.get('transparency_score', 0):.2f}")
        return success

    def test_enhanced_explainable_ai_retrieval(self):
        """Test GET /api/ai/enhanced-explanation/{explanation_id}"""
        if not self.patient_id:
            print("❌ No patient ID available")
            return False

        # First create an explanation
        explanation_data = {
            "patient_id": self.patient_id,
            "demographics": {"age": 58, "gender": "Female"},
            "medical_history": ["Osteoarthritis bilateral knees"]
        }

        create_success, create_response = self.run_test(
            "Setup: Create Explanation",
            "POST",
            "ai/enhanced-explanation",
            200,
            data=explanation_data,
            timeout=60
        )
        
        if not create_success:
            print("❌ Could not create explanation")
            return False
        
        explanation_id = create_response.get('enhanced_explanation', {}).get('explanation_id')
        if not explanation_id:
            print("❌ No explanation ID returned")
            return False

        success, response = self.run_test(
            "CRITICAL: Enhanced Explainable AI - Get Explanation",
            "GET",
            f"ai/enhanced-explanation/{explanation_id}",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Explanation ID: {response.get('explanation_id', 'Unknown')}")
            print(f"   Status: {response.get('status', 'Unknown')}")
        return success

    def test_enhanced_explainable_ai_visual_breakdown(self):
        """Test GET /api/ai/visual-breakdown/{explanation_id}"""
        if not self.patient_id:
            print("❌ No patient ID available")
            return False

        # First create an explanation
        explanation_data = {
            "patient_id": self.patient_id,
            "demographics": {"age": 58, "gender": "Female"},
            "medical_history": ["Osteoarthritis bilateral knees"]
        }

        create_success, create_response = self.run_test(
            "Setup: Create Explanation for Visual Breakdown",
            "POST",
            "ai/enhanced-explanation",
            200,
            data=explanation_data,
            timeout=60
        )
        
        if not create_success:
            print("❌ Could not create explanation")
            return False
        
        explanation_id = create_response.get('enhanced_explanation', {}).get('explanation_id')
        if not explanation_id:
            print("❌ No explanation ID returned")
            return False

        success, response = self.run_test(
            "CRITICAL: Enhanced Explainable AI - Visual Breakdown",
            "GET",
            f"ai/visual-breakdown/{explanation_id}",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Explanation ID: {response.get('explanation_id', 'Unknown')}")
            print(f"   Status: {response.get('status', 'Unknown')}")
            breakdown = response.get('visual_breakdown', {})
            if breakdown:
                print(f"   SHAP Values: {len(breakdown.get('shap_values', []))}")
                print(f"   LIME Explanations: {len(breakdown.get('lime_explanations', []))}")
        return success

    def test_enhanced_explainable_ai_feature_interactions(self):
        """Test POST /api/ai/feature-interactions"""
        if not self.patient_id:
            print("❌ No patient ID available")
            return False

        interaction_data = {
            "patient_id": self.patient_id,
            "features": [
                {"name": "age", "value": 58, "type": "numeric"},
                {"name": "gender", "value": "Female", "type": "categorical"},
                {"name": "pain_intensity", "value": 6, "type": "numeric"}
            ],
            "interaction_analysis": {
                "include_pairwise": True,
                "max_interactions": 10
            }
        }

        success, response = self.run_test(
            "CRITICAL: Enhanced Explainable AI - Feature Interactions",
            "POST",
            "ai/feature-interactions",
            200,
            data=interaction_data,
            timeout=60
        )
        
        if success:
            print(f"   Patient ID: {response.get('patient_id', 'Unknown')}")
            print(f"   Status: {response.get('status', 'Unknown')}")
            interactions = response.get('feature_interactions', [])
            print(f"   Interactions Found: {len(interactions)}")
        return success

    def test_enhanced_explainable_ai_transparency_assessment(self):
        """Test GET /api/ai/transparency-assessment/{explanation_id}"""
        if not self.patient_id:
            print("❌ No patient ID available")
            return False

        # First create an explanation
        explanation_data = {
            "patient_id": self.patient_id,
            "demographics": {"age": 58, "gender": "Female"},
            "medical_history": ["Osteoarthritis bilateral knees"]
        }

        create_success, create_response = self.run_test(
            "Setup: Create Explanation for Transparency Assessment",
            "POST",
            "ai/enhanced-explanation",
            200,
            data=explanation_data,
            timeout=60
        )
        
        if not create_success:
            print("❌ Could not create explanation")
            return False
        
        explanation_id = create_response.get('enhanced_explanation', {}).get('explanation_id')
        if not explanation_id:
            print("❌ No explanation ID returned")
            return False

        success, response = self.run_test(
            "CRITICAL: Enhanced Explainable AI - Transparency Assessment",
            "GET",
            f"ai/transparency-assessment/{explanation_id}",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Explanation ID: {response.get('explanation_id', 'Unknown')}")
            print(f"   Status: {response.get('status', 'Unknown')}")
            metrics = response.get('transparency_metrics', {})
            if metrics:
                print(f"   Overall Score: {metrics.get('overall_score', 0):.2f}")
                print(f"   Interpretability: {metrics.get('interpretability_score', 0):.2f}")
        return success

    # ========== MAIN TEST RUNNER ==========

    def run_all_tests(self):
        """Run all critical priority feature tests"""
        print("\n" + "="*80)
        print("🚀 CRITICAL PRIORITY FEATURES TESTING - RegenMed AI Pro Platform")
        print("="*80)
        print("Testing the three FIXED Critical Priority features:")
        print("1. Living Evidence Engine System")
        print("2. Advanced Differential Diagnosis System") 
        print("3. Enhanced Explainable AI System")
        print("="*80)

        # Setup test data
        if not self.setup_test_data():
            print("\n❌ SETUP FAILED - Cannot proceed with testing")
            return False

        print(f"\n✅ SETUP COMPLETE - Patient ID: {self.patient_id}, Protocol ID: {self.protocol_id}")

        # Test 1: Living Evidence Engine System
        print("\n" + "="*60)
        print("🧬 TESTING: Living Evidence Engine System")
        print("="*60)
        
        living_evidence_tests = [
            self.test_living_evidence_protocol_mapping,
            self.test_living_evidence_reviews,
            self.test_living_evidence_mapping_retrieval,
            self.test_living_evidence_alerts
        ]
        
        living_evidence_passed = sum(1 for test in living_evidence_tests if test())
        print(f"\n📊 Living Evidence Engine Results: {living_evidence_passed}/{len(living_evidence_tests)} tests passed")

        # Test 2: Advanced Differential Diagnosis System
        print("\n" + "="*60)
        print("🔬 TESTING: Advanced Differential Diagnosis System")
        print("="*60)
        
        differential_diagnosis_tests = [
            self.test_differential_diagnosis_comprehensive,
            self.test_differential_diagnosis_retrieval,
            self.test_differential_diagnosis_engine_status
        ]
        
        differential_diagnosis_passed = sum(1 for test in differential_diagnosis_tests if test())
        print(f"\n📊 Advanced Differential Diagnosis Results: {differential_diagnosis_passed}/{len(differential_diagnosis_tests)} tests passed")

        # Test 3: Enhanced Explainable AI System
        print("\n" + "="*60)
        print("🤖 TESTING: Enhanced Explainable AI System")
        print("="*60)
        
        explainable_ai_tests = [
            self.test_enhanced_explainable_ai_explanation,
            self.test_enhanced_explainable_ai_retrieval,
            self.test_enhanced_explainable_ai_visual_breakdown,
            self.test_enhanced_explainable_ai_feature_interactions,
            self.test_enhanced_explainable_ai_transparency_assessment
        ]
        
        explainable_ai_passed = sum(1 for test in explainable_ai_tests if test())
        print(f"\n📊 Enhanced Explainable AI Results: {explainable_ai_passed}/{len(explainable_ai_tests)} tests passed")

        # Final Results Summary
        total_tests = len(living_evidence_tests) + len(differential_diagnosis_tests) + len(explainable_ai_tests)
        total_passed = living_evidence_passed + differential_diagnosis_passed + explainable_ai_passed
        
        print("\n" + "="*80)
        print("🎯 CRITICAL PRIORITY FEATURES TESTING SUMMARY")
        print("="*80)
        print(f"Living Evidence Engine System:        {living_evidence_passed}/{len(living_evidence_tests)} tests passed ({living_evidence_passed/len(living_evidence_tests)*100:.1f}%)")
        print(f"Advanced Differential Diagnosis:      {differential_diagnosis_passed}/{len(differential_diagnosis_tests)} tests passed ({differential_diagnosis_passed/len(differential_diagnosis_tests)*100:.1f}%)")
        print(f"Enhanced Explainable AI System:       {explainable_ai_passed}/{len(explainable_ai_tests)} tests passed ({explainable_ai_passed/len(explainable_ai_tests)*100:.1f}%)")
        print("-" * 80)
        print(f"OVERALL CRITICAL PRIORITY RESULTS:    {total_passed}/{total_tests} tests passed ({total_passed/total_tests*100:.1f}%)")
        
        if total_passed == total_tests:
            print("🎉 ALL CRITICAL PRIORITY FEATURES WORKING PERFECTLY!")
        elif total_passed >= total_tests * 0.8:
            print("✅ CRITICAL PRIORITY FEATURES MOSTLY FUNCTIONAL")
        elif total_passed >= total_tests * 0.5:
            print("⚠️  CRITICAL PRIORITY FEATURES PARTIALLY FUNCTIONAL")
        else:
            print("❌ CRITICAL PRIORITY FEATURES NEED SIGNIFICANT FIXES")
        
        print("="*80)
        
        return {
            'living_evidence_passed': living_evidence_passed,
            'living_evidence_total': len(living_evidence_tests),
            'differential_diagnosis_passed': differential_diagnosis_passed,
            'differential_diagnosis_total': len(differential_diagnosis_tests),
            'explainable_ai_passed': explainable_ai_passed,
            'explainable_ai_total': len(explainable_ai_tests),
            'total_passed': total_passed,
            'total_tests': total_tests,
            'success_rate': total_passed/total_tests if total_tests > 0 else 0
        }

if __name__ == "__main__":
    print("🚀 Starting RegenMed AI Pro Critical Priority Features Testing...")
    
    tester = CriticalPriorityTester()
    
    # Run the critical priority features testing
    results = tester.run_all_tests()
    
    if results['success_rate'] >= 0.8:
        print("\n✅ Critical Priority Features Testing COMPLETED SUCCESSFULLY")
        sys.exit(0)
    else:
        print("\n❌ Critical Priority Features Testing FAILED")
        sys.exit(1)