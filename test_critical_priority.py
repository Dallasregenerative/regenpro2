#!/usr/bin/env python3
"""
Critical Priority Features Testing Script
Tests the three Critical Priority systems as requested in the review:
1. Living Evidence Engine System
2. Advanced Differential Diagnosis System  
3. Enhanced Explainable AI System
"""

import requests
import sys
import json
from datetime import datetime, timedelta

class CriticalPriorityTester:
    def __init__(self, base_url="https://7270ea2f-1d23-46a0-9a6e-bef595343dd6.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.patient_id = None
        self.protocol_id = None
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
        """Create test patient and protocol for testing"""
        print("\n🔧 SETUP: Creating test patient and protocol")
        print("-" * 60)
        
        # Create patient
        patient_data = {
            "demographics": {
                "name": "Dr. Sarah Mitchell",
                "age": "58",
                "gender": "Female",
                "occupation": "Physician",
                "insurance": "Self-pay"
            },
            "chief_complaint": "Bilateral knee osteoarthritis seeking regenerative alternatives",
            "history_present_illness": "58-year-old female physician with progressive bilateral knee pain over 3 years. Pain worse with activity, morning stiffness lasting 30 minutes. Failed conservative management including NSAIDs, physical therapy, and corticosteroid injections. Seeking regenerative medicine options to avoid knee replacement surgery.",
            "past_medical_history": ["Osteoarthritis", "Hypertension", "Hypothyroidism"],
            "medications": ["Lisinopril 10mg daily", "Levothyroxine 75mcg daily", "Ibuprofen PRN"],
            "allergies": ["NKDA"],
            "vital_signs": {
                "temperature": "98.6",
                "blood_pressure": "128/82",
                "heart_rate": "72",
                "respiratory_rate": "16",
                "oxygen_saturation": "98",
                "weight": "145",
                "height": "5'6\""
            },
            "symptoms": ["bilateral knee pain", "morning stiffness", "decreased mobility", "functional limitation"],
            "lab_results": {
                "inflammatory_markers": {
                    "CRP": "2.1 mg/L",
                    "ESR": "18 mm/hr"
                },
                "complete_blood_count": {
                    "WBC": "6.2 K/uL",
                    "RBC": "4.5 M/uL",
                    "platelets": "285 K/uL"
                }
            },
            "imaging_data": [
                {
                    "type": "X-ray",
                    "location": "bilateral knees",
                    "findings": "Grade 2-3 osteoarthritis with joint space narrowing and osteophyte formation",
                    "date": "2024-01-15"
                },
                {
                    "type": "MRI",
                    "location": "right knee",
                    "findings": "Cartilage thinning, meniscal degeneration, mild bone marrow edema",
                    "date": "2024-02-01"
                }
            ],
            "genetic_data": {
                "regenerative_markers": {
                    "VEGF_polymorphism": "positive",
                    "collagen_synthesis_genes": "normal"
                }
            }
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
            print(f"   Created Patient ID: {self.patient_id}")
        
        # Generate protocol
        if self.patient_id:
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
                print(f"   Created Protocol ID: {self.protocol_id}")

    # ========== CRITICAL PRIORITY SYSTEM 1: LIVING EVIDENCE ENGINE ==========
    
    def test_living_evidence_protocol_mapping(self):
        """Test POST /api/evidence/protocol-evidence-mapping"""
        if not self.protocol_id:
            print("❌ No protocol ID available for evidence mapping testing")
            return False

        mapping_data = {
            "protocol_id": self.protocol_id,
            "condition": "osteoarthritis",
            "therapies": ["PRP", "BMAC"],
            "patient_factors": {
                "age": 58,
                "severity": "moderate",
                "previous_treatments": ["NSAIDs", "physical_therapy", "corticosteroid_injections"]
            },
            "evidence_requirements": {
                "minimum_evidence_level": 2,
                "include_real_world_data": True,
                "geographic_relevance": ["US", "EU"],
                "recency_threshold": "2020-01-01"
            }
        }

        print("   This may take 30-60 seconds for comprehensive evidence mapping...")
        success, response = self.run_test(
            "Living Evidence Engine - Protocol Evidence Mapping",
            "POST",
            "evidence/protocol-evidence-mapping",
            200,
            data=mapping_data,
            timeout=90
        )
        
        if success:
            print(f"   Protocol ID: {response.get('protocol_id', 'Unknown')}")
            print(f"   Evidence Mapping Status: {response.get('status', 'Unknown')}")
            
            evidence_mapping = response.get('evidence_mapping', {})
            if evidence_mapping:
                print(f"   Total Evidence Sources: {evidence_mapping.get('total_sources', 0)}")
                print(f"   High Quality Evidence: {evidence_mapping.get('high_quality_sources', 0)}")
                print(f"   Evidence Strength Score: {evidence_mapping.get('evidence_strength_score', 0):.2f}")
            
            protocol_justification = response.get('protocol_justification', {})
            if protocol_justification:
                print(f"   Protocol Justification Score: {protocol_justification.get('justification_score', 0):.2f}")
                print(f"   Evidence-Based Recommendations: {len(protocol_justification.get('recommendations', []))}")
        
        return success

    def test_living_evidence_living_reviews(self):
        """Test GET /api/evidence/living-reviews/{condition}"""
        success, response = self.run_test(
            "Living Evidence Engine - Living Reviews",
            "GET",
            "evidence/living-reviews/osteoarthritis?therapies=PRP,BMAC&include_real_world=true&evidence_level=2",
            200,
            timeout=60
        )
        
        if success:
            print(f"   Condition: {response.get('condition', 'Unknown')}")
            print(f"   Review Status: {response.get('status', 'Unknown')}")
            
            living_review = response.get('living_review', {})
            if living_review:
                print(f"   Last Updated: {living_review.get('last_updated', 'Unknown')}")
                print(f"   Evidence Sources: {living_review.get('total_evidence_sources', 0)}")
                print(f"   Therapy Coverage: {len(living_review.get('therapies_covered', []))}")
                
            therapy_analysis = response.get('therapy_analysis', {})
            if therapy_analysis:
                prp_data = therapy_analysis.get('PRP', {})
                bmac_data = therapy_analysis.get('BMAC', {})
                
                if prp_data:
                    print(f"   PRP Evidence Quality: {prp_data.get('evidence_quality', 'Unknown')}")
                    print(f"   PRP Success Rate: {prp_data.get('pooled_success_rate', 0):.1%}")
                
                if bmac_data:
                    print(f"   BMAC Evidence Quality: {bmac_data.get('evidence_quality', 'Unknown')}")
                    print(f"   BMAC Success Rate: {bmac_data.get('pooled_success_rate', 0):.1%}")
                    
            real_world_data = response.get('real_world_evidence', {})
            if real_world_data:
                print(f"   Real-World Studies: {real_world_data.get('studies_included', 0)}")
                print(f"   Patient Population: {real_world_data.get('total_patients', 0)}")
        
        return success

    def test_living_evidence_protocol_retrieval(self):
        """Test GET /api/evidence/protocol/{protocol_id}/evidence-mapping"""
        if not self.protocol_id:
            print("❌ No protocol ID available for evidence mapping retrieval")
            return False
        
        success, response = self.run_test(
            "Living Evidence Engine - Protocol Evidence Mapping Retrieval",
            "GET",
            f"evidence/protocol/{self.protocol_id}/evidence-mapping",
            200
        )
        
        if success:
            print(f"   Protocol ID: {response.get('protocol_id', 'Unknown')}")
            print(f"   Mapping Status: {response.get('mapping_status', 'Unknown')}")
            print(f"   Evidence Features: {len(response.get('evidence_features', []))}")
            print(f"   Last Mapping Update: {response.get('last_mapping_update', 'Unknown')}")
        
        return success

    def test_living_evidence_alerts(self):
        """Test GET /api/evidence/alerts/{protocol_id}"""
        if not self.protocol_id:
            print("❌ No protocol ID available for evidence alerts testing")
            return False
        
        success, response = self.run_test(
            "Living Evidence Engine - Evidence Change Alerts",
            "GET",
            f"evidence/alerts/{self.protocol_id}",
            200
        )
        
        if success:
            print(f"   Protocol ID: {response.get('protocol_id', 'Unknown')}")
            print(f"   Alert Status: {response.get('status', 'Unknown')}")
            
            alerts = response.get('alerts', [])
            print(f"   Active Alerts: {len(alerts)}")
            
            if alerts:
                for i, alert in enumerate(alerts[:3], 1):  # Show first 3 alerts
                    print(f"   Alert {i}: {alert.get('alert_type', 'Unknown')} - {alert.get('severity', 'Unknown')}")
                    print(f"     Message: {alert.get('message', 'No message')[:60]}...")
                    
            evidence_changes = response.get('evidence_changes', {})
            if evidence_changes:
                print(f"   New Evidence Available: {evidence_changes.get('new_evidence_count', 0)}")
                print(f"   Updated Guidelines: {evidence_changes.get('updated_guidelines', 0)}")
                print(f"   Safety Updates: {evidence_changes.get('safety_updates', 0)}")
                
            monitoring_status = response.get('monitoring_status', {})
            if monitoring_status:
                print(f"   Monitoring Active: {monitoring_status.get('active', False)}")
                print(f"   Last Check: {monitoring_status.get('last_check', 'Unknown')}")
        
        return success

    # ========== CRITICAL PRIORITY SYSTEM 2: ADVANCED DIFFERENTIAL DIAGNOSIS ==========
    
    def test_advanced_differential_diagnosis_comprehensive(self):
        """Test POST /api/diagnosis/comprehensive-differential"""
        if not self.patient_id:
            print("❌ No patient ID available for comprehensive differential diagnosis testing")
            return False

        # Use realistic medical data as requested - osteoarthritis case
        differential_data = {
            "patient_id": self.patient_id,
            "clinical_presentation": {
                "chief_complaint": "Progressive bilateral knee pain and morning stiffness affecting daily activities",
                "symptom_duration": "3 years",
                "pain_characteristics": {
                    "intensity": 7,
                    "quality": "deep aching pain with morning stiffness lasting 45 minutes",
                    "aggravating_factors": ["prolonged standing", "stair climbing", "cold weather"],
                    "relieving_factors": ["rest", "heat application", "gentle movement"]
                },
                "functional_impact": {
                    "walking_distance": "limited to 2 blocks",
                    "stair_climbing": "requires handrail support",
                    "work_impact": "difficulty with prolonged standing during surgeries"
                }
            },
            "diagnostic_modalities": {
                "physical_examination": {
                    "inspection": "bilateral knee swelling, no erythema",
                    "palpation": "tenderness over medial joint lines bilaterally",
                    "range_of_motion": "flexion limited to 115 degrees bilaterally",
                    "special_tests": ["positive McMurray test bilateral", "negative drawer test"],
                    "gait_analysis": "antalgic gait with shortened stance phase"
                },
                "imaging": {
                    "xray_findings": "Grade 2-3 osteoarthritis with joint space narrowing, osteophyte formation, subchondral sclerosis",
                    "mri_findings": "cartilage thinning, meniscal degeneration, mild bone marrow edema, small effusions"
                },
                "laboratory": {
                    "inflammatory_markers": {"CRP": 2.1, "ESR": 18},
                    "autoimmune_markers": {"RF": "negative", "anti_CCP": "negative", "ANA": "negative"},
                    "metabolic_markers": {"uric_acid": 4.2, "vitamin_D": 32}
                }
            },
            "analysis_parameters": {
                "differential_count": 5,
                "confidence_threshold": 0.1,
                "include_rare_conditions": False,
                "regenerative_focus": True,
                "evidence_level_minimum": 2
            }
        }

        print("   Testing comprehensive differential diagnosis generation...")
        print("   This may take 60-90 seconds for AI analysis...")
        success, response = self.run_test(
            "Advanced Differential Diagnosis - Comprehensive Differential",
            "POST",
            "diagnosis/comprehensive-differential",
            200,
            data=differential_data,
            timeout=120
        )
        
        if success:
            print(f"   Analysis Status: {response.get('status', 'Unknown')}")
            print(f"   Patient ID: {response.get('patient_id', 'Unknown')}")
            
            # Check for diagnosis_id in response
            diagnosis_id = response.get('diagnosis_id')
            if diagnosis_id:
                print(f"   Diagnosis ID Generated: {diagnosis_id}")
                # Store for later tests
                self.diagnosis_id = diagnosis_id
            
            differential_diagnoses = response.get('differential_diagnoses', [])
            print(f"   Differential Diagnoses Generated: {len(differential_diagnoses)}")
            
            if differential_diagnoses:
                for i, diagnosis in enumerate(differential_diagnoses[:3], 1):
                    print(f"   Diagnosis {i}: {diagnosis.get('diagnosis', 'Unknown')}")
                    print(f"     Confidence: {diagnosis.get('confidence_score', 0):.2f}")
                    print(f"     ICD-10: {diagnosis.get('icd10_code', 'Unknown')}")
                    print(f"     Regenerative Suitability: {diagnosis.get('regenerative_suitability', 'Unknown')}")
            
            # Check for explainable AI analysis
            explainable_analysis = response.get('explainable_ai_analysis', {})
            if explainable_analysis:
                print(f"   Explainable AI Features: {len(explainable_analysis.get('feature_importance', []))}")
                print(f"   Transparency Score: {explainable_analysis.get('transparency_score', 0):.2f}")
            
            # Check for confidence analysis
            confidence_analysis = response.get('confidence_analysis', {})
            if confidence_analysis:
                print(f"   Confidence Intervals Generated: {len(confidence_analysis.get('confidence_intervals', []))}")
                print(f"   Overall Diagnostic Confidence: {confidence_analysis.get('overall_confidence', 0):.2f}")
            
            # Check for mechanism insights
            mechanism_insights = response.get('mechanism_insights', {})
            if mechanism_insights:
                print(f"   Mechanism Pathways Analyzed: {len(mechanism_insights.get('pathways', []))}")
                print(f"   Cellular Mechanisms: {len(mechanism_insights.get('cellular_mechanisms', []))}")
        
        return success

    def test_advanced_differential_diagnosis_engine_status(self):
        """Test GET /api/diagnosis/engine-status"""
        success, response = self.run_test(
            "Advanced Differential Diagnosis - Engine Status",
            "GET",
            "diagnosis/engine-status",
            200,
            timeout=60
        )
        
        if success:
            print(f"   Engine Status: {response.get('status', 'Unknown')}")
            print(f"   Engine Version: {response.get('version', 'Unknown')}")
            
            capabilities = response.get('capabilities', {})
            if capabilities:
                print(f"   Multi-Modal Integration: {capabilities.get('multi_modal_integration', False)}")
                print(f"   Bayesian Analysis: {capabilities.get('bayesian_analysis', False)}")
                print(f"   Explainable AI: {capabilities.get('explainable_ai', False)}")
                print(f"   Confidence Analysis: {capabilities.get('confidence_analysis', False)}")
                print(f"   Mechanism Insights: {capabilities.get('mechanism_insights', False)}")
            
            performance_metrics = response.get('performance_metrics', {})
            if performance_metrics:
                print(f"   Diagnostic Accuracy: {performance_metrics.get('diagnostic_accuracy', 0):.1%}")
                print(f"   Average Analysis Time: {performance_metrics.get('avg_analysis_time', 0):.2f}s")
                print(f"   Total Diagnoses Processed: {performance_metrics.get('total_diagnoses', 0)}")
            
            # Check for system health indicators
            system_health = response.get('system_health', {})
            if system_health:
                print(f"   Database Connection: {system_health.get('database_status', 'Unknown')}")
                print(f"   AI Models Loaded: {system_health.get('models_loaded', 0)}")
        
        return success

    def test_advanced_differential_diagnosis_retrieval(self):
        """Test GET /api/diagnosis/{diagnosis_id}"""
        # Use diagnosis_id from previous test or create a test one
        diagnosis_id = self.diagnosis_id or "test_diagnosis_001"
        
        success, response = self.run_test(
            "Advanced Differential Diagnosis - Get Diagnosis by ID",
            "GET",
            f"diagnosis/{diagnosis_id}",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Diagnosis ID: {response.get('diagnosis_id', 'Unknown')}")
            print(f"   Patient ID: {response.get('patient_id', 'Unknown')}")
            print(f"   Analysis Status: {response.get('status', 'Unknown')}")
            print(f"   Analysis Timestamp: {response.get('analysis_timestamp', 'Unknown')}")
            
            differential_diagnoses = response.get('differential_diagnoses', [])
            print(f"   Retrieved Diagnoses: {len(differential_diagnoses)}")
            
            if differential_diagnoses:
                top_diagnosis = differential_diagnoses[0]
                print(f"   Top Diagnosis: {top_diagnosis.get('diagnosis', 'Unknown')}")
                print(f"   Confidence: {top_diagnosis.get('confidence_score', 0):.2f}")
                print(f"   ICD-10 Code: {top_diagnosis.get('icd10_code', 'Unknown')}")
            
            # Check for comprehensive analysis components
            multi_modal_analysis = response.get('multi_modal_analysis', {})
            if multi_modal_analysis:
                print(f"   Multi-Modal Data Integration: {multi_modal_analysis.get('integration_score', 0):.2f}")
            
            explainable_ai = response.get('explainable_ai_analysis', {})
            if explainable_ai:
                print(f"   Explainable AI Transparency: {explainable_ai.get('transparency_score', 0):.2f}")
            
            confidence_analysis = response.get('confidence_analysis', {})
            if confidence_analysis:
                print(f"   Diagnostic Confidence: {confidence_analysis.get('overall_confidence', 0):.2f}")
        
        return success

    # ========== CRITICAL PRIORITY SYSTEM 3: ENHANCED EXPLAINABLE AI ==========
    
    def test_enhanced_explainable_ai_enhanced_explanation(self):
        """Test POST /api/ai/enhanced-explanation"""
        if not self.patient_id:
            print("❌ No patient ID available for enhanced explanation testing")
            return False

        explanation_data = {
            "patient_id": self.patient_id,
            "analysis_type": "comprehensive_diagnosis",
            "explanation_requirements": {
                "include_shap_analysis": True,
                "include_lime_breakdown": True,
                "include_feature_interactions": True,
                "visualization_level": "detailed"
            },
            "model_context": {
                "model_type": "regenerative_medicine_ai",
                "prediction_target": "treatment_recommendation"
            }
        }

        print("   This may take 30-45 seconds for enhanced AI explanation generation...")
        success, response = self.run_test(
            "Enhanced Explainable AI - Generate Enhanced Explanation",
            "POST",
            "ai/enhanced-explanation",
            200,
            data=explanation_data,
            timeout=60
        )
        
        if success:
            self.explanation_id = response.get('explanation_id')
            print(f"   Explanation ID: {response.get('explanation_id', 'Unknown')}")
            print(f"   SHAP Analysis: {response.get('shap_analysis', {}).get('status', 'Unknown')}")
            print(f"   LIME Breakdown: {response.get('lime_breakdown', {}).get('status', 'Unknown')}")
            print(f"   Feature Count: {len(response.get('feature_importance', []))}")
            print(f"   Transparency Score: {response.get('transparency_score', 0):.2f}")
            print(f"   Explanation Quality: {response.get('explanation_quality', 'Unknown')}")
        
        return success

    def test_enhanced_explainable_ai_explanation_retrieval(self):
        """Test GET /api/ai/enhanced-explanation/{explanation_id}"""
        explanation_id = self.explanation_id or "test_explanation_001"
        
        success, response = self.run_test(
            "Enhanced Explainable AI - Explanation Retrieval",
            "GET",
            f"ai/enhanced-explanation/{explanation_id}",
            200
        )
        
        if success:
            print(f"   Explanation ID: {response.get('explanation_id', 'Unknown')}")
            print(f"   Patient ID: {response.get('patient_id', 'Unknown')}")
            print(f"   Analysis Type: {response.get('analysis_type', 'Unknown')}")
            print(f"   Generated At: {response.get('generated_at', 'Unknown')}")
        
        return success

    def test_enhanced_explainable_ai_visual_breakdown(self):
        """Test GET /api/ai/visual-breakdown/{explanation_id}"""
        explanation_id = self.explanation_id or "test_explanation_001"
        
        success, response = self.run_test(
            "Enhanced Explainable AI - Visual Breakdown",
            "GET",
            f"ai/visual-breakdown/{explanation_id}",
            200,
            timeout=45
        )
        
        if success:
            print(f"   Explanation ID: {response.get('explanation_id', 'Unknown')}")
            print(f"   Visual Components: {len(response.get('visual_components', []))}")
            print(f"   SHAP Visualizations: {len(response.get('shap_visualizations', []))}")
            print(f"   LIME Visualizations: {len(response.get('lime_visualizations', []))}")
            print(f"   Interactive Elements: {response.get('interactive_elements', 0)}")
        
        return success

    def test_enhanced_explainable_ai_feature_interactions(self):
        """Test POST /api/ai/feature-interactions"""
        interaction_data = {
            "patient_id": self.patient_id or "test_patient_001",
            "feature_set": [
                "age", "diagnosis_confidence", "symptom_severity", 
                "medical_history", "lab_results", "imaging_findings"
            ],
            "interaction_analysis": {
                "include_pairwise_interactions": True,
                "include_higher_order_interactions": True,
                "significance_threshold": 0.05
            }
        }

        success, response = self.run_test(
            "Enhanced Explainable AI - Feature Interactions",
            "POST",
            "ai/feature-interactions",
            200,
            data=interaction_data,
            timeout=45
        )
        
        if success:
            print(f"   Analysis ID: {response.get('analysis_id', 'Unknown')}")
            print(f"   Feature Pairs Analyzed: {len(response.get('pairwise_interactions', []))}")
            print(f"   Significant Interactions: {len(response.get('significant_interactions', []))}")
            print(f"   Interaction Strength: {response.get('max_interaction_strength', 0):.3f}")
        
        return success

    def test_enhanced_explainable_ai_transparency_assessment(self):
        """Test GET /api/ai/transparency-assessment/{explanation_id}"""
        explanation_id = self.explanation_id or "test_explanation_001"
        
        success, response = self.run_test(
            "Enhanced Explainable AI - Transparency Assessment",
            "GET",
            f"ai/transparency-assessment/{explanation_id}",
            200
        )
        
        if success:
            print(f"   Explanation ID: {response.get('explanation_id', 'Unknown')}")
            print(f"   Transparency Score: {response.get('transparency_score', 0):.2f}")
            print(f"   Interpretability Level: {response.get('interpretability_level', 'Unknown')}")
            print(f"   Clinical Relevance: {response.get('clinical_relevance', 0):.2f}")
            print(f"   Explanation Fidelity: {response.get('explanation_fidelity', 0):.2f}")
        
        return success

    def run_critical_priority_tests(self):
        """Run CRITICAL PRIORITY FEATURES testing as requested in review"""
        print("🚀 Starting CRITICAL PRIORITY FEATURES Testing Suite")
        print("=" * 80)
        print("Testing three Critical Priority systems after comprehensive fixes:")
        print("1. Living Evidence Engine System (should be 100% functional)")
        print("2. Advanced Differential Diagnosis System (recently fixed)")
        print("3. Enhanced Explainable AI System (comprehensive implementation)")
        print("=" * 80)
        
        # Setup test data
        self.setup_test_data()
        
        if not self.patient_id:
            print("❌ CRITICAL ERROR: Cannot proceed without patient ID")
            return False
        
        # CRITICAL PRIORITY SYSTEM 1: Living Evidence Engine System
        print("\n⭐ CRITICAL PRIORITY SYSTEM 1: LIVING EVIDENCE ENGINE SYSTEM")
        print("-" * 60)
        print("Expected: 100% functional (4/4 endpoints working)")
        
        living_evidence_tests = [
            self.test_living_evidence_protocol_mapping,
            self.test_living_evidence_living_reviews,
            self.test_living_evidence_protocol_retrieval,
            self.test_living_evidence_alerts
        ]
        
        living_evidence_passed = 0
        for test in living_evidence_tests:
            if test():
                living_evidence_passed += 1
        
        print(f"\n📊 Living Evidence Engine Results: {living_evidence_passed}/{len(living_evidence_tests)} tests passed")
        
        # CRITICAL PRIORITY SYSTEM 2: Advanced Differential Diagnosis System
        print("\n⭐ CRITICAL PRIORITY SYSTEM 2: ADVANCED DIFFERENTIAL DIAGNOSIS SYSTEM")
        print("-" * 60)
        print("Expected: Fixed AttributeError issues, all 3 endpoints working")
        
        differential_diagnosis_tests = [
            self.test_advanced_differential_diagnosis_comprehensive,
            self.test_advanced_differential_diagnosis_engine_status,
            self.test_advanced_differential_diagnosis_retrieval
        ]
        
        differential_diagnosis_passed = 0
        for test in differential_diagnosis_tests:
            if test():
                differential_diagnosis_passed += 1
        
        print(f"\n📊 Advanced Differential Diagnosis Results: {differential_diagnosis_passed}/{len(differential_diagnosis_tests)} tests passed")
        
        # CRITICAL PRIORITY SYSTEM 3: Enhanced Explainable AI System
        print("\n⭐ CRITICAL PRIORITY SYSTEM 3: ENHANCED EXPLAINABLE AI SYSTEM")
        print("-" * 60)
        print("Expected: All 5 endpoints functional with comprehensive implementation")
        
        explainable_ai_tests = [
            self.test_enhanced_explainable_ai_enhanced_explanation,
            self.test_enhanced_explainable_ai_explanation_retrieval,
            self.test_enhanced_explainable_ai_visual_breakdown,
            self.test_enhanced_explainable_ai_feature_interactions,
            self.test_enhanced_explainable_ai_transparency_assessment
        ]
        
        explainable_ai_passed = 0
        for test in explainable_ai_tests:
            if test():
                explainable_ai_passed += 1
        
        print(f"\n📊 Enhanced Explainable AI Results: {explainable_ai_passed}/{len(explainable_ai_tests)} tests passed")
        
        # FINAL CRITICAL PRIORITY RESULTS
        total_critical_tests = len(living_evidence_tests) + len(differential_diagnosis_tests) + len(explainable_ai_tests)
        total_critical_passed = living_evidence_passed + differential_diagnosis_passed + explainable_ai_passed
        
        print("\n" + "=" * 80)
        print("🏁 CRITICAL PRIORITY FEATURES TESTING COMPLETE")
        print("=" * 80)
        print(f"⭐ Living Evidence Engine: {living_evidence_passed}/{len(living_evidence_tests)} ({'✅ WORKING' if living_evidence_passed == len(living_evidence_tests) else '❌ ISSUES'})")
        print(f"⭐ Advanced Differential Diagnosis: {differential_diagnosis_passed}/{len(differential_diagnosis_tests)} ({'✅ WORKING' if differential_diagnosis_passed == len(differential_diagnosis_tests) else '❌ ISSUES'})")
        print(f"⭐ Enhanced Explainable AI: {explainable_ai_passed}/{len(explainable_ai_tests)} ({'✅ WORKING' if explainable_ai_passed == len(explainable_ai_tests) else '❌ ISSUES'})")
        print("-" * 80)
        print(f"📊 OVERALL CRITICAL PRIORITY SUCCESS: {total_critical_passed}/{total_critical_tests} ({(total_critical_passed / total_critical_tests * 100):.1f}%)")
        
        if total_critical_passed == total_critical_tests:
            print("🎉 ALL CRITICAL PRIORITY FEATURES WORKING! Step 1 completion confirmed.")
        else:
            print("⚠️  Some Critical Priority features have issues. Check output above for details.")
        
        return total_critical_passed == total_critical_tests

if __name__ == "__main__":
    # Run Critical Priority Features testing as requested in review
    print("🎯 RUNNING CRITICAL PRIORITY FEATURES TESTING AS REQUESTED")
    print("This focuses on the three systems mentioned in the review request:")
    print("- Living Evidence Engine System")
    print("- Advanced Differential Diagnosis System") 
    print("- Enhanced Explainable AI System")
    print()
    
    tester = CriticalPriorityTester()
    success = tester.run_critical_priority_tests()
    
    print(f"\n📊 FINAL TEST RESULTS:")
    print(f"✅ Tests Passed: {tester.tests_passed}")
    print(f"❌ Tests Failed: {tester.tests_run - tester.tests_passed}")
    print(f"📊 Total Tests Run: {tester.tests_run}")
    print(f"🎯 Success Rate: {(tester.tests_passed / tester.tests_run * 100):.1f}%")
    
    if success:
        print("\n✅ SUCCESS: All Critical Priority Features are working!")
        print("Step 1 completion confirmed - ready for next phase.")
    else:
        print("\n❌ ISSUES FOUND: Some Critical Priority Features need attention.")
        print("Check the detailed output above for specific problems.")