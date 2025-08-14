#!/usr/bin/env python3

import requests
import json
import sys

def test_7_section_protocol():
    """Test the enhanced 7-section protocol generation system"""
    
    base_url = "https://a5405ec9-bfc7-45f4-af6d-6fb1a12b2148.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer demo-token'
    }
    
    print("🔍 ENHANCED 7-SECTION PROTOCOL GENERATION TESTING")
    print("=" * 60)
    
    # Step 1: Create John Hudson patient
    print("Step 1: Creating John Hudson patient...")
    
    john_hudson_data = {
        "demographics": {
            "name": "John Hudson",
            "age": "52",
            "gender": "Male",
            "occupation": "Executive",
            "insurance": "Self-pay"
        },
        "chief_complaint": "Multiple regenerative medicine needs including chronic shoulder injury, metabolic dysfunction, and chronic pain seeking comprehensive regenerative optimization",
        "history_present_illness": "52-year-old executive with complex medical history including chronic right shoulder injury from tennis (18 months duration), metabolic dysfunction with elevated inflammatory markers, chronic lower back pain affecting work performance, and seeking comprehensive regenerative medicine optimization. Failed multiple conservative treatments including physical therapy, NSAIDs, and corticosteroid injections. Specifically interested in comprehensive cellular therapy approach with PRP, BMAC, and advanced peptide protocols.",
        "past_medical_history": [
            "Chronic rotator cuff tendinopathy", 
            "Metabolic syndrome", 
            "Chronic lower back pain", 
            "Hypertension", 
            "Insulin resistance",
            "Previous tennis injuries"
        ],
        "medications": [
            "Metformin 1000mg BID", 
            "Lisinopril 10mg daily", 
            "Atorvastatin 20mg daily",
            "Ibuprofen PRN",
            "Omega-3 supplements"
        ],
        "allergies": ["NKDA"],
        "vital_signs": {
            "temperature": "98.6",
            "blood_pressure": "142/88",
            "heart_rate": "76",
            "respiratory_rate": "16",
            "oxygen_saturation": "98",
            "weight": "195",
            "height": "6'1\"",
            "BMI": "25.7"
        },
        "symptoms": [
            "chronic right shoulder pain",
            "decreased shoulder range of motion", 
            "chronic lower back pain",
            "fatigue",
            "metabolic dysfunction",
            "inflammatory markers elevation",
            "decreased exercise tolerance"
        ],
        "lab_results": {
            "inflammatory_markers": {
                "CRP": "4.2 mg/L",
                "ESR": "28 mm/hr",
                "IL-6": "3.8 pg/mL"
            },
            "metabolic_panel": {
                "glucose": "118 mg/dL",
                "HbA1c": "6.1%",
                "insulin": "18.5 mU/L",
                "HOMA-IR": "5.1"
            },
            "complete_blood_count": {
                "WBC": "7.2 K/uL",
                "RBC": "4.6 M/uL",
                "platelets": "320 K/uL",
                "hemoglobin": "14.8 g/dL"
            },
            "regenerative_markers": {
                "PDGF": "52 pg/mL",
                "VEGF": "145 pg/mL",
                "IGF-1": "165 ng/mL",
                "vitamin_D": "28 ng/mL"
            }
        },
        "imaging_data": [
            {
                "type": "MRI",
                "location": "right shoulder",
                "findings": "Partial thickness rotator cuff tear involving supraspinatus tendon, moderate subacromial impingement, mild glenohumeral arthritis with cartilage thinning",
                "date": "2024-01-25"
            },
            {
                "type": "MRI",
                "location": "lumbar spine",
                "findings": "L4-L5 disc degeneration with mild central stenosis, facet joint arthropathy, no nerve root compression",
                "date": "2024-02-10"
            }
        ],
        "genetic_data": {
            "regenerative_markers": {
                "VEGF_polymorphism": "positive",
                "collagen_synthesis_genes": "favorable",
                "inflammatory_response_genes": "moderate_risk",
                "healing_capacity_markers": "above_average"
            }
        }
    }
    
    try:
        response = requests.post(
            f"{api_url}/patients",
            json=john_hudson_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            patient_data = response.json()
            patient_id = patient_data.get('patient_id')
            print(f"✅ John Hudson created with ID: {patient_id}")
        else:
            print(f"❌ Failed to create patient: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating patient: {str(e)}")
        return False
    
    # Step 2: Generate protocol with enhanced 7-section format
    print("\nStep 2: Generating enhanced 7-section protocol...")
    print("This may take 60-90 seconds for comprehensive GPT-5 protocol generation...")
    
    protocol_data = {
        "patient_id": patient_id,
        "school_of_thought": "traditional_autologous"
    }
    
    try:
        response = requests.post(
            f"{api_url}/protocols/generate",
            json=protocol_data,
            headers=headers,
            timeout=120
        )
        
        if response.status_code == 200:
            protocol_response = response.json()
            print(f"✅ Protocol generated successfully")
            
            # Step 3: Validate 7-section format
            print("\nStep 3: Validating 7-section document format...")
            
            ai_reasoning = protocol_response.get('ai_reasoning', '')
            protocol_steps = protocol_response.get('protocol_steps', [])
            confidence_score = protocol_response.get('confidence_score', 0)
            
            print(f"Protocol ID: {protocol_response.get('protocol_id', 'Unknown')}")
            print(f"Confidence Score: {confidence_score:.2f}")
            print(f"Protocol Steps: {len(protocol_steps)}")
            print(f"AI Reasoning Length: {len(ai_reasoning)} characters")
            
            # Validation criteria
            validation_results = {}
            
            # 1. Check for 7-section format
            section_keywords = [
                "Section 1", "Section 2", "Section 3", "Section 4", 
                "Section 5", "Section 6", "Section 7"
            ]
            sections_found = sum(1 for keyword in section_keywords if keyword in ai_reasoning)
            validation_results['7_section_format'] = sections_found >= 7
            print(f"✅ 7-Section Format: {validation_results['7_section_format']} ({sections_found}/7 sections found)")
            
            # 2. Check for patient name personalization
            john_hudson_mentions = ai_reasoning.count("John Hudson")
            validation_results['patient_personalization'] = john_hudson_mentions >= 5
            print(f"✅ Patient Personalization: {validation_results['patient_personalization']} (John Hudson mentioned {john_hudson_mentions} times)")
            
            # 3. Check for comprehensive word count (3,000+ words)
            word_count = len(ai_reasoning.split())
            validation_results['comprehensive_length'] = word_count >= 3000
            print(f"✅ Comprehensive Length: {validation_results['comprehensive_length']} ({word_count} words, target: 3,000+)")
            
            # 4. Check for specific clinical details
            clinical_details = [
                "2-3 million", "WJ-MSCs", "BPC-157", "250-500 mcg", 
                "PI3K/Akt", "Wnt/β-catenin", "mTOR", "specific cell counts"
            ]
            clinical_details_found = sum(1 for detail in clinical_details if detail in ai_reasoning)
            validation_results['clinical_detail_level'] = clinical_details_found >= 3
            print(f"✅ Clinical Detail Level: {validation_results['clinical_detail_level']} ({clinical_details_found}/8 specific details found)")
            
            # 5. Check for scientific mechanisms
            scientific_mechanisms = [
                "pathway", "mechanism", "cellular", "molecular", "regenerative", 
                "growth factor", "stem cell", "tissue engineering"
            ]
            mechanisms_found = sum(1 for mechanism in scientific_mechanisms if mechanism.lower() in ai_reasoning.lower())
            validation_results['scientific_mechanisms'] = mechanisms_found >= 5
            print(f"✅ Scientific Mechanisms: {validation_results['scientific_mechanisms']} ({mechanisms_found}/8 mechanisms found)")
            
            # Overall assessment
            total_criteria = len(validation_results)
            passed_criteria = sum(1 for passed in validation_results.values() if passed)
            success_rate = passed_criteria / total_criteria
            
            print(f"\n📊 VALIDATION RESULTS: {passed_criteria}/{total_criteria} criteria met ({success_rate*100:.1f}%)")
            
            for criterion, passed in validation_results.items():
                status = "✅ PASSED" if passed else "❌ FAILED"
                print(f"   {status}: {criterion.replace('_', ' ').title()}")
            
            # Final determination
            overall_success = success_rate >= 0.6  # 60% threshold for success
            
            print(f"\n🎯 FINAL RESULT:")
            if overall_success:
                print("🎉 ENHANCED 7-SECTION PROTOCOL GENERATION: SUCCESS!")
                print("The GPT-5 enhanced prompts are generating comprehensive patient education documents")
                print("with improved 7-section format and detailed clinical content.")
            else:
                print("🚨 ENHANCED 7-SECTION PROTOCOL GENERATION: NEEDS IMPROVEMENT")
                print("The comprehensive document format requires further development.")
            
            # Show a sample of the AI reasoning for manual inspection
            if ai_reasoning:
                print(f"\n📄 SAMPLE AI REASONING (first 500 characters):")
                print(f"{ai_reasoning[:500]}...")
            
            return overall_success
            
        else:
            print(f"❌ Failed to generate protocol: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating protocol: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_7_section_protocol()
    
    print("\n" + "=" * 60)
    print("🏁 Enhanced 7-Section Protocol Test Complete")
    
    if success:
        print("🎉 SUCCESS: Enhanced 7-section protocol generation is working!")
        sys.exit(0)
    else:
        print("⚠️  NEEDS IMPROVEMENT: Enhanced 7-section format requires further development")
        sys.exit(1)