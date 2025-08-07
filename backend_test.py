import requests
import sys
import json
from datetime import datetime

class MedicalDiagnosticsAPITester:
    def __init__(self, base_url="https://efbc6239-ef8b-4912-8854-b1e0ad6f17df.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.patient_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
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
        """Test health check endpoint"""
        success, response = self.run_test(
            "Health Check",
            "GET",
            "health",
            200
        )
        if success:
            print(f"   System Status: {response.get('status', 'unknown')}")
            services = response.get('services', {})
            print(f"   Database: {services.get('database', 'unknown')}")
            print(f"   AI Engine: {services.get('ai_engine', 'unknown')}")
        return success

    def test_create_patient(self):
        """Test patient creation with sample data"""
        patient_data = {
            "demographics": {
                "name": "John Doe",
                "age": "45",
                "gender": "Male",
                "occupation": "Engineer"
            },
            "chief_complaint": "Chest pain and shortness of breath for 3 days",
            "history_present_illness": "Patient reports sharp chest pain that worsens with deep breathing, started 3 days ago after physical activity",
            "past_medical_history": ["Hypertension", "High cholesterol"],
            "medications": ["Lisinopril 10mg daily", "Atorvastatin 20mg daily"],
            "allergies": ["Penicillin"],
            "vital_signs": {
                "temperature": "99.2",
                "blood_pressure": "140/90",
                "heart_rate": "95",
                "respiratory_rate": "22",
                "oxygen_saturation": "96"
            },
            "symptoms": ["chest pain", "shortness of breath", "fatigue"]
        }

        success, response = self.run_test(
            "Create Patient",
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

    def test_get_patient(self):
        """Test retrieving patient data"""
        if not self.patient_id:
            print("❌ No patient ID available for testing")
            return False

        success, response = self.run_test(
            "Get Patient",
            "GET",
            f"patients/{self.patient_id}",
            200
        )
        
        if success:
            print(f"   Retrieved Patient: {response.get('demographics', {}).get('name', 'Unknown')}")
        return success

    def test_list_patients(self):
        """Test listing all patients"""
        success, response = self.run_test(
            "List Patients",
            "GET",
            "patients",
            200
        )
        
        if success:
            patient_count = len(response) if isinstance(response, list) else 0
            print(f"   Found {patient_count} patients")
        return success

    def test_diagnose_patient(self):
        """Test AI diagnosis generation"""
        if not self.patient_id:
            print("❌ No patient ID available for diagnosis testing")
            return False

        print("   This may take 10-30 seconds for AI processing...")
        success, response = self.run_test(
            "Generate AI Diagnosis",
            "POST",
            f"diagnose/{self.patient_id}",
            200,
            timeout=60  # Longer timeout for AI processing
        )
        
        if success:
            diagnoses = response.get('differential_diagnoses', [])
            print(f"   Generated {len(diagnoses)} differential diagnoses")
            if diagnoses:
                top_diagnosis = diagnoses[0]
                print(f"   Top Diagnosis: {top_diagnosis.get('diagnosis', 'Unknown')}")
                print(f"   Confidence: {top_diagnosis.get('confidence_score', 0):.2f}")
            processing_time = response.get('processing_time_seconds', 0)
            print(f"   Processing Time: {processing_time:.2f} seconds")
        return success

    def test_root_endpoint(self):
        """Test root API endpoint"""
        success, response = self.run_test(
            "Root API Endpoint",
            "GET",
            "",
            200
        )
        return success

def main():
    print("🏥 AI Medical Diagnostics System - Backend API Testing")
    print("=" * 60)
    
    # Initialize tester
    tester = MedicalDiagnosticsAPITester()
    
    # Run all tests in sequence
    tests = [
        ("Health Check", tester.test_health_check),
        ("Root Endpoint", tester.test_root_endpoint),
        ("Create Patient", tester.test_create_patient),
        ("Get Patient", tester.test_get_patient),
        ("List Patients", tester.test_list_patients),
        ("AI Diagnosis", tester.test_diagnose_patient),
    ]
    
    print(f"\nRunning {len(tests)} API tests...\n")
    
    for test_name, test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
    
    # Print final results
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed! Backend API is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())