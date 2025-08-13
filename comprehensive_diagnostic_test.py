#!/usr/bin/env python3
"""
Comprehensive Diagnostic and Protocol Generation Testing
Testing workflow with specific test patients as requested in review:
- Maria Rodriguez (ID: e40b1209-bdcb-49bd-b533-a9d6a56d9df2) - 45F with bilateral knee osteoarthritis
- David Chen (ID: dcaf95e0-8a15-4303-80fa-196ebb961af7) - 28M competitive swimmer with shoulder injury
"""

import requests
import json
import sys
from datetime import datetime
import time

class ComprehensiveDiagnosticTester:
    def __init__(self, base_url="https://medprotocol-3.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer demo-token'
        }
        
        # Test patient IDs as specified in review request
        self.maria_id = "e40b1209-bdcb-49bd-b533-a9d6a56d9df2"
        self.david_id = "dcaf95e0-8a15-4303-80fa-196ebb961af7"
        
        # Store protocol IDs for testing
        self.maria_protocol_id = None
        self.david_protocol_id = None

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

    # ========== PATIENT DATA VERIFICATION ==========
    
    def test_verify_maria_rodriguez_patient(self):
        """Verify Maria Rodriguez patient exists with proper data"""
        print(f"\n🔍 STEP 1: Patient Data Verification - Maria Rodriguez")
        print(f"   Expected ID: {self.maria_id}")
        
        success, response = self.run_test(
            "Verify Maria Rodriguez Patient Data",
            "GET",
            f"patients/{self.maria_id}",
            200
        )
        
        if success:
            demographics = response.get('demographics', {})
            print(f"   ✅ Patient Found: {demographics.get('name', 'Unknown')}")
            print(f"   Age: {demographics.get('age', 'Unknown')}")
            print(f"   Gender: {demographics.get('gender', 'Unknown')}")
            print(f"   Chief Complaint: {response.get('chief_complaint', 'Unknown')[:60]}...")
            
            # Verify it's the expected patient profile
            expected_keywords = ['knee', 'osteoarthritis', 'bilateral']
            chief_complaint = response.get('chief_complaint', '').lower()
            keywords_found = [kw for kw in expected_keywords if kw in chief_complaint]
            print(f"   Expected Keywords Found: {len(keywords_found)}/3 ({', '.join(keywords_found)})")
            
            return len(keywords_found) >= 2  # At least 2 keywords should match
        
        return False

    def test_verify_david_chen_patient(self):
        """Verify David Chen patient exists with proper data"""
        print(f"\n🔍 STEP 1: Patient Data Verification - David Chen")
        print(f"   Expected ID: {self.david_id}")
        
        success, response = self.run_test(
            "Verify David Chen Patient Data",
            "GET",
            f"patients/{self.david_id}",
            200
        )
        
        if success:
            demographics = response.get('demographics', {})
            print(f"   ✅ Patient Found: {demographics.get('name', 'Unknown')}")
            print(f"   Age: {demographics.get('age', 'Unknown')}")
            print(f"   Gender: {demographics.get('gender', 'Unknown')}")
            print(f"   Chief Complaint: {response.get('chief_complaint', 'Unknown')[:60]}...")
            
            # Verify it's the expected patient profile
            expected_keywords = ['shoulder', 'swimmer', 'injury']
            chief_complaint = response.get('chief_complaint', '').lower()
            keywords_found = [kw for kw in expected_keywords if kw in chief_complaint]
            print(f"   Expected Keywords Found: {len(keywords_found)}/3 ({', '.join(keywords_found)})")
            
            return len(keywords_found) >= 2  # At least 2 keywords should match
        
        return False

    # ========== FILE PROCESSING VERIFICATION ==========
    
    def test_verify_maria_uploaded_files(self):
        """Verify Maria's medical files were uploaded and processed"""
        print(f"\n🔍 STEP 2: File Processing Verification - Maria Rodriguez")
        
        success, response = self.run_test(
            "Verify Maria's Uploaded Files",
            "GET",
            f"patients/{self.maria_id}/files",
            200
        )
        
        if success:
            files_by_category = response.get('files_by_category', {})
            total_files = response.get('total_files', 0)
            
            print(f"   ✅ Total Files Found: {total_files}")
            print(f"   File Categories: {list(files_by_category.keys())}")
            
            # Check for expected file types for Maria
            expected_categories = ['imaging', 'labs', 'genetics']  # X-ray, lab results, genetic testing
            found_categories = []
            
            for category in expected_categories:
                if category in files_by_category and len(files_by_category[category]) > 0:
                    found_categories.append(category)
                    files_in_category = len(files_by_category[category])
                    print(f"   ✅ {category.title()}: {files_in_category} file(s)")
                    
                    # Show file details
                    for file_info in files_by_category[category][:2]:  # Show first 2 files
                        filename = file_info.get('filename', 'Unknown')
                        file_type = file_info.get('file_type', 'Unknown')
                        print(f"     - {filename} ({file_type})")
            
            print(f"   Expected Categories Found: {len(found_categories)}/3")
            return len(found_categories) >= 2  # At least 2 categories should be present
        
        return False

    def test_verify_david_uploaded_files(self):
        """Verify David's medical files were uploaded and processed"""
        print(f"\n🔍 STEP 2: File Processing Verification - David Chen")
        
        success, response = self.run_test(
            "Verify David's Uploaded Files",
            "GET",
            f"patients/{self.david_id}/files",
            200
        )
        
        if success:
            files_by_category = response.get('files_by_category', {})
            total_files = response.get('total_files', 0)
            
            print(f"   ✅ Total Files Found: {total_files}")
            print(f"   File Categories: {list(files_by_category.keys())}")
            
            # Check for expected file types for David
            expected_categories = ['imaging', 'labs', 'genetics']  # MRI, lab results, genetic testing
            found_categories = []
            
            for category in expected_categories:
                if category in files_by_category and len(files_by_category[category]) > 0:
                    found_categories.append(category)
                    files_in_category = len(files_by_category[category])
                    print(f"   ✅ {category.title()}: {files_in_category} file(s)")
                    
                    # Show file details
                    for file_info in files_by_category[category][:2]:  # Show first 2 files
                        filename = file_info.get('filename', 'Unknown')
                        file_type = file_info.get('file_type', 'Unknown')
                        print(f"     - {filename} ({file_type})")
            
            print(f"   Expected Categories Found: {len(found_categories)}/3")
            return len(found_categories) >= 2  # At least 2 categories should be present
        
        return False

    # ========== AI DIAGNOSTIC ANALYSIS ==========
    
    def test_maria_comprehensive_ai_analysis(self):
        """Run comprehensive AI analysis on Maria Rodriguez"""
        print(f"\n🔍 STEP 3: AI Diagnostic Analysis - Maria Rodriguez")
        print("   Testing multi-modal data integration and diagnostic capabilities...")
        print("   This may take 60-90 seconds for comprehensive AI analysis...")
        
        success, response = self.run_test(
            "Maria Rodriguez - Comprehensive AI Analysis",
            "POST",
            f"patients/{self.maria_id}/analyze",
            200,
            data={},
            timeout=120
        )
        
        if success:
            diagnostic_results = response.get('diagnostic_results', [])
            print(f"   ✅ Diagnostic Results Generated: {len(diagnostic_results)}")
            
            if diagnostic_results:
                primary_diagnosis = diagnostic_results[0]
                print(f"   Primary Diagnosis: {primary_diagnosis.get('diagnosis', 'Unknown')}")
                print(f"   Confidence Score: {primary_diagnosis.get('confidence_score', 0):.2f}")
                
                # Check for ICD-10 coding
                diagnosis_text = primary_diagnosis.get('diagnosis', '')
                has_icd10 = any(char.isdigit() for char in diagnosis_text) and ('M' in diagnosis_text or 'ICD' in diagnosis_text.upper())
                print(f"   ICD-10 Coding Present: {'✅' if has_icd10 else '❌'}")
                
                # Check regenerative targets
                regenerative_targets = primary_diagnosis.get('regenerative_targets', [])
                print(f"   Regenerative Targets Identified: {len(regenerative_targets)}")
                if regenerative_targets:
                    print(f"     Targets: {', '.join(regenerative_targets[:3])}")
                
                # Check mechanisms involved
                mechanisms = primary_diagnosis.get('mechanisms_involved', [])
                print(f"   Mechanisms Involved: {len(mechanisms)}")
                
                # Verify confidence score is reasonable
                confidence = primary_diagnosis.get('confidence_score', 0)
                confidence_valid = 0.0 <= confidence <= 1.0
                print(f"   Confidence Score Valid (0-1): {'✅' if confidence_valid else '❌'}")
                
                return len(diagnostic_results) > 0 and confidence_valid
        
        return False

    def test_david_comprehensive_ai_analysis(self):
        """Run comprehensive AI analysis on David Chen"""
        print(f"\n🔍 STEP 3: AI Diagnostic Analysis - David Chen")
        print("   Testing multi-modal data integration and diagnostic capabilities...")
        print("   This may take 60-90 seconds for comprehensive AI analysis...")
        
        success, response = self.run_test(
            "David Chen - Comprehensive AI Analysis",
            "POST",
            f"patients/{self.david_id}/analyze",
            200,
            data={},
            timeout=120
        )
        
        if success:
            diagnostic_results = response.get('diagnostic_results', [])
            print(f"   ✅ Diagnostic Results Generated: {len(diagnostic_results)}")
            
            if diagnostic_results:
                primary_diagnosis = diagnostic_results[0]
                print(f"   Primary Diagnosis: {primary_diagnosis.get('diagnosis', 'Unknown')}")
                print(f"   Confidence Score: {primary_diagnosis.get('confidence_score', 0):.2f}")
                
                # Check for ICD-10 coding
                diagnosis_text = primary_diagnosis.get('diagnosis', '')
                has_icd10 = any(char.isdigit() for char in diagnosis_text) and ('M' in diagnosis_text or 'ICD' in diagnosis_text.upper())
                print(f"   ICD-10 Coding Present: {'✅' if has_icd10 else '❌'}")
                
                # Check regenerative targets
                regenerative_targets = primary_diagnosis.get('regenerative_targets', [])
                print(f"   Regenerative Targets Identified: {len(regenerative_targets)}")
                if regenerative_targets:
                    print(f"     Targets: {', '.join(regenerative_targets[:3])}")
                
                # Check mechanisms involved
                mechanisms = primary_diagnosis.get('mechanisms_involved', [])
                print(f"   Mechanisms Involved: {len(mechanisms)}")
                
                # Verify confidence score is reasonable
                confidence = primary_diagnosis.get('confidence_score', 0)
                confidence_valid = 0.0 <= confidence <= 1.0
                print(f"   Confidence Score Valid (0-1): {'✅' if confidence_valid else '❌'}")
                
                return len(diagnostic_results) > 0 and confidence_valid
        
        return False

    # ========== PROTOCOL GENERATION TESTING ==========
    
    def test_maria_protocol_generation_traditional(self):
        """Generate Traditional Autologous protocol for Maria"""
        return self._test_protocol_generation(
            self.maria_id, 
            "traditional_autologous", 
            "Maria Rodriguez - Traditional Autologous Protocol",
            "maria"
        )

    def test_maria_protocol_generation_ai_optimized(self):
        """Generate AI-Optimized protocol for Maria"""
        return self._test_protocol_generation(
            self.maria_id, 
            "ai_optimized", 
            "Maria Rodriguez - AI-Optimized Protocol",
            "maria"
        )

    def test_david_protocol_generation_biologics(self):
        """Generate Biologics protocol for David"""
        return self._test_protocol_generation(
            self.david_id, 
            "biologics", 
            "David Chen - Biologics Protocol",
            "david"
        )

    def test_david_protocol_generation_experimental(self):
        """Generate Experimental protocol for David"""
        return self._test_protocol_generation(
            self.david_id, 
            "experimental", 
            "David Chen - Experimental Protocol",
            "david"
        )

    def _test_protocol_generation(self, patient_id, school_of_thought, test_name, patient_name):
        """Helper method to test protocol generation"""
        print(f"\n🔍 STEP 4: Protocol Generation Testing - {test_name}")
        print("   This may take 60-90 seconds for AI protocol generation...")
        
        protocol_data = {
            "patient_id": patient_id,
            "school_of_thought": school_of_thought
        }
        
        success, response = self.run_test(
            test_name,
            "POST",
            "protocols/generate",
            200,
            data=protocol_data,
            timeout=120
        )
        
        if success:
            protocol_id = response.get('protocol_id')
            if protocol_id:
                # Store protocol ID for later testing
                if patient_name == "maria" and not self.maria_protocol_id:
                    self.maria_protocol_id = protocol_id
                elif patient_name == "david" and not self.david_protocol_id:
                    self.david_protocol_id = protocol_id
                
                print(f"   ✅ Protocol Generated: {protocol_id}")
            
            print(f"   School of Thought: {response.get('school_of_thought', 'Unknown')}")
            print(f"   Confidence Score: {response.get('confidence_score', 0):.2f}")
            
            # Check protocol steps
            protocol_steps = response.get('protocol_steps', [])
            print(f"   Protocol Steps: {len(protocol_steps)}")
            
            if protocol_steps:
                first_step = protocol_steps[0]
                print(f"   First Step: {first_step.get('therapy', 'Unknown')}")
                print(f"   Dosage: {first_step.get('dosage', 'Unknown')}")
                print(f"   Delivery Method: {first_step.get('delivery_method', 'Unknown')}")
            
            # Check evidence-based recommendations
            supporting_evidence = response.get('supporting_evidence', [])
            print(f"   Supporting Evidence: {len(supporting_evidence)} items")
            
            # Check cost estimates
            cost_estimate = response.get('cost_estimate', 'Not provided')
            print(f"   Cost Estimate: {cost_estimate}")
            
            # Check contraindications
            contraindications = response.get('contraindications', [])
            print(f"   Contraindications: {len(contraindications)}")
            
            return len(protocol_steps) > 0 and response.get('confidence_score', 0) > 0
        
        return False

    # ========== ADVANCED FEATURES TESTING (CRITICAL PRIORITY) ==========
    
    def test_living_evidence_engine_maria(self):
        """Test Living Evidence Engine with Maria's protocol"""
        print(f"\n🔍 STEP 5: Advanced Features Testing - Living Evidence Engine (Maria)")
        
        if not self.maria_protocol_id:
            print("❌ No Maria protocol ID available - skipping Living Evidence Engine test")
            return False
        
        # Test protocol-to-evidence mapping
        mapping_data = {
            "protocol_id": self.maria_protocol_id,
            "condition": "osteoarthritis",
            "protocol_components": [
                {
                    "name": "PRP injection",
                    "therapy": "platelet rich plasma",
                    "dosage": "3-5ml intra-articular"
                }
            ],
            "evidence_requirements": {
                "minimum_evidence_level": "Level II",
                "include_recent_studies": True,
                "max_studies_per_component": 10
            }
        }
        
        success, response = self.run_test(
            "Living Evidence Engine - Protocol Evidence Mapping (Maria)",
            "POST",
            "evidence/protocol-evidence-mapping",
            200,
            data=mapping_data,
            timeout=90
        )
        
        if success:
            print(f"   ✅ Evidence Mapping Status: {response.get('status', 'Unknown')}")
            evidence_mapping = response.get('evidence_mapping', {})
            if evidence_mapping:
                print(f"   Components Mapped: {evidence_mapping.get('total_components', 0)}")
                print(f"   Evidence Quality Grade: {evidence_mapping.get('overall_evidence_quality', {}).get('grade', 'Unknown')}")
        
        return success

    def test_advanced_differential_diagnosis_david(self):
        """Test Advanced Differential Diagnosis with David's data"""
        print(f"\n🔍 STEP 5: Advanced Features Testing - Advanced Differential Diagnosis (David)")
        
        # Create comprehensive differential diagnosis request for David
        differential_data = {
            "patient_data": {
                "patient_id": self.david_id,
                "demographics": {"age": 28, "gender": "male"},
                "medical_history": ["Shoulder injury", "Athletic training"],
                "clinical_presentation": {
                    "chief_complaint": "Shoulder pain and decreased range of motion in competitive swimmer",
                    "symptom_duration": "6 months",
                    "pain_characteristics": {
                        "intensity": 6,
                        "quality": "sharp pain with overhead motion",
                        "aggravating_factors": ["swimming", "overhead activities"],
                        "relieving_factors": ["rest", "ice application"]
                    },
                    "functional_impact": {
                        "mobility_limitation": "moderate",
                        "activity_restriction": "significant for swimming",
                        "quality_of_life_impact": "high for athletic performance"
                    }
                },
                "physical_examination": {
                    "inspection": "no visible deformity",
                    "palpation": "tenderness over rotator cuff",
                    "range_of_motion": "limited overhead flexion",
                    "special_tests": ["positive impingement sign", "positive Hawkins test"]
                },
                "diagnostic_data": {
                    "imaging": {
                        "mri_findings": "rotator cuff tendinopathy with partial tear"
                    },
                    "laboratory": {
                        "inflammatory_markers": {"CRP": 1.2, "ESR": 8}
                    }
                }
            },
            "analysis_parameters": {
                "differential_count": 5,
                "confidence_threshold": 0.3,
                "include_rare_conditions": False,
                "regenerative_focus": True
            }
        }
        
        success, response = self.run_test(
            "Advanced Differential Diagnosis - Comprehensive Analysis (David)",
            "POST",
            "diagnosis/comprehensive-differential",
            200,
            data=differential_data,
            timeout=120
        )
        
        if success:
            print(f"   ✅ Analysis Status: {response.get('status', 'Unknown')}")
            comprehensive_diagnosis = response.get('comprehensive_diagnosis', {})
            if comprehensive_diagnosis:
                differential_diagnoses = comprehensive_diagnosis.get('differential_diagnoses', [])
                print(f"   Differential Diagnoses Generated: {len(differential_diagnoses)}")
                
                if differential_diagnoses:
                    primary = differential_diagnoses[0]
                    print(f"   Primary Diagnosis: {primary.get('diagnosis', 'Unknown')}")
                    print(f"   Confidence: {primary.get('confidence_score', 0):.2f}")
        
        return success

    def test_enhanced_explainable_ai_maria(self):
        """Test Enhanced Explainable AI with Maria's analysis"""
        print(f"\n🔍 STEP 5: Advanced Features Testing - Enhanced Explainable AI (Maria)")
        
        explanation_data = {
            "model_prediction": {
                "diagnosis": "Bilateral knee osteoarthritis",
                "confidence_score": 0.87,
                "severity_score": 0.72,
                "regenerative_suitability": 0.85
            },
            "patient_data": {
                "patient_id": self.maria_id,
                "demographics": {
                    "age": 45,
                    "gender": "female"
                },
                "medical_history": ["Osteoarthritis"],
                "clinical_features": {
                    "pain_level": 8,
                    "functional_limitation": "significant",
                    "inflammatory_markers": {"CRP": 2.1, "ESR": 18}
                }
            },
            "explanation_type": "comprehensive",
            "explanation_parameters": {
                "include_feature_importance": True,
                "include_counterfactuals": True,
                "include_similar_cases": True,
                "transparency_level": "high"
            }
        }
        
        success, response = self.run_test(
            "Enhanced Explainable AI - SHAP/LIME Analysis (Maria)",
            "POST",
            "ai/enhanced-explanation",
            200,
            data=explanation_data,
            timeout=120
        )
        
        if success:
            print(f"   ✅ Explanation Status: {response.get('status', 'Unknown')}")
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

    # ========== END-TO-END WORKFLOW VALIDATION ==========
    
    def test_end_to_end_workflow_maria(self):
        """Test complete patient → files → analysis → protocol → explanation workflow for Maria"""
        print(f"\n🔍 STEP 6: End-to-End Workflow Validation - Maria Rodriguez")
        print("   Testing complete workflow: Patient → Files → Analysis → Protocol → Explanation")
        
        workflow_steps = []
        
        # Step 1: Verify patient exists
        success, _ = self.run_test(
            "Workflow Step 1 - Patient Verification",
            "GET",
            f"patients/{self.maria_id}",
            200
        )
        workflow_steps.append(("Patient Verification", success))
        
        # Step 2: Verify files exist
        success, _ = self.run_test(
            "Workflow Step 2 - Files Verification",
            "GET",
            f"patients/{self.maria_id}/files",
            200
        )
        workflow_steps.append(("Files Verification", success))
        
        # Step 3: Run comprehensive analysis
        print("   Running comprehensive analysis (may take 60-90 seconds)...")
        success, analysis_response = self.run_test(
            "Workflow Step 3 - Comprehensive Analysis",
            "POST",
            f"patients/{self.maria_id}/analyze",
            200,
            data={},
            timeout=120
        )
        workflow_steps.append(("Comprehensive Analysis", success))
        
        # Step 4: Generate protocol if analysis succeeded
        if success and self.maria_protocol_id:
            success, _ = self.run_test(
                "Workflow Step 4 - Protocol Generation",
                "GET",
                f"protocols/{self.maria_protocol_id}",
                200
            )
            workflow_steps.append(("Protocol Generation", success))
        else:
            workflow_steps.append(("Protocol Generation", False))
        
        # Step 5: Generate explanation
        if analysis_response:
            explanation_data = {
                "model_prediction": {
                    "diagnosis": "Bilateral knee osteoarthritis",
                    "confidence_score": 0.87,
                    "regenerative_suitability": 0.85
                },
                "patient_data": {
                    "patient_id": self.maria_id,
                    "demographics": {"age": 45, "gender": "female"},
                    "medical_history": ["Osteoarthritis"]
                },
                "explanation_type": "comprehensive"
            }
            
            success, _ = self.run_test(
                "Workflow Step 5 - Explanation Generation",
                "POST",
                "ai/enhanced-explanation",
                200,
                data=explanation_data,
                timeout=90
            )
            workflow_steps.append(("Explanation Generation", success))
        else:
            workflow_steps.append(("Explanation Generation", False))
        
        # Summary
        print(f"\n   📊 WORKFLOW SUMMARY FOR MARIA RODRIGUEZ:")
        successful_steps = 0
        for step_name, step_success in workflow_steps:
            status = "✅ PASSED" if step_success else "❌ FAILED"
            print(f"   {status} - {step_name}")
            if step_success:
                successful_steps += 1
        
        workflow_success_rate = successful_steps / len(workflow_steps)
        print(f"   Overall Workflow Success Rate: {workflow_success_rate:.1%} ({successful_steps}/{len(workflow_steps)})")
        
        return workflow_success_rate >= 0.8  # 80% success rate required

    def test_end_to_end_workflow_david(self):
        """Test complete patient → files → analysis → protocol → explanation workflow for David"""
        print(f"\n🔍 STEP 6: End-to-End Workflow Validation - David Chen")
        print("   Testing complete workflow: Patient → Files → Analysis → Protocol → Explanation")
        
        workflow_steps = []
        
        # Step 1: Verify patient exists
        success, _ = self.run_test(
            "Workflow Step 1 - Patient Verification",
            "GET",
            f"patients/{self.david_id}",
            200
        )
        workflow_steps.append(("Patient Verification", success))
        
        # Step 2: Verify files exist
        success, _ = self.run_test(
            "Workflow Step 2 - Files Verification",
            "GET",
            f"patients/{self.david_id}/files",
            200
        )
        workflow_steps.append(("Files Verification", success))
        
        # Step 3: Run comprehensive analysis
        print("   Running comprehensive analysis (may take 60-90 seconds)...")
        success, analysis_response = self.run_test(
            "Workflow Step 3 - Comprehensive Analysis",
            "POST",
            f"patients/{self.david_id}/analyze",
            200,
            data={},
            timeout=120
        )
        workflow_steps.append(("Comprehensive Analysis", success))
        
        # Step 4: Generate protocol if analysis succeeded
        if success and self.david_protocol_id:
            success, _ = self.run_test(
                "Workflow Step 4 - Protocol Generation",
                "GET",
                f"protocols/{self.david_protocol_id}",
                200
            )
            workflow_steps.append(("Protocol Generation", success))
        else:
            workflow_steps.append(("Protocol Generation", False))
        
        # Step 5: Generate explanation
        if analysis_response:
            explanation_data = {
                "model_prediction": {
                    "diagnosis": "Rotator cuff injury",
                    "confidence_score": 0.82,
                    "regenerative_suitability": 0.88
                },
                "patient_data": {
                    "patient_id": self.david_id,
                    "demographics": {"age": 28, "gender": "male"},
                    "medical_history": ["Shoulder injury"]
                },
                "explanation_type": "comprehensive"
            }
            
            success, _ = self.run_test(
                "Workflow Step 5 - Explanation Generation",
                "POST",
                "ai/enhanced-explanation",
                200,
                data=explanation_data,
                timeout=90
            )
            workflow_steps.append(("Explanation Generation", success))
        else:
            workflow_steps.append(("Explanation Generation", False))
        
        # Summary
        print(f"\n   📊 WORKFLOW SUMMARY FOR DAVID CHEN:")
        successful_steps = 0
        for step_name, step_success in workflow_steps:
            status = "✅ PASSED" if step_success else "❌ FAILED"
            print(f"   {status} - {step_name}")
            if step_success:
                successful_steps += 1
        
        workflow_success_rate = successful_steps / len(workflow_steps)
        print(f"   Overall Workflow Success Rate: {workflow_success_rate:.1%} ({successful_steps}/{len(workflow_steps)})")
        
        return workflow_success_rate >= 0.8  # 80% success rate required

    # ========== MAIN TEST EXECUTION ==========
    
    def run_comprehensive_diagnostic_tests(self):
        """Run all comprehensive diagnostic and protocol generation tests"""
        print("=" * 80)
        print("🧬 COMPREHENSIVE DIAGNOSTIC AND PROTOCOL GENERATION TESTING")
        print("=" * 80)
        print(f"Testing with specific patients as requested:")
        print(f"• Maria Rodriguez (ID: {self.maria_id}) - 45F with bilateral knee osteoarthritis")
        print(f"• David Chen (ID: {self.david_id}) - 28M competitive swimmer with shoulder injury")
        print("=" * 80)
        
        # Test sequence as requested in review
        test_methods = [
            # Step 1: Patient Data Verification
            self.test_verify_maria_rodriguez_patient,
            self.test_verify_david_chen_patient,
            
            # Step 2: File Processing Verification
            self.test_verify_maria_uploaded_files,
            self.test_verify_david_uploaded_files,
            
            # Step 3: AI Diagnostic Analysis
            self.test_maria_comprehensive_ai_analysis,
            self.test_david_comprehensive_ai_analysis,
            
            # Step 4: Protocol Generation Testing
            self.test_maria_protocol_generation_traditional,
            self.test_maria_protocol_generation_ai_optimized,
            self.test_david_protocol_generation_biologics,
            self.test_david_protocol_generation_experimental,
            
            # Step 5: Advanced Features Testing (Critical Priority)
            self.test_living_evidence_engine_maria,
            self.test_advanced_differential_diagnosis_david,
            self.test_enhanced_explainable_ai_maria,
            
            # Step 6: End-to-End Workflow Validation
            self.test_end_to_end_workflow_maria,
            self.test_end_to_end_workflow_david,
        ]
        
        print(f"\n🚀 Starting {len(test_methods)} comprehensive tests...")
        start_time = time.time()
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                print(f"❌ Test {test_method.__name__} failed with exception: {str(e)}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Final summary
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TESTING SUMMARY")
        print("=" * 80)
        print(f"Total Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        print(f"Total Duration: {duration:.1f} seconds")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED - Comprehensive diagnostic workflow is fully functional!")
        elif self.tests_passed / self.tests_run >= 0.8:
            print("✅ MOSTLY SUCCESSFUL - Comprehensive diagnostic workflow is largely functional")
        else:
            print("⚠️  ISSUES DETECTED - Some components of the diagnostic workflow need attention")
        
        print("=" * 80)
        
        return self.tests_passed, self.tests_run

if __name__ == "__main__":
    tester = ComprehensiveDiagnosticTester()
    passed, total = tester.run_comprehensive_diagnostic_tests()
    
    # Exit with appropriate code
    if passed == total:
        sys.exit(0)  # All tests passed
    elif passed / total >= 0.8:
        sys.exit(1)  # Mostly successful but some issues
    else:
        sys.exit(2)  # Significant issues detected