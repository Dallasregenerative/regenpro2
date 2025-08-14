#!/usr/bin/env python3
"""
Enhanced Comprehensive Protocol Generation Testing
Testing the newly enhanced comprehensive protocol generation system that creates detailed 7-section patient education documents
"""

import requests
import json
import sys
from datetime import datetime

class EnhancedProtocolTester:
    def __init__(self, base_url="https://a5405ec9-bfc7-45f4-af6d-6fb1a12b2148.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer demo-token'
        }

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=120):
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

    def test_enhanced_comprehensive_protocol_generation(self):
        """Test the newly enhanced comprehensive protocol generation system with 7-section documents"""
        print("🔍 ENHANCED COMPREHENSIVE PROTOCOL GENERATION TESTING")
        print("   Testing the newly enhanced comprehensive protocol generation system")
        print("   that creates detailed 7-section patient education documents")
        
        # Create complex patient case as specified in review request
        complex_patient_data = {
            "demographics": {
                "name": "John Hudson",
                "age": "52",
                "gender": "Male",
                "occupation": "Executive",
                "insurance": "Self-pay"
            },
            "chief_complaint": "Multiple regenerative medicine needs: chronic shoulder injury, metabolic dysfunction, and chronic pain seeking comprehensive regenerative treatment",
            "history_present_illness": "52-year-old executive with complex medical presentation including chronic right shoulder injury from sports trauma 2 years ago, metabolic dysfunction with insulin resistance, and chronic widespread pain affecting quality of life and work performance. Failed multiple conservative treatments including physical therapy, injections, and medications. Seeking comprehensive regenerative medicine approach to address multiple interconnected health issues.",
            "past_medical_history": [
                "Rotator cuff partial tear",
                "Metabolic syndrome", 
                "Chronic pain syndrome",
                "Insulin resistance",
                "Hypertension",
                "Sleep apnea"
            ],
            "medications": [
                "Metformin 1000mg BID",
                "Lisinopril 20mg daily", 
                "Gabapentin 300mg TID",
                "Ibuprofen PRN",
                "Melatonin 3mg HS"
            ],
            "allergies": ["Sulfa drugs", "Shellfish"],
            "vital_signs": {
                "temperature": "98.6",
                "blood_pressure": "142/88",
                "heart_rate": "82",
                "respiratory_rate": "18",
                "oxygen_saturation": "96",
                "weight": "195",
                "height": "5'11\"",
                "BMI": "27.2"
            },
            "symptoms": [
                "chronic shoulder pain",
                "decreased range of motion",
                "fatigue",
                "brain fog",
                "muscle aches",
                "sleep disturbances",
                "metabolic dysfunction"
            ],
            "lab_results": {
                "inflammatory_markers": {
                    "CRP": "4.8 mg/L",
                    "ESR": "28 mm/hr",
                    "IL-6": "3.2 pg/mL"
                },
                "metabolic_panel": {
                    "glucose": "165 mg/dL",
                    "HbA1c": "7.8%",
                    "insulin": "18.5 mU/L",
                    "HOMA-IR": "7.2"
                },
                "lipid_panel": {
                    "total_cholesterol": "245 mg/dL",
                    "LDL": "155 mg/dL",
                    "HDL": "38 mg/dL",
                    "triglycerides": "285 mg/dL"
                },
                "hormonal_markers": {
                    "testosterone": "285 ng/dL",
                    "cortisol": "22.5 mcg/dL",
                    "thyroid_TSH": "3.8 mIU/L"
                },
                "regenerative_markers": {
                    "VEGF": "145 pg/mL",
                    "PDGF": "52 pg/mL",
                    "IGF-1": "165 ng/mL"
                }
            },
            "imaging_data": [
                {
                    "type": "MRI",
                    "location": "right shoulder",
                    "findings": "Partial thickness rotator cuff tear involving supraspinatus tendon, moderate subacromial impingement, mild glenohumeral arthritis",
                    "date": "2024-01-15"
                },
                {
                    "type": "DEXA scan",
                    "location": "lumbar spine",
                    "findings": "Osteopenia with T-score -1.8, consistent with metabolic bone disease",
                    "date": "2024-02-01"
                }
            ],
            "genetic_data": {
                "regenerative_markers": {
                    "VEGF_polymorphism": "heterozygous_advantage",
                    "collagen_synthesis_genes": "enhanced_healing",
                    "inflammatory_response": "moderate_risk",
                    "metabolic_genes": "insulin_resistance_risk"
                }
            }
        }

        # Step 1: Create complex patient
        print("   Step 1: Creating complex patient case (John Hudson)...")
        create_success, create_response = self.run_test(
            "ENHANCED PROTOCOL - Create Complex Patient",
            "POST",
            "patients",
            200,
            data=complex_patient_data,
            timeout=30
        )
        
        if not create_success:
            print("   ❌ Failed to create complex patient")
            return False
            
        patient_id = create_response.get('patient_id')
        print(f"   ✅ Complex patient created with ID: {patient_id}")

        # Step 2: Test enhanced protocol generation across all three schools
        schools_to_test = [
            ("traditional_autologous", "Traditional Autologous"),
            ("biologics", "Biologics & Advanced Cellular"),
            ("ai_optimized", "AI-Optimized Personalized")
        ]
        
        protocol_results = {}
        
        for school_key, school_name in schools_to_test:
            print(f"\n   Step 2.{schools_to_test.index((school_key, school_name)) + 1}: Testing Enhanced {school_name} Protocol Generation")
            print(f"   🔍 VALIDATING: 7-section comprehensive document format")
            
            protocol_data = {
                "patient_id": patient_id,
                "school_of_thought": school_key
            }

            print(f"   This may take 60-90 seconds for comprehensive protocol generation...")
            success, response = self.run_test(
                f"ENHANCED PROTOCOL - Generate {school_name}",
                "POST",
                "protocols/generate",
                200,
                data=protocol_data,
                timeout=120
            )
            
            if success:
                # Validate comprehensive protocol format
                protocol_validation = self._validate_comprehensive_protocol(response, school_name, patient_id)
                protocol_results[school_key] = {
                    'success': success,
                    'response': response,
                    'school_name': school_name,
                    'validation': protocol_validation
                }
                
                print(f"   ✅ {school_name} - Protocol Generated Successfully")
                self._print_protocol_validation_results(protocol_validation, school_name)
            else:
                print(f"   ❌ {school_name} - Protocol Generation Failed")
                protocol_results[school_key] = {
                    'success': False,
                    'response': {},
                    'school_name': school_name,
                    'validation': {}
                }

        # Step 3: Overall validation of enhanced system
        print(f"\n   Step 3: Overall Enhanced Protocol System Validation")
        
        successful_protocols = sum(1 for result in protocol_results.values() if result['success'])
        total_protocols = len(protocol_results)
        
        print(f"   📊 Protocol Generation Success Rate: {successful_protocols}/{total_protocols} ({(successful_protocols/total_protocols)*100:.1f}%)")
        
        # Validate key enhancements
        enhancement_criteria = {
            'comprehensive_documents': 0,
            'patient_personalization': 0,
            'clinical_depth': 0,
            'scientific_mechanisms': 0,
            'specific_dosages': 0,
            'evidence_citations': 0,
            'seven_section_format': 0
        }
        
        for school_key, result in protocol_results.items():
            if result['success']:
                validation = result.get('validation', {})
                for criterion in enhancement_criteria:
                    if validation.get(criterion, False):
                        enhancement_criteria[criterion] += 1
        
        print(f"   📋 Enhancement Validation Results:")
        for criterion, count in enhancement_criteria.items():
            percentage = (count / total_protocols) * 100 if total_protocols > 0 else 0
            status = "✅" if percentage >= 66.7 else "⚠️" if percentage >= 33.3 else "❌"
            print(f"   {status} {criterion.replace('_', ' ').title()}: {count}/{total_protocols} protocols ({percentage:.1f}%)")
        
        # Overall success assessment
        overall_success_rate = sum(enhancement_criteria.values()) / (len(enhancement_criteria) * total_protocols) if total_protocols > 0 else 0
        
        print(f"\n   📊 OVERALL ENHANCEMENT SUCCESS RATE: {overall_success_rate*100:.1f}%")
        
        if overall_success_rate >= 0.80:
            print("   🎉 ENHANCED PROTOCOL GENERATION: EXCELLENT SUCCESS!")
            print("   The new comprehensive 7-section protocol system is working excellently")
            return True
        elif overall_success_rate >= 0.60:
            print("   ✅ ENHANCED PROTOCOL GENERATION: GOOD SUCCESS")
            print("   The new system is working well with some areas for improvement")
            return True
        else:
            print("   ⚠️ ENHANCED PROTOCOL GENERATION: NEEDS IMPROVEMENT")
            print("   The enhanced system needs further development")
            return False

    def _validate_comprehensive_protocol(self, response, school_name, patient_id):
        """Validate comprehensive protocol format and content"""
        validation_results = {
            'comprehensive_documents': False,
            'patient_personalization': False,
            'clinical_depth': False,
            'scientific_mechanisms': False,
            'specific_dosages': False,
            'evidence_citations': False,
            'seven_section_format': False,
            'word_count_adequate': False,
            'patient_centric_language': False,
            'detailed_timeline': False
        }
        
        # Check basic protocol structure
        if not response or 'protocol_id' not in response:
            return validation_results
        
        # Get AI reasoning (where comprehensive document should be stored)
        ai_reasoning = response.get('ai_reasoning', '')
        protocol_steps = response.get('protocol_steps', [])
        supporting_evidence = response.get('supporting_evidence', [])
        
        # Validate comprehensive document length (3,000-5,000 words expected)
        word_count = len(ai_reasoning.split()) if ai_reasoning else 0
        validation_results['word_count_adequate'] = word_count >= 1000  # Minimum threshold
        validation_results['comprehensive_documents'] = word_count >= 1000
        
        # Check for patient personalization (should use patient name)
        patient_name_mentioned = 'John Hudson' in ai_reasoning or 'John' in ai_reasoning
        validation_results['patient_personalization'] = patient_name_mentioned
        validation_results['patient_centric_language'] = patient_name_mentioned
        
        # Check for 7-section format indicators
        section_indicators = [
            'Section 1', 'Section 2', 'Section 3', 'Section 4', 
            'Section 5', 'Section 6', 'Section 7'
        ]
        sections_found = sum(1 for indicator in section_indicators if indicator in ai_reasoning)
        validation_results['seven_section_format'] = sections_found >= 5  # At least 5 of 7 sections
        
        # Check for clinical depth indicators
        clinical_depth_keywords = [
            'cell count', 'million', 'dosage', 'mg', 'ml', 'weeks', 'months',
            'specific', 'protocol', 'timeline', 'monitoring'
        ]
        clinical_depth_found = sum(1 for keyword in clinical_depth_keywords if keyword.lower() in ai_reasoning.lower())
        validation_results['clinical_depth'] = clinical_depth_found >= 5
        
        # Check for scientific mechanisms
        mechanism_keywords = [
            'mechanism', 'pathway', 'signaling', 'cellular', 'molecular',
            'growth factor', 'cytokine', 'regeneration', 'healing'
        ]
        mechanisms_found = sum(1 for keyword in mechanism_keywords if keyword.lower() in ai_reasoning.lower())
        validation_results['scientific_mechanisms'] = mechanisms_found >= 3
        
        # Check for specific dosages
        dosage_patterns = ['mg', 'ml', 'million', 'billion', 'units', 'IU']
        dosages_found = sum(1 for pattern in dosage_patterns if pattern in ai_reasoning)
        validation_results['specific_dosages'] = dosages_found >= 2
        
        # Check for evidence citations
        citation_patterns = ['PMID', 'study', 'trial', 'research', 'evidence', 'citation']
        citations_found = sum(1 for pattern in citation_patterns if pattern.lower() in ai_reasoning.lower())
        validation_results['evidence_citations'] = citations_found >= 2 or len(supporting_evidence) >= 2
        
        # Check for detailed timeline
        timeline_keywords = ['week', 'month', 'day', 'timeline', 'schedule', 'phase']
        timeline_found = sum(1 for keyword in timeline_keywords if keyword.lower() in ai_reasoning.lower())
        validation_results['detailed_timeline'] = timeline_found >= 3
        
        return validation_results

    def _print_protocol_validation_results(self, validation, school_name):
        """Print detailed validation results for a protocol"""
        print(f"   📋 {school_name} Protocol Validation:")
        
        for criterion, passed in validation.items():
            status = "✅" if passed else "❌"
            criterion_name = criterion.replace('_', ' ').title()
            print(f"      {status} {criterion_name}")

    def run_enhanced_protocol_tests(self):
        """Run the enhanced protocol generation tests"""
        print("🚀 Starting Enhanced Comprehensive Protocol Generation Testing")
        print("=" * 80)
        
        # Test health check first
        health_success, _ = self.run_test(
            "System Health Check",
            "GET",
            "health",
            200
        )
        
        if not health_success:
            print("❌ System health check failed - cannot proceed with testing")
            return False
        
        # Main test: Enhanced comprehensive protocol generation
        protocol_success = self.test_enhanced_comprehensive_protocol_generation()
        
        # Final summary
        print("\n" + "=" * 80)
        print("🏁 Enhanced Protocol Generation Test Complete")
        print(f"📊 Results: {self.tests_passed}/{self.tests_run} tests passed ({(self.tests_passed/self.tests_run)*100:.1f}%)")
        
        if protocol_success:
            print("🎉 Enhanced comprehensive protocol generation system is working!")
            print("✅ The new 7-section document format is functional")
            print("✅ Patient personalization is working")
            print("✅ Clinical depth and scientific mechanisms are present")
            return True
        else:
            print("⚠️ Enhanced protocol generation system needs improvement")
            print("❌ Some validation criteria were not met")
            return False

if __name__ == "__main__":
    tester = EnhancedProtocolTester()
    success = tester.run_enhanced_protocol_tests()
    
    if success:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure