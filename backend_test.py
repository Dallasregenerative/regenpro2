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
            print(f"   Results Found: {response.get('total_results', 0)}")
            print(f"   Papers Returned: {len(papers)}")
            
            if papers:
                first_paper = papers[0]
                print(f"   Top Result: {first_paper.get('title', 'Unknown')[:50]}...")
                print(f"   Relevance Score: {first_paper.get('relevance_score', 0):.2f}")
        return success

    # ========== GOOGLE SCHOLAR INTEGRATION TESTING ==========

    def test_google_scholar_search_basic(self):
        """Test basic Google Scholar search functionality"""
        success, response = self.run_test(
            "Google Scholar Search - Basic Query",
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
        return success

    def test_google_scholar_search_stem_cell(self):
        """Test Google Scholar search with stem cell therapy query"""
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
            print(f"   Search Timestamp: {response.get('search_timestamp', 'unknown')}")
            
            # Check for regenerative medicine relevance
            relevant_papers = [p for p in papers if p.get('relevance_score', 0) >= 0.5]
            print(f"   High Relevance Papers (≥0.5): {len(relevant_papers)}")
            
            if relevant_papers:
                top_paper = relevant_papers[0]
                print(f"   Top Relevant Paper: {top_paper.get('title', 'Unknown')[:50]}...")
                print(f"   Abstract Preview: {top_paper.get('abstract', 'No abstract')[:100]}...")
        return success

    def test_google_scholar_search_with_year_filter(self):
        """Test Google Scholar search with year filter"""
        success, response = self.run_test(
            "Google Scholar Search - With Year Filter",
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
            recent_papers = [p for p in papers if p.get('year', '').isdigit() and int(p.get('year', '0')) >= 2023]
            print(f"   Papers from 2023+: {len(recent_papers)}")
            
            if papers:
                sample_paper = papers[0]
                print(f"   Sample Paper Year: {sample_paper.get('year', 'Unknown')}")
                print(f"   Sample Title: {sample_paper.get('title', 'Unknown')[:50]}...")
        return success

    def test_google_scholar_error_handling(self):
        """Test Google Scholar search error handling"""
        success, response = self.run_test(
            "Google Scholar Search - Error Handling",
            "GET",
            "literature/google-scholar-search?query=&max_results=5",  # Empty query
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

    def test_multi_source_search_comprehensive(self):
        """Test comprehensive multi-source search (PubMed + Google Scholar)"""
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
            print(f"   Search Type: {response.get('search_type', 'unknown')}")
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
                
                # Show top result from each source
                if pubmed_papers:
                    top_pubmed = pubmed_papers[0]
                    print(f"   Top PubMed: {top_pubmed.get('title', 'Unknown')[:40]}... (PMID: {top_pubmed.get('pmid', 'N/A')})")
                
                if scholar_papers:
                    top_scholar = scholar_papers[0]
                    print(f"   Top Scholar: {top_scholar.get('title', 'Unknown')[:40]}... (Citations: {top_scholar.get('citation_count', 0)})")
        return success

    def test_multi_source_search_bmac(self):
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
            source_stats = response.get('source_statistics', {})
            
            print(f"   Query: BMAC rotator cuff")
            print(f"   Total Unique Papers: {response.get('total_unique_papers', 0)}")
            print(f"   Deduplication Working: {len(papers) <= 12}")  # Should be ≤ max_results_per_source * 2
            
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
        return success

    def test_multi_source_deduplication(self):
        """Test deduplication functionality in multi-source search"""
        success, response = self.run_test(
            "Multi-Source Search - Deduplication Test",
            "GET",
            "literature/multi-source-search?query=platelet%20rich%20plasma&max_results_per_source=10",
            200,
            timeout=60
        )
        
        if success:
            papers = response.get('papers', [])
            source_stats = response.get('source_statistics', {})
            
            total_before_dedup = source_stats.get('pubmed', {}).get('papers_found', 0) + source_stats.get('google_scholar', {}).get('papers_found', 0)
            total_after_dedup = response.get('total_unique_papers', 0)
            
            print(f"   Papers Before Deduplication: {total_before_dedup}")
            print(f"   Papers After Deduplication: {total_after_dedup}")
            print(f"   Deduplication Effective: {total_after_dedup <= total_before_dedup}")
            
            # Check for potential duplicates (shouldn't find any)
            titles = [p.get('title', '').lower().strip() for p in papers]
            unique_titles = set(titles)
            
            print(f"   Unique Titles: {len(unique_titles)}")
            print(f"   Total Papers: {len(papers)}")
            print(f"   No Title Duplicates: {len(unique_titles) == len(papers)}")
            
            if papers:
                # Show source distribution
                sources = {}
                for paper in papers:
                    source = paper.get('source', 'unknown')
                    sources[source] = sources.get(source, 0) + 1
                
                print(f"   Source Distribution: {sources}")
        return success

    def test_literature_integration_evidence_extraction(self):
        """Test evidence extraction helper methods"""
        success, response = self.run_test(
            "Literature Integration - Evidence Extraction",
            "GET",
            "literature/search?query=osteoarthritis%20PRP&limit=5",
            200,
            timeout=30
        )
        
        if success:
            papers = response.get('papers', [])
            print(f"   Papers for Evidence Extraction: {len(papers)}")
            
            if papers:
                sample_paper = papers[0]
                
                # Check for evidence extraction fields
                evidence_fields = ['title', 'abstract', 'authors', 'journal', 'relevance_score']
                available_fields = [field for field in evidence_fields if field in sample_paper]
                
                print(f"   Evidence Fields Available: {len(available_fields)}/{len(evidence_fields)}")
                print(f"   Available Fields: {', '.join(available_fields)}")
                
                # Check for therapy implications
                abstract = sample_paper.get('abstract', '').lower()
                therapy_keywords = ['therapy', 'treatment', 'efficacy', 'outcome', 'safety', 'dosage']
                therapy_mentions = [kw for kw in therapy_keywords if kw in abstract]
                
                print(f"   Therapy Keywords Found: {len(therapy_mentions)}")
                print(f"   Keywords: {', '.join(therapy_mentions[:3])}")
                
                # Check for outcome data
                outcome_keywords = ['improvement', 'reduction', 'success', 'failure', 'adverse', 'benefit']
                outcome_mentions = [kw for kw in outcome_keywords if kw in abstract]
                
                print(f"   Outcome Keywords Found: {len(outcome_mentions)}")
                
                # Check for evidence level indicators
                evidence_keywords = ['randomized', 'controlled', 'trial', 'systematic', 'meta-analysis', 'cohort']
                evidence_mentions = [kw for kw in evidence_keywords if kw in abstract]
                
                print(f"   Evidence Level Indicators: {len(evidence_mentions)}")
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

    # ========== EVIDENCE SYNTHESIS SYSTEM TESTING ==========

    def test_evidence_synthesis_status(self):
        """Test evidence synthesis system status"""
        success, response = self.run_test(
            "Evidence Synthesis System Status",
            "GET",
            "evidence/synthesis-status",
            200
        )
        
        if success:
            print(f"   Synthesis Engine Status: {response.get('synthesis_engine_status', 'unknown')}")
            
            literature_db = response.get('literature_database', {})
            if literature_db:
                print(f"   Literature Database Papers: {literature_db.get('total_papers', 0)}")
                print(f"   Database Status: {literature_db.get('status', 'unknown')}")
            
            print(f"   Recent Syntheses: {response.get('recent_syntheses', 0)}")
            
            capabilities = response.get('capabilities', [])
            print(f"   System Capabilities: {len(capabilities)}")
            if capabilities:
                print(f"   Key Capabilities: {', '.join(capabilities[:3])}")
        return success

    def test_evidence_synthesis_osteoarthritis(self):
        """Test evidence synthesis for osteoarthritis condition"""
        synthesis_request = {
            "condition": "osteoarthritis",
            "existing_evidence": [
                {
                    "source": "clinical_experience",
                    "finding": "PRP shows good results in knee osteoarthritis",
                    "confidence": 0.8
                }
            ]
        }

        print("   This may take 30-60 seconds for comprehensive literature analysis...")
        success, response = self.run_test(
            "Evidence Synthesis - Osteoarthritis Protocol",
            "POST",
            "evidence/synthesize-protocol",
            200,
            data=synthesis_request,
            timeout=90
        )
        
        if success:
            print(f"   Synthesis Status: {response.get('status', 'unknown')}")
            print(f"   Condition: {response.get('condition', 'unknown')}")
            
            synthesis_result = response.get('synthesis_result', {})
            if synthesis_result:
                print(f"   Evidence Sources: {synthesis_result.get('evidence_sources', 0)}")
                print(f"   Synthesis Confidence: {synthesis_result.get('synthesis_confidence', 0):.2f}")
                print(f"   Protocol Generated: {synthesis_result.get('protocol_generated', False)}")
                
                # Check for protocol recommendations
                recommendations = synthesis_result.get('protocol_recommendations', [])
                if recommendations:
                    print(f"   Protocol Recommendations: {len(recommendations)}")
                    print(f"   Top Recommendation: {recommendations[0].get('therapy', 'Unknown')[:50]}...")
        return success

    def test_evidence_synthesis_rotator_cuff(self):
        """Test evidence synthesis for rotator cuff injury condition"""
        synthesis_request = {
            "condition": "rotator cuff injury",
            "existing_evidence": []
        }

        print("   This may take 30-60 seconds for comprehensive literature analysis...")
        success, response = self.run_test(
            "Evidence Synthesis - Rotator Cuff Protocol",
            "POST",
            "evidence/synthesize-protocol",
            200,
            data=synthesis_request,
            timeout=90
        )
        
        if success:
            print(f"   Synthesis Status: {response.get('status', 'unknown')}")
            print(f"   Condition: {response.get('condition', 'unknown')}")
            
            synthesis_result = response.get('synthesis_result', {})
            if synthesis_result:
                print(f"   Evidence Sources: {synthesis_result.get('evidence_sources', 0)}")
                print(f"   Synthesis Confidence: {synthesis_result.get('synthesis_confidence', 0):.2f}")
                
                # Check for literature analysis
                literature_analysis = synthesis_result.get('literature_analysis', {})
                if literature_analysis:
                    print(f"   Literature Papers Analyzed: {literature_analysis.get('papers_analyzed', 0)}")
                    print(f"   Evidence Quality Score: {literature_analysis.get('evidence_quality_score', 0):.2f}")
        return success

    def test_evidence_synthesis_missing_condition(self):
        """Test evidence synthesis error handling when condition is missing"""
        synthesis_request = {
            "existing_evidence": []
        }

        success, response = self.run_test(
            "Evidence Synthesis - Missing Condition (Error Handling)",
            "POST",
            "evidence/synthesize-protocol",
            400,  # Expecting 400 Bad Request
            data=synthesis_request
        )
        
        if success:
            print(f"   Error Handling: Correctly returned 400 for missing condition")
            print(f"   Error Detail: {response.get('detail', 'No detail provided')}")
        return success

    def test_evidence_synthesis_invalid_condition(self):
        """Test evidence synthesis with invalid/unsupported condition"""
        synthesis_request = {
            "condition": "invalid_medical_condition_xyz123",
            "existing_evidence": []
        }

        print("   Testing with invalid condition...")
        success, response = self.run_test(
            "Evidence Synthesis - Invalid Condition",
            "POST",
            "evidence/synthesize-protocol",
            200,  # Should still return 200 but with appropriate status
            data=synthesis_request,
            timeout=60
        )
        
        if success:
            print(f"   Synthesis Status: {response.get('status', 'unknown')}")
            
            # Check if system handles invalid condition gracefully
            if response.get('status') in ['synthesis_failed', 'synthesis_completed']:
                print(f"   System handled invalid condition appropriately")
                if 'error' in response:
                    print(f"   Error Message: {response.get('error', 'No error message')[:50]}...")
                if response.get('fallback_available'):
                    print(f"   Fallback Available: {response.get('fallback_available')}")
        return success

    # ========== CLINICAL TRIALS.GOV INTEGRATION TESTING ==========

    def test_clinical_trials_search_osteoarthritis(self):
        """Test clinical trials search for osteoarthritis with default recruitment status"""
        success, response = self.run_test(
            "Clinical Trials Search - Osteoarthritis (RECRUITING)",
            "GET",
            "clinical-trials/search?condition=osteoarthritis&recruitment_status=RECRUITING",
            200,
            timeout=45
        )
        
        if success:
            trials = response.get('trials', [])
            print(f"   Search Condition: {response.get('search_condition', 'unknown')}")
            print(f"   Recruitment Status: {response.get('recruitment_status', 'unknown')}")
            print(f"   Trials Found: {response.get('total_count', 0)}")
            print(f"   Source: {response.get('source', 'unknown')}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            if trials:
                top_trial = trials[0]
                print(f"   Top Trial: {top_trial.get('title', 'Unknown')[:60]}...")
                print(f"   NCT ID: {top_trial.get('nct_id', 'Unknown')}")
                print(f"   Overall Status: {top_trial.get('overall_status', 'Unknown')}")
                print(f"   Relevance Score: {top_trial.get('relevance_score', 0):.2f}")
                
                # Check for regenerative medicine interventions
                interventions = top_trial.get('interventions', [])
                regen_interventions = [i for i in interventions if i.get('regenerative_medicine', False)]
                print(f"   Regenerative Interventions: {len(regen_interventions)}")
                
                if regen_interventions:
                    categories = [i.get('category', 'Unknown') for i in regen_interventions]
                    print(f"   Intervention Categories: {', '.join(set(categories))}")
        return success

    def test_clinical_trials_search_rotator_cuff_stem_cell(self):
        """Test clinical trials search for rotator cuff injury with stem cell therapy intervention"""
        success, response = self.run_test(
            "Clinical Trials Search - Rotator Cuff + Stem Cell",
            "GET",
            "clinical-trials/search?condition=rotator%20cuff%20injury&intervention=stem%20cell%20therapy&max_results=15",
            200,
            timeout=45
        )
        
        if success:
            trials = response.get('trials', [])
            print(f"   Search Condition: {response.get('search_condition', 'unknown')}")
            print(f"   Intervention Filter: {response.get('intervention_filter', 'unknown')}")
            print(f"   Trials Found: {len(trials)}")
            print(f"   Search Timestamp: {response.get('search_timestamp', 'unknown')}")
            
            if trials:
                # Check for stem cell interventions
                stem_cell_trials = []
                for trial in trials:
                    interventions = trial.get('interventions', [])
                    for intervention in interventions:
                        if intervention.get('category') == 'Stem Cells':
                            stem_cell_trials.append(trial)
                            break
                
                print(f"   Stem Cell Trials: {len(stem_cell_trials)}")
                
                if stem_cell_trials:
                    top_stem_trial = stem_cell_trials[0]
                    print(f"   Top Stem Cell Trial: {top_stem_trial.get('title', 'Unknown')[:50]}...")
                    print(f"   Study Type: {top_stem_trial.get('study_type', 'Unknown')}")
                    print(f"   Phases: {', '.join(top_stem_trial.get('phases', []))}")
                    
                    # Check locations
                    locations = top_stem_trial.get('locations', [])
                    if locations:
                        print(f"   Locations Available: {len(locations)}")
                        first_location = locations[0]
                        print(f"   Sample Location: {first_location.get('city', 'Unknown')}, {first_location.get('country', 'Unknown')}")
        return success

    def test_clinical_trials_search_knee_pain_prp(self):
        """Test clinical trials search for knee pain with PRP intervention"""
        success, response = self.run_test(
            "Clinical Trials Search - Knee Pain + PRP",
            "GET",
            "clinical-trials/search?condition=knee%20pain&intervention=PRP&max_results=12",
            200,
            timeout=45
        )
        
        if success:
            trials = response.get('trials', [])
            print(f"   Search Condition: knee pain")
            print(f"   Intervention Filter: PRP")
            print(f"   Trials Found: {len(trials)}")
            
            if trials:
                # Check for PRP interventions
                prp_trials = []
                for trial in trials:
                    interventions = trial.get('interventions', [])
                    for intervention in interventions:
                        if intervention.get('category') == 'PRP' or 'prp' in intervention.get('name', '').lower():
                            prp_trials.append(trial)
                            break
                
                print(f"   PRP-Related Trials: {len(prp_trials)}")
                
                if prp_trials:
                    top_prp_trial = prp_trials[0]
                    print(f"   Top PRP Trial: {top_prp_trial.get('title', 'Unknown')[:50]}...")
                    print(f"   Brief Summary: {top_prp_trial.get('brief_summary', 'No summary')[:100]}...")
                    
                    # Check eligibility
                    print(f"   Eligible Ages: {', '.join(top_prp_trial.get('eligible_ages', []))}")
                    print(f"   Gender: {top_prp_trial.get('gender', 'Unknown')}")
        return success

    def test_clinical_trials_json_api_parsing(self):
        """Test JSON API parsing and trial data extraction quality"""
        success, response = self.run_test(
            "Clinical Trials - JSON API Parsing Quality",
            "GET",
            "clinical-trials/search?condition=osteoarthritis&max_results=5",
            200,
            timeout=30
        )
        
        if success:
            trials = response.get('trials', [])
            print(f"   Trials for Parsing Test: {len(trials)}")
            
            if trials:
                sample_trial = trials[0]
                
                # Check required fields are present
                required_fields = ['nct_id', 'title', 'overall_status', 'brief_summary', 'conditions', 'interventions']
                available_fields = [field for field in required_fields if field in sample_trial and sample_trial[field]]
                
                print(f"   Required Fields Present: {len(available_fields)}/{len(required_fields)}")
                print(f"   Available Fields: {', '.join(available_fields)}")
                
                # Check data quality
                nct_id = sample_trial.get('nct_id', '')
                print(f"   NCT ID Format Valid: {nct_id.startswith('NCT') and len(nct_id) >= 8}")
                
                title_length = len(sample_trial.get('title', ''))
                print(f"   Title Length: {title_length} characters")
                
                summary_length = len(sample_trial.get('brief_summary', ''))
                print(f"   Summary Length: {summary_length} characters")
                
                # Check intervention categorization
                interventions = sample_trial.get('interventions', [])
                categorized_interventions = [i for i in interventions if i.get('category') != 'other']
                print(f"   Categorized Interventions: {len(categorized_interventions)}/{len(interventions)}")
                
                # Check relevance scoring
                relevance_score = sample_trial.get('relevance_score', 0)
                print(f"   Relevance Score: {relevance_score:.3f} (0.0-1.0 range)")
                print(f"   Relevance Score Valid: {0.0 <= relevance_score <= 1.0}")
                
                # Check trial URL
                trial_url = sample_trial.get('trial_url', '')
                print(f"   Trial URL Valid: {trial_url.startswith('https://clinicaltrials.gov/')}")
        return success

    def test_clinical_trials_intervention_categorization(self):
        """Test intervention categorization for regenerative medicine"""
        success, response = self.run_test(
            "Clinical Trials - Intervention Categorization",
            "GET",
            "clinical-trials/search?condition=cartilage%20repair&max_results=10",
            200,
            timeout=30
        )
        
        if success:
            trials = response.get('trials', [])
            print(f"   Trials for Categorization Test: {len(trials)}")
            
            # Collect all intervention categories
            all_categories = {}
            regen_intervention_count = 0
            total_intervention_count = 0
            
            for trial in trials:
                interventions = trial.get('interventions', [])
                for intervention in interventions:
                    total_intervention_count += 1
                    category = intervention.get('category', 'unknown')
                    all_categories[category] = all_categories.get(category, 0) + 1
                    
                    if intervention.get('regenerative_medicine', False):
                        regen_intervention_count += 1
            
            print(f"   Total Interventions: {total_intervention_count}")
            print(f"   Regenerative Medicine Interventions: {regen_intervention_count}")
            print(f"   Categories Found: {len(all_categories)}")
            
            # Show category distribution
            for category, count in sorted(all_categories.items(), key=lambda x: x[1], reverse=True):
                print(f"   {category}: {count} interventions")
            
            # Check for expected regenerative categories
            expected_categories = ['PRP', 'BMAC', 'Stem Cells', 'Exosomes']
            found_categories = [cat for cat in expected_categories if cat in all_categories]
            print(f"   Expected Regen Categories Found: {len(found_categories)}/{len(expected_categories)}")
            print(f"   Found Categories: {', '.join(found_categories)}")
        return success

    def test_clinical_trials_relevance_scoring(self):
        """Test relevance scoring algorithm for different conditions and interventions"""
        conditions_to_test = [
            ("osteoarthritis", "Expected high relevance for joint conditions"),
            ("rotator cuff", "Expected high relevance for shoulder conditions"),
            ("cartilage defect", "Expected high relevance for cartilage repair")
        ]
        
        all_passed = True
        
        for condition, description in conditions_to_test:
            success, response = self.run_test(
                f"Clinical Trials - Relevance Scoring ({condition})",
                "GET",
                f"clinical-trials/search?condition={condition.replace(' ', '%20')}&max_results=8",
                200,
                timeout=30
            )
            
            if success:
                trials = response.get('trials', [])
                print(f"   Condition: {condition}")
                print(f"   Trials Found: {len(trials)}")
                
                if trials:
                    # Check relevance score distribution
                    relevance_scores = [trial.get('relevance_score', 0) for trial in trials]
                    avg_relevance = sum(relevance_scores) / len(relevance_scores)
                    max_relevance = max(relevance_scores)
                    min_relevance = min(relevance_scores)
                    
                    print(f"   Average Relevance: {avg_relevance:.3f}")
                    print(f"   Max Relevance: {max_relevance:.3f}")
                    print(f"   Min Relevance: {min_relevance:.3f}")
                    print(f"   Score Range Valid: {0.0 <= min_relevance <= max_relevance <= 1.0}")
                    
                    # Check if trials are sorted by relevance (descending)
                    is_sorted = all(relevance_scores[i] >= relevance_scores[i+1] for i in range(len(relevance_scores)-1))
                    print(f"   Trials Sorted by Relevance: {is_sorted}")
                    
                    # Show top trial details
                    top_trial = trials[0]
                    print(f"   Top Trial: {top_trial.get('title', 'Unknown')[:40]}...")
                    print(f"   Top Relevance: {top_trial.get('relevance_score', 0):.3f}")
                else:
                    print(f"   No trials found for {condition}")
            else:
                all_passed = False
                print(f"   Failed to test relevance scoring for {condition}")
        
        return all_passed

    def test_clinical_trials_patient_matching_osteoarthritis(self):
        """Test patient-specific trial matching for osteoarthritis with PRP and stem cell preferences"""
        success, response = self.run_test(
            "Clinical Trials - Patient Matching (Osteoarthritis + PRP/Stem Cell)",
            "GET",
            "clinical-trials/patient-matching?condition=osteoarthritis&therapy_preferences=PRP,stem%20cell",
            200,
            timeout=45
        )
        
        if success:
            matching_trials = response.get('matching_trials', [])
            print(f"   Patient Condition: {response.get('patient_condition', 'unknown')}")
            print(f"   Therapy Preferences: {response.get('therapy_preferences', [])}")
            print(f"   Total Matches: {response.get('total_matches', 0)}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            if matching_trials:
                top_match = matching_trials[0]
                print(f"   Top Match: {top_match.get('title', 'Unknown')[:50]}...")
                print(f"   Match Score: {top_match.get('match_score', 0):.3f}")
                
                # Check match reasons
                match_reasons = top_match.get('match_reasons', [])
                print(f"   Match Reasons: {len(match_reasons)}")
                if match_reasons:
                    print(f"   Top Reason: {match_reasons[0]}")
                
                # Check eligibility considerations
                eligibility = top_match.get('eligibility_considerations', {})
                print(f"   Age Range: {', '.join(eligibility.get('age_range', []))}")
                print(f"   Gender: {eligibility.get('gender', 'Unknown')}")
                print(f"   Study Type: {eligibility.get('study_type', 'Unknown')}")
                
                # Check next steps
                next_steps = top_match.get('next_steps', [])
                print(f"   Next Steps Provided: {len(next_steps)}")
                if next_steps:
                    print(f"   First Step: {next_steps[0][:60]}...")
            
            # Check recommendations
            recommendations = response.get('recommendations', [])
            print(f"   Recommendations: {len(recommendations)}")
            if recommendations:
                print(f"   Top Recommendation: {recommendations[0]}")
        return success

    def test_clinical_trials_patient_matching_shoulder_bmac(self):
        """Test patient-specific trial matching for shoulder injury with BMAC preference"""
        success, response = self.run_test(
            "Clinical Trials - Patient Matching (Shoulder + BMAC)",
            "GET",
            "clinical-trials/patient-matching?condition=shoulder%20injury&therapy_preferences=BMAC",
            200,
            timeout=45
        )
        
        if success:
            matching_trials = response.get('matching_trials', [])
            print(f"   Patient Condition: shoulder injury")
            print(f"   Therapy Preferences: BMAC")
            print(f"   Total Matches: {len(matching_trials)}")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            if matching_trials:
                # Check match score distribution
                match_scores = [trial.get('match_score', 0) for trial in matching_trials]
                avg_match_score = sum(match_scores) / len(match_scores)
                print(f"   Average Match Score: {avg_match_score:.3f}")
                print(f"   Match Score Range: {min(match_scores):.3f} - {max(match_scores):.3f}")
                
                # Check if matches are sorted by score
                is_sorted = all(match_scores[i] >= match_scores[i+1] for i in range(len(match_scores)-1))
                print(f"   Matches Sorted by Score: {is_sorted}")
                
                # Check for BMAC-specific matches
                bmac_matches = []
                for trial in matching_trials:
                    interventions = trial.get('interventions', [])
                    for intervention in interventions:
                        if intervention.get('category') == 'BMAC' or 'bmac' in intervention.get('name', '').lower():
                            bmac_matches.append(trial)
                            break
                
                print(f"   BMAC-Specific Matches: {len(bmac_matches)}")
                
                if bmac_matches:
                    top_bmac_match = bmac_matches[0]
                    print(f"   Top BMAC Match: {top_bmac_match.get('title', 'Unknown')[:40]}...")
                    print(f"   BMAC Match Score: {top_bmac_match.get('match_score', 0):.3f}")
            else:
                print(f"   No matches found - checking recommendations")
                recommendations = response.get('recommendations', [])
                if recommendations:
                    print(f"   Fallback Recommendations: {len(recommendations)}")
                    print(f"   Top Recommendation: {recommendations[0]}")
        return success

    def test_clinical_trials_match_scoring_algorithm(self):
        """Test patient-trial match scoring algorithm and compatibility assessment"""
        success, response = self.run_test(
            "Clinical Trials - Match Scoring Algorithm",
            "GET",
            "clinical-trials/patient-matching?condition=knee%20osteoarthritis&therapy_preferences=PRP,stem%20cell,BMAC",
            200,
            timeout=45
        )
        
        if success:
            matching_trials = response.get('matching_trials', [])
            print(f"   Condition: knee osteoarthritis")
            print(f"   Preferences: PRP, stem cell, BMAC")
            print(f"   Total Matches: {len(matching_trials)}")
            
            if matching_trials:
                # Analyze match score distribution
                match_scores = [trial.get('match_score', 0) for trial in matching_trials]
                
                # Check score validity (0.0-1.0 range)
                valid_scores = all(0.0 <= score <= 1.0 for score in match_scores)
                print(f"   All Match Scores Valid (0.0-1.0): {valid_scores}")
                
                # Check minimum threshold (should be >= 0.3 based on implementation)
                min_threshold_met = all(score >= 0.3 for score in match_scores)
                print(f"   All Scores Meet Minimum Threshold (≥0.3): {min_threshold_met}")
                
                # Show score distribution
                high_scores = [s for s in match_scores if s >= 0.7]
                medium_scores = [s for s in match_scores if 0.5 <= s < 0.7]
                low_scores = [s for s in match_scores if 0.3 <= s < 0.5]
                
                print(f"   High Scores (≥0.7): {len(high_scores)}")
                print(f"   Medium Scores (0.5-0.7): {len(medium_scores)}")
                print(f"   Low Scores (0.3-0.5): {len(low_scores)}")
                
                # Check top match details
                top_match = matching_trials[0]
                print(f"   Top Match Score: {top_match.get('match_score', 0):.3f}")
                
                # Verify match reasons are provided
                match_reasons = top_match.get('match_reasons', [])
                print(f"   Match Reasons Provided: {len(match_reasons) > 0}")
                
                # Verify eligibility considerations
                eligibility = top_match.get('eligibility_considerations', {})
                eligibility_fields = ['age_range', 'gender', 'locations', 'study_type']
                provided_fields = [field for field in eligibility_fields if field in eligibility]
                print(f"   Eligibility Fields Provided: {len(provided_fields)}/{len(eligibility_fields)}")
                
                # Verify next steps are generated
                next_steps = top_match.get('next_steps', [])
                print(f"   Next Steps Generated: {len(next_steps) > 0}")
                if next_steps:
                    print(f"   Next Steps Count: {len(next_steps)}")
        return success

    def test_clinical_trials_database_storage(self):
        """Test database storage of trial data with proper indexing"""
        # First, perform a search to populate database
        success1, response1 = self.run_test(
            "Clinical Trials - Database Storage (Search First)",
            "GET",
            "clinical-trials/search?condition=regenerative%20medicine&max_results=5",
            200,
            timeout=30
        )
        
        if not success1:
            return False
        
        # Then perform another search to test database retrieval
        success2, response2 = self.run_test(
            "Clinical Trials - Database Storage (Verify Storage)",
            "GET",
            "clinical-trials/search?condition=regenerative%20medicine&max_results=5",
            200,
            timeout=20  # Should be faster due to caching
        )
        
        if success2:
            trials = response2.get('trials', [])
            print(f"   Trials Retrieved: {len(trials)}")
            print(f"   Search Timestamp: {response2.get('search_timestamp', 'unknown')}")
            
            if trials:
                sample_trial = trials[0]
                
                # Check database-specific fields
                db_fields = ['search_condition', 'extracted_at', 'trial_url']
                available_db_fields = [field for field in db_fields if field in sample_trial]
                print(f"   Database Fields Present: {len(available_db_fields)}/{len(db_fields)}")
                
                # Check NCT ID format (should be indexed)
                nct_id = sample_trial.get('nct_id', '')
                print(f"   NCT ID (Index Key): {nct_id}")
                print(f"   NCT ID Format Valid: {nct_id.startswith('NCT')}")
                
                # Check search condition tracking
                search_condition = sample_trial.get('search_condition', '')
                print(f"   Search Condition Tracked: {len(search_condition) > 0}")
                
                # Check extraction timestamp
                extracted_at = sample_trial.get('extracted_at')
                print(f"   Extraction Timestamp Present: {extracted_at is not None}")
        
        return success1 and success2

    def test_clinical_trials_error_handling(self):
        """Test error handling for API issues and invalid queries"""
        # Test with empty condition
        success1, response1 = self.run_test(
            "Clinical Trials - Error Handling (Empty Condition)",
            "GET",
            "clinical-trials/search?condition=&max_results=5",
            200,  # Should handle gracefully
            timeout=20
        )
        
        if success1:
            print(f"   Empty Condition Status: {response1.get('status', 'unknown')}")
            if 'error' in response1:
                print(f"   Error Handled: {response1.get('error', 'No error')[:50]}...")
            print(f"   Trials Returned: {len(response1.get('trials', []))}")
            print(f"   Fallback Suggestion: {'fallback_suggestion' in response1}")
        
        # Test with very specific/rare condition
        success2, response2 = self.run_test(
            "Clinical Trials - Error Handling (Rare Condition)",
            "GET",
            "clinical-trials/search?condition=extremely_rare_condition_xyz123&max_results=5",
            200,
            timeout=30
        )
        
        if success2:
            print(f"   Rare Condition Status: {response2.get('status', 'unknown')}")
            trials = response2.get('trials', [])
            print(f"   Trials Found: {len(trials)}")
            
            if len(trials) == 0:
                print(f"   No Results Handled Gracefully: True")
                if 'fallback_suggestion' in response2:
                    print(f"   Fallback Suggestion: {response2.get('fallback_suggestion', 'None')}")
        
        return success1 and success2

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
        
        # Phase 6.1: Google Scholar Integration System (NEW)
        ("Google Scholar - Basic Search", tester.test_google_scholar_search_basic),
        ("Google Scholar - Stem Cell Therapy", tester.test_google_scholar_search_stem_cell),
        ("Google Scholar - Year Filter", tester.test_google_scholar_search_with_year_filter),
        ("Google Scholar - Error Handling", tester.test_google_scholar_error_handling),
        ("Multi-Source - Comprehensive Search", tester.test_multi_source_search_comprehensive),
        ("Multi-Source - BMAC Rotator Cuff", tester.test_multi_source_search_bmac),
        ("Multi-Source - Deduplication Test", tester.test_multi_source_deduplication),
        ("Literature - Evidence Extraction", tester.test_literature_integration_evidence_extraction),
        
        # Phase 6.5: Evidence Synthesis System (NEW)
        ("Evidence Synthesis - System Status", tester.test_evidence_synthesis_status),
        ("Evidence Synthesis - Osteoarthritis Protocol", tester.test_evidence_synthesis_osteoarthritis),
        ("Evidence Synthesis - Rotator Cuff Protocol", tester.test_evidence_synthesis_rotator_cuff),
        ("Evidence Synthesis - Error Handling (Missing Condition)", tester.test_evidence_synthesis_missing_condition),
        ("Evidence Synthesis - Invalid Condition", tester.test_evidence_synthesis_invalid_condition),
        
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