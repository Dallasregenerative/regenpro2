#!/usr/bin/env python3

import requests
import json
from datetime import datetime

class FocusedTester:
    def __init__(self):
        self.base_url = "https://ed4e4952-b9f5-42dd-8eae-fb43144bcaeb.preview.emergentagent.com"
        self.api_url = f"{self.base_url}/api"
        self.patient_id = "c458d177-712c-4eb9-8fd3-5f5e41fe7b71"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer demo-token'
        }

    def test_file_retrieval(self):
        """Test file retrieval endpoint"""
        print("🔍 Testing Get Patient Files...")
        try:
            response = requests.get(
                f"{self.api_url}/files/patient/{self.patient_id}",
                headers=self.headers,
                timeout=30
            )
            print(f"Status: {response.status_code}")
            if response.status_code != 200:
                print(f"Error: {response.text}")
            else:
                data = response.json()
                print(f"Success: Found {data.get('total_files', 0)} files")
        except Exception as e:
            print(f"Exception: {str(e)}")

    def test_comprehensive_analysis(self):
        """Test comprehensive file analysis"""
        print("\n🔍 Testing Comprehensive File Analysis...")
        try:
            response = requests.get(
                f"{self.api_url}/files/comprehensive-analysis/{self.patient_id}",
                headers=self.headers,
                timeout=45
            )
            print(f"Status: {response.status_code}")
            if response.status_code != 200:
                print(f"Error: {response.text}")
            else:
                data = response.json()
                print(f"Success: Analysis completed")
        except Exception as e:
            print(f"Exception: {str(e)}")

    def test_file_based_protocol(self):
        """Test file-based protocol generation"""
        print("\n🔍 Testing File-Based Protocol Generation...")
        try:
            response = requests.post(
                f"{self.api_url}/protocols/generate-from-files?patient_id={self.patient_id}&school_of_thought=ai_optimized",
                json={},
                headers=self.headers,
                timeout=60
            )
            print(f"Status: {response.status_code}")
            if response.status_code != 200:
                print(f"Error: {response.text}")
            else:
                data = response.json()
                protocol = data.get('protocol', {})
                print(f"Success: Protocol ID {protocol.get('protocol_id', 'Unknown')}")
        except Exception as e:
            print(f"Exception: {str(e)}")

    def test_outcome_prediction(self):
        """Test treatment outcome prediction"""
        print("\n🔍 Testing Treatment Outcome Prediction...")
        try:
            prediction_data = {
                "patient_id": self.patient_id,
                "therapy_plan": {
                    "therapy_name": "Platelet-Rich Plasma (PRP)",
                    "dosage": "3-5ml",
                    "delivery_method": "Intra-articular injection",
                    "target_location": "shoulder"
                }
            }
            response = requests.post(
                f"{self.api_url}/predictions/treatment-outcome",
                json=prediction_data,
                headers=self.headers,
                timeout=45
            )
            print(f"Status: {response.status_code}")
            if response.status_code != 200:
                print(f"Error: {response.text}")
            else:
                data = response.json()
                predictions = data.get('predictions', {})
                print(f"Success: Success probability {predictions.get('success_probability', 0):.2f}")
        except Exception as e:
            print(f"Exception: {str(e)}")

    def test_dashboard_analytics(self):
        """Test dashboard analytics"""
        print("\n🔍 Testing Dashboard Analytics...")
        try:
            response = requests.get(
                f"{self.api_url}/analytics/dashboard",
                headers=self.headers,
                timeout=30
            )
            print(f"Status: {response.status_code}")
            if response.status_code != 200:
                print(f"Error: {response.text}")
            else:
                data = response.json()
                stats = data.get('summary_stats', {})
                print(f"Success: {stats.get('total_patients', 0)} patients")
        except Exception as e:
            print(f"Exception: {str(e)}")

if __name__ == "__main__":
    print("🧬 Focused Testing of Failed Endpoints")
    print("=" * 50)
    
    tester = FocusedTester()
    tester.test_file_retrieval()
    tester.test_comprehensive_analysis()
    tester.test_file_based_protocol()
    tester.test_outcome_prediction()
    tester.test_dashboard_analytics()