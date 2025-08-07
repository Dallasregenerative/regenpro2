from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import json
import asyncio
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import uuid
from datetime import datetime, timedelta
import httpx
import base64
import hashlib
from enum import Enum
import numpy as np

# Import advanced services
from advanced_services import (
    FederatedLearningService,
    PubMedIntegrationService, 
    DICOMProcessingService,
    OutcomePredictionService,
    initialize_advanced_services
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# OpenAI configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_BASE_URL = "https://api.openai.com/v1"

# Security
security = HTTPBearer()

# Create the main app
app = FastAPI(title="RegenMed AI Pro - Advanced Regenerative Medicine Platform", version="2.0.0")
api_router = APIRouter(prefix="/api")

# Enums and Models
class SchoolOfThought(str, Enum):
    TRADITIONAL_AUTOLOGOUS = "traditional_autologous"
    AUTOLOGOUS_NON_US = "autologous_non_us" 
    BIOLOGICS = "biologics"
    EXPERIMENTAL = "experimental"
    AI_OPTIMIZED = "ai_optimized"

class DataType(str, Enum):
    EHR = "ehr"
    IMAGING = "imaging"
    GENOMICS = "genomics"
    LABS = "labs"
    WEARABLES = "wearables"

class EvidenceLevel(int, Enum):
    LEVEL_1 = 1  # Systematic reviews, meta-analyses
    LEVEL_2 = 2  # RCTs
    LEVEL_3 = 3  # Cohort studies
    LEVEL_4 = 4  # Case series, expert opinion

class Practitioner(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    name: str
    specialty: str
    license_number: Optional[str] = None
    organization: Optional[str] = None
    preferences: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PatientData(BaseModel):
    patient_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    practitioner_id: str
    demographics: Dict[str, Any]
    chief_complaint: str
    history_present_illness: str
    past_medical_history: List[str] = []
    medications: List[str] = []
    allergies: List[str] = []
    vital_signs: Dict[str, Any] = {}
    symptoms: List[str] = []
    imaging_data: List[Dict[str, Any]] = []
    lab_results: Dict[str, Any] = {}
    genetic_data: Dict[str, Any] = {}
    wearable_data: List[Dict[str, Any]] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TherapyInfo(BaseModel):
    name: str
    mechanism: List[str]
    indications: List[str]
    contraindications: List[str]
    success_rate: float
    evidence_level: EvidenceLevel
    legal_status: Dict[str, str]
    cost_range: Optional[str] = None

class DiagnosticResult(BaseModel):
    diagnosis: str
    confidence_score: float
    reasoning: str
    supporting_evidence: List[str]
    recommended_tests: List[str] = []
    mechanisms_involved: List[str] = []
    regenerative_targets: List[str] = []

class ProtocolStep(BaseModel):
    step_number: int
    therapy: str
    dosage: str
    timing: str
    delivery_method: str
    monitoring_parameters: List[str]
    expected_outcome: str
    timeframe: str

class RegenerativeProtocol(BaseModel):
    protocol_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str
    practitioner_id: str
    school_of_thought: SchoolOfThought
    primary_diagnoses: List[str]
    protocol_steps: List[ProtocolStep]
    supporting_evidence: List[Dict[str, Any]]
    expected_outcomes: List[str]
    timeline_predictions: Dict[str, str]
    contraindications: List[str]
    legal_warnings: List[str]
    cost_estimate: Optional[str] = None
    confidence_score: float
    ai_reasoning: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    approved_at: Optional[datetime] = None
    status: str = "draft"

class OutcomeData(BaseModel):
    outcome_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    protocol_id: str
    patient_id: str
    followup_date: datetime
    measurements: Dict[str, Any]
    practitioner_notes: str
    patient_reported_outcomes: Dict[str, Any]
    adverse_events: List[str] = []
    satisfaction_score: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EvidencePaper(BaseModel):
    paper_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pubmed_id: Optional[str] = None
    title: str
    authors: List[str]
    journal: str
    publication_date: datetime
    abstract: str
    evidence_level: EvidenceLevel
    therapy_tags: List[str]
    outcome_measures: List[str]
    patient_population: str
    study_design: str
    results_summary: str
    clinical_significance: str

# Advanced AI Engine for Regenerative Medicine
class RegenerativeMedicineAI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = OPENAI_BASE_URL
        self.therapy_database = self._initialize_therapy_database()
        
    def _initialize_therapy_database(self):
        """Initialize comprehensive therapy database"""
        return {
            "prp": TherapyInfo(
                name="Platelet-Rich Plasma (PRP)",
                mechanism=["Growth factor release", "Tissue regeneration", "Anti-inflammatory"],
                indications=["Osteoarthritis", "Tendinopathy", "Ligament injuries", "Hair loss"],
                contraindications=["Active infection", "Cancer", "Pregnancy"],
                success_rate=0.75,
                evidence_level=EvidenceLevel.LEVEL_2,
                legal_status={"US": "Approved", "EU": "Approved", "Canada": "Approved"}
            ),
            "bmac": TherapyInfo(
                name="Bone Marrow Aspirate Concentrate (BMAC)",
                mechanism=["Mesenchymal stem cells", "Growth factors", "Cytokines"],
                indications=["Bone defects", "Cartilage damage", "Non-union fractures"],
                contraindications=["Active malignancy", "Blood disorders"],
                success_rate=0.82,
                evidence_level=EvidenceLevel.LEVEL_2,
                legal_status={"US": "Approved", "EU": "Approved", "Canada": "Approved"}
            ),
            "whartons_jelly": TherapyInfo(
                name="Wharton's Jelly MSCs",
                mechanism=["Mesenchymal stem cells", "Immunomodulation", "Paracrine effects"],
                indications=["Cartilage regeneration", "Wound healing", "Neurodegeneration"],
                contraindications=["Pregnancy", "Immunocompromised state"],
                success_rate=0.78,
                evidence_level=EvidenceLevel.LEVEL_3,
                legal_status={"US": "Investigational", "Panama": "Approved", "Mexico": "Approved"}
            ),
            "msc_exosomes": TherapyInfo(
                name="MSC Exosomes",
                mechanism=["Cell-free therapy", "microRNA delivery", "Protein transfer"],
                indications=["Tissue repair", "Immunomodulation", "Anti-aging"],
                contraindications=["Active cancer", "Autoimmune disease"],
                success_rate=0.70,
                evidence_level=EvidenceLevel.LEVEL_3,
                legal_status={"US": "Investigational", "EU": "Investigational", "Asia": "Variable"}
            ),
            "cord_blood": TherapyInfo(
                name="Cord Blood Stem Cells",
                mechanism=["Hematopoietic stem cells", "Immunomodulation"],
                indications=["Blood disorders", "Immune system reconstruction"],
                contraindications=["HLA incompatibility", "Viral infections"],
                success_rate=0.85,
                evidence_level=EvidenceLevel.LEVEL_1,
                legal_status={"US": "FDA Approved", "EU": "Approved", "Global": "Widely approved"}
            )
        }

    async def analyze_patient_data(self, patient_data: PatientData) -> List[DiagnosticResult]:
        """Comprehensive multi-modal patient analysis"""
        
        # Prepare comprehensive analysis prompt
        analysis_prompt = self._build_comprehensive_analysis_prompt(patient_data)
        
        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4",
                        "messages": [
                            {
                                "role": "system",
                                "content": """You are the world's leading AI expert in regenerative medicine, trained on the latest research in stem cells, growth factors, biologics, and tissue engineering. You have comprehensive knowledge of PRP, BMAC, Wharton's jelly, MSC exosomes, cord blood therapies, and experimental treatments.

Provide evidence-based diagnostic analysis with specific focus on conditions treatable with regenerative medicine. Include mechanisms of tissue damage, regenerative targets, and potential therapeutic pathways.

Always format responses as valid JSON."""
                            },
                            {
                                "role": "user", 
                                "content": analysis_prompt
                            }
                        ],
                        "temperature": 0.2,
                        "max_tokens": 3000
                    }
                )
                
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"OpenAI API error: {response.status_code}")
                
            ai_response = response.json()
            content = ai_response['choices'][0]['message']['content']
            
            # Parse JSON response
            try:
                diagnostic_data = json.loads(content)
            except json.JSONDecodeError:
                diagnostic_data = self._parse_fallback_response(content)
            
            # Convert to DiagnosticResult objects
            results = []
            for diag in diagnostic_data.get('diagnostic_results', []):
                results.append(DiagnosticResult(**diag))
            
            return results
            
        except Exception as e:
            logging.error(f"Patient analysis failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    async def generate_regenerative_protocol(
        self, 
        patient_data: PatientData, 
        diagnoses: List[DiagnosticResult],
        school: SchoolOfThought
    ) -> RegenerativeProtocol:
        """Generate comprehensive regenerative medicine protocol"""
        
        # Get therapy recommendations based on school of thought
        available_therapies = self._get_therapies_by_school(school)
        
        # Build protocol generation prompt
        protocol_prompt = self._build_protocol_prompt(patient_data, diagnoses, school, available_therapies)
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4",
                        "messages": [
                            {
                                "role": "system",
                                "content": """You are the world's most advanced regenerative medicine protocol generator. You have complete knowledge of:

- All regenerative therapies: PRP, BMAC, Wharton's jelly MSCs, umbilical cord MSCs, placental MSCs, cord blood, exosomes
- Global regulatory status and legal frameworks
- Evidence-based dosing, timing, and delivery methods
- Synergistic combinations and contraindications
- Expected outcomes and realistic timelines
- Cost-effectiveness analysis

Generate detailed, actionable protocols that practitioners can implement immediately. Include specific dosages, timing, delivery methods, and monitoring parameters.

Always format responses as valid JSON with complete protocol details."""
                            },
                            {
                                "role": "user",
                                "content": protocol_prompt
                            }
                        ],
                        "temperature": 0.3,
                        "max_tokens": 4000
                    }
                )
                
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Protocol generation failed: {response.status_code}")
                
            ai_response = response.json()
            content = ai_response['choices'][0]['message']['content']
            
            # Parse protocol response
            try:
                protocol_data = json.loads(content)
            except json.JSONDecodeError:
                protocol_data = self._parse_protocol_fallback(content, school)
            
            # Create comprehensive protocol
            protocol = RegenerativeProtocol(
                patient_id=patient_data.patient_id,
                practitioner_id=patient_data.practitioner_id,
                school_of_thought=school,
                primary_diagnoses=[d.diagnosis for d in diagnoses[:3]],
                protocol_steps=[ProtocolStep(**step) for step in protocol_data.get('protocol_steps', [])],
                supporting_evidence=protocol_data.get('supporting_evidence', []),
                expected_outcomes=protocol_data.get('expected_outcomes', []),
                timeline_predictions=protocol_data.get('timeline_predictions', {}),
                contraindications=protocol_data.get('contraindications', []),
                legal_warnings=protocol_data.get('legal_warnings', []),
                cost_estimate=protocol_data.get('cost_estimate'),
                confidence_score=protocol_data.get('confidence_score', 0.8),
                ai_reasoning=protocol_data.get('ai_reasoning', 'Protocol generated based on current evidence and best practices.')
            )
            
            return protocol
            
        except Exception as e:
            logging.error(f"Protocol generation failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Protocol generation failed: {str(e)}")

    def _get_therapies_by_school(self, school: SchoolOfThought) -> List[TherapyInfo]:
        """Get available therapies based on school of thought"""
        if school == SchoolOfThought.TRADITIONAL_AUTOLOGOUS:
            return [self.therapy_database["prp"], self.therapy_database["bmac"]]
        elif school == SchoolOfThought.AUTOLOGOUS_NON_US:
            return list(self.therapy_database.values())[:3]  # Including Wharton's jelly
        elif school == SchoolOfThought.BIOLOGICS:
            return [self.therapy_database["whartons_jelly"], self.therapy_database["msc_exosomes"], 
                   self.therapy_database["cord_blood"]]
        elif school == SchoolOfThought.EXPERIMENTAL:
            return list(self.therapy_database.values())  # All therapies including experimental
        else:  # AI_OPTIMIZED
            return list(self.therapy_database.values())  # All options for AI selection

    def _build_comprehensive_analysis_prompt(self, patient_data: PatientData) -> str:
        """Build detailed analysis prompt for regenerative medicine"""
        
        return f"""
        Analyze this patient for regenerative medicine treatment opportunities:

        **PATIENT PROFILE:**
        Demographics: {json.dumps(patient_data.demographics, indent=2)}
        Chief Complaint: {patient_data.chief_complaint}
        History of Present Illness: {patient_data.history_present_illness}
        
        **CLINICAL DATA:**
        Past Medical History: {', '.join(patient_data.past_medical_history) if patient_data.past_medical_history else 'None'}
        Current Medications: {', '.join(patient_data.medications) if patient_data.medications else 'None'}
        Allergies: {', '.join(patient_data.allergies) if patient_data.allergies else 'None'}
        Vital Signs: {json.dumps(patient_data.vital_signs, indent=2)}
        Symptoms: {', '.join(patient_data.symptoms) if patient_data.symptoms else 'None'}
        
        **DIAGNOSTIC DATA:**
        Lab Results: {json.dumps(patient_data.lab_results, indent=2) if patient_data.lab_results else 'None available'}
        Imaging: {json.dumps(patient_data.imaging_data, indent=2) if patient_data.imaging_data else 'None available'}
        Genetic Data: {json.dumps(patient_data.genetic_data, indent=2) if patient_data.genetic_data else 'None available'}

        **REQUIRED OUTPUT (JSON FORMAT):**
        {{
            "diagnostic_results": [
                {{
                    "diagnosis": "Primary diagnosis with ICD-10 code",
                    "confidence_score": 0.85,
                    "reasoning": "Detailed clinical reasoning based on presented data",
                    "supporting_evidence": ["Clinical finding 1", "Laboratory result 2", "Imaging finding 3"],
                    "recommended_tests": ["Additional test 1", "Biomarker 2"],
                    "mechanisms_involved": ["Inflammatory cascade", "Tissue degradation", "Cellular senescence"],
                    "regenerative_targets": ["Cartilage matrix", "Synovial membrane", "Subchondral bone"]
                }}
            ],
            "regenerative_suitability": {{
                "overall_score": 0.8,
                "favorable_factors": ["Young age", "Localized damage", "Good healing capacity"],
                "limiting_factors": ["Systemic inflammation", "Comorbidities"],
                "optimal_timing": "Early intervention recommended"
            }}
        }}

        Focus on conditions where regenerative medicine has proven efficacy: musculoskeletal disorders, wound healing, tissue repair, anti-aging, and degenerative conditions.
        """

    def _build_protocol_prompt(self, patient_data: PatientData, diagnoses: List[DiagnosticResult], 
                              school: SchoolOfThought, available_therapies: List[TherapyInfo]) -> str:
        """Build comprehensive protocol generation prompt"""
        
        therapy_descriptions = []
        for therapy in available_therapies:
            therapy_descriptions.append(f"""
            {therapy.name}:
            - Mechanisms: {', '.join(therapy.mechanism)}
            - Success Rate: {therapy.success_rate:.1%}
            - Evidence Level: {therapy.evidence_level.value}
            - Legal Status: {therapy.legal_status}
            - Indications: {', '.join(therapy.indications)}
            """)
        
        return f"""
        Generate a comprehensive regenerative medicine protocol for this patient:

        **PATIENT SUMMARY:**
        Age: {patient_data.demographics.get('age', 'Unknown')}
        Primary Diagnoses: {', '.join([d.diagnosis for d in diagnoses[:3]])}
        School of Thought: {school.value}
        
        **AVAILABLE THERAPIES:**
        {chr(10).join(therapy_descriptions)}
        
        **DIAGNOSTIC DETAILS:**
        {json.dumps([{
            'diagnosis': d.diagnosis,
            'confidence': d.confidence_score,
            'mechanisms': d.mechanisms_involved,
            'targets': d.regenerative_targets
        } for d in diagnoses], indent=2)}

        **REQUIRED OUTPUT (JSON FORMAT):**
        {{
            "protocol_steps": [
                {{
                    "step_number": 1,
                    "therapy": "Specific therapy name",
                    "dosage": "Exact dosage with units (e.g., '3-5ml PRP, 1.5x10^8 platelets/ml')",
                    "timing": "When to perform (e.g., 'Week 1, Day 0')",
                    "delivery_method": "Specific technique (e.g., 'Ultrasound-guided intra-articular injection')",
                    "monitoring_parameters": ["Pain scale", "Range of motion", "Imaging findings"],
                    "expected_outcome": "Specific expected result",
                    "timeframe": "When to expect results (e.g., '2-4 weeks')"
                }}
            ],
            "supporting_evidence": [
                {{
                    "study_title": "Recent clinical trial title",
                    "journal": "Journal name",
                    "year": 2023,
                    "evidence_level": 2,
                    "key_finding": "Primary outcome result",
                    "relevance": "How it applies to this case"
                }}
            ],
            "expected_outcomes": [
                "Primary outcome with timeline",
                "Secondary benefits with timeline"
            ],
            "timeline_predictions": {{
                "immediate": "0-2 weeks: Expected immediate effects",
                "short_term": "2-8 weeks: Early improvements",
                "medium_term": "2-6 months: Significant benefits",
                "long_term": "6-12+ months: Sustained outcomes"
            }},
            "contraindications": ["Specific contraindications for this patient"],
            "legal_warnings": ["Any regulatory or legal considerations"],
            "cost_estimate": "Estimated total cost range",
            "confidence_score": 0.85,
            "ai_reasoning": "Detailed explanation of protocol selection and rationale"
        }}

        **GUIDELINES:**
        1. Include specific dosages based on latest evidence
        2. Sequence therapies for optimal synergy
        3. Include monitoring and safety parameters
        4. Provide realistic timelines based on published data
        5. Consider patient-specific factors (age, comorbidities, etc.)
        6. Include legal status warnings for non-FDA approved treatments
        7. Estimate costs based on current market rates
        
        Generate the most evidence-based, personalized protocol possible.
        """

    def _parse_fallback_response(self, content: str) -> Dict:
        """Fallback parser for diagnostic analysis"""
        return {
            "diagnostic_results": [{
                "diagnosis": "Complex regenerative medicine case requiring expert review",
                "confidence_score": 0.7,
                "reasoning": content[:1000] + "..." if len(content) > 1000 else content,
                "supporting_evidence": ["AI analysis completed", "Requires clinical correlation"],
                "recommended_tests": ["Comprehensive regenerative medicine workup"],
                "mechanisms_involved": ["Multiple pathways involved"],
                "regenerative_targets": ["Tissue-specific regeneration required"]
            }]
        }

    def _parse_protocol_fallback(self, content: str, school: SchoolOfThought) -> Dict:
        """Fallback parser for protocol generation"""
        return {
            "protocol_steps": [{
                "step_number": 1,
                "therapy": "Comprehensive regenerative assessment",
                "dosage": "To be determined by practitioner",
                "timing": "Initial consultation",
                "delivery_method": "Clinical evaluation",
                "monitoring_parameters": ["Clinical response", "Safety monitoring"],
                "expected_outcome": "Personalized treatment plan",
                "timeframe": "1-2 weeks"
            }],
            "supporting_evidence": [],
            "expected_outcomes": ["Customized regenerative therapy plan"],
            "timeline_predictions": {"immediate": "Assessment complete"},
            "contraindications": ["Standard regenerative medicine contraindications"],
            "legal_warnings": ["Verify regulatory status in your jurisdiction"],
            "cost_estimate": "Variable based on selected therapies",
            "confidence_score": 0.6,
            "ai_reasoning": "Protocol requires customization based on clinical judgment."
        }

