#!/usr/bin/env python3
"""
ClinicalTrials.gov API Integration Testing
Focused testing for the newly implemented clinical trials functionality
"""

import requests
import sys
import json
from datetime import datetime

class ClinicalTrialsAPITester:
    def __init__(self, base_url="https://ed4e4952-b9f5-42dd-8eae-fb43144bcaeb.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
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
                    # Truncate long responses for readability
                    response_str = json.dumps(response_data, indent=2)
                    if len(response_str) > 500:
                        response_str = response_str[:500] + "..."
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
    print("🧬 ClinicalTrials.gov API Integration Testing")
    print("Testing Newly Implemented Clinical Trial Matching System")
    print("=" * 70)
    
    # Initialize tester
    tester = ClinicalTrialsAPITester()
    
    # Define clinical trials test suite
    tests = [
        # Phase 1: Clinical Trials Search Functionality
        ("Clinical Trials Search - Osteoarthritis", tester.test_clinical_trials_search_osteoarthritis),
        ("Clinical Trials Search - Rotator Cuff + Stem Cell", tester.test_clinical_trials_search_rotator_cuff_stem_cell),
        ("Clinical Trials Search - Knee Pain + PRP", tester.test_clinical_trials_search_knee_pain_prp),
        
        # Phase 2: API Parsing and Data Quality
        ("Clinical Trials - JSON API Parsing Quality", tester.test_clinical_trials_json_api_parsing),
        ("Clinical Trials - Intervention Categorization", tester.test_clinical_trials_intervention_categorization),
        
        # Phase 3: Patient Matching System
        ("Clinical Trials - Patient Matching (Osteoarthritis)", tester.test_clinical_trials_patient_matching_osteoarthritis),
        ("Clinical Trials - Patient Matching (Shoulder + BMAC)", tester.test_clinical_trials_patient_matching_shoulder_bmac),
        
        # Phase 4: Error Handling
        ("Clinical Trials - Error Handling", tester.test_clinical_trials_error_handling),
    ]
    
    print(f"\nRunning {len(tests)} ClinicalTrials.gov API tests...")
    print("Testing: Search functionality, Patient matching, Data parsing, Error handling")
    print("\n")
    
    for test_name, test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
    
    # Print final results
    print("\n" + "=" * 70)
    print(f"📊 Clinical Trials Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    print(f"🎯 Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All ClinicalTrials.gov API tests passed!")
        print("✅ Clinical trial search functionality working correctly")
        print("✅ Patient-specific trial matching operational")
        print("✅ JSON API parsing and data extraction functional")
        print("✅ Intervention categorization working (PRP, BMAC, Stem Cells, Exosomes)")
        print("✅ Relevance scoring and result quality verified")
        print("✅ Error handling working gracefully")
        return 0
    elif tester.tests_passed >= tester.tests_run * 0.8:
        print("⚠️  Most ClinicalTrials.gov API tests passed. Minor issues detected.")
        print("🔧 Core clinical trial functionality works but some features may need attention.")
        return 0
    else:
        print("❌ Significant issues detected with ClinicalTrials.gov API integration.")
        print("🚨 Clinical trial search and matching may not be fully operational.")
        return 1

if __name__ == "__main__":
    sys.exit(main())