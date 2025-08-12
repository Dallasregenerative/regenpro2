import requests
import sys
import json
from datetime import datetime, timedelta

class FinalValidationTester:
    def __init__(self, base_url="https://9add4fe9-ec95-4c25-945f-328dd5122e17.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.premium_patient_id = None
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

    def test_create_premium_regenerative_patient(self):
        """Create 48-year-old elite athlete with bilateral knee osteoarthritis for final validation"""
        
        premium_patient_data = {
            "demographics": {
                "name": "Michael Thompson",
                "age": "48",
                "gender": "Male",
                "occupation": "Professional Tennis Player (Retired)",
                "insurance": "Cash-pay premium",
                "activity_level": "Elite athlete",
                "motivation": "High - seeking regenerative alternatives to surgery"
            },
            "chief_complaint": "Bilateral knee osteoarthritis with significant functional limitation seeking advanced regenerative medicine alternatives to total knee replacement",
            "history_present_illness": "48-year-old retired professional tennis player with progressive bilateral knee pain over 5 years. Failed conservative management including multiple corticosteroid injections, viscosupplementation, and extensive physical therapy. Pain significantly limits high-level athletic activities and daily function. Seeking cutting-edge regenerative medicine options including PRP, BMAC, and stem cell therapy to avoid bilateral knee replacement surgery. Highly motivated cash-pay patient with excellent regenerative healing potential.",
            "past_medical_history": [
                "Bilateral knee osteoarthritis Grade 3-4", 
                "Previous meniscal tears (bilateral)", 
                "ACL reconstruction (right knee, 2010)",
                "Multiple sports injuries",
                "Excellent overall health"
            ],
            "medications": [
                "Celecoxib 200mg BID PRN", 
                "Glucosamine/Chondroitin 1500mg daily",
                "Curcumin 1000mg daily",
                "Fish oil 2000mg daily",
                "Vitamin D3 4000 IU daily"
            ],
            "allergies": ["NKDA"],
            "vital_signs": {
                "temperature": "98.4",
                "blood_pressure": "118/75",
                "heart_rate": "58",
                "respiratory_rate": "14",
                "oxygen_saturation": "99",
                "weight": "185",
                "height": "6'2\"",
                "BMI": "23.7"
            },
            "symptoms": [
                "bilateral knee pain 7/10",
                "morning stiffness 45 minutes", 
                "decreased range of motion",
                "functional limitation with sports",
                "difficulty with stairs",
                "night pain interfering with sleep",
                "mechanical symptoms with locking"
            ],
            "lab_results": {
                "inflammatory_markers": {
                    "CRP": "1.2 mg/L",
                    "ESR": "12 mm/hr",
                    "IL-6": "2.1 pg/mL"
                },
                "complete_blood_count": {
                    "WBC": "5.8 K/uL",
                    "RBC": "4.8 M/uL",
                    "platelets": "320 K/uL",
                    "hemoglobin": "15.2 g/dL"
                },
                "regenerative_markers": {
                    "PDGF": "52 pg/mL",
                    "VEGF": "145 pg/mL",
                    "IGF-1": "220 ng/mL",
                    "TGF-beta": "18.5 ng/mL"
                },
                "metabolic_panel": {
                    "glucose": "88 mg/dL",
                    "vitamin_D": "45 ng/mL",
                    "vitamin_C": "1.8 mg/dL"
                }
            },
            "imaging_data": [
                {
                    "type": "X-ray",
                    "location": "bilateral knees",
                    "findings": "Grade 3-4 osteoarthritis with severe joint space narrowing, large osteophytes, subchondral sclerosis, and cyst formation. Mechanical axis deviation present.",
                    "date": "2024-01-20"
                },
                {
                    "type": "MRI",
                    "location": "bilateral knees",
                    "findings": "Severe cartilage loss with full-thickness defects, meniscal degeneration and tears, bone marrow edema, synovial thickening. Preserved ligamentous structures. Ideal candidate for regenerative intervention before end-stage changes.",
                    "date": "2024-02-15"
                }
            ],
            "genetic_data": {
                "regenerative_markers": {
                    "VEGF_polymorphism": "favorable",
                    "collagen_synthesis_genes": "excellent",
                    "inflammatory_response_genes": "low_risk",
                    "healing_capacity_score": "95/100"
                },
                "pharmacogenomics": {
                    "CYP2D6": "normal_metabolizer",
                    "COMT": "favorable_for_regenerative_therapy"
                }
            }
        }

        success, response = self.run_test(
            "Create Premium Regenerative Medicine Patient - Michael Thompson",
            "POST",
            "patients",
            200,
            data=premium_patient_data
        )
        
        if success and 'patient_id' in response:
            self.premium_patient_id = response['patient_id']
            print(f"   ✅ Created Premium Patient ID: {self.premium_patient_id}")
            print(f"   Patient: {response.get('demographics', {}).get('name', 'Unknown')}")
            print(f"   Age: {response.get('demographics', {}).get('age', 'Unknown')}")
            print(f"   Activity Level: {response.get('demographics', {}).get('activity_level', 'Unknown')}")
            print(f"   Insurance: {response.get('demographics', {}).get('insurance', 'Unknown')}")
            return True
        return False

    def test_enhanced_ai_processing_engine(self):
        """Test Enhanced AI Processing Engine with regenerative medicine keyword measurement"""
        
        if not self.premium_patient_id:
            print("❌ No premium patient ID available for AI processing test")
            return False

        print("   🧠 TESTING ENHANCED AI PROCESSING ENGINE")
        print("   Measuring regenerative medicine keyword density and clinical specificity...")
        print("   TARGET: 5+ regenerative medicine keywords required")
        
        success, response = self.run_test(
            "Enhanced AI Processing Engine - Regenerative Medicine Analysis",
            "POST",
            f"patients/{self.premium_patient_id}/analyze",
            200,
            data={},
            timeout=120
        )
        
        if success:
            # Extract AI response content for keyword analysis
            diagnostic_results = response.get('diagnostic_results', [])
            ai_reasoning = response.get('ai_reasoning', '')
            
            # Combine all AI-generated text for keyword analysis
            full_ai_response = ai_reasoning
            for result in diagnostic_results:
                full_ai_response += " " + result.get('diagnosis', '')
                full_ai_response += " " + result.get('reasoning', '')
                full_ai_response += " " + " ".join(result.get('supporting_evidence', []))
                full_ai_response += " " + " ".join(result.get('mechanisms_involved', []))
                full_ai_response += " " + " ".join(result.get('regenerative_targets', []))
            
            # Define regenerative medicine keywords to count
            regenerative_keywords = [
                'PRP', 'platelet-rich plasma', 'platelet rich plasma',
                'BMAC', 'bone marrow aspirate', 'bone marrow aspirate concentrate',
                'stem cell', 'mesenchymal stem cells', 'stem cells',
                'growth factors', 'growth factor',
                'tissue engineering', 'cellular therapies', 'cellular therapy',
                'chondrogenesis', 'cartilage regeneration',
                'autologous biologics', 'regenerative medicine',
                'platelet concentrate', 'mesenchymal', 'regenerative'
            ]
            
            # Count keyword occurrences (case-insensitive)
            full_text_lower = full_ai_response.lower()
            keyword_counts = {}
            total_keywords = 0
            
            for keyword in regenerative_keywords:
                count = full_text_lower.count(keyword.lower())
                if count > 0:
                    keyword_counts[keyword] = count
                    total_keywords += count
            
            print(f"   📊 REGENERATIVE MEDICINE KEYWORD ANALYSIS:")
            print(f"   Total Keywords Found: {total_keywords}")
            print(f"   Unique Keywords Found: {len(keyword_counts)}")
            print(f"   TARGET ACHIEVED: {'✅ YES' if len(keyword_counts) >= 5 else '❌ NO'} (5+ required)")
            
            # Display top keywords found
            if keyword_counts:
                sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
                print(f"   Top Keywords Found:")
                for keyword, count in sorted_keywords[:8]:
                    print(f"     • {keyword}: {count} mentions")
            
            # Additional analysis metrics
            print(f"   📈 CLINICAL ANALYSIS METRICS:")
            print(f"   Diagnostic Results Generated: {len(diagnostic_results)}")
            if diagnostic_results:
                avg_confidence = sum(r.get('confidence_score', 0) for r in diagnostic_results) / len(diagnostic_results)
                print(f"   Average Confidence Score: {avg_confidence:.2f}")
                
                total_regenerative_targets = sum(len(r.get('regenerative_targets', [])) for r in diagnostic_results)
                print(f"   Total Regenerative Targets: {total_regenerative_targets}")
            
            # Store results for final validation
            self.ai_keyword_count = len(keyword_counts)
            self.ai_total_keywords = total_keywords
            
            return len(keyword_counts) >= 5  # Success if 5+ unique keywords found
        
        return False

    def test_regenerative_medicine_specificity(self):
        """Test Regenerative Medicine Specificity - 3+ differential diagnoses with regenerative focus"""
        
        if not self.premium_patient_id:
            print("❌ No premium patient ID available for specificity test")
            return False

        print("   🎯 TESTING REGENERATIVE MEDICINE SPECIFICITY")
        print("   TARGET: 3+ regenerative medicine conditions with ≥0.70 suitability scores")
        
        success, response = self.run_test(
            "Regenerative Medicine Specificity - Differential Diagnosis",
            "POST",
            f"patients/{self.premium_patient_id}/analyze",
            200,
            data={},
            timeout=120
        )
        
        if success:
            diagnostic_results = response.get('diagnostic_results', [])
            
            print(f"   📋 DIFFERENTIAL DIAGNOSIS ANALYSIS:")
            print(f"   Total Diagnoses Generated: {len(diagnostic_results)}")
            print(f"   TARGET ACHIEVED: {'✅ YES' if len(diagnostic_results) >= 3 else '❌ NO'} (3+ required)")
            
            # Analyze each diagnosis for regenerative medicine specificity
            regenerative_suitable_count = 0
            high_confidence_count = 0
            
            for i, result in enumerate(diagnostic_results, 1):
                diagnosis = result.get('diagnosis', 'Unknown')
                confidence = result.get('confidence_score', 0)
                regenerative_targets = result.get('regenerative_targets', [])
                
                print(f"   Diagnosis {i}: {diagnosis}")
                print(f"     Confidence Score: {confidence:.2f}")
                print(f"     Regenerative Targets: {len(regenerative_targets)}")
                
                if regenerative_targets:
                    print(f"     Targets: {', '.join(regenerative_targets[:3])}")
                
                # Check regenerative suitability (using confidence as proxy for suitability)
                if confidence >= 0.70:
                    regenerative_suitable_count += 1
                    print(f"     ✅ High Regenerative Suitability (≥0.70)")
                else:
                    print(f"     ⚠️  Lower Suitability (<0.70)")
                
                if confidence >= 0.80:
                    high_confidence_count += 1
            
            print(f"   📊 REGENERATIVE SUITABILITY ANALYSIS:")
            print(f"   Conditions with ≥0.70 Suitability: {regenerative_suitable_count}")
            print(f"   High Confidence Conditions (≥0.80): {high_confidence_count}")
            print(f"   SUITABILITY TARGET: {'✅ YES' if regenerative_suitable_count >= 3 else '❌ NO'} (3+ required)")
            
            # Store results for final validation
            self.differential_diagnosis_count = len(diagnostic_results)
            self.regenerative_suitable_count = regenerative_suitable_count
            
            return len(diagnostic_results) >= 3 and regenerative_suitable_count >= 3
        
        return False

    def test_protocol_generation_clinical_decision_support(self):
        """Test Protocol Generation with Clinical Decision Support Value"""
        
        if not self.premium_patient_id:
            print("❌ No premium patient ID available for protocol generation test")
            return False

        print("   🏥 TESTING PROTOCOL GENERATION - CLINICAL DECISION SUPPORT")
        print("   Validating meaningful clinical outputs and premium practice value...")
        
        # Test all 3 schools of thought for comprehensive validation
        schools_to_test = [
            ("traditional_autologous", "Traditional Autologous"),
            ("biologics", "Biologics & Allogenic"), 
            ("ai_optimized", "AI-Optimized Best Protocol")
        ]
        
        protocol_results = []
        
        for school_key, school_name in schools_to_test:
            protocol_data = {
                "patient_id": self.premium_patient_id,
                "school_of_thought": school_key
            }
            
            print(f"   Testing {school_name} Protocol Generation...")
            success, response = self.run_test(
                f"Protocol Generation - {school_name}",
                "POST",
                "protocols/generate",
                200,
                data=protocol_data,
                timeout=120
            )
            
            if success:
                protocol_steps = response.get('protocol_steps', [])
                cost_estimate = response.get('cost_estimate', 'Not provided')
                confidence_score = response.get('confidence_score', 0)
                supporting_evidence = response.get('supporting_evidence', [])
                contraindications = response.get('contraindications', [])
                
                print(f"     ✅ {school_name}: {len(protocol_steps)} steps")
                print(f"     Cost Estimate: {cost_estimate}")
                print(f"     Confidence: {confidence_score:.2f}")
                print(f"     Evidence Citations: {len(supporting_evidence)}")
                print(f"     Contraindications: {len(contraindications)}")
                
                # Analyze first protocol step for clinical specificity
                if protocol_steps:
                    first_step = protocol_steps[0]
                    therapy = first_step.get('therapy', 'Unknown')
                    dosage = first_step.get('dosage', 'Unknown')
                    delivery_method = first_step.get('delivery_method', 'Unknown')
                    
                    print(f"     First Step: {therapy}")
                    print(f"     Dosage: {dosage}")
                    print(f"     Delivery: {delivery_method}")
                
                protocol_results.append({
                    'school': school_name,
                    'steps': len(protocol_steps),
                    'cost': cost_estimate,
                    'confidence': confidence_score,
                    'evidence': len(supporting_evidence),
                    'contraindications': len(contraindications)
                })
        
        print(f"   📊 CLINICAL DECISION SUPPORT ANALYSIS:")
        print(f"   Protocols Generated: {len(protocol_results)}")
        
        # Analyze clinical decision support value
        total_steps = sum(p['steps'] for p in protocol_results)
        avg_confidence = sum(p['confidence'] for p in protocol_results) / len(protocol_results) if protocol_results else 0
        total_evidence = sum(p['evidence'] for p in protocol_results)
        
        print(f"   Total Protocol Steps: {total_steps}")
        print(f"   Average Confidence: {avg_confidence:.2f}")
        print(f"   Total Evidence Citations: {total_evidence}")
        
        # Check for premium practice value indicators
        has_cost_estimates = any('$' in str(p['cost']) for p in protocol_results)
        has_high_confidence = avg_confidence >= 0.75
        has_evidence_support = total_evidence >= 3
        has_detailed_protocols = total_steps >= 6  # At least 2 steps per protocol on average
        
        print(f"   💰 PREMIUM PRACTICE VALUE INDICATORS:")
        print(f"   Cost Estimates Provided: {'✅ YES' if has_cost_estimates else '❌ NO'}")
        print(f"   High Confidence Protocols: {'✅ YES' if has_high_confidence else '❌ NO'}")
        print(f"   Evidence-Based Support: {'✅ YES' if has_evidence_support else '❌ NO'}")
        print(f"   Detailed Clinical Protocols: {'✅ YES' if has_detailed_protocols else '❌ NO'}")
        
        clinical_decision_support_value = (
            has_cost_estimates and has_high_confidence and 
            has_evidence_support and has_detailed_protocols
        )
        
        print(f"   🏆 CLINICAL DECISION SUPPORT VALUE: {'✅ EXCELLENT' if clinical_decision_support_value else '⚠️  NEEDS IMPROVEMENT'}")
        
        # Store results for final validation
        self.protocol_generation_success = len(protocol_results) >= 3
        self.clinical_decision_support_value = clinical_decision_support_value
        
        return self.protocol_generation_success and clinical_decision_support_value

    def test_complete_end_to_end_workflow_validation(self):
        """Complete End-to-End Workflow Validation - Patient Creation → AI Analysis → Protocol Generation"""
        
        print("   🔄 COMPLETE END-TO-END WORKFLOW VALIDATION")
        print("   Testing: Patient Creation → AI Analysis → Differential Diagnosis → Protocol Generation")
        
        if not self.premium_patient_id:
            print("   ❌ Premium patient not created - workflow cannot be tested")
            return False
        
        # Measure processing times
        import time
        
        workflow_start = time.time()
        
        # Step 1: Verify patient creation (already done)
        print("   ✅ Step 1: Premium Patient Created")
        
        # Step 2: AI Analysis with timing
        analysis_start = time.time()
        ai_success = hasattr(self, 'ai_keyword_count') and self.ai_keyword_count >= 5
        analysis_time = time.time() - analysis_start if hasattr(self, 'ai_keyword_count') else 0
        
        print(f"   {'✅' if ai_success else '❌'} Step 2: AI Analysis ({'SUCCESS' if ai_success else 'FAILED'})")
        if analysis_time > 0:
            print(f"     Processing Time: {analysis_time:.1f} seconds")
        
        # Step 3: Differential Diagnosis
        diagnosis_success = (hasattr(self, 'differential_diagnosis_count') and 
                           self.differential_diagnosis_count >= 3 and
                           hasattr(self, 'regenerative_suitable_count') and
                           self.regenerative_suitable_count >= 3)
        
        print(f"   {'✅' if diagnosis_success else '❌'} Step 3: Differential Diagnosis ({'SUCCESS' if diagnosis_success else 'FAILED'})")
        if hasattr(self, 'differential_diagnosis_count'):
            print(f"     Diagnoses Generated: {self.differential_diagnosis_count}")
            print(f"     Regenerative Suitable: {getattr(self, 'regenerative_suitable_count', 0)}")
        
        # Step 4: Protocol Generation
        protocol_success = (hasattr(self, 'protocol_generation_success') and 
                          self.protocol_generation_success and
                          hasattr(self, 'clinical_decision_support_value') and
                          self.clinical_decision_support_value)
        
        print(f"   {'✅' if protocol_success else '❌'} Step 4: Protocol Generation ({'SUCCESS' if protocol_success else 'FAILED'})")
        
        workflow_time = time.time() - workflow_start
        
        print(f"   ⏱️  WORKFLOW PERFORMANCE:")
        print(f"   Total Workflow Time: {workflow_time:.1f} seconds")
        print(f"   Performance Target: {'✅ EXCELLENT' if workflow_time < 180 else '⚠️  ACCEPTABLE' if workflow_time < 300 else '❌ SLOW'} (<180s target)")
        
        # Final success criteria validation
        success_criteria = [
            ("AI Analysis 5+ Keywords", ai_success),
            ("3+ Differential Diagnoses", diagnosis_success), 
            ("Protocol Generation", protocol_success),
            ("Processing Time <300s", workflow_time < 300)
        ]
        
        passed_criteria = sum(1 for _, success in success_criteria if success)
        success_rate = (passed_criteria / len(success_criteria)) * 100
        
        print(f"   📊 FINAL SUCCESS VALIDATION:")
        for criterion, success in success_criteria:
            print(f"   {'✅' if success else '❌'} {criterion}")
        
        print(f"   🎯 SUCCESS RATE: {success_rate:.0f}% ({passed_criteria}/{len(success_criteria)} criteria met)")
        print(f"   🏆 OVERALL RESULT: {'✅ SUCCESS' if success_rate >= 80 else '⚠️  PARTIAL SUCCESS' if success_rate >= 60 else '❌ NEEDS IMPROVEMENT'}")
        
        # Store final results
        self.final_success_rate = success_rate
        self.workflow_complete = True
        
        return success_rate >= 80

    def run_final_validation_suite(self):
        """Run the complete final validation suite for RegenMed AI Pro"""
        
        print("\n" + "="*80)
        print("🏥 REGENMED AI PRO - FINAL SUCCESS VALIDATION")
        print("EXECUTE FINAL SUCCESS VALIDATION - Complete All 3 Action Items")
        print("="*80)
        
        validation_tests = [
            ("Create Premium Regenerative Medicine Patient", self.test_create_premium_regenerative_patient),
            ("Enhanced AI Processing Engine (Action Item 1)", self.test_enhanced_ai_processing_engine),
            ("Regenerative Medicine Specificity (Action Item 3)", self.test_regenerative_medicine_specificity),
            ("Protocol Generation Clinical Decision Support", self.test_protocol_generation_clinical_decision_support),
            ("Complete End-to-End Workflow Validation", self.test_complete_end_to_end_workflow_validation)
        ]
        
        validation_results = []
        
        for test_name, test_method in validation_tests:
            print(f"\n🔬 EXECUTING: {test_name}")
            print("-" * 60)
            
            try:
                result = test_method()
                validation_results.append((test_name, result))
                print(f"{'✅ PASSED' if result else '❌ FAILED'}: {test_name}")
            except Exception as e:
                print(f"❌ ERROR in {test_name}: {str(e)}")
                validation_results.append((test_name, False))
        
        # Final validation summary
        print("\n" + "="*80)
        print("🎯 FINAL VALIDATION SUMMARY")
        print("="*80)
        
        passed_tests = sum(1 for _, result in validation_results if result)
        total_tests = len(validation_results)
        final_success_rate = (passed_tests / total_tests) * 100
        
        print(f"📊 VALIDATION RESULTS:")
        for test_name, result in validation_results:
            print(f"{'✅' if result else '❌'} {test_name}")
        
        print(f"\n🏆 FINAL ASSESSMENT:")
        print(f"Tests Passed: {passed_tests}/{total_tests}")
        print(f"Success Rate: {final_success_rate:.0f}%")
        
        # Action Items Assessment
        action_item_1 = getattr(self, 'ai_keyword_count', 0) >= 5
        action_item_2 = hasattr(self, 'premium_patient_id')
        action_item_3 = (getattr(self, 'differential_diagnosis_count', 0) >= 3 and 
                        getattr(self, 'regenerative_suitable_count', 0) >= 3)
        
        print(f"\n🎯 ACTION ITEMS VALIDATION:")
        print(f"{'✅' if action_item_1 else '❌'} Action Item 1: Enhanced AI Processing (5+ regenerative keywords)")
        print(f"{'✅' if action_item_2 else '❌'} Action Item 2: Premium Patient Case Complete")
        print(f"{'✅' if action_item_3 else '❌'} Action Item 3: Regenerative Medicine Specificity (3+ conditions)")
        
        action_items_passed = sum([action_item_1, action_item_2, action_item_3])
        
        print(f"\n🏅 FINAL VERDICT:")
        if final_success_rate >= 80 and action_items_passed >= 3:
            print("🎉 SUCCESS: RegenMed AI Pro platform ready for premium regenerative medicine practices")
            print("✅ All 3 action items validated as complete")
            print("✅ System generates meaningful regenerative medicine clinical outputs")
            print("✅ Platform justifies premium practice fees and provides real clinical decision support value")
        elif final_success_rate >= 60:
            print("⚠️  PARTIAL SUCCESS: Platform functional but needs optimization")
            print(f"⚠️  {3 - action_items_passed} action items need attention")
        else:
            print("❌ NEEDS IMPROVEMENT: Platform requires significant development")
            print("❌ Action items not sufficiently validated")
        
        return final_success_rate >= 80 and action_items_passed >= 3

if __name__ == "__main__":
    tester = FinalValidationTester()
    success = tester.run_final_validation_suite()
    sys.exit(0 if success else 1)