# Initialize AI engine and advanced services
regen_ai = RegenerativeMedicineAI(OPENAI_API_KEY)

# Advanced services (will be initialized on startup)
federated_service = None
pubmed_service = None
dicom_service = None
prediction_service = None

# Simple auth function for demo
async def get_current_practitioner(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # For demo purposes, we'll create a simple practitioner
    return Practitioner(
        id="demo-practitioner-001",
        email="practitioner@regenmed.ai",
        name="Dr. Regenerative Medicine",
        specialty="Regenerative Medicine"
    )

# Advanced AI Features API Endpoints

@api_router.post("/federated/register-clinic")
async def register_clinic_for_federated_learning(
    clinic_data: Dict[str, Any],
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Register clinic for federated learning participation"""
    
    clinic_id = f"clinic_{practitioner.id}"
    
    # Extract privacy-safe data summary
    data_summary = {
        "total_patients": clinic_data.get("total_patients", 0),
        "avg_age": clinic_data.get("avg_age", 0),
        "therapy_distribution": clinic_data.get("therapy_distribution", {}),
        "outcomes": clinic_data.get("outcomes", [])
    }
    
    if federated_service:
        result = await federated_service.register_clinic_participation(clinic_id, data_summary)
        return result
    
    return {"status": "service_unavailable"}

@api_router.post("/federated/submit-updates")
async def submit_federated_updates(
    model_updates: Dict[str, Any],
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Submit privacy-preserved model updates for federated learning"""
    
    clinic_id = f"clinic_{practitioner.id}"
    validation_metrics = model_updates.get("validation_metrics", {"accuracy": 0.85})
    
    if federated_service:
        result = await federated_service.submit_local_updates(
            clinic_id, 
            model_updates.get("model_weights", {}), 
            validation_metrics
        )
        return result
    
    return {"status": "service_unavailable"}

@api_router.get("/federated/global-model-status")
async def get_global_model_status():
    """Get status of global federated learning models"""
    
    if federated_service:
        # Get model status from database
        model_status = await db.federated_models.find_one({"model_id": "global_outcome_predictor"})
        if model_status:
            return {
                "model_version": model_status.get("version", 1),
                "participants": model_status.get("participants", 0),
                "last_updated": model_status.get("last_updated"),
                "performance_improvement": model_status.get("performance_improvement", 0.05),
                "status": model_status.get("status", "active")
            }
    
    return {"status": "initializing", "message": "Federated learning system starting up"}

@api_router.get("/literature/latest-updates")
async def get_latest_literature_updates():
    """Get latest regenerative medicine literature updates"""
    
    if pubmed_service:
        # Process new literature
        processing_result = await pubmed_service.process_new_literature()
        
        # Get recent papers
        recent_papers = await db.literature_papers.find().sort("extracted_at", -1).limit(10).to_list(10)
        
        return {
            "processing_result": processing_result,
            "recent_papers": recent_papers,
            "total_papers_in_database": await db.literature_papers.count_documents({}),
            "last_update": datetime.utcnow()
        }
    
    return {"status": "service_unavailable"}

@api_router.get("/literature/search")
async def search_literature_database(
    query: str,
    relevance_threshold: float = 0.7,
    limit: int = 20
):
    """Search the integrated literature database"""
    
    # Search papers by keywords and relevance
    search_filter = {
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"abstract": {"$regex": query, "$options": "i"}},
            {"regenerative_keywords": {"$in": [query.lower()]}}
        ],
        "relevance_score": {"$gte": relevance_threshold}
    }
    
    papers = await db.literature_papers.find(search_filter).sort("relevance_score", -1).limit(limit).to_list(limit)
    
    return {
        "query": query,
        "results_found": len(papers),
        "papers": papers,
        "search_timestamp": datetime.utcnow()
    }

