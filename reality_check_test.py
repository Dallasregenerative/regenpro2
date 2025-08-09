#!/usr/bin/env python3
"""
COMPREHENSIVE BACKEND REALITY CHECK
Tests actual functionality vs claimed features to identify genuine vs mock implementations
"""

import requests
import json
import sys
from datetime import datetime
import time

class BackendRealityChecker:
    def __init__(self):
        self.base_url = "https://e39019a0-74aa-4828-80fe-b1e4b1fed539.preview.emergentagent.com"
        self.api_url = f"{self.base_url}/api"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer demo-token'
        }
        self.reality_score = 0
        self.total_checks = 0
        self.critical_issues = []
        self.genuine_features = []
        self.mock_features = []

    def log_reality_check(self, feature, is_genuine, details):
        """Log reality check results"""
        self.total_checks += 1
        if is_genuine:
            self.reality_score += 1
            self.genuine_features.append(f"✅ {feature}: {details}")
        else:
            self.mock_features.append(f"❌ {feature}: {details}")

    def test_protocol_generation_reality(self):
        """REALITY CHECK: Are protocols actually AI-generated or templates?"""
        print("\n🔍 PROTOCOL GENERATION REALITY CHECK")
        
        # Create test patient
        patient_data = {
            "demographics": {"name": "Reality Check Patient", "age": "45", "gender": "Male"},
            "chief_complaint": "Chronic shoulder pain from rotator cuff injury",
            "history_present_illness": "6-month history of progressive shoulder pain after sports injury",
            "past_medical_history": ["Diabetes Type 2", "Hypertension"],
            "medications": ["Metformin", "Lisinopril"],
            "allergies": ["Penicillin"],
            "symptoms": ["shoulder pain", "limited range of motion", "weakness"]
        }
        
        try:
            # Create patient
            response = requests.post(f"{self.api_url}/patients", json=patient_data, headers=self.headers, timeout=30)
            if response.status_code != 200:
                self.log_reality_check("Protocol Generation", False, "Cannot create test patient")
                return
            
            patient_id = response.json().get('patient_id')
            
            # Generate protocols with different schools - check for variation
            schools = ["traditional_autologous", "biologics", "ai_optimized"]
            protocols = []
            
            for school in schools:
                protocol_data = {"patient_id": patient_id, "school_of_thought": school}
                response = requests.post(f"{self.api_url}/protocols/generate", json=protocol_data, headers=self.headers, timeout=60)
                
                if response.status_code == 200:
                    protocol = response.json()
                    protocols.append({
                        "school": school,
                        "steps": protocol.get('protocol_steps', []),
                        "reasoning": protocol.get('ai_reasoning', ''),
                        "confidence": protocol.get('confidence_score', 0)
                    })
            
            # REALITY CHECK: Do protocols actually vary by school?
            if len(protocols) >= 2:
                step_variations = []
                reasoning_variations = []
                
                for i in range(len(protocols)-1):
                    # Check if protocol steps are different
                    steps1 = json.dumps(protocols[i]['steps'], sort_keys=True)
                    steps2 = json.dumps(protocols[i+1]['steps'], sort_keys=True)
                    step_variations.append(steps1 != steps2)
                    
                    # Check if AI reasoning is different
                    reasoning1 = protocols[i]['reasoning']
                    reasoning2 = protocols[i+1]['reasoning']
                    reasoning_variations.append(reasoning1 != reasoning2)
                
                if any(step_variations) and any(reasoning_variations):
                    self.log_reality_check("Protocol Generation", True, 
                        f"Protocols genuinely vary by school of thought - {len(protocols)} different protocols generated")
                else:
                    self.log_reality_check("Protocol Generation", False, 
                        "Protocols appear to be templates - no meaningful variation between schools")
            
            # REALITY CHECK: Are protocols patient-specific?
            if protocols:
                first_protocol = protocols[0]
                reasoning = first_protocol['reasoning'].lower()
                
                # Check if patient-specific data is referenced
                patient_specific_refs = [
                    "shoulder" in reasoning,
                    "rotator cuff" in reasoning,
                    "diabetes" in reasoning,
                    "45" in reasoning or "age" in reasoning,
                    "male" in reasoning or "gender" in reasoning
                ]
                
                if sum(patient_specific_refs) >= 2:
                    self.log_reality_check("Patient-Specific Protocols", True, 
                        f"Protocol references patient-specific data: {sum(patient_specific_refs)}/5 factors")
                else:
                    self.log_reality_check("Patient-Specific Protocols", False, 
                        "Protocol appears generic - minimal patient-specific references")
                        
        except Exception as e:
            self.log_reality_check("Protocol Generation", False, f"Error during testing: {str(e)}")

    def test_literature_integration_reality(self):
        """REALITY CHECK: Real PubMed data or mock responses?"""
        print("\n🔍 LITERATURE INTEGRATION REALITY CHECK")
        
        try:
            # Test PubMed search
            response = requests.get(f"{self.api_url}/literature/search?query=osteoarthritis%20PRP&limit=5", 
                                  headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                papers = data.get('papers', [])
                
                if papers:
                    # REALITY CHECK: Are PMIDs real?
                    pmids = [p.get('pmid') for p in papers if p.get('pmid')]
                    valid_pmids = [pmid for pmid in pmids if pmid.isdigit() and len(pmid) >= 7]
                    
                    # REALITY CHECK: Are abstracts substantial?
                    abstracts = [p.get('abstract', '') for p in papers]
                    substantial_abstracts = [abs for abs in abstracts if len(abs) > 200]
                    
                    # REALITY CHECK: Are authors real?
                    authors = []
                    for paper in papers:
                        paper_authors = paper.get('authors', [])
                        authors.extend(paper_authors)
                    
                    if len(valid_pmids) >= 3 and len(substantial_abstracts) >= 3:
                        self.log_reality_check("PubMed Integration", True, 
                            f"Real PMIDs ({len(valid_pmids)}), substantial abstracts ({len(substantial_abstracts)}), {len(authors)} authors")
                    else:
                        self.log_reality_check("PubMed Integration", False, 
                            f"Questionable data quality - PMIDs: {len(valid_pmids)}, abstracts: {len(substantial_abstracts)}")
                else:
                    self.log_reality_check("PubMed Integration", False, "No papers returned from search")
            
            # Test Google Scholar integration
            response = requests.get(f"{self.api_url}/literature/google-scholar-search?query=stem%20cell%20therapy&max_results=5", 
                                  headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                papers = data.get('papers', [])
                
                if papers:
                    # Check for Google Scholar specific features
                    citation_counts = [p.get('citation_count', 0) for p in papers]
                    valid_citations = [c for c in citation_counts if c > 0]
                    
                    if len(valid_citations) >= 2:
                        self.log_reality_check("Google Scholar Integration", True, 
                            f"Real citation data found: {len(valid_citations)} papers with citations")
                    else:
                        self.log_reality_check("Google Scholar Integration", False, 
                            "No citation data - may be mock implementation")
                        
        except Exception as e:
            self.log_reality_check("Literature Integration", False, f"Error during testing: {str(e)}")

    def test_ai_processing_reality(self):
        """REALITY CHECK: Genuine AI processing or predetermined responses?"""
        print("\n🔍 AI PROCESSING REALITY CHECK")
        
        try:
            # Create two very different patients
            patients = [
                {
                    "demographics": {"name": "Young Athlete", "age": "25", "gender": "Male"},
                    "chief_complaint": "Acute ACL tear from basketball injury",
                    "history_present_illness": "Sudden knee injury during sports",
                    "past_medical_history": [],
                    "medications": [],
                    "symptoms": ["knee instability", "swelling", "pain with movement"]
                },
                {
                    "demographics": {"name": "Elderly Patient", "age": "75", "gender": "Female"},
                    "chief_complaint": "Chronic hip arthritis with severe pain",
                    "history_present_illness": "Progressive hip pain over 10 years",
                    "past_medical_history": ["Osteoporosis", "Heart Disease", "Diabetes"],
                    "medications": ["Warfarin", "Insulin", "Alendronate"],
                    "symptoms": ["hip pain", "limited mobility", "difficulty walking"]
                }
            ]
            
            analyses = []
            for i, patient_data in enumerate(patients):
                # Create patient
                response = requests.post(f"{self.api_url}/patients", json=patient_data, headers=self.headers, timeout=30)
                if response.status_code != 200:
                    continue
                    
                patient_id = response.json().get('patient_id')
                
                # Analyze patient
                response = requests.post(f"{self.api_url}/patients/{patient_id}/analyze", 
                                       json={}, headers=self.headers, timeout=60)
                
                if response.status_code == 200:
                    analysis = response.json()
                    analyses.append({
                        "patient_type": "young_athlete" if i == 0 else "elderly_patient",
                        "diagnoses": analysis.get('diagnostic_results', []),
                        "reasoning": [d.get('reasoning', '') for d in analysis.get('diagnostic_results', [])]
                    })
            
            # REALITY CHECK: Do analyses differ meaningfully?
            if len(analyses) == 2:
                young_diagnoses = [d.get('diagnosis', '') for d in analyses[0]['diagnoses']]
                elderly_diagnoses = [d.get('diagnosis', '') for d in analyses[1]['diagnoses']]
                
                young_reasoning = ' '.join(analyses[0]['reasoning']).lower()
                elderly_reasoning = ' '.join(analyses[1]['reasoning']).lower()
                
                # Check for age-appropriate diagnoses
                young_appropriate = any(term in ' '.join(young_diagnoses).lower() for term in ['acl', 'ligament', 'sports', 'tear'])
                elderly_appropriate = any(term in ' '.join(elderly_diagnoses).lower() for term in ['arthritis', 'degenerative', 'osteo'])
                
                # Check for age-specific reasoning
                age_specific_reasoning = (
                    ("young" in young_reasoning or "athlete" in young_reasoning) and
                    ("elderly" in elderly_reasoning or "age" in elderly_reasoning)
                )
                
                if young_appropriate and elderly_appropriate and age_specific_reasoning:
                    self.log_reality_check("AI Diagnostic Processing", True, 
                        "AI generates age-appropriate diagnoses with specific reasoning")
                else:
                    self.log_reality_check("AI Diagnostic Processing", False, 
                        "AI responses appear generic - not patient-specific")
                        
        except Exception as e:
            self.log_reality_check("AI Processing", False, f"Error during testing: {str(e)}")

    def test_database_persistence_reality(self):
        """REALITY CHECK: Real database storage or session-only data?"""
        print("\n🔍 DATABASE PERSISTENCE REALITY CHECK")
        
        try:
            # Get existing patients
            response = requests.get(f"{self.api_url}/patients", headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                patients = response.json()
                
                if isinstance(patients, list) and len(patients) > 0:
                    # Check if patients have realistic data
                    patient_count = len(patients)
                    
                    # Check for data consistency
                    patient_ids = [p.get('patient_id') for p in patients]
                    unique_ids = set(patient_ids)
                    
                    # Check for realistic patient data
                    realistic_patients = 0
                    for patient in patients[:5]:  # Check first 5
                        demographics = patient.get('demographics', {})
                        if (demographics.get('name') and 
                            demographics.get('age') and 
                            patient.get('chief_complaint')):
                            realistic_patients += 1
                    
                    if len(unique_ids) == patient_count and realistic_patients >= min(3, patient_count):
                        self.log_reality_check("Database Persistence", True, 
                            f"{patient_count} patients with unique IDs and realistic data")
                    else:
                        self.log_reality_check("Database Persistence", False, 
                            "Patient data appears inconsistent or duplicated")
                        
                    # Test data retrieval consistency
                    if patients:
                        test_patient_id = patients[0].get('patient_id')
                        response = requests.get(f"{self.api_url}/patients/{test_patient_id}", 
                                              headers=self.headers, timeout=30)
                        
                        if response.status_code == 200:
                            retrieved_patient = response.json()
                            original_name = patients[0].get('demographics', {}).get('name')
                            retrieved_name = retrieved_patient.get('demographics', {}).get('name')
                            
                            if original_name == retrieved_name:
                                self.log_reality_check("Data Consistency", True, 
                                    "Patient data retrieval is consistent")
                            else:
                                self.log_reality_check("Data Consistency", False, 
                                    "Patient data inconsistent between list and individual retrieval")
                else:
                    self.log_reality_check("Database Persistence", False, "No patients found in database")
                    
        except Exception as e:
            self.log_reality_check("Database Persistence", False, f"Error: {str(e)}")

    def test_advanced_features_reality(self):
        """REALITY CHECK: Are advanced features functional or placeholders?"""
        print("\n🔍 ADVANCED FEATURES REALITY CHECK")
        
        # Test Federated Learning
        try:
            response = requests.get(f"{self.api_url}/federated/global-model-status", 
                                  headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if (data.get('participants', 0) > 0 and 
                    data.get('model_version') and 
                    data.get('status') == 'active'):
                    self.log_reality_check("Federated Learning", True, 
                        f"Active with {data.get('participants')} participants, version {data.get('model_version')}")
                else:
                    self.log_reality_check("Federated Learning", False, 
                        "No active participants or inactive status")
        except:
            self.log_reality_check("Federated Learning", False, "Service unavailable")
        
        # Test Clinical Trials Integration
        try:
            response = requests.get(f"{self.api_url}/clinical-trials/search?condition=osteoarthritis&max_results=5", 
                                  headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                trials = data.get('trials', [])
                
                if trials:
                    # Check for real NCT IDs
                    nct_ids = [t.get('nct_id', '') for t in trials]
                    valid_nct_ids = [nct for nct in nct_ids if nct.startswith('NCT') and len(nct) >= 8]
                    
                    # Check for substantial trial descriptions
                    substantial_summaries = [t for t in trials if len(t.get('brief_summary', '')) > 100]
                    
                    if len(valid_nct_ids) >= 3 and len(substantial_summaries) >= 3:
                        self.log_reality_check("Clinical Trials Integration", True, 
                            f"Real NCT IDs ({len(valid_nct_ids)}) with substantial descriptions")
                    else:
                        self.log_reality_check("Clinical Trials Integration", False, 
                            "Trial data appears mock or incomplete")
                else:
                    self.log_reality_check("Clinical Trials Integration", False, "No trials returned")
        except:
            self.log_reality_check("Clinical Trials Integration", False, "Service error")

    def test_file_processing_reality(self):
        """REALITY CHECK: Real file processing or simulation?"""
        print("\n🔍 FILE PROCESSING REALITY CHECK")
        
        try:
            # Get existing patients to test file upload
            response = requests.get(f"{self.api_url}/patients", headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                patients = response.json()
                if patients:
                    test_patient_id = patients[0].get('patient_id')
                    
                    # Check existing files for this patient
                    response = requests.get(f"{self.api_url}/files/patient/{test_patient_id}", 
                                          headers=self.headers, timeout=30)
                    
                    if response.status_code == 200:
                        file_data = response.json()
                        uploaded_files = file_data.get('uploaded_files', [])
                        processed_files = file_data.get('processed_files', [])
                        
                        if uploaded_files or processed_files:
                            # Check file processing quality
                            total_files = len(uploaded_files) + len(processed_files)
                            
                            # Check for realistic file categories
                            categories = set()
                            for file_info in uploaded_files:
                                categories.add(file_info.get('file_category', 'unknown'))
                            
                            expected_categories = {'chart', 'genetics', 'imaging', 'labs'}
                            category_overlap = len(categories.intersection(expected_categories))
                            
                            if total_files >= 5 and category_overlap >= 2:
                                self.log_reality_check("File Processing", True, 
                                    f"{total_files} files across {len(categories)} categories")
                            else:
                                self.log_reality_check("File Processing", False, 
                                    f"Limited file processing: {total_files} files, {len(categories)} categories")
                        else:
                            self.log_reality_check("File Processing", False, "No files found for testing")
                    else:
                        self.log_reality_check("File Processing", False, "Cannot retrieve patient files")
                else:
                    self.log_reality_check("File Processing", False, "No patients available for file testing")
                    
        except Exception as e:
            self.log_reality_check("File Processing", False, f"Error: {str(e)}")

    def test_evidence_synthesis_reality(self):
        """REALITY CHECK: Real evidence synthesis or template responses?"""
        print("\n🔍 EVIDENCE SYNTHESIS REALITY CHECK")
        
        try:
            # Test evidence synthesis status
            response = requests.get(f"{self.api_url}/evidence/synthesis-status", 
                                  headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                status_data = response.json()
                
                # Check for real literature database
                lit_db = status_data.get('literature_database', {})
                total_papers = lit_db.get('total_papers', 0)
                
                if total_papers > 100:  # Substantial literature database
                    self.log_reality_check("Evidence Database", True, 
                        f"Substantial literature database with {total_papers} papers")
                else:
                    self.log_reality_check("Evidence Database", False, 
                        f"Limited literature database: {total_papers} papers")
                
                # Test actual evidence synthesis
                synthesis_request = {
                    "condition": "rotator cuff injury",
                    "existing_evidence": []
                }
                
                response = requests.post(f"{self.api_url}/evidence/synthesize-protocol", 
                                       json=synthesis_request, headers=self.headers, timeout=60)
                
                if response.status_code == 200:
                    synthesis_data = response.json()
                    synthesis_result = synthesis_data.get('synthesis_result', {})
                    
                    evidence_sources = synthesis_result.get('evidence_sources', 0)
                    synthesis_confidence = synthesis_result.get('synthesis_confidence', 0)
                    
                    if evidence_sources >= 3 and synthesis_confidence > 0.7:
                        self.log_reality_check("Evidence Synthesis", True, 
                            f"Real synthesis: {evidence_sources} sources, {synthesis_confidence:.2f} confidence")
                    else:
                        self.log_reality_check("Evidence Synthesis", False, 
                            f"Limited synthesis: {evidence_sources} sources, {synthesis_confidence:.2f} confidence")
                        
        except Exception as e:
            self.log_reality_check("Evidence Synthesis", False, f"Error: {str(e)}")

    def test_outcome_prediction_reality(self):
        """REALITY CHECK: Real ML models or mock predictions?"""
        print("\n🔍 OUTCOME PREDICTION REALITY CHECK")
        
        try:
            # Test model performance metrics
            response = requests.get(f"{self.api_url}/predictions/model-performance", 
                                  headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', {})
                total_predictions = data.get('total_predictions', 0)
                
                if len(models) >= 2 and total_predictions > 50:
                    # Check for realistic performance metrics
                    realistic_models = 0
                    for model_name, model_data in models.items():
                        performance = model_data.get('performance', {})
                        accuracy = performance.get('accuracy', 0)
                        if 0.6 <= accuracy <= 0.95:  # Realistic accuracy range
                            realistic_models += 1
                    
                    if realistic_models >= 2:
                        self.log_reality_check("ML Models", True, 
                            f"{len(models)} models with realistic performance, {total_predictions} predictions")
                    else:
                        self.log_reality_check("ML Models", False, 
                            "Model performance metrics appear unrealistic")
                else:
                    self.log_reality_check("ML Models", False, 
                        f"Limited ML implementation: {len(models)} models, {total_predictions} predictions")
                        
        except Exception as e:
            self.log_reality_check("ML Models", False, f"Error: {str(e)}")

    def test_system_integration_reality(self):
        """REALITY CHECK: Real system integration or isolated components?"""
        print("\n🔍 SYSTEM INTEGRATION REALITY CHECK")
        
        try:
            # Test advanced system status
            response = requests.get(f"{self.api_url}/advanced/system-status", 
                                  headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                services = data.get('services', {})
                db_stats = data.get('database_stats', {})
                
                # Check service integration
                active_services = 0
                for service_name, service_data in services.items():
                    if service_data.get('status') == 'active':
                        active_services += 1
                
                # Check database integration
                total_patients = db_stats.get('total_patients', 0)
                total_protocols = db_stats.get('total_protocols', 0)
                literature_papers = db_stats.get('literature_papers', 0)
                
                if (active_services >= 3 and 
                    total_patients > 5 and 
                    total_protocols > 10 and 
                    literature_papers > 50):
                    self.log_reality_check("System Integration", True, 
                        f"{active_services} active services, integrated database with substantial data")
                else:
                    self.log_reality_check("System Integration", False, 
                        f"Limited integration: {active_services} services, minimal data")
                        
        except Exception as e:
            self.log_reality_check("System Integration", False, f"Error: {str(e)}")

    def run_comprehensive_reality_check(self):
        """Run all reality checks and provide honest assessment"""
        print("🎯 COMPREHENSIVE BACKEND REALITY CHECK STARTING...")
        print("=" * 60)
        
        # Run all reality checks
        self.test_protocol_generation_reality()
        self.test_literature_integration_reality()
        self.test_ai_processing_reality()
        self.test_database_persistence_reality()
        self.test_advanced_features_reality()
        self.test_outcome_prediction_reality()
        self.test_system_integration_reality()
        
        # Calculate reality score
        reality_percentage = (self.reality_score / self.total_checks * 100) if self.total_checks > 0 else 0
        
        print("\n" + "=" * 60)
        print("🎯 REALITY CHECK RESULTS")
        print("=" * 60)
        
        print(f"\n📊 OVERALL REALITY SCORE: {self.reality_score}/{self.total_checks} ({reality_percentage:.1f}%)")
        
        print(f"\n✅ GENUINE FEATURES ({len(self.genuine_features)}):")
        for feature in self.genuine_features:
            print(f"   {feature}")
        
        print(f"\n❌ MOCK/LIMITED FEATURES ({len(self.mock_features)}):")
        for feature in self.mock_features:
            print(f"   {feature}")
        
        # Provide honest assessment
        print(f"\n🎯 HONEST ASSESSMENT:")
        if reality_percentage >= 80:
            print("   🟢 HIGH REALITY: Most features are genuinely implemented")
        elif reality_percentage >= 60:
            print("   🟡 MODERATE REALITY: Mix of genuine and mock features")
        elif reality_percentage >= 40:
            print("   🟠 LIMITED REALITY: Many features are placeholders")
        else:
            print("   🔴 LOW REALITY: Mostly mock implementation")
        
        return {
            "reality_score": self.reality_score,
            "total_checks": self.total_checks,
            "reality_percentage": reality_percentage,
            "genuine_features": self.genuine_features,
            "mock_features": self.mock_features
        }

if __name__ == "__main__":
    checker = BackendRealityChecker()
    results = checker.run_comprehensive_reality_check()
    
    # Exit with appropriate code
    if results["reality_percentage"] >= 70:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Issues found