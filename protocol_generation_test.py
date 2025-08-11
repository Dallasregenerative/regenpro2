import requests
import sys
import json
from datetime import datetime, timedelta

class ProtocolGenerationTester:
    def __init__(self, base_url="https://9add4fe9-ec95-4c25-945f-328dd5122e17.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer demo-token'
        }
        
        # Test patient IDs from review request
        self.maria_rodriguez_id = "e40b1209-bdcb-49bd-b533-a9d6a56d9df2"
        self.david_chen_id = "dcaf95e0-8a15-4303-80fa-196ebb961af7"
        
        # Protocol IDs for testing
        self.protocol_ids = []

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

    def create_maria_rodriguez_patient(self):
        """Create Maria Rodriguez test patient with comprehensive data"""
        patient_data = {
            "patient_id": self.maria_rodriguez_id,
            "demographics": {
                "name": "Maria Rodriguez",
                "age": "45",
                "gender": "Female",
                "occupation": "Software Engineer",
                "insurance": "Private Insurance"
            },
            "chief_complaint": "Chronic bilateral knee osteoarthritis with progressive functional decline seeking regenerative medicine alternatives to avoid total knee replacement",
            "history_present_illness": "45-year-old female software engineer with 4-year history of progressive bilateral knee osteoarthritis. Initially managed with NSAIDs and physical therapy with good response. Over past 18 months, significant worsening with daily pain 7/10, morning stiffness lasting 45 minutes, difficulty with stairs and prolonged sitting. Failed multiple conservative treatments including corticosteroid injections (temporary relief only), hyaluronic acid injections (minimal benefit), and extensive physical therapy. Patient is highly motivated to avoid knee replacement surgery and seeks evidence-based regenerative medicine options.",
            "past_medical_history": ["Osteoarthritis bilateral knees", "Mild hypertension", "Seasonal allergies"],
            "medications": ["Lisinopril 5mg daily", "Ibuprofen 600mg TID PRN", "Glucosamine/Chondroitin supplement", "Turmeric supplement"],
            "allergies": ["Penicillin (rash)", "Shellfish (mild reaction)"],
            "vital_signs": {
                "temperature": "98.4",
                "blood_pressure": "132/78",
                "heart_rate": "68",
                "respiratory_rate": "16",
                "oxygen_saturation": "99",
                "weight": "155",
                "height": "5'5\"",
                "BMI": "25.8"
            },
            "symptoms": [
                "bilateral knee pain", 
                "morning stiffness", 
                "functional limitation", 
                "difficulty with stairs",
                "pain with prolonged sitting",
                "decreased exercise tolerance",
                "sleep disruption due to pain"
            ],
            "lab_results": {
                "inflammatory_markers": {
                    "CRP": "1.8 mg/L",
                    "ESR": "15 mm/hr"
                },
                "complete_blood_count": {
                    "WBC": "6.8 K/uL",
                    "RBC": "4.6 M/uL",
                    "platelets": "295 K/uL",
                    "hemoglobin": "13.2 g/dL"
                },
                "metabolic_panel": {
                    "glucose": "92 mg/dL",
                    "creatinine": "0.9 mg/dL",
                    "BUN": "18 mg/dL"
                },
                "regenerative_markers": {
                    "vitamin_D": "38 ng/mL",
                    "vitamin_C": "1.4 mg/dL",
                    "zinc": "105 mcg/dL",
                    "PDGF": "52 pg/mL",
                    "VEGF": "145 pg/mL"
                }
            },
            "imaging_data": [
                {
                    "type": "X-ray",
                    "location": "bilateral knees",
                    "findings": "Grade 3 osteoarthritis with moderate joint space narrowing, osteophyte formation, and subchondral sclerosis. More pronounced in medial compartments bilaterally.",
                    "date": "2024-01-20"
                },
                {
                    "type": "MRI",
                    "location": "right knee",
                    "findings": "Moderate cartilage thinning in medial and patellofemoral compartments, complex meniscal tears, mild bone marrow edema, moderate synovial thickening. No significant ligamentous injury.",
                    "date": "2024-02-15"
                },
                {
                    "type": "MRI",
                    "location": "left knee", 
                    "findings": "Similar findings to right knee with moderate cartilage loss, meniscal degeneration, and synovial inflammation. Slightly less severe than right side.",
                    "date": "2024-02-15"
                }
            ],
            "genetic_data": {
                "regenerative_markers": {
                    "VEGF_polymorphism": "favorable",
                    "collagen_synthesis_genes": "normal",
                    "inflammatory_response_genes": "low_risk",
                    "healing_capacity_score": "above_average"
                },
                "pharmacogenomics": {
                    "NSAID_metabolism": "normal",
                    "opioid_sensitivity": "standard"
                }
            }
        }

        success, response = self.run_test(
            "Create Maria Rodriguez Patient Record",
            "POST",
            "patients",
            200,
            data=patient_data
        )
        
        if success:
            print(f"   ✅ Maria Rodriguez patient created successfully")
            print(f"   Patient ID: {self.maria_rodriguez_id}")
            return True
        return False

    def create_david_chen_patient(self):
        """Create David Chen test patient with shoulder injury"""
        patient_data = {
            "patient_id": self.david_chen_id,
            "demographics": {
                "name": "David Chen",
                "age": "52",
                "gender": "Male",
                "occupation": "Construction Manager",
                "insurance": "Workers Compensation"
            },
            "chief_complaint": "Chronic right shoulder rotator cuff injury with persistent pain and functional limitation despite conservative treatment, seeking regenerative medicine options",
            "history_present_illness": "52-year-old male construction manager with 8-month history of right shoulder pain following work-related injury. Initial MRI showed partial-thickness rotator cuff tear involving supraspinatus and infraspinatus tendons. Conservative management including physical therapy, NSAIDs, and corticosteroid injection provided only temporary relief. Patient experiences daily pain 6/10, significant weakness with overhead activities, and sleep disruption. Unable to return to full work duties. Seeking regenerative medicine alternatives to surgical repair.",
            "past_medical_history": ["Rotator cuff injury right shoulder", "Type 2 diabetes mellitus", "Hyperlipidemia", "Previous left shoulder injury (resolved)"],
            "medications": ["Metformin 1000mg BID", "Atorvastatin 20mg daily", "Meloxicam 15mg daily", "Tramadol 50mg PRN"],
            "allergies": ["NKDA"],
            "vital_signs": {
                "temperature": "98.6",
                "blood_pressure": "138/84",
                "heart_rate": "72",
                "respiratory_rate": "18",
                "oxygen_saturation": "98",
                "weight": "185",
                "height": "5'10\"",
                "BMI": "26.5"
            },
            "symptoms": [
                "right shoulder pain",
                "weakness with overhead activities", 
                "night pain",
                "functional limitation",
                "decreased range of motion",
                "work disability",
                "sleep disruption"
            ],
            "lab_results": {
                "inflammatory_markers": {
                    "CRP": "2.4 mg/L",
                    "ESR": "22 mm/hr"
                },
                "complete_blood_count": {
                    "WBC": "7.2 K/uL",
                    "RBC": "4.4 M/uL",
                    "platelets": "275 K/uL",
                    "hemoglobin": "14.1 g/dL"
                },
                "metabolic_panel": {
                    "glucose": "128 mg/dL",
                    "HbA1c": "6.8%",
                    "creatinine": "1.1 mg/dL"
                },
                "regenerative_markers": {
                    "vitamin_D": "28 ng/mL",
                    "vitamin_C": "0.9 mg/dL",
                    "zinc": "88 mcg/dL",
                    "PDGF": "38 pg/mL",
                    "VEGF": "112 pg/mL"
                }
            },
            "imaging_data": [
                {
                    "type": "MRI",
                    "location": "right shoulder",
                    "findings": "Partial-thickness rotator cuff tear involving supraspinatus and infraspinatus tendons. Moderate tendinosis with intratendinous signal changes. Mild subacromial bursitis. No full-thickness tears identified.",
                    "date": "2024-01-10"
                },
                {
                    "type": "Ultrasound",
                    "location": "right shoulder",
                    "findings": "Hypoechoic areas within supraspinatus tendon consistent with partial tear. Increased vascularity suggesting active inflammation. Subacromial bursal thickening.",
                    "date": "2024-02-28"
                }
            ],
            "genetic_data": {
                "regenerative_markers": {
                    "VEGF_polymorphism": "standard",
                    "collagen_synthesis_genes": "slightly_reduced",
                    "inflammatory_response_genes": "moderate_risk",
                    "healing_capacity_score": "average"
                },
                "pharmacogenomics": {
                    "NSAID_metabolism": "slow",
                    "diabetes_related_healing": "impaired"
                }
            }
        }

        success, response = self.run_test(
            "Create David Chen Patient Record",
            "POST",
            "patients",
            200,
            data=patient_data
        )
        
        if success:
            print(f"   ✅ David Chen patient created successfully")
            print(f"   Patient ID: {self.david_chen_id}")
            return True
        return False

    def test_maria_rodriguez_protocol_traditional_autologous(self):
        """Test Traditional Autologous protocol generation for Maria Rodriguez"""
        return self._test_protocol_generation(
            self.maria_rodriguez_id,
            "traditional_autologous", 
            "Traditional Autologous (US Legal) - Maria Rodriguez"
        )

    def test_maria_rodriguez_protocol_ai_optimized(self):
        """Test AI-Optimized protocol generation for Maria Rodriguez"""
        return self._test_protocol_generation(
            self.maria_rodriguez_id,
            "ai_optimized", 
            "AI-Optimized Best Protocol - Maria Rodriguez"
        )

    def test_maria_rodriguez_protocol_biologics(self):
        """Test Biologics protocol generation for Maria Rodriguez"""
        return self._test_protocol_generation(
            self.maria_rodriguez_id,
            "biologics", 
            "Biologics & Allogenic - Maria Rodriguez"
        )

    def test_maria_rodriguez_protocol_experimental(self):
        """Test Experimental protocol generation for Maria Rodriguez"""
        return self._test_protocol_generation(
            self.maria_rodriguez_id,
            "experimental", 
            "Experimental & Cutting-Edge - Maria Rodriguez"
        )

    def test_david_chen_protocol_generation(self):
        """Test protocol generation for David Chen shoulder injury"""
        return self._test_protocol_generation(
            self.david_chen_id,
            "ai_optimized", 
            "AI-Optimized Protocol - David Chen Shoulder Injury"
        )

    def _test_protocol_generation(self, patient_id, school_key, test_name):
        """Helper method to test protocol generation"""
        protocol_data = {
            "patient_id": patient_id,
            "school_of_thought": school_key
        }

        print(f"   This may take 60-90 seconds for AI protocol generation...")
        success, response = self.run_test(
            f"Generate Protocol - {test_name}",
            "POST",
            "protocols/generate",
            200,
            data=protocol_data,
            timeout=120
        )
        
        if success:
            protocol_id = response.get('protocol_id')
            if protocol_id:
                self.protocol_ids.append(protocol_id)
            
            print(f"   ✅ Protocol Generated Successfully")
            print(f"   Protocol ID: {protocol_id}")
            print(f"   School: {response.get('school_of_thought', 'Unknown')}")
            print(f"   Confidence Score: {response.get('confidence_score', 0):.2f}")
            print(f"   Protocol Steps: {len(response.get('protocol_steps', []))}")
            print(f"   Expected Outcomes: {len(response.get('expected_outcomes', []))}")
            print(f"   Cost Estimate: {response.get('cost_estimate', 'Not provided')}")
            print(f"   Legal Warnings: {len(response.get('legal_warnings', []))}")
            
            # Validate protocol content
            self._validate_protocol_content(response, test_name)
            
        return success

    def _validate_protocol_content(self, protocol_response, test_name):
        """Validate that protocol contains required content"""
        print(f"   📋 Validating Protocol Content for {test_name}:")
        
        # Check for detailed therapy steps
        protocol_steps = protocol_response.get('protocol_steps', [])
        if protocol_steps:
            first_step = protocol_steps[0]
            print(f"   ✅ Detailed Steps: {first_step.get('therapy', 'Unknown')} - {first_step.get('dosage', 'Unknown')}")
            print(f"   ✅ Timing: {first_step.get('timing', 'Unknown')}")
            print(f"   ✅ Delivery Method: {first_step.get('delivery_method', 'Unknown')}")
        
        # Check for evidence citations
        supporting_evidence = protocol_response.get('supporting_evidence', [])
        if supporting_evidence:
            print(f"   ✅ Evidence Citations: {len(supporting_evidence)} citations provided")
            if supporting_evidence[0].get('citation'):
                print(f"   ✅ PMID/Citation: {supporting_evidence[0].get('citation', 'Unknown')[:50]}...")
        
        # Check for cost estimates
        cost_estimate = protocol_response.get('cost_estimate')
        if cost_estimate:
            print(f"   ✅ Cost Estimate: {cost_estimate}")
        
        # Check for contraindications
        contraindications = protocol_response.get('contraindications', [])
        if contraindications:
            print(f"   ✅ Contraindications: {len(contraindications)} identified")
        
        # Check for AI reasoning
        ai_reasoning = protocol_response.get('ai_reasoning', '')
        if ai_reasoning and len(ai_reasoning) > 50:
            print(f"   ✅ AI Reasoning: Comprehensive explanation provided ({len(ai_reasoning)} chars)")
        
        # Check confidence score
        confidence_score = protocol_response.get('confidence_score', 0)
        if confidence_score >= 0.7:
            print(f"   ✅ High Confidence: {confidence_score:.2f}")
        elif confidence_score >= 0.5:
            print(f"   ⚠️ Moderate Confidence: {confidence_score:.2f}")
        else:
            print(f"   ❌ Low Confidence: {confidence_score:.2f}")

    def test_living_evidence_engine_maria(self):
        """Test Living Evidence Engine with Maria Rodriguez data"""
        mapping_data = {
            "protocol_id": self.protocol_ids[0] if self.protocol_ids else "maria_protocol_test",
            "condition": "osteoarthritis",
            "patient_id": self.maria_rodriguez_id,
            "protocol_components": [
                {
                    "name": "PRP injection bilateral knees",
                    "therapy": "platelet rich plasma",
                    "dosage": "4-6ml intra-articular per knee"
                },
                {
                    "name": "BMAC injection",
                    "therapy": "bone marrow aspirate concentrate",
                    "dosage": "2-3ml intra-articular per knee"
                }
            ]
        }

        success, response = self.run_test(
            "Living Evidence Engine - Maria Rodriguez Protocol Mapping",
            "POST",
            "evidence/protocol-evidence-mapping",
            200,
            data=mapping_data,
            timeout=90
        )
        
        if success:
            print(f"   ✅ Evidence Mapping Generated")
            print(f"   Status: {response.get('status', 'Unknown')}")
            evidence_mapping = response.get('evidence_mapping', {})
            if evidence_mapping:
                print(f"   Components Mapped: {evidence_mapping.get('total_components', 0)}")
                print(f"   Evidence Quality: {evidence_mapping.get('overall_evidence_quality', {}).get('grade', 'Unknown')}")
        
        return success

    def test_advanced_differential_diagnosis_maria(self):
        """Test Advanced Differential Diagnosis with Maria Rodriguez"""
        differential_data = {
            "patient_data": {
                "patient_id": self.maria_rodriguez_id,
                "demographics": {"age": 45, "gender": "female"},
                "medical_history": ["Osteoarthritis bilateral knees", "Mild hypertension"],
                "clinical_presentation": {
                    "chief_complaint": "Chronic bilateral knee osteoarthritis with progressive functional decline",
                    "symptom_duration": "4 years",
                    "pain_characteristics": {
                        "intensity": 7,
                        "quality": "aching pain with stiffness",
                        "aggravating_factors": ["stairs", "prolonged sitting"],
                        "relieving_factors": ["rest", "NSAIDs"]
                    }
                },
                "diagnostic_data": {
                    "imaging": {
                        "xray_findings": "Grade 3 osteoarthritis with moderate joint space narrowing",
                        "mri_findings": "Moderate cartilage thinning, complex meniscal tears"
                    },
                    "laboratory": {
                        "inflammatory_markers": {"CRP": 1.8, "ESR": 15}
                    }
                }
            },
            "analysis_parameters": {
                "differential_count": 3,
                "regenerative_focus": True
            }
        }

        success, response = self.run_test(
            "Advanced Differential Diagnosis - Maria Rodriguez",
            "POST",
            "diagnosis/comprehensive-differential",
            200,
            data=differential_data,
            timeout=120
        )
        
        if success:
            print(f"   ✅ Differential Diagnosis Generated")
            comprehensive_diagnosis = response.get('comprehensive_diagnosis', {})
            if comprehensive_diagnosis:
                differential_diagnoses = comprehensive_diagnosis.get('differential_diagnoses', [])
                print(f"   Diagnoses Generated: {len(differential_diagnoses)}")
                if differential_diagnoses:
                    print(f"   Primary Diagnosis: {differential_diagnoses[0].get('diagnosis', 'Unknown')}")
                    print(f"   Confidence: {differential_diagnoses[0].get('confidence_score', 0):.2f}")
        
        return success

    def test_enhanced_explainable_ai_maria(self):
        """Test Enhanced Explainable AI with Maria Rodriguez protocol"""
        if not self.protocol_ids:
            print("❌ No protocol ID available for explainable AI testing")
            return False

        explanation_data = {
            "model_prediction": {
                "diagnosis": "Bilateral knee osteoarthritis Grade 3",
                "confidence_score": 0.89,
                "regenerative_suitability": 0.85,
                "protocol_recommendation": "Combined PRP and BMAC therapy"
            },
            "patient_data": {
                "patient_id": self.maria_rodriguez_id,
                "demographics": {"age": 45, "gender": "female", "occupation": "software engineer"},
                "medical_history": ["Osteoarthritis bilateral knees", "Mild hypertension"],
                "clinical_features": {
                    "pain_level": 7,
                    "functional_limitation": "moderate to severe",
                    "inflammatory_markers": {"CRP": 1.8, "ESR": 15}
                }
            },
            "explanation_parameters": {
                "include_feature_importance": True,
                "include_counterfactuals": True,
                "transparency_level": "high"
            }
        }

        success, response = self.run_test(
            "Enhanced Explainable AI - Maria Rodriguez Protocol",
            "POST",
            "ai/enhanced-explanation",
            200,
            data=explanation_data,
            timeout=120
        )
        
        if success:
            print(f"   ✅ Explainable AI Analysis Generated")
            enhanced_explanation = response.get('enhanced_explanation', {})
            if enhanced_explanation:
                feature_importance = enhanced_explanation.get('feature_importance_analysis', {})
                if feature_importance:
                    features = feature_importance.get('feature_contributions', [])
                    print(f"   Feature Importance Factors: {len(features)}")
                
                transparency_assessment = enhanced_explanation.get('transparency_assessment', {})
                if transparency_assessment:
                    print(f"   Transparency Score: {transparency_assessment.get('transparency_score', 0):.2f}")
        
        return success

    def test_end_to_end_workflow_maria(self):
        """Test complete end-to-end workflow for Maria Rodriguez"""
        print("\n🔄 Testing Complete End-to-End Workflow for Maria Rodriguez:")
        
        # Step 1: Patient Analysis
        success, analysis_response = self.run_test(
            "Step 1: AI Patient Analysis - Maria Rodriguez",
            "POST",
            f"patients/{self.maria_rodriguez_id}/analyze",
            200,
            data={},
            timeout=90
        )
        
        if not success:
            return False
        
        # Step 2: Protocol Generation (AI-Optimized)
        protocol_data = {
            "patient_id": self.maria_rodriguez_id,
            "school_of_thought": "ai_optimized"
        }
        
        success, protocol_response = self.run_test(
            "Step 2: Protocol Generation - Maria Rodriguez",
            "POST",
            "protocols/generate",
            200,
            data=protocol_data,
            timeout=120
        )
        
        if not success:
            return False
        
        protocol_id = protocol_response.get('protocol_id')
        
        # Step 3: Protocol Explanation
        if protocol_id:
            success, explanation_response = self.run_test(
                "Step 3: Protocol Explanation - Maria Rodriguez",
                "POST",
                f"protocols/{protocol_id}/explanation",
                200,
                data={},
                timeout=90
            )
            
            if success:
                print(f"   ✅ Complete End-to-End Workflow Successful")
                print(f"   Analysis → Protocol → Explanation: All steps completed")
                return True
        
        return False

    def test_end_to_end_workflow_david(self):
        """Test complete end-to-end workflow for David Chen"""
        print("\n🔄 Testing Complete End-to-End Workflow for David Chen:")
        
        # Step 1: Patient Analysis
        success, analysis_response = self.run_test(
            "Step 1: AI Patient Analysis - David Chen",
            "POST",
            f"patients/{self.david_chen_id}/analyze",
            200,
            data={},
            timeout=90
        )
        
        if not success:
            return False
        
        # Step 2: Protocol Generation (AI-Optimized for shoulder)
        protocol_data = {
            "patient_id": self.david_chen_id,
            "school_of_thought": "ai_optimized"
        }
        
        success, protocol_response = self.run_test(
            "Step 2: Protocol Generation - David Chen",
            "POST",
            "protocols/generate",
            200,
            data=protocol_data,
            timeout=120
        )
        
        if not success:
            return False
        
        protocol_id = protocol_response.get('protocol_id')
        
        # Step 3: Protocol Explanation
        if protocol_id:
            success, explanation_response = self.run_test(
                "Step 3: Protocol Explanation - David Chen",
                "POST",
                f"protocols/{protocol_id}/explanation",
                200,
                data={},
                timeout=90
            )
            
            if success:
                print(f"   ✅ Complete End-to-End Workflow Successful")
                print(f"   Analysis → Protocol → Explanation: All steps completed")
                return True
        
        return False

    def run_comprehensive_protocol_tests(self):
        """Run all comprehensive protocol generation tests"""
        print("=" * 80)
        print("🧪 COMPREHENSIVE PROTOCOL GENERATION TESTING")
        print("Testing OpenAI API Key Fix and Complete Protocol Workflow")
        print("=" * 80)
        
        # Create test patients
        print("\n📋 STEP 1: Creating Test Patients")
        maria_created = self.create_maria_rodriguez_patient()
        david_created = self.create_david_chen_patient()
        
        if not maria_created or not david_created:
            print("❌ Failed to create test patients - aborting tests")
            return False
        
        # Test Maria Rodriguez - All Schools of Thought
        print("\n🏥 STEP 2: Testing Maria Rodriguez - All Schools of Thought")
        maria_traditional = self.test_maria_rodriguez_protocol_traditional_autologous()
        maria_ai = self.test_maria_rodriguez_protocol_ai_optimized()
        maria_biologics = self.test_maria_rodriguez_protocol_biologics()
        maria_experimental = self.test_maria_rodriguez_protocol_experimental()
        
        # Test David Chen - Shoulder Injury
        print("\n🏥 STEP 3: Testing David Chen - Shoulder Injury Protocol")
        david_protocol = self.test_david_chen_protocol_generation()
        
        # Test Critical Priority Features
        print("\n🔬 STEP 4: Testing Critical Priority Features")
        living_evidence = self.test_living_evidence_engine_maria()
        differential_diagnosis = self.test_advanced_differential_diagnosis_maria()
        explainable_ai = self.test_enhanced_explainable_ai_maria()
        
        # Test End-to-End Workflows
        print("\n🔄 STEP 5: Testing End-to-End Workflows")
        maria_workflow = self.test_end_to_end_workflow_maria()
        david_workflow = self.test_end_to_end_workflow_david()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 80)
        
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        print("\n🎯 PROTOCOL GENERATION RESULTS:")
        print(f"   Maria Rodriguez - Traditional Autologous: {'✅' if maria_traditional else '❌'}")
        print(f"   Maria Rodriguez - AI-Optimized: {'✅' if maria_ai else '❌'}")
        print(f"   Maria Rodriguez - Biologics: {'✅' if maria_biologics else '❌'}")
        print(f"   Maria Rodriguez - Experimental: {'✅' if maria_experimental else '❌'}")
        print(f"   David Chen - Shoulder Injury: {'✅' if david_protocol else '❌'}")
        
        print("\n🔬 CRITICAL PRIORITY FEATURES:")
        print(f"   Living Evidence Engine: {'✅' if living_evidence else '❌'}")
        print(f"   Advanced Differential Diagnosis: {'✅' if differential_diagnosis else '❌'}")
        print(f"   Enhanced Explainable AI: {'✅' if explainable_ai else '❌'}")
        
        print("\n🔄 END-TO-END WORKFLOWS:")
        print(f"   Maria Rodriguez Complete Workflow: {'✅' if maria_workflow else '❌'}")
        print(f"   David Chen Complete Workflow: {'✅' if david_workflow else '❌'}")
        
        # Check if OpenAI API key fix resolved 401 errors
        all_protocol_tests_passed = all([maria_traditional, maria_ai, maria_biologics, maria_experimental, david_protocol])
        
        if all_protocol_tests_passed:
            print("\n🎉 SUCCESS: OpenAI API key fix resolved 401 Unauthorized errors!")
            print("   All protocol generation tests passed - 100% functionality achieved")
        else:
            print("\n⚠️ PARTIAL SUCCESS: Some protocol generation tests failed")
            print("   OpenAI API key may need further investigation")
        
        return all_protocol_tests_passed

if __name__ == "__main__":
    tester = ProtocolGenerationTester()
    success = tester.run_comprehensive_protocol_tests()
    
    if success:
        print("\n✅ All comprehensive protocol generation tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed - check results above")
        sys.exit(1)