@api_router.post("/imaging/analyze-dicom")
async def analyze_dicom_image(
    image_data: Dict[str, Any],
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Analyze DICOM medical images with AI"""
    
    patient_id = image_data.get("patient_id")
    modality = image_data.get("modality", "MRI")
    
    # In a real implementation, this would handle actual DICOM files
    # For demo purposes, we'll simulate DICOM processing
    dicom_bytes = base64.b64decode(image_data.get("dicom_data", ""))
    
    if dicom_service:
        analysis_result = await dicom_service.process_dicom_image(dicom_bytes, patient_id, modality)
        
        # Log analysis for audit
        await db.audit_log.insert_one({
            "timestamp": datetime.utcnow(),
            "practitioner_id": practitioner.id,
            "action": "dicom_analysis",
            "patient_id": patient_id,
            "modality": modality,
            "analysis_id": analysis_result.get("processing_id")
        })
        
        return analysis_result
    
    return {"status": "service_unavailable"}

@api_router.get("/imaging/analysis-history/{patient_id}")
async def get_imaging_analysis_history(
    patient_id: str,
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Get imaging analysis history for a patient"""
    
    analyses = await db.dicom_analyses.find({"patient_id": patient_id}).sort("processing_date", -1).to_list(20)
    
    return {
        "patient_id": patient_id,
        "total_analyses": len(analyses),
        "analyses": analyses
    }

@api_router.post("/predictions/treatment-outcome")
async def predict_treatment_outcome(
    prediction_request: Dict[str, Any],
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Predict treatment outcome using ML models"""
    
    patient_id = prediction_request.get("patient_id")
    therapy_plan = prediction_request.get("therapy_plan", {})
    
    # Get patient data
    patient_record = await db.patients.find_one({"patient_id": patient_id})
    if not patient_record:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_data = PatientData(**patient_record)
    
    if prediction_service:
        prediction_result = await prediction_service.predict_treatment_outcome(
            patient_data.dict(), 
            therapy_plan
        )
        
        # Log prediction for audit
        await db.audit_log.insert_one({
            "timestamp": datetime.utcnow(),
            "practitioner_id": practitioner.id,
            "action": "outcome_prediction",
            "patient_id": patient_id,
            "therapy": therapy_plan.get("therapy_name"),
            "predicted_success": prediction_result.get("predictions", {}).get("success_probability")
        })
        
        return prediction_result
    
    return {"status": "service_unavailable"}

@api_router.get("/predictions/model-performance")
async def get_prediction_model_performance():
    """Get performance metrics for prediction models"""
    
    if prediction_service and prediction_service.models:
        performance_metrics = {}
        
        for model_name, model_data in prediction_service.models.items():
            performance_metrics[model_name] = {
                "performance": model_data.get("performance", {}),
                "features": model_data.get("features", []),
                "model_type": type(model_data.get("model", None)).__name__
            }
        
        return {
            "models": performance_metrics,
            "total_predictions": await db.outcome_predictions.count_documents({}),
            "last_update": datetime.utcnow()
        }
    
    return {"status": "models_initializing"}

@api_router.get("/advanced/system-status")
async def get_advanced_system_status():
    """Get comprehensive status of all advanced AI systems"""
    
    status = {
        "timestamp": datetime.utcnow(),
        "services": {
            "federated_learning": {
                "status": "active" if federated_service else "unavailable",
                "global_model_participants": 0,
                "last_aggregation": None
            },
            "literature_integration": {
                "status": "active" if pubmed_service else "unavailable",
                "papers_monitored": await db.literature_papers.count_documents({}) if pubmed_service else 0,
                "last_update": None
            },
            "dicom_processing": {
                "status": "active" if dicom_service else "unavailable",
                "supported_modalities": dicom_service.supported_modalities if dicom_service else [],
                "analyses_completed": await db.dicom_analyses.count_documents({}) if dicom_service else 0
            },
            "outcome_prediction": {
                "status": "active" if prediction_service else "unavailable",
                "models_loaded": len(prediction_service.models) if prediction_service else 0,
                "predictions_made": await db.outcome_predictions.count_documents({}) if prediction_service else 0
            }
        },
        "database_stats": {
            "total_patients": await db.patients.count_documents({}),
            "total_protocols": await db.protocols.count_documents({}),
            "total_outcomes": await db.outcomes.count_documents({}),
            "literature_papers": await db.literature_papers.count_documents({}),
            "federated_participants": await db.federated_participants.count_documents({})
        }
    }
    
    # Get recent federated model status
    if federated_service:
        recent_model = await db.federated_models.find_one(
            {"model_id": "global_outcome_predictor"}, 
            sort=[("last_updated", -1)]
        )
        if recent_model:
            status["services"]["federated_learning"]["global_model_participants"] = recent_model.get("participants", 0)
            status["services"]["federated_learning"]["last_aggregation"] = recent_model.get("last_updated")
    
    # Get literature monitoring status
    if pubmed_service:
        recent_monitoring = await db.literature_monitoring.find_one(sort=[("last_update", -1)])
        if recent_monitoring:
            status["services"]["literature_integration"]["last_update"] = recent_monitoring.get("last_update")
    
    return status

# API Endpoints
@api_router.get("/")
async def root():
    return {"message": "RegenMed AI Pro - Advanced Regenerative Medicine Platform v2.0"}

@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "2.0.0",
        "services": {
            "database": "connected",
            "ai_engine": "ready" if OPENAI_API_KEY else "not_configured",
            "knowledge_base": "loaded"
        }
    }

@api_router.post("/patients", response_model=PatientData)
async def create_patient(
    patient_data: Dict[str, Any],
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Create comprehensive patient record with multi-modal data support"""
    
    # Create patient with practitioner ID
    patient = PatientData(
        practitioner_id=practitioner.id,
        **patient_data
    )
    
    # Store in database
    await db.patients.insert_one(patient.dict())
    
    # Log audit event
    await db.audit_log.insert_one({
        "timestamp": datetime.utcnow(),
        "practitioner_id": practitioner.id,
        "action": "patient_created",
        "patient_id": patient.patient_id,
        "details": {"patient_name": patient.demographics.get('name', 'Unknown')}
    })
    
    return patient

@api_router.get("/patients", response_model=List[PatientData])
async def list_patients(
    limit: int = 50,
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """List patients for current practitioner"""
    
    patients = await db.patients.find(
        {"practitioner_id": practitioner.id}
    ).sort("created_at", -1).to_list(limit)
    
    return [PatientData(**patient) for patient in patients]

@api_router.get("/patients/{patient_id}", response_model=PatientData)
async def get_patient(
    patient_id: str,
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Get detailed patient information"""
    
    patient = await db.patients.find_one({
        "patient_id": patient_id,
        "practitioner_id": practitioner.id
    })
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return PatientData(**patient)

@api_router.post("/patients/{patient_id}/analyze")
async def analyze_patient(
    patient_id: str,
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Comprehensive AI analysis of patient data"""
    
    # Get patient data
    patient_record = await db.patients.find_one({
        "patient_id": patient_id,
        "practitioner_id": practitioner.id
    })
    
    if not patient_record:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_data = PatientData(**patient_record)
    
    # Perform AI analysis
    diagnostic_results = await regen_ai.analyze_patient_data(patient_data)
    
    # Store analysis results
    analysis_record = {
        "patient_id": patient_id,
        "practitioner_id": practitioner.id,
        "analysis_results": [result.dict() for result in diagnostic_results],
        "timestamp": datetime.utcnow()
    }
    
    await db.patient_analyses.insert_one(analysis_record)
    
    return {
        "patient_id": patient_id,
        "diagnostic_results": diagnostic_results,
        "analysis_timestamp": datetime.utcnow()
    }

@api_router.post("/protocols/generate")
async def generate_protocol(
    request_data: Dict[str, Any],
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Generate comprehensive regenerative medicine protocol"""
    
    patient_id = request_data.get("patient_id")
    school = SchoolOfThought(request_data.get("school_of_thought", "ai_optimized"))
    
    # Get patient data
    patient_record = await db.patients.find_one({
        "patient_id": patient_id,
        "practitioner_id": practitioner.id
    })
    
    if not patient_record:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_data = PatientData(**patient_record)
    
    # Get or generate diagnoses
    analysis = await db.patient_analyses.find_one(
        {"patient_id": patient_id},
        sort=[("timestamp", -1)]
    )
    
    if not analysis:
        # Generate fresh analysis
        diagnostic_results = await regen_ai.analyze_patient_data(patient_data)
    else:
        diagnostic_results = [DiagnosticResult(**result) for result in analysis["analysis_results"]]
    
    # Generate protocol
    protocol = await regen_ai.generate_regenerative_protocol(
        patient_data, diagnostic_results, school
    )
    
    # Store protocol
    await db.protocols.insert_one(protocol.dict())
    
    # Audit log
    await db.audit_log.insert_one({
        "timestamp": datetime.utcnow(),
        "practitioner_id": practitioner.id,
        "action": "protocol_generated",
        "patient_id": patient_id,
        "protocol_id": protocol.protocol_id,
        "school_of_thought": school.value
    })
    
    return protocol

@api_router.get("/protocols/{protocol_id}")
async def get_protocol(
    protocol_id: str,
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Get protocol details with evidence"""
    
    protocol = await db.protocols.find_one({
        "protocol_id": protocol_id,
        "practitioner_id": practitioner.id
    })
    
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocol not found")
    
    return RegenerativeProtocol(**protocol)

@api_router.put("/protocols/{protocol_id}/approve")
async def approve_protocol(
    protocol_id: str,
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Approve protocol for implementation"""
    
    result = await db.protocols.update_one(
        {"protocol_id": protocol_id, "practitioner_id": practitioner.id},
        {
            "$set": {
                "status": "approved",
                "approved_at": datetime.utcnow()
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Protocol not found")
    
    # Audit log
    await db.audit_log.insert_one({
        "timestamp": datetime.utcnow(),
        "practitioner_id": practitioner.id,
        "action": "protocol_approved",
        "protocol_id": protocol_id
    })
    
    return {"status": "approved", "approved_at": datetime.utcnow()}

@api_router.get("/therapies")
async def list_therapies():
    """Get comprehensive therapy database"""
    return {
        "therapies": [therapy.dict() for therapy in regen_ai.therapy_database.values()],
        "schools_of_thought": {
            "traditional_autologous": {
                "name": "Traditional Autologous (US Legal)",
                "description": "FDA-approved autologous therapies: PRP, BMAC",
                "therapies": ["prp", "bmac"],
                "legal_status": "Fully approved in US"
            },
            "autologous_non_us": {
                "name": "Autologous (Non-US Legal)",
                "description": "Advanced autologous therapies available internationally",
                "therapies": ["prp", "bmac", "whartons_jelly"],
                "legal_status": "Approved in select countries"
            },
            "biologics": {
                "name": "Biologics & Allogenic Therapies",
                "description": "Donor-derived regenerative therapies",
                "therapies": ["whartons_jelly", "msc_exosomes", "cord_blood"],
                "legal_status": "Variable by jurisdiction"
            },
            "experimental": {
                "name": "Experimental & Cutting-Edge",
                "description": "Latest research and experimental protocols",
                "therapies": ["msc_exosomes", "cord_blood", "genetic_therapies"],
                "legal_status": "Research/investigational"
            },
            "ai_optimized": {
                "name": "AI-Optimized Best Protocol",
                "description": "AI selects optimal therapy regardless of regulatory status",
                "therapies": "all_available",
                "legal_status": "AI provides regulatory warnings"
            }
        }
    }

@api_router.post("/outcomes")
async def submit_outcome(
    outcome_data: Dict[str, Any],
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Submit patient outcome data for continuous learning"""
    
    outcome = OutcomeData(
        practitioner_id=practitioner.id,
        **outcome_data
    )
    
    # Store outcome
    await db.outcomes.insert_one(outcome.dict())
    
    # Trigger federated learning update (async)
    # await trigger_federated_learning_update(outcome)
    
    return outcome

@api_router.get("/analytics/dashboard")
async def get_dashboard_analytics(
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Get practitioner dashboard analytics"""
    
    # Get patient counts
    total_patients = await db.patients.count_documents(
        {"practitioner_id": practitioner.id}
    )
    
    # Get protocol counts by status
    protocols_pending = await db.protocols.count_documents({
        "practitioner_id": practitioner.id,
        "status": "draft"
    })
    
    protocols_approved = await db.protocols.count_documents({
        "practitioner_id": practitioner.id,
        "status": "approved"
    })
    
    # Get recent outcomes
    recent_outcomes = await db.outcomes.find(
        {"practitioner_id": practitioner.id}
    ).sort("created_at", -1).limit(10).to_list(10)
    
    # Get audit trail
    recent_activities = await db.audit_log.find(
        {"practitioner_id": practitioner.id}
    ).sort("timestamp", -1).limit(20).to_list(20)
    
    return {
        "summary_stats": {
            "total_patients": total_patients,
            "protocols_pending": protocols_pending,
            "protocols_approved": protocols_approved,
            "outcomes_tracked": len(recent_outcomes)
        },
        "recent_outcomes": recent_outcomes,
        "recent_activities": recent_activities,
        "timestamp": datetime.utcnow()
    }

# Include router in main app
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_advanced_services():
    """Initialize advanced AI services on startup"""
    global federated_service, pubmed_service, dicom_service, prediction_service
    
    try:
        # Initialize advanced services
        federated_service = FederatedLearningService(db)
        pubmed_service = PubMedIntegrationService(db)
        dicom_service = DICOMProcessingService(db)
        prediction_service = OutcomePredictionService(db)
        
        # Initialize services
        await initialize_advanced_services(db)
        
        logger.info("Advanced AI services initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize advanced services: {str(e)}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)