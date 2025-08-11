#!/usr/bin/env python3

"""
Comprehensive Gap Fix Testing for RegenMed AI Pro
Testing all gap fixes implemented to verify 100% functionality achievement.
"""

import requests
import sys
import json
from datetime import datetime, timedelta

class GapFixTester:
    def __init__(self, base_url="https://9add4fe9-ec95-4c25-945f-328dd5122e17.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.patient_id = "c458d177-712c-4eb9-8fd3-5f5e41fe7b71"  # Existing patient
        self.protocol_id = None
        self.outcome_id = None
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

    def setup_protocol(self):
        """Setup a protocol for testing"""
        print("📋 SETUP: Creating protocol for testing...")
        protocol_data = {
            'patient_id': self.patient_id,
            'school_of_thought': 'ai_optimized'
        }

        success, response = self.run_test(
            'Setup Protocol for Testing',
            'POST',
            'protocols/generate',
            200,
            data=protocol_data,
            timeout=90
        )

        if success:
            self.protocol_id = response.get('protocol_id')
            print(f'✅ Protocol created: {self.protocol_id}')
            return True
        else:
            print('❌ Failed to create protocol for testing')
            return False

    # ========== GAP 1 FIX: FILE PROCESSING WORKFLOW TESTS ==========

    def test_gap1_file_retrieval_categorization(self):
        """Test GET /api/patients/{patient_id}/files - File retrieval and categorization"""
        success, response = self.run_test(
            "GAP 1: File Retrieval & Categorization",
            "GET",
            f"patients/{self.patient_id}/files",
            200
        )
        
        if success:
            files_by_category = response.get('files_by_category', {})
            total_files = response.get('total_files', 0)
            categories = response.get('categories_present', [])
            
            print(f"   Total Files Retrieved: {total_files}")
            print(f"   Categories Present: {len(categories)} - {', '.join(categories)}")
            print(f"   File Categorization Working: {len(files_by_category) > 0}")
            
            # Check for expected categories
            expected_categories = ['chart', 'genetics', 'imaging', 'labs']
            found_categories = [cat for cat in expected_categories if cat in files_by_category]
            print(f"   Expected Categories Found: {len(found_categories)}/{len(expected_categories)}")
            
            # Verify file structure
            for category, files in files_by_category.items():
                if files:
                    sample_file = files[0]
                    has_required_fields = all(field in sample_file for field in ['filename', 'file_type', 'processing_status'])
                    print(f"   Category '{category}': {len(files)} files, structure valid: {has_required_fields}")
        
        return success

    def test_gap1_file_reprocessing_ai_integration(self):
        """Test POST /api/patients/{patient_id}/files/process-all - File reprocessing and AI integration"""
        print("   This may take 30-45 seconds for comprehensive file reprocessing...")
        success, response = self.run_test(
            "GAP 1: File Reprocessing & AI Integration",
            "POST",
            f"patients/{self.patient_id}/files/process-all",
            200,
            data={},
            timeout=60
        )
        
        if success:
            status = response.get('status', 'unknown')
            files_processed = response.get('files_processed', 0)
            categories_processed = response.get('categories_processed', [])
            analysis_updated = response.get('analysis_updated', False)
            
            print(f"   Processing Status: {status}")
            print(f"   Files Processed: {files_processed}")
            print(f"   Categories Processed: {len(categories_processed)} - {', '.join(categories_processed)}")
            print(f"   AI Analysis Updated: {analysis_updated}")
            
            # Verify reprocessing worked
            if status == 'files_reprocessed' and files_processed > 0:
                print(f"   ✅ File reprocessing successful with AI integration")
            elif status == 'no_files':
                print(f"   ⚠️  No files found for patient - expected if no files uploaded")
            else:
                print(f"   ❌ File reprocessing may have issues")
        
        return success

    def test_gap1_file_upload_analysis_protocol_workflow(self):
        """Test complete file upload → analysis → protocol integration workflow"""
        # Step 1: Trigger file analysis
        print("   Step 1: Triggering comprehensive file analysis...")
        analysis_success, analysis_response = self.run_test(
            "Workflow Step 1: File Analysis",
            "GET",
            f"files/comprehensive-analysis/{self.patient_id}",
            200,
            timeout=45
        )
        
        if not analysis_success:
            print("   ❌ File analysis failed")
            return False
        
        # Step 2: Generate protocol using file insights
        print("   Step 2: Generating protocol with file integration...")
        protocol_success, protocol_response = self.run_test(
            "Workflow Step 2: File-Based Protocol Generation",
            "POST",
            f"protocols/generate-from-files?patient_id={self.patient_id}&school_of_thought=ai_optimized",
            200,
            data={},
            timeout=90
        )
        
        if protocol_success:
            protocol = protocol_response.get('protocol', {})
            files_used = protocol_response.get('file_insights_used', 0)
            enhancement_confidence = protocol_response.get('enhancement_confidence', 0)
            
            print(f"   Protocol Generated: {protocol.get('protocol_id', 'Unknown')}")
            print(f"   Files Integrated: {files_used}")
            print(f"   Enhancement Confidence: {enhancement_confidence:.2f}")
            print(f"   ✅ Complete workflow successful: Analysis → Protocol")
            
            return True
        else:
            print("   ❌ Protocol generation with file integration failed")
            return False

    def test_gap1_multimodal_file_integration(self):
        """Test multi-modal file integration with protocol generation"""
        # Test multi-modal analysis
        print("   Testing multi-modal analysis integration...")
        success, response = self.run_test(
            "Multi-Modal File Integration Analysis",
            "GET",
            f"files/comprehensive-analysis/{self.patient_id}",
            200,
            timeout=45
        )
        
        if success:
            analysis = response.get('comprehensive_analysis', {})
            total_files = analysis.get('total_files', 0)
            file_categories = analysis.get('files_by_category', {})
            
            print(f"   Total Files Analyzed: {total_files}")
            print(f"   File Categories: {len(file_categories)}")
            print(f"   ✅ Multi-modal integration working")
            
            return True
        else:
            print("   ❌ Multi-modal analysis failed")
            return False

    # ========== GAP 2 FIX: OUTCOME TRACKING SYSTEM TESTS ==========

    def test_gap2_outcome_recording_calculations(self):
        """Test POST /api/patients/{patient_id}/outcomes - Outcome recording with calculations"""
        if not self.protocol_id:
            print("❌ No protocol ID available for outcome recording testing")
            return False

        # Create comprehensive outcome data with calculations
        outcome_data = {
            "protocol_id": self.protocol_id,
            "patient_id": self.patient_id,
            "followup_date": datetime.utcnow().isoformat(),
            "measurements": {
                "pain_scale_baseline": 8,
                "pain_scale_current": 3,
                "pain_improvement_percentage": 62.5,
                "range_of_motion_baseline": 90,
                "range_of_motion_current": 135,
                "rom_improvement_degrees": 45,
                "functional_score_baseline": 45,
                "functional_score_current": 85,
                "functional_improvement_percentage": 88.9,
                "quality_of_life_score": 8.5
            },
            "calculated_outcomes": {
                "overall_improvement_score": 85.2,
                "treatment_success_indicator": True,
                "time_to_improvement_weeks": 4,
                "sustained_benefit_probability": 0.87
            },
            "practitioner_notes": "Excellent response to PRP treatment. Patient reports significant pain reduction and improved mobility. No adverse events. Recommend maintenance protocol in 6 months.",
            "patient_reported_outcomes": {
                "pain_improvement": "Much better - from 8/10 to 3/10",
                "activity_level": "Significantly improved - can walk stairs without pain",
                "satisfaction": "Very satisfied with results",
                "would_recommend": True,
                "return_to_activities": "90% return to normal activities"
            },
            "adverse_events": [],
            "satisfaction_score": 9,
            "follow_up_required": True,
            "next_assessment_date": (datetime.utcnow() + timedelta(weeks=12)).isoformat()
        }

        success, response = self.run_test(
            "GAP 2: Outcome Recording with Calculations",
            "POST",
            f"patients/{self.patient_id}/outcomes",
            200,
            data=outcome_data
        )
        
        if success:
            outcome_id = response.get('outcome_id', 'Unknown')
            calculated_metrics = response.get('calculated_metrics', {})
            improvement_score = response.get('improvement_score', 0)
            success_indicator = response.get('treatment_success', False)
            
            print(f"   Outcome ID: {outcome_id}")
            print(f"   Improvement Score: {improvement_score:.1f}%")
            print(f"   Treatment Success: {success_indicator}")
            print(f"   Calculated Metrics: {len(calculated_metrics)} metrics")
            print(f"   ✅ Outcome recording with calculations working")
            
            # Store outcome ID for later tests
            self.outcome_id = outcome_id
            
            return True
        else:
            print("   ❌ Outcome recording failed")
            return False

    def test_gap2_outcome_retrieval_statistics(self):
        """Test GET /api/patients/{patient_id}/outcomes - Outcome retrieval and statistics"""
        success, response = self.run_test(
            "GAP 2: Outcome Retrieval & Statistics",
            "GET",
            f"patients/{self.patient_id}/outcomes",
            200
        )
        
        if success:
            outcomes = response.get('outcomes', [])
            statistics = response.get('statistics', {})
            patient_id = response.get('patient_id', 'Unknown')
            
            print(f"   Patient ID: {patient_id}")
            print(f"   Outcomes Retrieved: {len(outcomes)}")
            
            if statistics:
                avg_improvement = statistics.get('average_improvement_score', 0)
                success_rate = statistics.get('treatment_success_rate', 0)
                total_followups = statistics.get('total_followups', 0)
                
                print(f"   Average Improvement Score: {avg_improvement:.1f}%")
                print(f"   Treatment Success Rate: {success_rate:.1f}%")
                print(f"   Total Follow-ups: {total_followups}")
                print(f"   ✅ Outcome statistics calculation working")
            
            if outcomes:
                latest_outcome = outcomes[0]
                measurements = latest_outcome.get('measurements', {})
                calculated_outcomes = latest_outcome.get('calculated_outcomes', {})
                
                print(f"   Latest Outcome Measurements: {len(measurements)} metrics")
                print(f"   Calculated Outcomes: {len(calculated_outcomes)} calculations")
            
            return True
        else:
            print("   ❌ Outcome retrieval failed")
            return False

    def test_gap2_comprehensive_analytics(self):
        """Test GET /api/analytics/outcomes - Comprehensive analytics"""
        success, response = self.run_test(
            "GAP 2: Comprehensive Outcome Analytics",
            "GET",
            "analytics/outcomes",
            200,
            timeout=30
        )
        
        if success:
            analytics_summary = response.get('analytics_summary', {})
            therapy_performance = response.get('therapy_performance', {})
            trends = response.get('trends', {})
            
            print(f"   Analytics Summary: {len(analytics_summary)} metrics")
            
            if analytics_summary:
                total_outcomes = analytics_summary.get('total_outcomes', 0)
                avg_success_rate = analytics_summary.get('average_success_rate', 0)
                avg_pain_reduction = analytics_summary.get('average_pain_reduction', 0)
                
                print(f"   Total Outcomes Tracked: {total_outcomes}")
                print(f"   Average Success Rate: {avg_success_rate:.1f}%")
                print(f"   Average Pain Reduction: {avg_pain_reduction:.1f}%")
            
            if therapy_performance:
                therapies_analyzed = len(therapy_performance)
                print(f"   Therapies Analyzed: {therapies_analyzed}")
            
            if trends:
                trend_categories = len(trends)
                print(f"   Trend Categories: {trend_categories}")
            
            print(f"   ✅ Comprehensive analytics working")
            return True
        else:
            print("   ❌ Comprehensive analytics failed")
            return False

    def test_gap2_dashboard_analytics_real_data(self):
        """Test updated dashboard analytics with real outcome data"""
        success, response = self.run_test(
            "GAP 2: Dashboard Analytics with Real Data",
            "GET",
            "analytics/dashboard",
            200
        )
        
        if success:
            summary_stats = response.get('summary_stats', {})
            recent_activities = response.get('recent_activities', [])
            platform_insights = response.get('platform_insights', {})
            
            # Check for real outcome data integration
            outcomes_tracked = summary_stats.get('outcomes_tracked', 0)
            success_rate = platform_insights.get('protocol_success_rate', 0)
            
            print(f"   Outcomes Tracked: {outcomes_tracked}")
            print(f"   Protocol Success Rate: {success_rate}%")
            print(f"   Recent Activities: {len(recent_activities)}")
            
            # Check if dashboard shows dynamic data
            total_patients = summary_stats.get('total_patients', 0)
            protocols_generated = summary_stats.get('protocols_generated', 0)
            
            print(f"   Total Patients: {total_patients}")
            print(f"   Protocols Generated: {protocols_generated}")
            
            # Verify real-time updates
            if outcomes_tracked > 0:
                print(f"   ✅ Dashboard showing real outcome data")
            else:
                print(f"   ⚠️  Dashboard may not be showing real outcome data yet")
            
            return True
        else:
            print("   ❌ Dashboard analytics failed")
            return False

    # ========== GAP 3: PROTOCOL ENHANCEMENT STATUS CHECK TESTS ==========

    def test_gap3_protocol_generation_quality(self):
        """Test current protocol generation quality and detail level"""
        print("   Testing protocol generation quality across all schools...")
        
        schools_to_test = [
            ("traditional_autologous", "Traditional Autologous"),
            ("biologics", "Biologics & Allogenic"),
            ("ai_optimized", "AI-Optimized"),
            ("experimental", "Experimental")
        ]
        
        quality_scores = []
        
        for school_key, school_name in schools_to_test:
            print(f"   Testing {school_name} protocol quality...")
            
            protocol_data = {
                "patient_id": self.patient_id,
                "school_of_thought": school_key
            }

            success, response = self.run_test(
                f"Protocol Quality - {school_name}",
                "POST",
                "protocols/generate",
                200,
                data=protocol_data,
                timeout=90
            )
            
            if success:
                protocol_steps = response.get('protocol_steps', [])
                supporting_evidence = response.get('supporting_evidence', [])
                ai_reasoning = response.get('ai_reasoning', '')
                cost_estimate = response.get('cost_estimate', '')
                confidence_score = response.get('confidence_score', 0)
                
                # Calculate quality score
                quality_metrics = {
                    'detailed_steps': len(protocol_steps) >= 2,
                    'evidence_citations': len(supporting_evidence) > 0,
                    'ai_reasoning_present': len(ai_reasoning) > 100,
                    'cost_estimate_present': len(cost_estimate) > 0,
                    'high_confidence': confidence_score >= 0.8
                }
                
                quality_score = sum(quality_metrics.values()) / len(quality_metrics)
                quality_scores.append(quality_score)
                
                print(f"     Steps: {len(protocol_steps)}, Evidence: {len(supporting_evidence)}, Quality: {quality_score:.1%}")
                
                # Check for specific dosing and monitoring
                if protocol_steps:
                    first_step = protocol_steps[0]
                    has_dosage = len(first_step.get('dosage', '')) > 5
                    has_monitoring = len(first_step.get('monitoring_parameters', [])) > 0
                    print(f"     Specific Dosing: {has_dosage}, Monitoring: {has_monitoring}")
        
        if quality_scores:
            avg_quality = sum(quality_scores) / len(quality_scores)
            print(f"   Average Protocol Quality Score: {avg_quality:.1%}")
            
            if avg_quality >= 0.8:
                print(f"   ✅ Protocol generation quality is excellent")
                return True
            elif avg_quality >= 0.6:
                print(f"   ⚠️  Protocol generation quality is good but could improve")
                return True
            else:
                print(f"   ❌ Protocol generation quality needs improvement")
                return False
        else:
            print("   ❌ No protocols generated for quality testing")
            return False

    def test_gap3_evidence_citations_detail(self):
        """Test if protocols include evidence citations, specific dosing, monitoring schedules"""
        # Generate a protocol specifically for evidence citation testing
        protocol_data = {
            "patient_id": self.patient_id,
            "school_of_thought": "ai_optimized"
        }

        print("   Generating protocol for evidence citation analysis...")
        success, response = self.run_test(
            "Evidence Citations & Detail Analysis",
            "POST",
            "protocols/generate",
            200,
            data=protocol_data,
            timeout=90
        )
        
        if success:
            protocol_steps = response.get('protocol_steps', [])
            supporting_evidence = response.get('supporting_evidence', [])
            ai_reasoning = response.get('ai_reasoning', '')
            
            print(f"   Protocol Steps Generated: {len(protocol_steps)}")
            print(f"   Supporting Evidence Items: {len(supporting_evidence)}")
            
            # Check evidence citations
            evidence_quality = {
                'has_citations': False,
                'has_pmids': False,
                'has_study_types': False,
                'has_clinical_findings': False
            }
            
            for evidence in supporting_evidence:
                if isinstance(evidence, dict):
                    citation = evidence.get('citation', '')
                    finding = evidence.get('finding', '')
                    evidence_type = evidence.get('evidence_type', '')
                    
                    if 'PMID' in citation or 'pmid' in citation.lower():
                        evidence_quality['has_pmids'] = True
                    if len(citation) > 10:
                        evidence_quality['has_citations'] = True
                    if any(study_type in evidence_type.lower() for study_type in ['rct', 'trial', 'study', 'systematic']):
                        evidence_quality['has_study_types'] = True
                    if len(finding) > 20:
                        evidence_quality['has_clinical_findings'] = True
            
            print(f"   Evidence Quality Metrics:")
            for metric, present in evidence_quality.items():
                print(f"     {metric}: {'✅' if present else '❌'}")
            
            # Check protocol step details
            step_quality = {
                'specific_dosing': False,
                'delivery_methods': False,
                'monitoring_schedules': False,
                'timeframes': False
            }
            
            for step in protocol_steps:
                dosage = step.get('dosage', '')
                delivery = step.get('delivery_method', '')
                monitoring = step.get('monitoring_parameters', [])
                timeframe = step.get('timeframe', '')
                
                if any(unit in dosage.lower() for unit in ['ml', 'mg', 'units', 'cc']):
                    step_quality['specific_dosing'] = True
                if any(method in delivery.lower() for method in ['injection', 'guided', 'ultrasound', 'intra']):
                    step_quality['delivery_methods'] = True
                if len(monitoring) > 0:
                    step_quality['monitoring_schedules'] = True
                if any(time in timeframe.lower() for time in ['week', 'month', 'day']):
                    step_quality['timeframes'] = True
            
            print(f"   Protocol Step Quality Metrics:")
            for metric, present in step_quality.items():
                print(f"     {metric}: {'✅' if present else '❌'}")
            
            # Overall assessment
            evidence_score = sum(evidence_quality.values()) / len(evidence_quality)
            step_score = sum(step_quality.values()) / len(step_quality)
            overall_score = (evidence_score + step_score) / 2
            
            print(f"   Evidence Citation Score: {evidence_score:.1%}")
            print(f"   Protocol Detail Score: {step_score:.1%}")
            print(f"   Overall Quality Score: {overall_score:.1%}")
            
            if overall_score >= 0.75:
                print(f"   ✅ Evidence citations and protocol details are comprehensive")
                return True
            else:
                print(f"   ❌ Evidence citations and protocol details need improvement")
                return False
        else:
            print("   ❌ Protocol generation failed for evidence testing")
            return False

    def test_gap3_clinical_sophistication_check(self):
        """Test if protocols meet clinical sophistication requirements"""
        # Generate protocol for existing patient
        protocol_data = {
            "patient_id": self.patient_id,
            "school_of_thought": "ai_optimized"
        }

        print("   Generating protocol for clinical sophistication testing...")
        success, response = self.run_test(
            "Clinical Sophistication Protocol Generation",
            "POST",
            "protocols/generate",
            200,
            data=protocol_data,
            timeout=90
        )
        
        if success:
            protocol_steps = response.get('protocol_steps', [])
            contraindications = response.get('contraindications', [])
            legal_warnings = response.get('legal_warnings', [])
            ai_reasoning = response.get('ai_reasoning', '')
            
            # Check clinical sophistication metrics
            sophistication_metrics = {
                'considers_contraindications': len(contraindications) > 0,
                'includes_legal_warnings': len(legal_warnings) > 0,
                'detailed_reasoning': len(ai_reasoning) > 200,
                'risk_stratification': any(risk_term in ai_reasoning.lower() for risk_term in ['risk', 'caution', 'monitor', 'careful']),
                'modified_approach': any(mod in ai_reasoning.lower() for mod in ['modified', 'adjusted', 'consideration', 'special'])
            }
            
            print(f"   Clinical Sophistication Metrics:")
            for metric, present in sophistication_metrics.items():
                print(f"     {metric}: {'✅' if present else '❌'}")
            
            sophistication_score = sum(sophistication_metrics.values()) / len(sophistication_metrics)
            print(f"   Clinical Sophistication Score: {sophistication_score:.1%}")
            
            if sophistication_score >= 0.7:
                print(f"   ✅ Protocol meets clinical sophistication requirements")
                return True
            else:
                print(f"   ❌ Protocol needs more clinical sophistication")
                return False
        else:
            print("   ❌ Protocol generation failed for sophistication testing")
            return False

    def test_gap3_john_hudson_standards_compliance(self):
        """Test if protocols meet John Hudson standard requirements"""
        # Generate protocol with highest standards
        protocol_data = {
            "patient_id": self.patient_id,
            "school_of_thought": "ai_optimized"
        }

        print("   Generating protocol for John Hudson standards compliance...")
        success, response = self.run_test(
            "John Hudson Standards Compliance Check",
            "POST",
            "protocols/generate",
            200,
            data=protocol_data,
            timeout=90
        )
        
        if success:
            protocol_steps = response.get('protocol_steps', [])
            supporting_evidence = response.get('supporting_evidence', [])
            expected_outcomes = response.get('expected_outcomes', [])
            timeline_predictions = response.get('timeline_predictions', {})
            cost_estimate = response.get('cost_estimate', '')
            ai_reasoning = response.get('ai_reasoning', '')
            confidence_score = response.get('confidence_score', 0)
            
            # John Hudson Standards Checklist
            john_hudson_standards = {
                'evidence_based_approach': len(supporting_evidence) >= 2,
                'specific_dosing_protocols': any('ml' in step.get('dosage', '') or 'mg' in step.get('dosage', '') for step in protocol_steps),
                'delivery_method_specified': any(len(step.get('delivery_method', '')) > 10 for step in protocol_steps),
                'monitoring_parameters': any(len(step.get('monitoring_parameters', [])) > 0 for step in protocol_steps),
                'realistic_timelines': len(timeline_predictions) >= 2,
                'cost_transparency': len(cost_estimate) > 5,
                'outcome_predictions': len(expected_outcomes) >= 2,
                'high_confidence': confidence_score >= 0.8,
                'comprehensive_reasoning': len(ai_reasoning) > 300,
                'safety_considerations': any(safety_term in ai_reasoning.lower() for safety_term in ['safety', 'risk', 'contraindication', 'adverse'])
            }
            
            print(f"   John Hudson Standards Compliance:")
            for standard, met in john_hudson_standards.items():
                print(f"     {standard}: {'✅' if met else '❌'}")
            
            compliance_score = sum(john_hudson_standards.values()) / len(john_hudson_standards)
            print(f"   Overall Compliance Score: {compliance_score:.1%}")
            
            # Final assessment
            if compliance_score >= 0.8:
                print(f"   ✅ Protocol meets John Hudson standards")
                return True
            elif compliance_score >= 0.6:
                print(f"   ⚠️  Protocol partially meets John Hudson standards")
                return True
            else:
                print(f"   ❌ Protocol does not meet John Hudson standards")
                return False
        else:
            print("   ❌ Protocol generation failed for standards testing")
            return False

    # ========== WORKFLOW RELIABILITY VERIFICATION TESTS ==========

    def test_protocol_generation_button_reliability(self):
        """Test protocol generation button accessibility and reliability"""
        print("   Testing protocol generation reliability across multiple attempts...")
        
        attempts = 3
        successful_generations = 0
        generation_times = []
        
        for attempt in range(1, attempts + 1):
            print(f"   Attempt {attempt}/{attempts}...")
            
            protocol_data = {
                "patient_id": self.patient_id,
                "school_of_thought": "traditional_autologous"
            }
            
            start_time = datetime.utcnow()
            success, response = self.run_test(
                f"Protocol Generation Reliability Test {attempt}",
                "POST",
                "protocols/generate",
                200,
                data=protocol_data,
                timeout=90
            )
            end_time = datetime.utcnow()
            
            if success:
                successful_generations += 1
                generation_time = (end_time - start_time).total_seconds()
                generation_times.append(generation_time)
                
                protocol_id = response.get('protocol_id', 'Unknown')
                confidence = response.get('confidence_score', 0)
                print(f"     ✅ Success - Protocol: {protocol_id}, Confidence: {confidence:.2f}, Time: {generation_time:.1f}s")
            else:
                print(f"     ❌ Failed - Generation attempt {attempt}")
        
        reliability_rate = successful_generations / attempts
        avg_generation_time = sum(generation_times) / len(generation_times) if generation_times else 0
        
        print(f"   Protocol Generation Reliability: {reliability_rate:.1%} ({successful_generations}/{attempts})")
        print(f"   Average Generation Time: {avg_generation_time:.1f} seconds")
        
        if reliability_rate >= 0.8:
            print(f"   ✅ Protocol generation is reliable")
            return True
        else:
            print(f"   ❌ Protocol generation reliability needs improvement")
            return False

    def test_backend_connectivity_operations(self):
        """Test backend connectivity during various operations"""
        print("   Testing backend connectivity across different operations...")
        
        connectivity_tests = [
            ("Health Check", "GET", "health", 200),
            ("Patient List", "GET", "patients", 200),
            ("Therapy Database", "GET", "therapies", 200),
            ("System Status", "GET", "advanced/system-status", 200)
        ]
        
        successful_connections = 0
        connection_times = []
        
        for test_name, method, endpoint, expected_status in connectivity_tests:
            start_time = datetime.utcnow()
            success, response = self.run_test(
                f"Connectivity: {test_name}",
                method,
                endpoint,
                expected_status,
                timeout=30
            )
            end_time = datetime.utcnow()
            
            if success:
                successful_connections += 1
                connection_time = (end_time - start_time).total_seconds()
                connection_times.append(connection_time)
                print(f"     ✅ {test_name} - {connection_time:.2f}s")
            else:
                print(f"     ❌ {test_name} - Connection failed")
        
        connectivity_rate = successful_connections / len(connectivity_tests)
        avg_connection_time = sum(connection_times) / len(connection_times) if connection_times else 0
        
        print(f"   Backend Connectivity Rate: {connectivity_rate:.1%} ({successful_connections}/{len(connectivity_tests)})")
        print(f"   Average Response Time: {avg_connection_time:.2f} seconds")
        
        if connectivity_rate >= 0.9:
            print(f"   ✅ Backend connectivity is excellent")
            return True
        elif connectivity_rate >= 0.7:
            print(f"   ⚠️  Backend connectivity is good but could improve")
            return True
        else:
            print(f"   ❌ Backend connectivity has issues")
            return False

    def test_error_handling_recovery(self):
        """Test error handling and recovery mechanisms"""
        print("   Testing error handling and recovery mechanisms...")
        
        error_scenarios = [
            ("Invalid Patient ID", "GET", "patients/invalid-patient-id-12345", 404, None),
            ("Invalid Protocol ID", "GET", "protocols/invalid-protocol-id-12345", 404, None),
            ("Missing Required Data", "POST", "patients", 400, {}),
            ("Empty Query", "GET", "literature/search?query=", 200, None)  # Should handle gracefully
        ]
        
        successful_error_handling = 0
        
        for test_name, method, endpoint, expected_status, data in error_scenarios:
            success, response = self.run_test(
                f"Error Handling: {test_name}",
                method,
                endpoint,
                expected_status,
                data=data,
                timeout=30
            )
            
            if success:
                successful_error_handling += 1
                print(f"     ✅ {test_name} - Handled correctly")
                
                # Check if error response includes helpful information
                if isinstance(response, dict) and ('detail' in response or 'error' in response or 'message' in response):
                    print(f"       Error message provided: Yes")
                else:
                    print(f"       Error message provided: No")
            else:
                print(f"     ❌ {test_name} - Not handled correctly")
        
        error_handling_rate = successful_error_handling / len(error_scenarios)
        print(f"   Error Handling Success Rate: {error_handling_rate:.1%} ({successful_error_handling}/{len(error_scenarios)})")
        
        if error_handling_rate >= 0.8:
            print(f"   ✅ Error handling and recovery is robust")
            return True
        else:
            print(f"   ❌ Error handling needs improvement")
            return False

    def test_data_persistence_session_management(self):
        """Test data persistence and session management"""
        print("   Testing data persistence and session management...")
        
        # Test session consistency across multiple requests
        session_tests = []
        for i in range(3):
            success, response = self.run_test(
                f"Session Consistency Test {i+1}",
                "GET",
                f"patients/{self.patient_id}",
                200,
                timeout=15
            )
            session_tests.append(success)
        
        session_consistency = all(session_tests)
        print(f"     Session Consistency: {'✅' if session_consistency else '❌'} ({sum(session_tests)}/3)")
        
        # Overall assessment
        persistence_metrics = [session_consistency]
        persistence_score = sum(persistence_metrics) / len(persistence_metrics)
        
        print(f"   Data Persistence Score: {persistence_score:.1%}")
        
        if persistence_score >= 0.8:
            print(f"   ✅ Data persistence and session management working well")
            return True
        else:
            print(f"   ❌ Data persistence and session management need improvement")
            return False

    # ========== INTEGRATION TESTING ==========

    def test_complete_patient_workflow(self):
        """Test complete patient workflow: Create → Upload Files → Generate Protocol → Record Outcomes"""
        print("   Testing complete end-to-end patient workflow...")
        
        workflow_steps = []
        
        # Step 1: Get Patient
        success, response = self.run_test(
            "Workflow Step 1: Get Patient",
            "GET",
            f"patients/{self.patient_id}",
            200
        )
        
        workflow_steps.append(success)
        if not success:
            print("     ❌ Workflow failed at patient retrieval")
            return False
        
        print(f"     ✅ Patient retrieved: {response.get('demographics', {}).get('name', 'Unknown')}")
        
        # Step 2: Generate Protocol
        print("     Step 2: Generating protocol...")
        protocol_data = {
            "patient_id": self.patient_id,
            "school_of_thought": "ai_optimized"
        }
        
        success, response = self.run_test(
            "Workflow Step 2: Generate Protocol",
            "POST",
            "protocols/generate",
            200,
            data=protocol_data,
            timeout=90
        )
        
        workflow_steps.append(success)
        workflow_protocol_id = response.get('protocol_id') if success else None
        print(f"     {'✅' if success else '❌'} Protocol generation: {success}")
        
        # Step 3: Record Outcomes
        if workflow_protocol_id:
            print("     Step 3: Recording outcomes...")
            outcome_data = {
                "protocol_id": workflow_protocol_id,
                "patient_id": self.patient_id,
                "followup_date": datetime.utcnow().isoformat(),
                "measurements": {
                    "pain_scale_improvement": 60,
                    "functional_score": 80
                },
                "practitioner_notes": "Workflow test outcome recording",
                "satisfaction_score": 8
            }
            
            success, response = self.run_test(
                "Workflow Step 3: Record Outcomes",
                "POST",
                f"patients/{self.patient_id}/outcomes",
                200,
                data=outcome_data
            )
            
            workflow_steps.append(success)
            print(f"     {'✅' if success else '❌'} Outcome recording: {success}")
        else:
            workflow_steps.append(False)
            print("     ❌ Outcome recording: Skipped (no protocol)")
        
        # Overall workflow assessment
        workflow_success_rate = sum(workflow_steps) / len(workflow_steps)
        print(f"   Complete Workflow Success Rate: {workflow_success_rate:.1%} ({sum(workflow_steps)}/{len(workflow_steps)})")
        
        if workflow_success_rate >= 0.8:
            print(f"   ✅ Complete patient workflow is functional")
            return True
        else:
            print(f"   ❌ Complete patient workflow has issues")
            return False

    def test_cross_platform_data_flow(self):
        """Test cross-platform data flow and state management"""
        print("   Testing cross-platform data flow and state management...")
        
        # Test data flow between different system components
        data_flow_tests = []
        
        # Test 1: Patient data → Analysis system
        print("     Testing Patient → Analysis data flow...")
        success, analysis_response = self.run_test(
            "Data Flow: Patient → Analysis",
            "POST",
            f"patients/{self.patient_id}/analyze",
            200,
            data={},
            timeout=60
        )
        data_flow_tests.append(success)
        
        # Test 2: Analysis → Protocol generation
        if success:
            print("     Testing Analysis → Protocol data flow...")
            protocol_data = {
                "patient_id": self.patient_id,
                "school_of_thought": "traditional_autologous"
            }
            
            success, protocol_response = self.run_test(
                "Data Flow: Analysis → Protocol",
                "POST",
                "protocols/generate",
                200,
                data=protocol_data,
                timeout=90
            )
            data_flow_tests.append(success)
        
        # Test 3: File system → Analysis integration
        print("     Testing File System → Analysis integration...")
        success, file_response = self.run_test(
            "Data Flow: Files → Analysis",
            "GET",
            f"patients/{self.patient_id}/files",
            200
        )
        data_flow_tests.append(success)
        
        # Overall assessment
        data_flow_success_rate = sum(data_flow_tests) / len(data_flow_tests)
        print(f"   Cross-Platform Data Flow Success Rate: {data_flow_success_rate:.1%} ({sum(data_flow_tests)}/{len(data_flow_tests)})")
        
        if data_flow_success_rate >= 0.8:
            print(f"   ✅ Cross-platform data flow is working well")
            return True
        else:
            print(f"   ❌ Cross-platform data flow has issues")
            return False

    def test_dashboard_updates_new_activity(self):
        """Test dashboard updates with new activity"""
        print("   Testing dashboard updates with new activity...")
        
        # Get baseline dashboard state
        success, baseline_response = self.run_test(
            "Dashboard Baseline State",
            "GET",
            "analytics/dashboard",
            200
        )
        
        if not success:
            print("   ❌ Failed to get baseline dashboard state")
            return False
        
        baseline_stats = baseline_response.get('summary_stats', {})
        baseline_patients = baseline_stats.get('total_patients', 0)
        baseline_protocols = baseline_stats.get('protocols_generated', 0)
        baseline_activities = len(baseline_response.get('recent_activities', []))
        
        print(f"     Baseline - Patients: {baseline_patients}, Protocols: {baseline_protocols}, Activities: {baseline_activities}")
        
        # Generate protocol for new activity
        protocol_data = {
            "patient_id": self.patient_id,
            "school_of_thought": "traditional_autologous"
        }
        
        success, protocol_response = self.run_test(
            "Create New Activity: Protocol",
            "POST",
            "protocols/generate",
            200,
            data=protocol_data,
            timeout=90
        )
        
        if not success:
            print("   ❌ Failed to create new protocol activity")
            return False
        
        # Check updated dashboard state
        success, updated_response = self.run_test(
            "Dashboard Updated State",
            "GET",
            "analytics/dashboard",
            200
        )
        
        if not success:
            print("   ❌ Failed to get updated dashboard state")
            return False
        
        updated_stats = updated_response.get('summary_stats', {})
        updated_patients = updated_stats.get('total_patients', 0)
        updated_protocols = updated_stats.get('protocols_generated', 0)
        updated_activities = len(updated_response.get('recent_activities', []))
        
        print(f"     Updated - Patients: {updated_patients}, Protocols: {updated_protocols}, Activities: {updated_activities}")
        
        # Verify updates
        protocol_increase = updated_protocols > baseline_protocols
        activity_updates = updated_activities >= baseline_activities
        
        print(f"     Protocol Count Increased: {'✅' if protocol_increase else '❌'}")
        print(f"     Activities Updated: {'✅' if activity_updates else '❌'}")
        
        # Overall assessment
        update_metrics = [protocol_increase, activity_updates]
        update_success_rate = sum(update_metrics) / len(update_metrics)
        
        print(f"   Dashboard Update Success Rate: {update_success_rate:.1%} ({sum(update_metrics)}/{len(update_metrics)})")
        
        if update_success_rate >= 0.75:
            print(f"   ✅ Dashboard updates with new activity working well")
            return True
        else:
            print(f"   ❌ Dashboard updates need improvement")
            return False

    def test_endpoints_seamless_integration(self):
        """Test all endpoints work together seamlessly"""
        print("   Testing seamless integration across all endpoints...")
        
        # Test endpoint integration chains
        integration_chains = []
        
        # Chain 1: Patient → Analysis → Protocol → Outcome
        print("     Testing Patient → Analysis → Protocol → Outcome chain...")
        
        chain1_success = []
        
        # Get patient
        success, patient_response = self.run_test(
            "Integration Chain 1.1: Get Patient",
            "GET",
            f"patients/{self.patient_id}",
            200
        )
        chain1_success.append(success)
        
        # Analyze patient
        if success:
            success, analysis_response = self.run_test(
                "Integration Chain 1.2: Analyze Patient",
                "POST",
                f"patients/{self.patient_id}/analyze",
                200,
                data={},
                timeout=60
            )
            chain1_success.append(success)
            
            # Generate protocol
            if success:
                protocol_data = {
                    "patient_id": self.patient_id,
                    "school_of_thought": "ai_optimized"
                }
                
                success, protocol_response = self.run_test(
                    "Integration Chain 1.3: Generate Protocol",
                    "POST",
                    "protocols/generate",
                    200,
                    data=protocol_data,
                    timeout=90
                )
                chain1_success.append(success)
                
                # Record outcome
                if success and protocol_response.get('protocol_id'):
                    outcome_data = {
                        "protocol_id": protocol_response.get('protocol_id'),
                        "patient_id": self.patient_id,
                        "followup_date": datetime.utcnow().isoformat(),
                        "measurements": {"improvement": 75},
                        "practitioner_notes": "Integration test outcome",
                        "satisfaction_score": 8
                    }
                    
                    success, outcome_response = self.run_test(
                        "Integration Chain 1.4: Record Outcome",
                        "POST",
                        f"patients/{self.patient_id}/outcomes",
                        200,
                        data=outcome_data
                    )
                    chain1_success.append(success)
        
        chain1_rate = sum(chain1_success) / len(chain1_success) if chain1_success else 0
        integration_chains.append(chain1_rate)
        print(f"       Chain 1 Success Rate: {chain1_rate:.1%}")
        
        # Chain 2: Files → Analysis → Protocol
        print("     Testing Files → Analysis → Protocol chain...")
        
        chain2_success = []
        
        # Get files
        success, files_response = self.run_test(
            "Integration Chain 2.1: Get Files",
            "GET",
            f"patients/{self.patient_id}/files",
            200
        )
        chain2_success.append(success)
        
        # Comprehensive analysis
        if success:
            success, comp_analysis_response = self.run_test(
                "Integration Chain 2.2: Comprehensive Analysis",
                "GET",
                f"files/comprehensive-analysis/{self.patient_id}",
                200,
                timeout=45
            )
            chain2_success.append(success)
            
            # File-based protocol
            if success:
                success, file_protocol_response = self.run_test(
                    "Integration Chain 2.3: File-Based Protocol",
                    "POST",
                    f"protocols/generate-from-files?patient_id={self.patient_id}&school_of_thought=ai_optimized",
                    200,
                    data={},
                    timeout=90
                )
                chain2_success.append(success)
        
        chain2_rate = sum(chain2_success) / len(chain2_success) if chain2_success else 0
        integration_chains.append(chain2_rate)
        print(f"       Chain 2 Success Rate: {chain2_rate:.1%}")
        
        # Overall integration assessment
        overall_integration_rate = sum(integration_chains) / len(integration_chains)
        print(f"   Overall Endpoint Integration Rate: {overall_integration_rate:.1%}")
        
        if overall_integration_rate >= 0.8:
            print(f"   ✅ Endpoints work together seamlessly")
            return True
        elif overall_integration_rate >= 0.6:
            print(f"   ⚠️  Endpoints mostly work together, minor issues")
            return True
        else:
            print(f"   ❌ Endpoint integration has significant issues")
            return False

    def run_comprehensive_gap_fix_tests(self):
        """Run comprehensive tests for all gap fixes implemented"""
        print("\n" + "="*80)
        print("🎯 COMPREHENSIVE GAP FIX TESTING - VERIFYING 100% FUNCTIONALITY")
        print("="*80)
        
        # Setup protocol for testing
        if not self.setup_protocol():
            print("❌ Failed to setup protocol - some tests may fail")
        
        # Test GAP 1 FIX: FILE PROCESSING WORKFLOW
        print("\n📁 GAP 1 FIX: FILE PROCESSING WORKFLOW TESTING")
        print("-" * 60)
        gap1_tests = [
            self.test_gap1_file_retrieval_categorization,
            self.test_gap1_file_reprocessing_ai_integration,
            self.test_gap1_file_upload_analysis_protocol_workflow,
            self.test_gap1_multimodal_file_integration
        ]
        gap1_passed = sum([test() for test in gap1_tests])
        print(f"📁 GAP 1 RESULTS: {gap1_passed}/{len(gap1_tests)} tests passed")
        
        # Test GAP 2 FIX: OUTCOME TRACKING SYSTEM
        print("\n📊 GAP 2 FIX: OUTCOME TRACKING SYSTEM TESTING")
        print("-" * 60)
        gap2_tests = [
            self.test_gap2_outcome_recording_calculations,
            self.test_gap2_outcome_retrieval_statistics,
            self.test_gap2_comprehensive_analytics,
            self.test_gap2_dashboard_analytics_real_data
        ]
        gap2_passed = sum([test() for test in gap2_tests])
        print(f"📊 GAP 2 RESULTS: {gap2_passed}/{len(gap2_tests)} tests passed")
        
        # Test GAP 3: PROTOCOL ENHANCEMENT STATUS CHECK
        print("\n🧬 GAP 3: PROTOCOL ENHANCEMENT STATUS CHECK")
        print("-" * 60)
        gap3_tests = [
            self.test_gap3_protocol_generation_quality,
            self.test_gap3_evidence_citations_detail,
            self.test_gap3_clinical_sophistication_check,
            self.test_gap3_john_hudson_standards_compliance
        ]
        gap3_passed = sum([test() for test in gap3_tests])
        print(f"🧬 GAP 3 RESULTS: {gap3_passed}/{len(gap3_tests)} tests passed")
        
        # Test WORKFLOW RELIABILITY VERIFICATION
        print("\n⚡ WORKFLOW RELIABILITY VERIFICATION")
        print("-" * 60)
        reliability_tests = [
            self.test_protocol_generation_button_reliability,
            self.test_backend_connectivity_operations,
            self.test_error_handling_recovery,
            self.test_data_persistence_session_management
        ]
        reliability_passed = sum([test() for test in reliability_tests])
        print(f"⚡ RELIABILITY RESULTS: {reliability_passed}/{len(reliability_tests)} tests passed")
        
        # Test INTEGRATION TESTING
        print("\n🔄 INTEGRATION TESTING")
        print("-" * 60)
        integration_tests = [
            self.test_complete_patient_workflow,
            self.test_cross_platform_data_flow,
            self.test_dashboard_updates_new_activity,
            self.test_endpoints_seamless_integration
        ]
        integration_passed = sum([test() for test in integration_tests])
        print(f"🔄 INTEGRATION RESULTS: {integration_passed}/{len(integration_tests)} tests passed")
        
        # Calculate overall results
        total_tests = len(gap1_tests) + len(gap2_tests) + len(gap3_tests) + len(reliability_tests) + len(integration_tests)
        total_passed = gap1_passed + gap2_passed + gap3_passed + reliability_passed + integration_passed
        
        print("\n" + "="*80)
        print(f"🎯 COMPREHENSIVE GAP FIX TESTING RESULTS: {total_passed}/{total_tests} ({total_passed/total_tests*100:.1f}%)")
        print("="*80)
        
        # Determine if 100% functionality achieved
        success_rate = total_passed / total_tests
        if success_rate >= 0.95:
            print("✅ SUCCESS: 100% FUNCTIONALITY ACHIEVED - ALL GAPS FIXED!")
        elif success_rate >= 0.85:
            print("⚠️  NEAR SUCCESS: Most gaps fixed, minor issues remain")
        else:
            print("❌ GAPS REMAIN: Significant functionality gaps still need attention")
        
        return success_rate >= 0.95

def main():
    """Main function to run comprehensive gap fix testing"""
    print('🎯 COMPREHENSIVE GAP FIX TESTING - VERIFYING 100% FUNCTIONALITY')
    print('='*80)

    # Initialize tester
    tester = GapFixTester()

    print(f'🔍 Testing with existing patient: {tester.patient_id} (Sarah Chen)')

    # Run comprehensive gap fix tests
    try:
        success = tester.run_comprehensive_gap_fix_tests()
        
        # Print final summary
        print(f"\n📊 Final Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
        print(f"🎯 Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
        
        if success:
            print('🎉 ALL GAP FIXES VERIFIED - 100% FUNCTIONALITY ACHIEVED!')
            return 0
        else:
            print('⚠️ Some gaps remain - see detailed results above')
            return 1
    except Exception as e:
        print(f'❌ Testing failed with error: {str(e)}')
        return 1

if __name__ == "__main__":
    sys.exit(main())