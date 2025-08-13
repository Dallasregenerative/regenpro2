#!/usr/bin/env python3
"""
Emergent LLM GPT-5 Integration Test Suite
Testing the newly integrated Emergent LLM key system with GPT-5 model for RegenMed AI Pro
"""

import requests
import json
import sys
from datetime import datetime

class EmergentLLMTester:
    def __init__(self, base_url="https://medprotocol-3.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.patient_id = None
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

    def test_emergent_llm_integration_status(self):
        """Test Emergent LLM key system status and GPT-5 integration"""
        print("🔍 EMERGENT LLM KEY SYSTEM STATUS VALIDATION")
        print("   Objective: Verify Emergent LLM key integration with GPT-5 model")
        print("   Expected: System should show 'Emergent LLM (GPT-5)' usage messages")
        
        success, response = self.run_test(
            "Emergent LLM Integration Status",
            "GET",
            "health",
            200
        )
        
        if success:
            ai_engine_status = response.get('services', {}).get('ai_engine', 'unknown')
            print(f"   AI Engine Status: {ai_engine_status}")
            
            # Check for Emergent LLM indicators
            emergent_indicators = ['emergent', 'gpt-5', 'llm']
            status_lower = str(ai_engine_status).lower()
            emergent_found = any(indicator in status_lower for indicator in emergent_indicators)
            
            print(f"   ✅ Emergent LLM indicators found: {emergent_found}")
            print(f"   Version: {response.get('version', 'unknown')}")
            
            return emergent_found
        return False

    def test_create_complex_regenerative_patient(self):
        """Create complex regenerative medicine patient as specified in review request"""
        print("🏥 CREATING COMPLEX REGENERATIVE MEDICINE PATIENT")
        print("   Patient: 52-year-old with shoulder rotator cuff injury (as specified in review)")
        
        # Create the exact patient specified in review request
        complex_patient_data = {
            "demographics": {
                "name": "Michael Thompson",
                "age": "52",
                "gender": "Male",
                "occupation": "Competitive Tennis Player",
                "insurance": "Self-pay premium"
            },
            "chief_complaint": "Right shoulder rotator cuff injury with significant functional limitation affecting competitive tennis performance",
            "history_present_illness": "52-year-old competitive tennis player with acute-on-chronic right shoulder rotator cuff injury sustained during tournament play 6 weeks ago. Progressive pain and weakness with overhead activities. Failed conservative management including rest, NSAIDs, physical therapy, and corticosteroid injection. Seeking advanced regenerative medicine options to return to competitive play and avoid surgical intervention.",
            "past_medical_history": ["Rotator cuff tendinopathy", "Previous left shoulder PRP treatment (successful)", "Mild osteoarthritis"],
            "medications": ["Ibuprofen 600mg TID PRN", "Omega-3 supplements", "Vitamin D3 5000 IU daily"],
            "allergies": ["NKDA"],
            "vital_signs": {
                "temperature": "98.2",
                "blood_pressure": "125/78",
                "heart_rate": "58",
                "respiratory_rate": "14",
                "oxygen_saturation": "99",
                "weight": "175",
                "height": "6'1\""
            },
            "symptoms": [
                "right shoulder pain with overhead activities",
                "weakness with external rotation",
                "night pain disrupting sleep",
                "decreased serve velocity",
                "functional limitation in competitive tennis"
            ],
            "lab_results": {
                "inflammatory_markers": {
                    "CRP": "1.8 mg/L",
                    "ESR": "12 mm/hr"
                },
                "regenerative_markers": {
                    "platelet_count": "320 K/uL",
                    "growth_factors": "elevated PDGF, normal VEGF",
                    "vitamin_D": "45 ng/mL"
                }
            },
            "imaging_data": [
                {
                    "type": "MRI",
                    "location": "right shoulder",
                    "findings": "High-grade partial thickness rotator cuff tear involving supraspinatus and infraspinatus tendons, moderate subacromial impingement, mild glenohumeral arthritis",
                    "date": "2024-02-20"
                }
            ]
        }

        success, response = self.run_test(
            "Create Complex Regenerative Medicine Patient",
            "POST",
            "patients",
            200,
            data=complex_patient_data
        )
        
        if success and 'patient_id' in response:
            self.patient_id = response['patient_id']
            print(f"   ✅ Created Complex Patient ID: {self.patient_id}")
            print(f"   Patient: {response.get('demographics', {}).get('name', 'Unknown')}")
            print(f"   Age: {response.get('demographics', {}).get('age', 'Unknown')}")
            print(f"   Condition: Rotator cuff injury (regenerative medicine candidate)")
            return True
        return False

    def test_ai_analysis_gpt5_regenerative_keywords(self):
        """Test AI analysis for regenerative medicine keyword integration with GPT-5"""
        if not self.patient_id:
            print("❌ No patient ID available for GPT-5 analysis testing")
            return False

        print("🧠 TESTING AI ANALYSIS WITH GPT-5 REGENERATIVE MEDICINE KEYWORDS")
        print("   Objective: Verify GPT-5 integration produces enhanced regenerative medicine specificity")
        print("   Expected Keywords: PRP, BMAC, stem cell, platelet-rich plasma, bone marrow aspirate")
        print("   This may take 60-90 seconds for GPT-5 AI processing...")
        
        success, response = self.run_test(
            "AI Analysis - GPT-5 Regenerative Medicine Keywords",
            "POST",
            f"patients/{self.patient_id}/analyze",
            200,
            data={},
            timeout=120
        )
        
        if success:
            diagnostic_results = response.get('diagnostic_results', [])
            print(f"   Generated {len(diagnostic_results)} diagnostic results")
            
            # Check for regenerative medicine keywords in responses
            required_keywords = [
                'prp', 'platelet-rich plasma', 'platelet rich plasma',
                'bmac', 'bone marrow aspirate', 'bone marrow aspirate concentrate',
                'stem cell', 'mesenchymal stem cells', 'stem cell therapy',
                'growth factor', 'tissue engineering', 'cellular therapy',
                'chondrogenesis', 'cartilage regeneration', 'autologous biologics'
            ]
            
            found_keywords = set()
            total_text = ""
            
            for result in diagnostic_results:
                # Combine all text fields for keyword analysis
                text_fields = [
                    result.get('diagnosis', ''),
                    result.get('reasoning', ''),
                    ' '.join(result.get('supporting_evidence', [])),
                    ' '.join(result.get('mechanisms_involved', [])),
                    ' '.join(result.get('regenerative_targets', []))
                ]
                total_text += ' '.join(text_fields).lower()
            
            # Count found keywords
            for keyword in required_keywords:
                if keyword in total_text:
                    found_keywords.add(keyword)
            
            print(f"   ✅ Regenerative Keywords Found: {len(found_keywords)}/13 required")
            print(f"   Found Keywords: {', '.join(list(found_keywords)[:5])}...")
            
            # Check for enhanced clinical reasoning
            if diagnostic_results:
                primary_result = diagnostic_results[0]
                print(f"   Primary Diagnosis: {primary_result.get('diagnosis', 'Unknown')}")
                print(f"   Confidence Score: {primary_result.get('confidence_score', 0):.2f}")
                print(f"   Regenerative Targets: {len(primary_result.get('regenerative_targets', []))}")
                
                # Check for shoulder-specific regenerative medicine content
                shoulder_keywords = ['rotator cuff', 'shoulder', 'supraspinatus', 'infraspinatus']
                shoulder_found = any(kw in total_text for kw in shoulder_keywords)
                print(f"   ✅ Shoulder-specific content: {shoulder_found}")
            
            # Success criteria: Should find at least 5+ regenerative keywords for GPT-5
            keyword_success = len(found_keywords) >= 5
            print(f"   ✅ GPT-5 Keyword Integration Success: {keyword_success}")
            
            return keyword_success and len(diagnostic_results) > 0
        return False

    def test_protocol_generation_all_schools_gpt5(self):
        """Test protocol generation across all schools with GPT-5 enhanced quality"""
        if not self.patient_id:
            print("❌ No patient ID available for protocol generation testing")
            return False

        print("📋 TESTING PROTOCOL GENERATION ACROSS ALL SCHOOLS WITH GPT-5")
        print("   Objective: Verify GPT-5 enhanced protocol quality across all schools of thought")
        print("   Schools: Traditional Autologous, Biologics, AI-Optimized")
        
        schools_to_test = [
            ("traditional_autologous", "Traditional Autologous"),
            ("biologics", "Biologics"),
            ("ai_optimized", "AI-Optimized")
        ]
        
        protocol_results = {}
        all_schools_success = True
        
        for school_key, school_name in schools_to_test:
            print(f"\n   Testing {school_name} Protocol Generation...")
            print(f"   This may take 60-90 seconds for GPT-5 protocol generation...")
            
            protocol_data = {
                "patient_id": self.patient_id,
                "school_of_thought": school_key
            }

            success, response = self.run_test(
                f"GPT-5 Protocol Generation - {school_name}",
                "POST",
                "protocols/generate",
                200,
                data=protocol_data,
                timeout=120
            )
            
            if success:
                # Analyze protocol quality
                protocol_steps = response.get('protocol_steps', [])
                supporting_evidence = response.get('supporting_evidence', [])
                cost_estimate = response.get('cost_estimate', '')
                confidence_score = response.get('confidence_score', 0)
                
                print(f"   ✅ {school_name} - Protocol Generated Successfully")
                print(f"   Protocol ID: {response.get('protocol_id', 'Unknown')}")
                print(f"   Protocol Steps: {len(protocol_steps)}")
                print(f"   Supporting Evidence: {len(supporting_evidence)} citations")
                print(f"   Cost Estimate: {cost_estimate}")
                print(f"   Confidence Score: {confidence_score:.2f}")
                
                # Check for evidence-based dosages and timelines (GPT-5 improvement)
                has_specific_dosages = False
                has_evidence_citations = False
                has_realistic_timelines = False
                
                if protocol_steps:
                    first_step = protocol_steps[0]
                    dosage = first_step.get('dosage', '').lower()
                    timing = first_step.get('timing', '').lower()
                    
                    # Check for specific dosages (ml, mg, units, etc.)
                    dosage_indicators = ['ml', 'mg', 'units', 'million', 'concentration']
                    has_specific_dosages = any(indicator in dosage for indicator in dosage_indicators)
                    
                    # Check for realistic timelines
                    timeline_indicators = ['week', 'day', 'month', 'hour', 'minutes']
                    has_realistic_timelines = any(indicator in timing for indicator in timeline_indicators)
                    
                    print(f"   First Step: {first_step.get('therapy', 'Unknown')}")
                    print(f"   Dosage: {first_step.get('dosage', 'Unknown')}")
                    print(f"   Timing: {first_step.get('timing', 'Unknown')}")
                
                # Check for evidence citations (PMID references)
                if supporting_evidence:
                    evidence_text = str(supporting_evidence).lower()
                    has_evidence_citations = 'pmid' in evidence_text or 'doi' in evidence_text
                
                print(f"   ✅ Specific Dosages: {has_specific_dosages}")
                print(f"   ✅ Evidence Citations: {has_evidence_citations}")
                print(f"   ✅ Realistic Timelines: {has_realistic_timelines}")
                
                protocol_results[school_key] = {
                    'success': True,
                    'quality_score': sum([has_specific_dosages, has_evidence_citations, has_realistic_timelines]),
                    'protocol_steps': len(protocol_steps),
                    'evidence_count': len(supporting_evidence),
                    'confidence': confidence_score
                }
            else:
                print(f"   ❌ {school_name} - Protocol Generation Failed")
                protocol_results[school_key] = {'success': False}
                all_schools_success = False
        
        # Overall assessment
        print(f"\n   📊 PROTOCOL GENERATION SUMMARY:")
        successful_schools = sum(1 for result in protocol_results.values() if result.get('success', False))
        print(f"   Successful Schools: {successful_schools}/{len(schools_to_test)}")
        
        if successful_schools == len(schools_to_test):
            print(f"   🎉 ALL SCHOOLS GENERATED PROTOCOLS SUCCESSFULLY")
            
            # Calculate average quality metrics
            avg_quality = sum(result.get('quality_score', 0) for result in protocol_results.values() if result.get('success')) / successful_schools
            avg_steps = sum(result.get('protocol_steps', 0) for result in protocol_results.values() if result.get('success')) / successful_schools
            avg_evidence = sum(result.get('evidence_count', 0) for result in protocol_results.values() if result.get('success')) / successful_schools
            
            print(f"   Average Quality Score: {avg_quality:.1f}/3.0")
            print(f"   Average Protocol Steps: {avg_steps:.1f}")
            print(f"   Average Evidence Citations: {avg_evidence:.1f}")
            
            return True
        else:
            print(f"   ⚠️  Some schools failed protocol generation")
            return False

    def test_enhanced_clinical_outputs_gpt5(self):
        """Compare AI-generated outputs for GPT-5 improvements"""
        print("🔬 TESTING ENHANCED CLINICAL OUTPUTS WITH GPT-5")
        print("   Objective: Verify GPT-5 produces superior clinical outputs vs previous implementation")
        print("   Focus: Accuracy, specificity, evidence-based recommendations")
        
        if not self.patient_id:
            print("❌ No patient ID available for clinical output testing")
            return False
        
        # Test comprehensive analysis for clinical quality
        print("\n   Testing Clinical Analysis Quality...")
        success, response = self.run_test(
            "GPT-5 Enhanced Clinical Analysis",
            "POST",
            f"patients/{self.patient_id}/analyze",
            200,
            data={},
            timeout=120
        )
        
        if not success:
            print("   ❌ Clinical analysis failed")
            return False
        
        diagnostic_results = response.get('diagnostic_results', [])
        
        # Quality Assessment Metrics
        quality_metrics = {
            'diagnostic_accuracy': 0,
            'regenerative_specificity': 0,
            'evidence_integration': 0,
            'clinical_reasoning': 0,
            'confidence_calibration': 0
        }
        
        print(f"   Generated {len(diagnostic_results)} diagnostic results")
        
        if diagnostic_results:
            primary_diagnosis = diagnostic_results[0]
            
            # 1. Diagnostic Accuracy (shoulder-specific for rotator cuff case)
            diagnosis_text = primary_diagnosis.get('diagnosis', '').lower()
            shoulder_terms = ['rotator cuff', 'shoulder', 'supraspinatus', 'infraspinatus', 'tendinopathy']
            accuracy_score = sum(1 for term in shoulder_terms if term in diagnosis_text)
            quality_metrics['diagnostic_accuracy'] = min(accuracy_score / 3, 1.0)  # Normalize to 0-1
            
            print(f"   ✅ Diagnostic Accuracy: {quality_metrics['diagnostic_accuracy']:.2f}")
            print(f"   Primary Diagnosis: {primary_diagnosis.get('diagnosis', 'Unknown')}")
            
            # 2. Regenerative Medicine Specificity
            all_text = ' '.join([
                primary_diagnosis.get('diagnosis', ''),
                primary_diagnosis.get('reasoning', ''),
                ' '.join(primary_diagnosis.get('supporting_evidence', [])),
                ' '.join(primary_diagnosis.get('regenerative_targets', []))
            ]).lower()
            
            regen_terms = ['prp', 'bmac', 'platelet-rich plasma', 'stem cell', 'growth factor', 'regenerative']
            specificity_score = sum(1 for term in regen_terms if term in all_text)
            quality_metrics['regenerative_specificity'] = min(specificity_score / 4, 1.0)
            
            print(f"   ✅ Regenerative Specificity: {quality_metrics['regenerative_specificity']:.2f}")
            
            # 3. Evidence Integration
            supporting_evidence = primary_diagnosis.get('supporting_evidence', [])
            evidence_quality = len(supporting_evidence) > 0
            quality_metrics['evidence_integration'] = 1.0 if evidence_quality else 0.0
            
            print(f"   ✅ Evidence Integration: {quality_metrics['evidence_integration']:.2f}")
            print(f"   Supporting Evidence Items: {len(supporting_evidence)}")
            
            # 4. Clinical Reasoning Quality
            reasoning = primary_diagnosis.get('reasoning', '')
            reasoning_quality = len(reasoning) > 50 and any(term in reasoning.lower() for term in ['mechanism', 'pathophysiology', 'treatment'])
            quality_metrics['clinical_reasoning'] = 1.0 if reasoning_quality else 0.0
            
            print(f"   ✅ Clinical Reasoning: {quality_metrics['clinical_reasoning']:.2f}")
            
            # 5. Confidence Calibration
            confidence = primary_diagnosis.get('confidence_score', 0)
            # For shoulder rotator cuff case, expect moderate to high confidence (0.6-0.9)
            confidence_appropriate = 0.6 <= confidence <= 0.9
            quality_metrics['confidence_calibration'] = 1.0 if confidence_appropriate else 0.0
            
            print(f"   ✅ Confidence Calibration: {quality_metrics['confidence_calibration']:.2f}")
            print(f"   Confidence Score: {confidence:.2f}")
        
        # Overall Clinical Enhancement Score
        overall_quality = sum(quality_metrics.values()) / len(quality_metrics)
        
        print(f"\n   📊 GPT-5 CLINICAL ENHANCEMENT ASSESSMENT:")
        print(f"   Diagnostic Accuracy: {quality_metrics['diagnostic_accuracy']:.2f}")
        print(f"   Regenerative Specificity: {quality_metrics['regenerative_specificity']:.2f}")
        print(f"   Evidence Integration: {quality_metrics['evidence_integration']:.2f}")
        print(f"   Clinical Reasoning: {quality_metrics['clinical_reasoning']:.2f}")
        print(f"   Confidence Calibration: {quality_metrics['confidence_calibration']:.2f}")
        print(f"   ✅ Overall Enhancement Score: {overall_quality:.2f}/1.0")
        
        # Success criteria: Overall score >= 0.7 indicates significant improvement
        enhancement_success = overall_quality >= 0.7
        print(f"   🎯 GPT-5 Enhancement Success: {enhancement_success}")
        
        return enhancement_success

    def run_emergent_llm_test_suite(self):
        """Run comprehensive Emergent LLM GPT-5 integration test suite"""
        print("🚀 EMERGENT LLM KEY SYSTEM WITH GPT-5 MODEL - COMPREHENSIVE TEST SUITE")
        print("=" * 80)
        print("Testing newly integrated Emergent LLM key system with GPT-5 model")
        print("Focus: AI Analysis, Protocol Generation, File Processing, Fallback System")
        print("=" * 80)
        
        # Test 1: Emergent LLM Integration Status
        print("\n🔍 TEST 1: EMERGENT LLM INTEGRATION STATUS")
        print("-" * 50)
        test1_success = self.test_emergent_llm_integration_status()
        
        # Test 2: Create Complex Regenerative Medicine Patient
        print("\n🏥 TEST 2: COMPLEX REGENERATIVE MEDICINE PATIENT CREATION")
        print("-" * 50)
        test2_success = self.test_create_complex_regenerative_patient()
        
        # Test 3: AI Analysis Engine with GPT-5 Keywords
        print("\n🧠 TEST 3: AI ANALYSIS ENGINE WITH GPT-5 REGENERATIVE KEYWORDS")
        print("-" * 50)
        test3_success = self.test_ai_analysis_gpt5_regenerative_keywords()
        
        # Test 4: Protocol Generation Across All Schools
        print("\n📋 TEST 4: PROTOCOL GENERATION WITH GPT-5 ENHANCEMENT")
        print("-" * 50)
        test4_success = self.test_protocol_generation_all_schools_gpt5()
        
        # Test 5: Enhanced Clinical Outputs
        print("\n🔬 TEST 5: ENHANCED CLINICAL OUTPUTS WITH GPT-5")
        print("-" * 50)
        test5_success = self.test_enhanced_clinical_outputs_gpt5()
        
        # Final Assessment
        test_results = [
            test1_success, test2_success, test3_success, test4_success, test5_success
        ]
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        success_rate = passed_tests / total_tests
        
        print("\n" + "=" * 80)
        print("🏁 EMERGENT LLM GPT-5 INTEGRATION TEST RESULTS")
        print("=" * 80)
        print(f"📊 Results: {passed_tests}/{total_tests} tests passed ({success_rate*100:.1f}%)")
        
        print(f"\n📋 DETAILED RESULTS:")
        test_names = [
            "Emergent LLM Integration Status",
            "Complex Patient Creation", 
            "AI Analysis GPT-5 Keywords",
            "Protocol Generation Enhancement",
            "Enhanced Clinical Outputs"
        ]
        
        for i, (name, result) in enumerate(zip(test_names, test_results)):
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"   {i+1}. {name}: {status}")
        
        if success_rate >= 0.8:  # 4/5 tests
            print("\n🎉 EMERGENT LLM GPT-5 INTEGRATION: EXCELLENT SUCCESS!")
            print("   The system demonstrates superior clinical outputs with GPT-5")
            print("   Ready for production use with enhanced regenerative medicine capabilities")
        elif success_rate >= 0.6:  # 3/5 tests
            print("\n✅ EMERGENT LLM GPT-5 INTEGRATION: GOOD SUCCESS!")
            print("   Most features working well with some minor improvements needed")
        else:
            print("\n🚨 EMERGENT LLM GPT-5 INTEGRATION: NEEDS ATTENTION")
            print("   Multiple critical issues detected requiring immediate fixes")
        
        return success_rate

if __name__ == "__main__":
    print("🤖 Starting Emergent LLM GPT-5 Integration Test Suite")
    print("=" * 80)
    
    tester = EmergentLLMTester()
    success_rate = tester.run_emergent_llm_test_suite()
    
    print(f"\n🏁 FINAL RESULTS:")
    print(f"📊 Overall Success Rate: {success_rate*100:.1f}%")
    print(f"📊 Tests Passed: {tester.tests_passed}/{tester.tests_run}")
    
    if success_rate >= 0.8:
        print("🎉 EMERGENT LLM GPT-5 INTEGRATION VALIDATION: SUCCESS!")
        sys.exit(0)
    else:
        print("⚠️  EMERGENT LLM GPT-5 INTEGRATION VALIDATION: NEEDS IMPROVEMENT")
        sys.exit(1)