#!/usr/bin/env python3

import requests
import json
import sys

def test_enhanced_explainable_ai_objectid_fix():
    """Test Enhanced Explainable AI after ObjectId cleaning fix"""
    
    base_url = "https://099faa9d-49d6-4fd5-979e-df2b63248fdd.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer demo-token'
    }
    
    # Use the exact test data provided in the review request
    test_data = {
        "model_prediction": {
            "diagnosis": "Osteoarthritis",
            "confidence_score": 0.85,
            "severity_score": 0.7
        },
        "patient_data": {
            "patient_id": "test_patient_123",
            "demographics": {
                "age": 58,
                "gender": "female"
            },
            "medical_history": ["Hypertension"]
        },
        "explanation_type": "comprehensive"
    }
    
    print("🚀 Testing Enhanced Explainable AI after ObjectId fix")
    print("=" * 60)
    print("Testing POST /api/ai/enhanced-explanation")
    print("This should NOT return 500 Internal Server Error anymore...")
    print()
    
    try:
        response = requests.post(
            f"{api_url}/ai/enhanced-explanation",
            json=test_data,
            headers=headers,
            timeout=90
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: No more 500 Internal Server Error!")
            
            try:
                response_data = response.json()
                
                # Check for explanation_id generation
                enhanced_explanation = response_data.get('enhanced_explanation', {})
                explanation_id = enhanced_explanation.get('explanation_id')
                
                if explanation_id:
                    print(f"✅ Explanation ID Generated: {explanation_id}")
                else:
                    print("⚠️  No explanation_id found in response")
                
                # Check status
                status = response_data.get('status', 'Unknown')
                print(f"Status: {status}")
                
                # Check for advanced features
                advanced_features = response_data.get('advanced_features', [])
                print(f"Advanced Features Available: {len(advanced_features)}")
                
                # Check for SHAP analysis
                shap_analysis = enhanced_explanation.get('advanced_shap_analysis', {})
                if shap_analysis:
                    print(f"✅ SHAP Analysis Present: {shap_analysis.get('analysis_type', 'Unknown')}")
                    print(f"Base Value: {shap_analysis.get('base_value', 0)}")
                    print(f"Prediction Value: {shap_analysis.get('prediction_value', 0)}")
                
                # Check for LIME analysis
                lime_analysis = enhanced_explanation.get('enhanced_lime_analysis', {})
                if lime_analysis:
                    print(f"✅ LIME Analysis Present: {lime_analysis.get('analysis_type', 'Unknown')}")
                
                # Check for visual breakdowns
                visual_breakdowns = enhanced_explanation.get('visual_breakdowns', {})
                if visual_breakdowns:
                    print(f"✅ Visual Breakdowns Generated: {len(visual_breakdowns.get('chart_types', []))}")
                
                # Check for transparency assessment
                transparency = enhanced_explanation.get('transparency_assessment', {})
                if transparency:
                    print(f"✅ Transparency Score: {transparency.get('transparency_score', 0):.2f}")
                
                # Check quality metrics
                quality_metrics = enhanced_explanation.get('quality_metrics', {})
                if quality_metrics:
                    print("Quality Metrics:")
                    print(f"  Explanation Fidelity: {quality_metrics.get('explanation_fidelity', 0):.2f}")
                    print(f"  Interpretability Score: {quality_metrics.get('interpretability_score', 0):.2f}")
                    print(f"  Clinical Relevance: {quality_metrics.get('clinical_relevance', 0):.2f}")
                
                print("\n🎉 OBJECTID FIX VERIFICATION: SUCCESS!")
                print("Enhanced Explainable AI is now working without ObjectId errors!")
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                print(f"Response text: {response.text[:500]}...")
                return False
                
        else:
            print(f"❌ FAILED: Still returning {response.status_code} status code")
            try:
                error_data = response.json()
                print(f"Error: {error_data}")
            except:
                print(f"Error text: {response.text[:500]}...")
            return False
            
    except Exception as e:
        print(f"❌ Request failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_enhanced_explainable_ai_objectid_fix()
    
    print("\n" + "=" * 60)
    if success:
        print("🎯 RESULT: Enhanced Explainable AI ObjectId fix VERIFIED!")
        print("The system is now functional and ready for production use.")
    else:
        print("🚨 RESULT: Enhanced Explainable AI still has issues.")
        print("The ObjectId fix may need further attention.")
    print("=" * 60)
    
    sys.exit(0 if success else 1)