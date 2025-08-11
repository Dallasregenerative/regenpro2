#!/usr/bin/env python3
"""
DETAILED PROTOCOL GENERATION REALITY CHECK
Tests if protocols are genuinely AI-generated or templates
"""

import requests
import json
import hashlib

def test_protocol_generation_reality():
    base_url = "https://9add4fe9-ec95-4c25-945f-328dd5122e17.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer demo-token'}
    
    print("🔍 DETAILED PROTOCOL GENERATION REALITY CHECK")
    print("=" * 60)
    
    # Create two very different patients
    patients = [
        {
            "demographics": {"name": "Young Athlete Test", "age": "22", "gender": "Male"},
            "chief_complaint": "Acute ACL tear from soccer injury",
            "history_present_illness": "Sudden knee injury during competitive soccer match",
            "past_medical_history": [],
            "medications": [],
            "symptoms": ["knee instability", "acute pain", "swelling"]
        },
        {
            "demographics": {"name": "Senior Patient Test", "age": "78", "gender": "Female"},
            "chief_complaint": "Chronic severe hip arthritis with mobility issues",
            "history_present_illness": "Progressive hip degeneration over 15 years",
            "past_medical_history": ["Osteoporosis", "Heart Disease", "Diabetes", "Kidney Disease"],
            "medications": ["Warfarin", "Insulin", "Metformin", "Alendronate"],
            "symptoms": ["severe hip pain", "limited walking", "dependency on walker"]
        }
    ]
    
    protocols_generated = []
    
    for i, patient_data in enumerate(patients):
        patient_type = "young_athlete" if i == 0 else "elderly_patient"
        print(f"\n🧪 Testing {patient_type}...")
        
        try:
            # Create patient
            response = requests.post(f"{api_url}/patients", json=patient_data, headers=headers, timeout=30)
            if response.status_code != 200:
                print(f"❌ Failed to create {patient_type}")
                continue
                
            patient_id = response.json().get('patient_id')
            print(f"   Created patient: {patient_id}")
            
            # Generate protocol for each school of thought
            schools = ["traditional_autologous", "biologics", "ai_optimized"]
            patient_protocols = []
            
            for school in schools:
                protocol_data = {"patient_id": patient_id, "school_of_thought": school}
                response = requests.post(f"{api_url}/protocols/generate", 
                                       json=protocol_data, headers=headers, timeout=45)
                
                if response.status_code == 200:
                    protocol = response.json()
                    
                    # Extract key protocol elements for comparison
                    protocol_summary = {
                        "patient_type": patient_type,
                        "school": school,
                        "steps": protocol.get('protocol_steps', []),
                        "reasoning": protocol.get('ai_reasoning', ''),
                        "confidence": protocol.get('confidence_score', 0),
                        "contraindications": protocol.get('contraindications', []),
                        "cost_estimate": protocol.get('cost_estimate', ''),
                        "expected_outcomes": protocol.get('expected_outcomes', [])
                    }
                    
                    patient_protocols.append(protocol_summary)
                    print(f"   ✅ Generated {school} protocol")
                else:
                    print(f"   ❌ Failed to generate {school} protocol")
            
            protocols_generated.append({
                "patient_type": patient_type,
                "protocols": patient_protocols
            })
            
        except Exception as e:
            print(f"❌ Error testing {patient_type}: {str(e)}")
    
    # REALITY ANALYSIS
    print(f"\n🎯 PROTOCOL GENERATION REALITY ANALYSIS")
    print("=" * 60)
    
    if len(protocols_generated) >= 2:
        young_protocols = protocols_generated[0]['protocols']
        elderly_protocols = protocols_generated[1]['protocols']
        
        # Check 1: Do protocols vary by patient age/condition?
        if young_protocols and elderly_protocols:
            young_reasoning = ' '.join([p['reasoning'] for p in young_protocols]).lower()
            elderly_reasoning = ' '.join([p['reasoning'] for p in elderly_protocols]).lower()
            
            # Check for age-specific content
            young_specific = any(term in young_reasoning for term in ['young', 'athlete', 'acute', 'soccer', 'acl'])
            elderly_specific = any(term in elderly_reasoning for term in ['elderly', 'senior', 'chronic', 'arthritis', 'hip'])
            
            if young_specific and elderly_specific:
                print("✅ GENUINE: Protocols are patient-specific (age/condition appropriate)")
            else:
                print("❌ TEMPLATE: Protocols appear generic regardless of patient")
        
        # Check 2: Do protocols vary by school of thought?
        if len(young_protocols) >= 2:
            school_variations = []
            for i in range(len(young_protocols)-1):
                steps1 = json.dumps(young_protocols[i]['steps'], sort_keys=True)
                steps2 = json.dumps(young_protocols[i+1]['steps'], sort_keys=True)
                school_variations.append(steps1 != steps2)
            
            if any(school_variations):
                print("✅ GENUINE: Protocols vary meaningfully by school of thought")
            else:
                print("❌ TEMPLATE: Protocols identical across schools of thought")
        
        # Check 3: Are contraindications patient-specific?
        all_contraindications = []
        for patient_data in protocols_generated:
            for protocol in patient_data['protocols']:
                all_contraindications.extend(protocol.get('contraindications', []))
        
        unique_contraindications = set(all_contraindications)
        if len(unique_contraindications) > 3:
            print(f"✅ GENUINE: Diverse contraindications identified ({len(unique_contraindications)} unique)")
        else:
            print(f"❌ TEMPLATE: Limited contraindication variety ({len(unique_contraindications)} unique)")
        
        # Check 4: Are cost estimates realistic and varied?
        cost_estimates = []
        for patient_data in protocols_generated:
            for protocol in patient_data['protocols']:
                cost = protocol.get('cost_estimate', '')
                if cost and cost != 'Variable based on selected therapies':
                    cost_estimates.append(cost)
        
        if len(set(cost_estimates)) > 1:
            print(f"✅ GENUINE: Varied cost estimates ({len(set(cost_estimates))} different estimates)")
        else:
            print(f"❌ TEMPLATE: Generic or identical cost estimates")
    
    else:
        print("❌ INSUFFICIENT DATA: Could not generate enough protocols for comparison")

if __name__ == "__main__":
    test_protocol_generation_reality()