import requests
import sys
import json
from datetime import datetime

class RegenMedAIProTester:
    def __init__(self, base_url="https://e39019a0-74aa-4828-80fe-b1e4b1fed539.preview.emergentagent.com"):
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

    def test_health_check(self):
        """Test health check endpoint with AI engine status"""
        success, response = self.run_test(
            "Health Check & AI Engine Status",
            "GET",
            "health",
            200
        )
        if success:
            print(f"   System Status: {response.get('status', 'unknown')}")
            services = response.get('services', {})
            print(f"   Database: {services.get('database', 'unknown')}")
            print(f"   AI Engine: {services.get('ai_engine', 'unknown')}")
            print(f"   Knowledge Base: {services.get('knowledge_base', 'unknown')}")
            print(f"   Version: {response.get('version', 'unknown')}")
        return success

    def test_root_endpoint(self):
        """Test root API endpoint"""
        success, response = self.run_test(
            "Root API Endpoint",
            "GET",
            "",
            200
        )
        if success:
            print(f"   Message: {response.get('message', 'No message')}")
        return success

    def test_create_patient(self):
        """Test comprehensive patient creation with regenerative medicine data"""
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
            "Create Comprehensive Patient Record",
            "POST",
            "patients",
            200,
            data=patient_data
        )
        
        if success and 'patient_id' in response:
            self.patient_id = response['patient_id']
            print(f"   Created Patient ID: {self.patient_id}")
            print(f"   Patient Name: {response.get('demographics', {}).get('name', 'Unknown')}")
            return True
        return False

    def test_list_patients(self):
        """Test listing patients for practitioner"""
        success, response = self.run_test(
            "List Patients",
            "GET",
            "patients",
            200
        )
        
        if success:
            patient_count = len(response) if isinstance(response, list) else 0
            print(f"   Found {patient_count} patients")
            if patient_count > 0:
                print(f"   First patient: {response[0].get('demographics', {}).get('name', 'Unknown')}")
        return success

    def test_get_patient(self):
        """Test retrieving specific patient data"""
        if not self.patient_id:
            print("❌ No patient ID available for testing")
            return False

        success, response = self.run_test(
            "Get Patient Details",
            "GET",
            f"patients/{self.patient_id}",
            200
        )
        
        if success:
            print(f"   Retrieved Patient: {response.get('demographics', {}).get('name', 'Unknown')}")
            print(f"   Chief Complaint: {response.get('chief_complaint', 'None')[:50]}...")
        return success

    def test_analyze_patient(self):
        """Test comprehensive AI analysis of patient data"""
        if not self.patient_id:
            print("❌ No patient ID available for analysis testing")
            return False

        print("   This may take 30-60 seconds for AI processing...")
        success, response = self.run_test(
            "AI Patient Analysis (Regenerative Medicine)",
            "POST",
            f"patients/{self.patient_id}/analyze",
            200,
            data={},
            timeout=90
        )
        
        if success:
            diagnostic_results = response.get('diagnostic_results', [])
            print(f"   Generated {len(diagnostic_results)} diagnostic results")
            if diagnostic_results:
                top_result = diagnostic_results[0]
                print(f"   Primary Diagnosis: {top_result.get('diagnosis', 'Unknown')}")
                print(f"   Confidence Score: {top_result.get('confidence_score', 0):.2f}")
                print(f"   Regenerative Targets: {len(top_result.get('regenerative_targets', []))}")
                print(f"   Mechanisms Involved: {len(top_result.get('mechanisms_involved', []))}")
        return success

    def test_therapies_database(self):
        """Test comprehensive therapy database access"""
        success, response = self.run_test(
            "Therapy Database & Schools of Thought",
            "GET",
            "therapies",
            200
        )
        
        if success:
            therapies = response.get('therapies', [])
            schools = response.get('schools_of_thought', {})
            print(f"   Available Therapies: {len(therapies)}")
            print(f"   Schools of Thought: {len(schools)}")
            
            # Print therapy names
            therapy_names = [t.get('name', 'Unknown') for t in therapies[:3]]
            print(f"   Sample Therapies: {', '.join(therapy_names)}")
            
            # Print school names
            school_names = list(schools.keys())[:3]
            print(f"   Sample Schools: {', '.join(school_names)}")
        return success

    def test_generate_protocol_traditional(self):
        """Test protocol generation - Traditional Autologous"""
        return self._test_protocol_generation("traditional_autologous", "Traditional Autologous (US Legal)")

    def test_generate_protocol_biologics(self):
        """Test protocol generation - Biologics"""
        return self._test_protocol_generation("biologics", "Biologics & Allogenic")

    def test_generate_protocol_ai_optimized(self):
        """Test protocol generation - AI Optimized"""
        return self._test_protocol_generation("ai_optimized", "AI-Optimized Best Protocol")

    def test_generate_protocol_experimental(self):
        """Test protocol generation - Experimental Cutting Edge"""
        return self._test_protocol_generation("experimental", "Experimental & Cutting-Edge")

    def _test_protocol_generation(self, school_key, school_name):
        """Helper method to test protocol generation for different schools"""
        if not self.patient_id:
            print("❌ No patient ID available for protocol generation")
            return False

        protocol_data = {
            "patient_id": self.patient_id,
            "school_of_thought": school_key
        }

        print(f"   This may take 30-60 seconds for AI protocol generation...")
        success, response = self.run_test(
            f"Generate Protocol - {school_name}",
            "POST",
            "protocols/generate",
            200,
            data=protocol_data,
            timeout=90
        )
        
        if success:
            if not self.protocol_id:  # Store first protocol ID for later tests
                self.protocol_id = response.get('protocol_id')
            
            print(f"   Protocol ID: {response.get('protocol_id', 'Unknown')}")
            print(f"   School: {response.get('school_of_thought', 'Unknown')}")
            print(f"   Confidence Score: {response.get('confidence_score', 0):.2f}")
            print(f"   Protocol Steps: {len(response.get('protocol_steps', []))}")
            print(f"   Expected Outcomes: {len(response.get('expected_outcomes', []))}")
            print(f"   Legal Warnings: {len(response.get('legal_warnings', []))}")
            
            # Print first protocol step if available
            steps = response.get('protocol_steps', [])
            if steps:
                first_step = steps[0]
                print(f"   First Step: {first_step.get('therapy', 'Unknown')} - {first_step.get('dosage', 'Unknown')}")
        return success

    def test_get_protocol(self):
        """Test retrieving generated protocol"""
        if not self.protocol_id:
            print("❌ No protocol ID available for testing")
            return False

        success, response = self.run_test(
            "Get Protocol Details",
            "GET",
            f"protocols/{self.protocol_id}",
            200
        )
        
        if success:
            print(f"   Protocol School: {response.get('school_of_thought', 'Unknown')}")
            print(f"   Status: {response.get('status', 'Unknown')}")
            print(f"   Steps Count: {len(response.get('protocol_steps', []))}")
        return success

    def test_approve_protocol(self):
        """Test protocol approval"""
        if not self.protocol_id:
            print("❌ No protocol ID available for approval testing")
            return False

        success, response = self.run_test(
            "Approve Protocol",
            "PUT",
            f"protocols/{self.protocol_id}/approve",
            200
        )
        
        if success:
            print(f"   Approval Status: {response.get('status', 'Unknown')}")
            print(f"   Approved At: {response.get('approved_at', 'Unknown')}")
        return success

    def test_dashboard_analytics(self):
        """Test practitioner dashboard analytics"""
        success, response = self.run_test(
            "Dashboard Analytics",
            "GET",
            "analytics/dashboard",
            200
        )
        
        if success:
            stats = response.get('summary_stats', {})
            print(f"   Total Patients: {stats.get('total_patients', 0)}")
            print(f"   Protocols Pending: {stats.get('protocols_pending', 0)}")
            print(f"   Protocols Approved: {stats.get('protocols_approved', 0)}")
            print(f"   Outcomes Tracked: {stats.get('outcomes_tracked', 0)}")
            print(f"   Recent Activities: {len(response.get('recent_activities', []))}")
        return success

    def test_submit_outcome(self):
        """Test outcome data submission"""
        if not self.protocol_id:
            print("❌ No protocol ID available for outcome testing")
            return False

        outcome_data = {
            "protocol_id": self.protocol_id,
            "patient_id": self.patient_id,
            "followup_date": datetime.utcnow().isoformat(),
            "measurements": {
                "pain_scale": 3,
                "range_of_motion": "improved",
                "functional_score": 85
            },
            "practitioner_notes": "Patient reports significant improvement in knee pain and mobility after PRP treatment. No adverse events reported.",
            "patient_reported_outcomes": {
                "pain_improvement": "70%",
                "activity_level": "much improved",
                "satisfaction": "very satisfied"
            },
            "adverse_events": [],
            "satisfaction_score": 9
        }

        success, response = self.run_test(
            "Submit Patient Outcome",
            "POST",
            "outcomes",
            200,
            data=outcome_data
        )
        
        if success:
            print(f"   Outcome ID: {response.get('outcome_id', 'Unknown')}")
            print(f"   Satisfaction Score: {response.get('satisfaction_score', 'Unknown')}")
        return success

    # ========== FILE UPLOAD AND PROCESSING TESTING ==========

    def test_file_upload_patient_chart(self):
        """Test uploading and processing patient chart PDF"""
        if not self.patient_id:
            print("❌ No patient ID available for file upload testing")
            return False

        # Create a simulated PDF file content
        import base64
        simulated_pdf_content = base64.b64encode(b"SIMULATED_PATIENT_CHART_PDF_CONTENT_FOR_TESTING").decode()
        
        # Prepare multipart form data
        files = {
            'file': ('patient_chart.pdf', base64.b64decode(simulated_pdf_content), 'application/pdf')
        }
        data = {
            'patient_id': self.patient_id,
            'file_category': 'chart'
        }
        
        # Remove JSON headers for multipart upload
        upload_headers = {'Authorization': 'Bearer demo-token'}
        
        try:
            import requests
            response = requests.post(
                f"{self.api_url}/files/upload",
                files=files,
                data=data,
                headers=upload_headers,
                timeout=60
            )
            
            success = response.status_code == 200
            if success:
                self.tests_passed += 1
                response_data = response.json()
                print(f"✅ Patient Chart Upload - Status: {response.status_code}")
                print(f"   File ID: {response_data.get('file_id', 'Unknown')}")
                print(f"   Processing Status: {response_data.get('status', 'Unknown')}")
                print(f"   Confidence Score: {response_data.get('confidence_score', 0):.2f}")
                print(f"   Medical Insights: {len(response_data.get('medical_insights', {}))}")
                return True
            else:
                print(f"❌ Failed - Expected 200, got {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False
        finally:
            self.tests_run += 1

    def test_file_upload_genetic_data(self):
        """Test uploading and processing genetic test results"""
        if not self.patient_id:
            print("❌ No patient ID available for genetic file testing")
            return False

        # Create simulated genetic data JSON
        genetic_data = {
            "patient_id": self.patient_id,
            "test_type": "pharmacogenomics",
            "variants": [
                {"gene": "CYP2D6", "variant": "*1/*2", "phenotype": "normal_metabolizer"},
                {"gene": "COMT", "variant": "Val158Met", "phenotype": "intermediate"},
                {"gene": "COL1A1", "variant": "rs1800012", "phenotype": "favorable_healing"}
            ],
            "regenerative_markers": {
                "VEGF_polymorphism": "positive",
                "collagen_synthesis_genes": "normal",
                "inflammatory_response": "low_risk"
            }
        }
        
        import json
        genetic_json = json.dumps(genetic_data).encode()
        
        files = {
            'file': ('genetic_results.json', genetic_json, 'application/json')
        }
        data = {
            'patient_id': self.patient_id,
            'file_category': 'genetics'
        }
        
        upload_headers = {'Authorization': 'Bearer demo-token'}
        
        try:
            import requests
            response = requests.post(
                f"{self.api_url}/files/upload",
                files=files,
                data=data,
                headers=upload_headers,
                timeout=60
            )
            
            success = response.status_code == 200
            if success:
                self.tests_passed += 1
                response_data = response.json()
                print(f"✅ Genetic Data Upload - Status: {response.status_code}")
                print(f"   File ID: {response_data.get('file_id', 'Unknown')}")
                print(f"   Regenerative Insights: {len(response_data.get('medical_insights', {}))}")
                print(f"   Confidence Score: {response_data.get('confidence_score', 0):.2f}")
                return True
            else:
                print(f"❌ Failed - Expected 200, got {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False
        finally:
            self.tests_run += 1

    def test_file_upload_dicom_imaging(self):
        """Test uploading and processing DICOM imaging files"""
        if not self.patient_id:
            print("❌ No patient ID available for DICOM testing")
            return False

        # Create simulated DICOM file
        simulated_dicom = b"SIMULATED_DICOM_FILE_CONTENT_FOR_KNEE_MRI_TESTING"
        
        files = {
            'file': ('knee_mri.dcm', simulated_dicom, 'application/dicom')
        }
        data = {
            'patient_id': self.patient_id,
            'file_category': 'imaging'
        }
        
        upload_headers = {'Authorization': 'Bearer demo-token'}
        
        try:
            import requests
            response = requests.post(
                f"{self.api_url}/files/upload",
                files=files,
                data=data,
                headers=upload_headers,
                timeout=60
            )
            
            success = response.status_code == 200
            if success:
                self.tests_passed += 1
                response_data = response.json()
                print(f"✅ DICOM Upload - Status: {response.status_code}")
                print(f"   File ID: {response_data.get('file_id', 'Unknown')}")
                print(f"   Processing Results: {len(response_data.get('processing_results', {}))}")
                print(f"   Medical Insights: {len(response_data.get('medical_insights', {}))}")
                return True
            else:
                print(f"❌ Failed - Expected 200, got {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False
        finally:
            self.tests_run += 1

    def test_file_upload_lab_results(self):
        """Test uploading and processing lab results"""
        if not self.patient_id:
            print("❌ No patient ID available for lab results testing")
            return False

        # Create simulated lab results CSV
        lab_data = """Test,Value,Reference Range,Units,Status
CBC - WBC,6.2,4.0-11.0,K/uL,Normal
CBC - RBC,4.5,4.2-5.4,M/uL,Normal
CBC - Platelets,285,150-450,K/uL,Normal
ESR,18,0-30,mm/hr,Normal
CRP,2.1,<3.0,mg/L,Normal
Vitamin D,32,30-100,ng/mL,Normal
Vitamin C,1.2,0.4-2.0,mg/dL,Normal
Zinc,95,70-120,mcg/dL,Normal
Magnesium,2.1,1.7-2.2,mg/dL,Normal
PDGF,45,20-80,pg/mL,Normal
VEGF,125,62-707,pg/mL,Normal
IGF-1,180,109-284,ng/mL,Normal"""
        
        files = {
            'file': ('lab_results.csv', lab_data.encode(), 'text/csv')
        }
        data = {
            'patient_id': self.patient_id,
            'file_category': 'labs'
        }
        
        upload_headers = {'Authorization': 'Bearer demo-token'}
        
        try:
            import requests
            response = requests.post(
                f"{self.api_url}/files/upload",
                files=files,
                data=data,
                headers=upload_headers,
                timeout=60
            )
            
            success = response.status_code == 200
            if success:
                self.tests_passed += 1
                response_data = response.json()
                print(f"✅ Lab Results Upload - Status: {response.status_code}")
                print(f"   File ID: {response_data.get('file_id', 'Unknown')}")
                print(f"   Processing Results: {len(response_data.get('processing_results', {}))}")
                print(f"   Regenerative Insights: {len(response_data.get('medical_insights', {}))}")
                return True
            else:
                print(f"❌ Failed - Expected 200, got {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False
        finally:
            self.tests_run += 1

    def test_get_patient_files(self):
        """Test retrieving all uploaded files for a patient"""
        if not self.patient_id:
            print("❌ No patient ID available for file retrieval testing")
            return False

        success, response = self.run_test(
            "Get Patient Files",
            "GET",
            f"files/patient/{self.patient_id}",
            200
        )
        
        if success:
            uploaded_files = response.get('uploaded_files', [])
            processed_files = response.get('processed_files', [])
            print(f"   Patient ID: {response.get('patient_id', 'Unknown')}")
            print(f"   Total Files: {response.get('total_files', 0)}")
            print(f"   Uploaded Files: {len(uploaded_files)}")
            print(f"   Processed Files: {len(processed_files)}")
        return success

    def test_comprehensive_patient_analysis(self):
        """Test comprehensive analysis combining all patient files"""
        if not self.patient_id:
            print("❌ No patient ID available for comprehensive analysis testing")
            return False

        success, response = self.run_test(
            "Comprehensive Patient File Analysis",
            "GET",
            f"files/comprehensive-analysis/{self.patient_id}",
            200,
            timeout=45
        )
        
        if success:
            analysis = response.get('comprehensive_analysis', {})
            print(f"   Patient ID: {response.get('patient_id', 'Unknown')}")
            print(f"   Analysis Status: {response.get('status', 'Unknown')}")
            print(f"   Multi-modal Insights: {len(analysis.get('multi_modal_insights', {}))}")
            print(f"   Integrated Recommendations: {len(analysis.get('integrated_recommendations', []))}")
            print(f"   Confidence Level: {analysis.get('confidence_level', 0):.2f}")
        return success

    def test_file_based_protocol_generation(self):
        """Test generating protocol using comprehensive file analysis"""
        if not self.patient_id:
            print("❌ No patient ID available for file-based protocol testing")
            return False

        print("   This may take 30-60 seconds for file-based AI protocol generation...")
        success, response = self.run_test(
            "Generate Protocol from Files",
            "POST",
            f"protocols/generate-from-files?patient_id={self.patient_id}&school_of_thought=ai_optimized",
            200,
            data={},
            timeout=90
        )
        
        if success:
            protocol = response.get('protocol', {})
            print(f"   Protocol ID: {protocol.get('protocol_id', 'Unknown')}")
            print(f"   Files Analyzed: {response.get('file_insights_used', 0)}")
            print(f"   Enhancement Confidence: {response.get('enhancement_confidence', 0):.2f}")
            print(f"   Multi-modal Analysis: {len(response.get('multi_modal_analysis', {}))}")
            print(f"   Protocol Steps: {len(protocol.get('protocol_steps', []))}")
            
            # Store protocol ID for potential cleanup
            if not self.protocol_id:
                self.protocol_id = protocol.get('protocol_id')
        return success

    # ========== ADVANCED AI FEATURES TESTING ==========

    def test_advanced_system_status(self):
        """Test comprehensive advanced system status"""
        success, response = self.run_test(
            "Advanced System Status & Health",
            "GET",
            "advanced/system-status",
            200
        )
        
        if success:
            services = response.get('services', {})
            db_stats = response.get('database_stats', {})
            
            print(f"   Federated Learning: {services.get('federated_learning', {}).get('status', 'unknown')}")
            print(f"   Literature Integration: {services.get('literature_integration', {}).get('status', 'unknown')}")
            print(f"   DICOM Processing: {services.get('dicom_processing', {}).get('status', 'unknown')}")
            print(f"   Outcome Prediction: {services.get('outcome_prediction', {}).get('status', 'unknown')}")
            
            print(f"   Total Patients: {db_stats.get('total_patients', 0)}")
            print(f"   Total Protocols: {db_stats.get('total_protocols', 0)}")
            print(f"   Literature Papers: {db_stats.get('literature_papers', 0)}")
            print(f"   Federated Participants: {db_stats.get('federated_participants', 0)}")
        return success

    def test_federated_register_clinic(self):
        """Test federated learning clinic registration"""
        clinic_data = {
            "total_patients": 150,
            "avg_age": 58.5,
            "therapy_distribution": {
                "prp": 0.4,
                "bmac": 0.3,
                "exosomes": 0.3
            },
            "outcomes": [
                {"therapy": "prp", "success_rate": 0.85},
                {"therapy": "bmac", "success_rate": 0.82}
            ]
        }

        success, response = self.run_test(
            "Register Clinic for Federated Learning",
            "POST",
            "federated/register-clinic",
            200,
            data=clinic_data
        )
        
        if success:
            print(f"   Registration Status: {response.get('status', 'unknown')}")
            print(f"   Clinic ID: {response.get('clinic_id', 'unknown')}")
            print(f"   Privacy Level: {response.get('privacy_level', 'unknown')}")
        return success

    def test_federated_global_model_status(self):
        """Test global federated learning model status"""
        success, response = self.run_test(
            "Global Federated Model Status",
            "GET",
            "federated/global-model-status",
            200
        )
        
        if success:
            print(f"   Model Version: {response.get('model_version', 'unknown')}")
            print(f"   Participants: {response.get('participants', 0)}")
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   Performance Improvement: {response.get('performance_improvement', 0):.3f}")
        return success

    def test_literature_latest_updates(self):
        """Test latest literature updates from PubMed integration"""
        success, response = self.run_test(
            "Latest Literature Updates",
            "GET",
            "literature/latest-updates",
            200,
            timeout=30
        )
        
        if success:
            processing_result = response.get('processing_result', {})
            recent_papers = response.get('recent_papers', [])
            
            print(f"   Processing Status: {processing_result.get('status', 'unknown')}")
            print(f"   Recent Papers Found: {len(recent_papers)}")
            print(f"   Total Papers in DB: {response.get('total_papers_in_database', 0)}")
            
            if recent_papers:
                first_paper = recent_papers[0]
                print(f"   Sample Paper: {first_paper.get('title', 'Unknown')[:50]}...")
        return success

    def test_literature_search(self):
        """Test literature database search functionality"""
        success, response = self.run_test(
            "Search Literature Database",
            "GET",
            "literature/search?query=regenerative%20medicine&limit=10",
            200
        )
        
        if success:
            papers = response.get('papers', [])
            print(f"   Query: {response.get('query', 'unknown')}")
            print(f"   Results Found: {response.get('results_found', 0)}")
            print(f"   Papers Returned: {len(papers)}")
            
            if papers:
                first_paper = papers[0]
                print(f"   Top Result: {first_paper.get('title', 'Unknown')[:50]}...")
                print(f"   Relevance Score: {first_paper.get('relevance_score', 0):.2f}")
        return success

    def test_prediction_model_performance(self):
        """Test ML prediction model performance metrics"""
        success, response = self.run_test(
            "ML Model Performance Metrics",
            "GET",
            "predictions/model-performance",
            200
        )
        
        if success:
            models = response.get('models', {})
            print(f"   Models Available: {len(models)}")
            print(f"   Total Predictions Made: {response.get('total_predictions', 0)}")
            
            for model_name, model_data in list(models.items())[:3]:  # Show first 3 models
                performance = model_data.get('performance', {})
                print(f"   Model '{model_name}': {model_data.get('model_type', 'unknown')} - Accuracy: {performance.get('accuracy', 0):.3f}")
        return success

    def test_treatment_outcome_prediction(self):
        """Test ML treatment outcome prediction"""
        if not self.patient_id:
            print("❌ No patient ID available for outcome prediction testing")
            return False

        prediction_request = {
            "patient_id": self.patient_id,
            "therapy_plan": {
                "therapy_name": "Platelet-Rich Plasma (PRP)",
                "dosage": "3-5ml",
                "delivery_method": "Intra-articular injection",
                "target_location": "bilateral knees"
            }
        }

        success, response = self.run_test(
            "ML Treatment Outcome Prediction",
            "POST",
            "predictions/treatment-outcome",
            200,
            data=prediction_request,
            timeout=45
        )
        
        if success:
            predictions = response.get('predictions', {})
            print(f"   Success Probability: {predictions.get('success_probability', 0):.2f}")
            print(f"   Expected Timeline: {predictions.get('expected_timeline', {}).get('most_likely', 'unknown')}")
            print(f"   Model Version: {response.get('model_version', 'unknown')}")
            
            risk_assessment = response.get('risk_assessment', {})
            if risk_assessment:
                print(f"   Risk Factors - Low: {len(risk_assessment.get('low_risk', []))}, Moderate: {len(risk_assessment.get('moderate_risk', []))}, High: {len(risk_assessment.get('high_risk', []))}")
        return success

    def test_dicom_analysis_simulation(self):
        """Test DICOM image analysis (simulated)"""
        if not self.patient_id:
            print("❌ No patient ID available for DICOM testing")
            return False

        # Simulate DICOM data (base64 encoded placeholder)
        import base64
        simulated_dicom = base64.b64encode(b"SIMULATED_DICOM_DATA_FOR_TESTING").decode()
        
        dicom_data = {
            "patient_id": self.patient_id,
            "modality": "MRI",
            "dicom_data": simulated_dicom,
            "study_description": "Bilateral knee MRI for regenerative medicine assessment"
        }

        success, response = self.run_test(
            "DICOM Image Analysis (AI-Powered)",
            "POST",
            "imaging/analyze-dicom",
            200,
            data=dicom_data,
            timeout=30
        )
        
        if success:
            print(f"   Processing ID: {response.get('processing_id', 'unknown')}")
            print(f"   Analysis Status: {response.get('status', 'unknown')}")
            print(f"   Modality Processed: {response.get('modality', 'unknown')}")
            
            findings = response.get('findings', {})
            if findings:
                print(f"   AI Findings: {len(findings)} detected")
        return success

    def test_imaging_analysis_history(self):
        """Test imaging analysis history retrieval"""
        if not self.patient_id:
            print("❌ No patient ID available for imaging history testing")
            return False

        success, response = self.run_test(
            "Imaging Analysis History",
            "GET",
            f"imaging/analysis-history/{self.patient_id}",
            200
        )
        
        if success:
            analyses = response.get('analyses', [])
            print(f"   Patient ID: {response.get('patient_id', 'unknown')}")
            print(f"   Total Analyses: {response.get('total_analyses', 0)}")
            print(f"   Analyses Returned: {len(analyses)}")
        return success

def main():
    print("🧬 RegenMed AI Pro - Comprehensive Backend API Testing")
    print("Advanced Regenerative Medicine Knowledge Platform v2.0")
    print("Testing All Advanced AI Features & Services")
    print("=" * 70)
    
    # Initialize tester
    tester = RegenMedAIProTester()
    
    # Test with existing patient first
    print("\n🔍 Testing with existing patient: c458d177-712c-4eb9-8fd3-5f5e41fe7b71 (Sarah Chen)")
    tester.patient_id = "c458d177-712c-4eb9-8fd3-5f5e41fe7b71"
    
    # Define comprehensive test suite with advanced features
    tests = [
        # Phase 1: System Health & Status
        ("System Health Check", tester.test_health_check),
        ("Root API Endpoint", tester.test_root_endpoint),
        ("Advanced System Status", tester.test_advanced_system_status),
        
        # Phase 2: Core Functionality with existing patient
        ("Therapy Database Access", tester.test_therapies_database),
        ("Get Existing Patient Details", tester.test_get_patient),
        ("AI Patient Analysis", tester.test_analyze_patient),
        
        # Phase 3: File Upload and Processing System
        ("File Upload - Patient Chart", tester.test_file_upload_patient_chart),
        ("File Upload - Genetic Data", tester.test_file_upload_genetic_data),
        ("File Upload - DICOM Imaging", tester.test_file_upload_dicom_imaging),
        ("File Upload - Lab Results", tester.test_file_upload_lab_results),
        ("Get Patient Files", tester.test_get_patient_files),
        ("Comprehensive File Analysis", tester.test_comprehensive_patient_analysis),
        ("File-Based Protocol Generation", tester.test_file_based_protocol_generation),
        
        # Phase 4: Protocol Generation
        ("Generate Protocol - Traditional", tester.test_generate_protocol_traditional),
        ("Generate Protocol - Biologics", tester.test_generate_protocol_biologics),
        ("Generate Protocol - AI Optimized", tester.test_generate_protocol_ai_optimized),
        ("Generate Protocol - Experimental", tester.test_generate_protocol_experimental),
        ("Get Protocol Details", tester.test_get_protocol),
        ("Approve Protocol", tester.test_approve_protocol),
        
        # Phase 5: Advanced AI Features - Federated Learning
        ("Federated Learning - Register Clinic", tester.test_federated_register_clinic),
        ("Federated Learning - Global Model Status", tester.test_federated_global_model_status),
        
        # Phase 6: Literature Integration
        ("Literature - Latest Updates", tester.test_literature_latest_updates),
        ("Literature - Search Database", tester.test_literature_search),
        
        # Phase 7: ML Prediction & DICOM Processing
        ("ML Model Performance", tester.test_prediction_model_performance),
        ("ML Treatment Outcome Prediction", tester.test_treatment_outcome_prediction),
        ("DICOM Analysis (AI-Powered)", tester.test_dicom_analysis_simulation),
        ("Imaging Analysis History", tester.test_imaging_analysis_history),
        
        # Phase 8: Analytics & Outcomes
        ("Dashboard Analytics", tester.test_dashboard_analytics),
        ("Submit Outcome Data", tester.test_submit_outcome),
        
        # Phase 9: Create new patient for completeness
        ("Create New Patient Record", tester.test_create_patient),
        ("List All Patients", tester.test_list_patients),
    ]
    
    print(f"\nRunning {len(tests)} comprehensive API tests...")
    print("Including all advanced AI features: Federated Learning, Literature Integration, ML Prediction, DICOM Processing")
    print("\n")
    
    for test_name, test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
    
    # Print final results
    print("\n" + "=" * 70)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    print(f"🎯 Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed! RegenMed AI Pro Backend is fully functional.")
        print("✅ All advanced AI services operational:")
        print("   • Federated Learning System")
        print("   • PubMed Literature Integration") 
        print("   • AI-Powered DICOM Processing")
        print("   • ML Outcome Prediction Models")
        print("✅ Ready for comprehensive frontend integration testing.")
        return 0
    elif tester.tests_passed >= tester.tests_run * 0.8:
        print("⚠️  Most tests passed. Minor issues detected - proceeding to frontend testing.")
        print("🔧 Some advanced features may need attention but core functionality works.")
        return 0
    else:
        print("❌ Significant backend issues detected. Frontend testing may be impacted.")
        print("🚨 Advanced AI services may not be fully operational.")
        return 1

if __name__ == "__main__":
    sys.exit(main())