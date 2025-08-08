from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Form, Depends
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

# Import advanced services and file processing
from advanced_services import (
    FederatedLearningService,
    PubMedIntegrationService, 
    DICOMProcessingService,
    OutcomePredictionService,
    initialize_advanced_services
)
from file_processing import (
    MedicalFileProcessor,
    FileUpload,
    ProcessedFileData
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
        """Comprehensive multi-modal patient analysis with differential diagnosis"""
        
        try:
            # Get uploaded files for multi-modal integration
            uploaded_files = {}
            if file_processor:
                try:
                    file_summary = await file_processor.get_patient_file_summary(patient_data.patient_id)
                    uploaded_files = file_summary.get("files_by_category", {})
                except Exception as e:
                    logging.warning(f"File summary retrieval failed: {str(e)}")
            
            # Build enhanced analysis prompt with multi-modal data
            analysis_prompt = self._build_enhanced_analysis_prompt(patient_data, uploaded_files)
            
            # Generate comprehensive AI analysis
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
                                "content": """You are the world's leading AI expert in regenerative medicine with 25+ years of clinical experience. You specialize in:

- Differential diagnosis for regenerative medicine conditions
- Multi-modal data integration (labs, genetics, imaging, clinical)
- Outcome prediction with confidence intervals
- Mechanism-based therapy selection
- Risk stratification and personalized treatment planning

Your expertise includes stem cells, PRP, BMAC, Wharton's jelly, MSC exosomes, cord blood therapies, and cutting-edge biologics.

Always provide comprehensive differential diagnosis with probability rankings, integrate all available data sources, and give evidence-based confidence scores.

Format all responses as valid JSON with detailed reasoning."""
                            },
                            {
                                "role": "user", 
                                "content": analysis_prompt
                            }
                        ],
                        "temperature": 0.2,
                        "max_tokens": 4000
                    }
                )
                
            if response.status_code != 200:
                logging.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return await self._generate_fallback_diagnostics(patient_data, uploaded_files)
                
            ai_response = response.json()
            content = ai_response['choices'][0]['message']['content']
            
            # Parse and structure the comprehensive analysis
            try:
                diagnostic_data = json.loads(content)
                
                # Convert to DiagnosticResult objects with enhanced information
                diagnostic_results = []
                
                differential_diagnoses = diagnostic_data.get('differential_diagnosis', [])
                
                for i, diagnosis in enumerate(differential_diagnoses):
                    # Enhanced diagnostic result with multi-modal insights
                    result = DiagnosticResult(
                        diagnosis=diagnosis.get('diagnosis', f'Diagnosis {i+1}'),
                        confidence_score=diagnosis.get('probability', 0.7),
                        reasoning=diagnosis.get('mechanism', 'Mechanism under evaluation'),
                        supporting_evidence=diagnosis.get('supporting_evidence', []),
                        mechanisms_involved=[diagnosis.get('mechanism', 'Mechanism under evaluation')],
                        regenerative_targets=diagnosis.get('regenerative_targets', [])
                    )
                    diagnostic_results.append(result)
                
                # Store comprehensive analysis for later retrieval
                await self._store_comprehensive_analysis(patient_data.patient_id, diagnostic_data, uploaded_files)
                
                return diagnostic_results if diagnostic_results else await self._generate_fallback_diagnostics(patient_data, uploaded_files)
                
            except (json.JSONDecodeError, KeyError) as e:
                logging.error(f"Failed to parse AI response: {str(e)}")
                return await self._generate_fallback_diagnostics(patient_data, uploaded_files)
                
        except Exception as e:
            logging.error(f"Patient analysis error: {str(e)}")
            return await self._generate_fallback_diagnostics(patient_data, uploaded_files)

    def _build_enhanced_analysis_prompt(self, patient_data: PatientData, uploaded_files: Dict) -> str:
        """Build enhanced analysis prompt with multi-modal data integration"""
        
        prompt = f"""
**COMPREHENSIVE PATIENT ANALYSIS REQUEST**

**PATIENT PRESENTATION:**
- Age: {patient_data.demographics.get('age', 'Unknown')} years
- Gender: {patient_data.demographics.get('gender', 'Unknown')}
- Occupation: {patient_data.demographics.get('occupation', 'Not specified')}

**CHIEF COMPLAINT:**
{patient_data.chief_complaint}

**HISTORY OF PRESENT ILLNESS:**
{patient_data.history_present_illness}

**PAST MEDICAL HISTORY:**
{', '.join(patient_data.past_medical_history) if patient_data.past_medical_history else 'None reported'}

**CURRENT MEDICATIONS:**
{', '.join(patient_data.medications) if patient_data.medications else 'None reported'}

**CURRENT SYMPTOMS:**
{', '.join(patient_data.symptoms) if patient_data.symptoms else 'Not specified'}

**ALLERGIES:**
{', '.join(patient_data.allergies) if patient_data.allergies else 'NKDA'}
"""
        
        # Add multi-modal data integration
        if uploaded_files:
            prompt += "\n\n**MULTI-MODAL DATA AVAILABLE FOR INTEGRATION:**"
            
            if "labs" in uploaded_files:
                lab_count = len(uploaded_files["labs"])
                prompt += f"\n• Laboratory Results: {lab_count} file(s) - Include inflammatory markers, biomarkers, metabolic panels in analysis"
            
            if "genetics" in uploaded_files:  
                genetic_count = len(uploaded_files["genetics"])
                prompt += f"\n• Genetic Testing: {genetic_count} file(s) - Consider healing variants, drug metabolism, regenerative capacity"
                
            if "imaging" in uploaded_files:
                imaging_count = len(uploaded_files["imaging"])
                prompt += f"\n• Medical Imaging: {imaging_count} file(s) - Integrate structural findings, severity assessment, injection targets"
                
            if "chart" in uploaded_files:
                chart_count = len(uploaded_files["chart"])
                prompt += f"\n• Clinical Charts: {chart_count} file(s) - Include comprehensive clinical assessment, exam findings"
        
        prompt += """

**REQUIRED ANALYSIS FORMAT:**

Provide comprehensive analysis in this exact JSON structure:

{
    "differential_diagnosis": [
        {
            "diagnosis": "Primary diagnosis with ICD-10 code",
            "probability": 0.85,
            "supporting_evidence": ["Clinical evidence 1", "Multi-modal finding 2", "Literature support 3"],
            "mechanism": "Detailed pathophysiological mechanism",
            "regenerative_targets": ["Specific tissue target", "Cellular mechanism", "Molecular pathway"]
        },
        {
            "diagnosis": "Secondary differential diagnosis",
            "probability": 0.15, 
            "supporting_evidence": ["Supporting evidence"],
            "mechanism": "Alternative mechanism",
            "regenerative_targets": ["Alternative targets"]
        }
    ],
    "multi_modal_insights": {
        "data_integration_confidence": 0.90,
        "key_correlations": ["Finding 1 supports diagnosis", "Biomarker X indicates severity"],
        "prognostic_indicators": ["Positive prognostic factor", "Concerning finding"]
    },
    "risk_assessment": {
        "regenerative_suitability": "Excellent/Good/Fair/Poor",
        "complication_risk": "Low/Moderate/High",
        "success_predictors": ["Factor 1", "Factor 2"]
    },
    "confidence_metrics": {
        "diagnostic_confidence": 0.85,
        "data_completeness": 0.80,
        "clinical_complexity": "Low/Moderate/High"
    }
}

**CRITICAL REQUIREMENTS:**
1. Rank differential diagnoses by probability (most likely first)
2. Integrate ALL available multi-modal data sources
3. Provide mechanism-based reasoning for each diagnosis
4. Include specific regenerative targets for each condition
5. Give realistic confidence scores based on available evidence
6. Consider patient-specific factors (age, occupation, comorbidities)

Generate the most accurate, evidence-based analysis possible using all available information.
"""
        
        return prompt

    async def _store_comprehensive_analysis(self, patient_id: str, analysis_data: Dict, uploaded_files: Dict):
        """Store comprehensive analysis for later retrieval"""
        
        try:
            analysis_doc = {
                "patient_id": patient_id,
                "comprehensive_analysis": analysis_data,
                "multi_modal_files_used": sum(len(files) for files in uploaded_files.values()) if uploaded_files else 0,
                "file_categories": list(uploaded_files.keys()) if uploaded_files else [],
                "analysis_timestamp": datetime.utcnow(),
                "analysis_type": "enhanced_differential_diagnosis"
            }
            
            # Upsert the analysis (replace if exists)
            await db.comprehensive_analyses.replace_one(
                {"patient_id": patient_id},
                analysis_doc,
                upsert=True
            )
            
        except Exception as e:
            logging.error(f"Failed to store comprehensive analysis: {str(e)}")

    async def _generate_fallback_diagnostics(self, patient_data: PatientData, uploaded_files: Dict) -> List[DiagnosticResult]:
        """Generate fallback diagnostics when AI analysis fails"""
        
        # Basic rule-based diagnosis based on chief complaint
        chief_complaint = patient_data.chief_complaint.lower()
        
        if any(term in chief_complaint for term in ['knee', 'osteoarthritis', 'joint']):
            primary_diagnosis = DiagnosticResult(
                diagnosis="M17.9 - Osteoarthritis of knee, unspecified",
                confidence_score=0.7,
                reasoning="Cartilage degeneration and inflammation",
                supporting_evidence=[patient_data.chief_complaint],
                mechanisms_involved=["Cartilage degeneration and inflammation"],
                regenerative_targets=["Articular cartilage", "Synovial membrane", "Subchondral bone"]
            )
        elif any(term in chief_complaint for term in ['shoulder', 'rotator cuff']):
            primary_diagnosis = DiagnosticResult(
                diagnosis="M75.3 - Calcific tendinitis of shoulder",
                confidence_score=0.7,
                reasoning="Tendon degeneration and calcium deposits",
                supporting_evidence=[patient_data.chief_complaint],
                mechanisms_involved=["Tendon degeneration and calcium deposits"],
                regenerative_targets=["Rotator cuff tendons", "Subacromial bursa"]
            )
        else:
            primary_diagnosis = DiagnosticResult(
                diagnosis="M79.3 - Panniculitis, unspecified",
                confidence_score=0.5,
                reasoning="Tissue inflammation and repair deficit",
                supporting_evidence=[patient_data.chief_complaint],
                mechanisms_involved=["Tissue inflammation and repair deficit"],
                regenerative_targets=["Affected tissue areas"]
            )
        
        return [primary_diagnosis]

    async def _get_literature_evidence(self, diagnoses: List[DiagnosticResult]) -> str:
        """Get relevant literature evidence for the given diagnoses"""
        literature_evidence = ""
        if pubmed_service:
            try:
                # Extract condition keywords for literature search
                condition_keywords = []
                for diagnosis in diagnoses[:2]:
                    if "osteoarthritis" in diagnosis.diagnosis.lower():
                        condition_keywords.append("platelet rich plasma osteoarthritis")
                    elif "rotator cuff" in diagnosis.diagnosis.lower() or "shoulder" in diagnosis.diagnosis.lower():
                        condition_keywords.append("BMAC rotator cuff") 
                    elif "tendon" in diagnosis.diagnosis.lower():
                        condition_keywords.append("stem cell therapy tendinopathy")
                    else:
                        condition_keywords.append("regenerative medicine")
                
                # Search literature database for relevant papers
                for keyword in condition_keywords[:2]:  # Limit to 2 searches
                    try:
                        # Search local database first
                        papers = await db.literature_papers.find({
                            "$or": [
                                {"title": {"$regex": keyword.split()[0], "$options": "i"}},
                                {"search_queries": {"$in": [keyword.lower()]}}
                            ]
                        }).sort("relevance_score", -1).limit(2).to_list(2)
                        
                        if papers:
                            literature_evidence += f"\n**RELEVANT EVIDENCE for {keyword.upper()}:**\n"
                            for i, paper in enumerate(papers, 1):
                                literature_evidence += f"{i}. {paper.get('title', 'Unknown title')} ({paper.get('year', 'Unknown')})\n"
                                literature_evidence += f"   Journal: {paper.get('journal', 'Unknown')}\n" 
                                literature_evidence += f"   Abstract: {paper.get('abstract', 'No abstract')[:300]}...\n"
                                literature_evidence += f"   PMID: {paper.get('pmid', 'Unknown')}\n\n"
                    except Exception as e:
                        continue
                        
            except Exception as e:
                logging.error(f"Literature search error: {str(e)}")
        
        return literature_evidence

    async def generate_regenerative_protocol(
        self, 
        patient_data: PatientData, 
        diagnoses: List[DiagnosticResult],
        school: SchoolOfThought
    ) -> RegenerativeProtocol:
        """Generate comprehensive regenerative medicine protocol"""
        
        # Get therapy recommendations based on school of thought
        available_therapies = self._get_therapies_by_school(school)
        
        # Get literature evidence for the diagnoses
        literature_evidence = await self._get_literature_evidence(diagnoses)
        
        # Build protocol generation prompt
        protocol_prompt = self._build_protocol_prompt(patient_data, diagnoses, school, available_therapies)
        
        # Add literature evidence to the prompt
        if literature_evidence:
            protocol_prompt = protocol_prompt.replace(
                "{literature_evidence}",
                literature_evidence
            )
        else:
            protocol_prompt = protocol_prompt.replace(
                "{literature_evidence}",
                "\n**LITERATURE EVIDENCE:**\nNo specific literature evidence found in database for this condition. Protocol based on general regenerative medicine principles.\n"
            )
        
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
        """Build comprehensive protocol generation prompt with literature evidence"""
        
        # Get therapy descriptions
        therapy_descriptions = []
        for therapy in available_therapies:
            therapy_descriptions.append(f"""
            **{therapy.name}**
            - Mechanisms: {', '.join(therapy.mechanism)}
            - Evidence Level: {therapy.evidence_level.value}
            - Legal Status: {therapy.legal_status}
            - Indications: {', '.join(therapy.indications)}
            """)
        
        # Note: Literature evidence will be added by the calling async method
        literature_evidence = ""
        
        return f"""
        Generate a comprehensive regenerative medicine protocol for this patient:

        **PATIENT SUMMARY:**
        Age: {patient_data.demographics.get('age', 'Unknown')}
        Gender: {patient_data.demographics.get('gender', 'Unknown')}
        Primary Diagnoses: {', '.join([d.diagnosis for d in diagnoses[:3]])}
        School of Thought: {school.value}
        Chief Complaint: {patient_data.chief_complaint}
        
        **AVAILABLE THERAPIES:**
        {chr(10).join(therapy_descriptions)}
        
        **DIAGNOSTIC DETAILS:**
        {json.dumps([{
            'diagnosis': d.diagnosis,
            'confidence': d.confidence_score,
            'mechanisms': d.mechanisms_involved,
            'supporting_evidence': d.supporting_evidence
        } for d in diagnoses[:3]], indent=2)}
        
        **MEDICAL HISTORY:**
        Past History: {', '.join(patient_data.past_medical_history) if patient_data.past_medical_history else 'None reported'}
        Current Medications: {', '.join(patient_data.medications) if patient_data.medications else 'None reported'}
        Allergies: {', '.join(patient_data.allergies) if patient_data.allergies else 'NKDA'}
        
        {literature_evidence}
        
        **INSTRUCTIONS:**
        Generate a detailed, evidence-based regenerative medicine protocol in JSON format with the following structure:
        
        {{
            "protocol_steps": [
                {{
                    "step_number": 1,
                    "therapy": "Therapy Name",
                    "dosage": "Specific dosage/concentration",
                    "timing": "When to perform (e.g., Week 1)",
                    "delivery_method": "Injection technique and guidance",
                    "monitoring_parameters": ["Pain scale", "Range of motion", "Imaging findings"],
                    "expected_outcome": "What to expect and timeline",
                    "timeframe": "When to expect results (e.g., 2-4 weeks)"
                }}
            ],
            "supporting_evidence": [
                {{
                    "citation": "Study citation with PMID",
                    "finding": "Key clinical finding supporting this protocol",
                    "evidence_level": "Study type and quality"
                }}
            ],
            "expected_outcomes": [
                "Pain reduction 30-50% within 2-4 weeks",
                "Functional improvement at 6-12 weeks",
                "Sustained benefit at 6-12 months"
            ],
            "timeline_predictions": {{
                "short_term": "2-4 weeks: Initial improvement",
                "medium_term": "2-3 months: Significant functional gains", 
                "long_term": "6-12 months: Maximum benefit achieved"
            }},
            "contraindications": ["List specific contraindications"],
            "legal_warnings": ["Regulatory considerations and off-label warnings"],
            "cost_estimate": "$X,XXX - $X,XXX",
            "confidence_score": 0.85,
            "lifestyle_recommendations": [
                "Specific activity modifications",
                "Nutritional recommendations",
                "Supplement protocols"
            ],
            "monitoring_schedule": [
                {{
                    "timepoint": "Week 2",
                    "assessment": "Pain and function evaluation",
                    "action": "Consider dose adjustment"
                }}
            ],
            "ai_reasoning": "Detailed explanation of why this protocol was selected based on patient factors and evidence"
        }}
        
        Base all recommendations on the provided evidence literature. Reference specific studies from the evidence section above. Ensure realistic timelines and success probabilities based on clinical data.
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
file_processor = None

# Simple auth function for demo
async def get_current_practitioner(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # For demo purposes, we'll create a simple practitioner
    return Practitioner(
        id="demo-practitioner-001",
        email="practitioner@regenmed.ai",
        name="Dr. Regenerative Medicine",
        specialty="Regenerative Medicine"
    )

# File Upload and Processing API Endpoints

@api_router.post("/files/upload")
async def upload_patient_file(
    file: UploadFile = File(...),
    patient_id: str = Form(...),
    file_category: str = Form(...),  # 'chart', 'genetics', 'imaging', 'labs', 'other'
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Upload and process patient files (charts, genetics, imaging, labs)"""
    
    if not file_processor:
        raise HTTPException(status_code=503, detail="File processing service unavailable")
    
    try:
        # Read file data
        file_data = await file.read()
        
        # Determine file type
        file_extension = Path(file.filename).suffix.lower()
        if file_extension in ['.dcm', '.dicom']:
            file_type = 'dicom'
        elif file_extension in ['.pdf']:
            file_type = 'pdf'
        elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            file_type = 'image'
        elif file_extension in ['.csv', '.xlsx']:
            file_type = 'csv'
        elif file_extension in ['.json']:
            file_type = 'json'
        elif file_extension in ['.xml', '.hl7']:
            file_type = 'xml'
        else:
            file_type = 'document'
        
        # Create file upload record
        file_upload = FileUpload(
            patient_id=patient_id,
            filename=file.filename,
            file_type=file_type,
            file_category=file_category,
            file_size=len(file_data)
        )
        
        # Store file record
        await db.uploaded_files.insert_one(file_upload.dict())
        
        # Process file in background
        processed_data = await file_processor.process_uploaded_file(file_data, file_upload)
        
        # Audit log
        await db.audit_log.insert_one({
            "timestamp": datetime.utcnow(),
            "practitioner_id": practitioner.id,
            "action": "file_upload_processed",
            "patient_id": patient_id,
            "file_id": file_upload.file_id,
            "file_category": file_category,
            "file_type": file_type,
            "processing_confidence": processed_data.confidence_score
        })
        
        return {
            "status": "processed",
            "file_id": file_upload.file_id,
            "processing_results": processed_data.extraction_results,
            "confidence_score": processed_data.confidence_score,
            "processing_time": processed_data.processing_time,
            "medical_insights": processed_data.medical_insights
        }
        
    except Exception as e:
        logging.error(f"File upload processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

@api_router.get("/files/patient/{patient_id}")
async def get_patient_files(
    patient_id: str,
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Get all uploaded files for a patient"""
    
    # Get uploaded files
    uploaded_files = await db.uploaded_files.find(
        {"patient_id": patient_id}
    ).sort("upload_date", -1).to_list(50)
    
    # Get processed files
    processed_files = await db.processed_files.find(
        {"patient_id": patient_id}
    ).sort("processing_time", -1).to_list(50)
    
    # Convert ObjectIds to strings for JSON serialization
    for file_doc in uploaded_files:
        if '_id' in file_doc:
            file_doc['_id'] = str(file_doc['_id'])
    
    for file_doc in processed_files:
        if '_id' in file_doc:
            file_doc['_id'] = str(file_doc['_id'])
    
    return {
        "patient_id": patient_id,
        "uploaded_files": uploaded_files,
        "processed_files": processed_files,
        "total_files": len(uploaded_files)
    }

@api_router.get("/files/comprehensive-analysis/{patient_id}")
async def get_comprehensive_patient_analysis(
    patient_id: str,
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Get comprehensive analysis combining all patient files"""
    
    if not file_processor:
        raise HTTPException(status_code=503, detail="File processing service unavailable")
    
    try:
        comprehensive_analysis = await file_processor.get_patient_file_summary(patient_id)
        
        return {
            "patient_id": patient_id,
            "comprehensive_analysis": comprehensive_analysis,
            "analysis_timestamp": datetime.utcnow(),
            "status": "complete"
        }
        
    except Exception as e:
        logging.error(f"Comprehensive analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@api_router.post("/protocols/generate-from-files")
async def generate_protocol_from_files(
    patient_id: str,
    school_of_thought: str = "ai_optimized",
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Generate protocol using comprehensive file analysis"""
    
    if not file_processor:
        raise HTTPException(status_code=503, detail="File processing service unavailable")
    
    try:
        # Get comprehensive file analysis
        file_summary = await file_processor.get_patient_file_summary(patient_id)
        
        # Get patient basic data
        patient_record = await db.patients.find_one({"patient_id": patient_id})
        if not patient_record:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        patient_data = PatientData(**patient_record)
        
        # Enhance patient data with file insights
        enhanced_patient_data = await _enhance_patient_data_with_files(patient_data, file_summary)
        
        # Generate enhanced diagnostic analysis
        diagnostic_results = await regen_ai.analyze_patient_data(enhanced_patient_data)
        
        # Generate protocol with file-based insights
        school = SchoolOfThought(school_of_thought)
        protocol = await regen_ai.generate_regenerative_protocol(
            enhanced_patient_data, diagnostic_results, school
        )
        
        # Enhance protocol with file-specific recommendations
        enhanced_protocol = await _enhance_protocol_with_file_insights(protocol, file_summary)
        
        # Store enhanced protocol
        await db.protocols.insert_one(enhanced_protocol.dict())
        
        # Audit log
        await db.audit_log.insert_one({
            "timestamp": datetime.utcnow(),
            "practitioner_id": practitioner.id,
            "action": "file_based_protocol_generated",
            "patient_id": patient_id,
            "protocol_id": enhanced_protocol.protocol_id,
            "files_analyzed": file_summary.get("total_files", 0),
            "confidence_enhancement": "file_based_analysis"
        })
        
        return {
            "protocol": enhanced_protocol,
            "file_insights_used": file_summary.get("total_files", 0),
            "enhancement_confidence": file_summary.get("comprehensive_analysis", {}).get("confidence_level", 0),
            "multi_modal_analysis": file_summary.get("comprehensive_analysis", {}).get("multi_modal_insights", {})
        }
        
    except Exception as e:
        logging.error(f"File-based protocol generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Protocol generation failed: {str(e)}")

@api_router.delete("/files/{file_id}")
async def delete_patient_file(
    file_id: str,
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Delete uploaded patient file"""
    
    # Delete from uploaded_files
    upload_result = await db.uploaded_files.delete_one({"file_id": file_id})
    
    # Delete from processed_files
    processed_result = await db.processed_files.delete_one({"file_id": file_id})
    
    if upload_result.deleted_count == 0 and processed_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Audit log
    await db.audit_log.insert_one({
        "timestamp": datetime.utcnow(),
        "practitioner_id": practitioner.id,
        "action": "file_deleted",
        "file_id": file_id
    })
    
    return {"status": "deleted", "file_id": file_id}

# Helper functions for file-based protocol enhancement
async def _enhance_patient_data_with_files(patient_data: PatientData, file_summary: Dict) -> PatientData:
    """Enhance patient data with insights from uploaded files"""
    
    comprehensive_analysis = file_summary.get("comprehensive_analysis", {})
    files_by_category = file_summary.get("files_by_category", {})
    
    # Create enhanced patient data
    enhanced_data = patient_data.dict()
    
    # Add genetic insights if available
    if "genetic_data" in files_by_category:
        genetic_files = files_by_category["genetic_data"]
        if genetic_files:
            genetic_insights = genetic_files[0].get("extraction_results", {}).get("regenerative_insights", {})
            enhanced_data["genetic_data"] = genetic_insights
    
    # Add imaging insights
    if "dicom" in files_by_category or "medical_image" in files_by_category:
        imaging_files = files_by_category.get("dicom", []) + files_by_category.get("medical_image", [])
        if imaging_files:
            imaging_insights = imaging_files[0].get("extraction_results", {}).get("regenerative_assessment", {})
            enhanced_data["imaging_data"] = [imaging_insights]
    
    # Add lab results
    if "lab_results" in files_by_category:
        lab_files = files_by_category["lab_results"]
        if lab_files:
            lab_insights = lab_files[0].get("extraction_results", {})
            enhanced_data["lab_results"] = lab_insights.get("lab_values", {})
    
    # Add chart information
    if "patient_chart" in files_by_category:
        chart_files = files_by_category["patient_chart"]
        if chart_files:
            chart_data = chart_files[0].get("extraction_results", {})
            
            # Update medical history
            if chart_data.get("medical_history"):
                enhanced_data["past_medical_history"].extend(chart_data["medical_history"])
            
            # Update medications
            if chart_data.get("current_medications"):
                enhanced_data["medications"].extend(chart_data["current_medications"])
            
            # Update allergies
            if chart_data.get("allergies"):
                enhanced_data["allergies"].extend(chart_data["allergies"])
            
            # Update chief complaint if more detailed
            if chart_data.get("chief_complaint") and len(chart_data["chief_complaint"]) > len(enhanced_data.get("chief_complaint", "")):
                enhanced_data["chief_complaint"] = chart_data["chief_complaint"]
    
    return PatientData(**enhanced_data)

async def _enhance_protocol_with_file_insights(protocol: RegenerativeProtocol, file_summary: Dict) -> RegenerativeProtocol:
    """Enhance protocol with file-specific insights and recommendations"""
    
    comprehensive_analysis = file_summary.get("comprehensive_analysis", {})
    enhanced_protocol = protocol.dict()
    
    # Add file-based evidence to supporting evidence
    integrated_recommendations = comprehensive_analysis.get("integrated_recommendations", [])
    if integrated_recommendations:
        enhanced_protocol["supporting_evidence"].extend([
            {
                "source": "multi_modal_file_analysis",
                "evidence_type": "integrated_patient_data",
                "recommendations": integrated_recommendations,
                "confidence": comprehensive_analysis.get("confidence_level", 0.8)
            }
        ])
    
    # Enhance AI reasoning with file insights
    multi_modal_insights = comprehensive_analysis.get("multi_modal_insights", {})
    if multi_modal_insights:
        enhanced_protocol["ai_reasoning"] += f"\n\nFile-Based Analysis: {json.dumps(multi_modal_insights, indent=2)}"
    
    # Update confidence score based on file analysis
    if comprehensive_analysis.get("confidence_level"):
        file_confidence = comprehensive_analysis["confidence_level"]
        original_confidence = enhanced_protocol["confidence_score"]
        # Weighted average favoring file-based analysis
        enhanced_protocol["confidence_score"] = (original_confidence * 0.4 + file_confidence * 0.6)
    
    return RegenerativeProtocol(**enhanced_protocol)

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
    """Get latest regenerative medicine literature updates with real PubMed search"""
    
    if pubmed_service:
        try:
            # First, populate database with essential papers if it's empty
            db_status = await pubmed_service.get_literature_database_status()
            
            if db_status.get("total_papers", 0) == 0:
                population_result = await pubmed_service.populate_initial_literature_database()
                logger.info(f"Literature database initialization: {population_result}")
            
            # Now perform PubMed searches for additional papers
            search_topics = [
                "platelet rich plasma osteoarthritis",
                "stem cell therapy tendinopathy", 
                "BMAC rotator cuff",
                "regenerative medicine cartilage repair"
            ]
            
            all_papers = []
            total_processed = 0
            
            # Try PubMed search for each topic, fallback to database
            for topic in search_topics:
                try:
                    result = await pubmed_service.perform_pubmed_search(topic, max_results=3)
                    if result.get("papers"):
                        all_papers.extend(result["papers"])
                        total_processed += len(result["papers"])
                except Exception as e:
                    logger.warning(f"PubMed search failed for {topic}: {str(e)}")
                    continue
            
            # If PubMed searches failed, get papers from local database
            if not all_papers:
                try:
                    local_papers = await db.literature_papers.find().sort("relevance_score", -1).limit(10).to_list(10)
                    # Convert ObjectId to string for JSON serialization
                    for paper in local_papers:
                        if '_id' in paper:
                            paper['_id'] = str(paper['_id'])
                    all_papers = local_papers
                    total_processed = len(local_papers)
                except Exception as e:
                    logger.error(f"Database fallback failed: {str(e)}")
            
            # Get updated database status
            updated_db_status = await pubmed_service.get_literature_database_status()
            
            return {
                "processing_result": {
                    "new_papers_processed": total_processed,
                    "search_topics": search_topics,
                    "status": "completed",
                    "data_source": "pubmed_api_and_database" if all_papers else "database_only"
                },
                "recent_papers": all_papers[:10],  # Most recent/relevant
                "total_papers_in_database": updated_db_status.get("total_papers", 0),
                "last_update": datetime.utcnow().isoformat(),
                "database_status": updated_db_status
            }
            
        except Exception as e:
            logger.error(f"Literature update error: {str(e)}")
            return {
                "processing_result": {"error": str(e), "new_papers_processed": 0},
                "recent_papers": [],
                "total_papers_in_database": 0,
                "last_update": datetime.utcnow().isoformat()
            }
    
    return {"status": "service_unavailable", "message": "PubMed service not initialized"}

@api_router.get("/literature/search")
async def search_literature_database(
    query: str,
    relevance_threshold: float = 0.7,
    limit: int = 20
):
    """Search literature using real PubMed API and local database"""
    
    if pubmed_service:
        try:
            # First, search local database
            search_filter = {
                "$or": [
                    {"title": {"$regex": query, "$options": "i"}},
                    {"abstract": {"$regex": query, "$options": "i"}},
                    {"search_queries": {"$in": [query.lower()]}}
                ],
                "relevance_score": {"$gte": relevance_threshold}
            }
            
            local_papers = await db.literature_papers.find(search_filter).sort("relevance_score", -1).limit(limit).to_list(limit)
            
            # Convert ObjectId to string for JSON serialization
            for paper in local_papers:
                if '_id' in paper:
                    paper['_id'] = str(paper['_id'])
            
            # If we don't have enough papers locally, search PubMed
            if len(local_papers) < limit:
                remaining_limit = limit - len(local_papers)
                pubmed_result = await pubmed_service.perform_pubmed_search(query, max_results=remaining_limit)
                
                if pubmed_result.get("papers"):
                    # Filter by relevance threshold
                    filtered_pubmed = [p for p in pubmed_result["papers"] if p.get("relevance_score", 0) >= relevance_threshold]
                    
                    # Combine results, avoiding duplicates
                    existing_pmids = {p.get("pmid") for p in local_papers}
                    new_papers = [p for p in filtered_pubmed if p.get("pmid") not in existing_pmids]
                    
                    local_papers.extend(new_papers)
            
            return {
                "query": query,
                "papers": local_papers,
                "total_results": len(local_papers),
                "relevance_threshold": relevance_threshold,
                "search_timestamp": datetime.utcnow().isoformat(),
                "sources": ["local_database", "pubmed_api"]
            }
            
        except Exception as e:
            logger.error(f"Literature search error: {str(e)}")
            return {
                "query": query,
                "papers": [],
                "total_results": 0,
                "error": str(e),
                "search_timestamp": datetime.utcnow().isoformat()
            }
    
    return {"status": "service_unavailable", "message": "Literature search service not available"}
    
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

def _build_outcome_prediction_prompt(patient, comprehensive_analysis, therapy_plan, uploaded_files):
    """Build comprehensive outcome prediction prompt"""
    
    prompt = f"""
**ADVANCED OUTCOME PREDICTION REQUEST**

**PATIENT PROFILE:**
- Age: {patient.get('demographics', {}).get('age', 'Unknown')} years
- Gender: {patient.get('demographics', {}).get('gender', 'Unknown')}
- Chief Complaint: {patient.get('chief_complaint', 'Not specified')}

**COMPREHENSIVE ANALYSIS AVAILABLE:**
"""
    
    if comprehensive_analysis:
        analysis_data = comprehensive_analysis.get('comprehensive_analysis', {})
        if analysis_data.get('differential_diagnosis'):
            prompt += f"\n• Primary Diagnosis: {analysis_data['differential_diagnosis'][0].get('diagnosis', 'Unknown')}"
            prompt += f"\n• Diagnostic Confidence: {analysis_data['differential_diagnosis'][0].get('probability', 0.0)}"
        
        if analysis_data.get('risk_assessment'):
            risk_data = analysis_data['risk_assessment']
            prompt += f"\n• Regenerative Suitability: {risk_data.get('regenerative_suitability', 'Unknown')}"
            prompt += f"\n• Complication Risk: {risk_data.get('complication_risk', 'Unknown')}"
    
    prompt += f"""

**PROPOSED THERAPY PLAN:**
- Therapy: {therapy_plan.get('therapy_name', 'Not specified')}
- Dosage: {therapy_plan.get('dosage', 'Standard protocol')}
- Delivery Method: {therapy_plan.get('delivery_method', 'Standard injection')}
- Treatment Schedule: {therapy_plan.get('schedule', 'Single treatment')}

**MULTI-MODAL DATA INTEGRATION:**
"""
    
    if uploaded_files:
        total_files = sum(len(files) for files in uploaded_files.values())
        prompt += f"\n• Total Files Analyzed: {total_files}"
        
        for category, files in uploaded_files.items():
            if files:
                prompt += f"\n• {category.title()}: {len(files)} file(s)"
    else:
        prompt += "\n• No additional files available for analysis"
    
    prompt += """

**REQUIRED PREDICTION OUTPUT (JSON FORMAT):**

{
    "outcome_predictions": {
        "success_probability": 0.85,
        "confidence_interval": [0.75, 0.95],
        "timeline_to_improvement": {
            "initial_response": "2-4 weeks",
            "significant_improvement": "6-12 weeks", 
            "maximum_benefit": "3-6 months"
        },
        "expected_outcomes": [
            "Pain reduction: 40-60%",
            "Functional improvement: 30-50%",
            "Quality of life enhancement: Moderate to significant"
        ]
    },
    "risk_factors": {
        "positive_predictors": ["Factor 1", "Factor 2"],
        "negative_predictors": ["Risk factor 1", "Risk factor 2"],
        "overall_risk_score": "Low/Moderate/High"
    },
    "biomarker_analysis": {
        "inflammatory_markers": "Expected trend",
        "regenerative_indicators": "Predicted response",
        "monitoring_recommendations": ["Biomarker 1", "Biomarker 2"]
    },
    "personalized_optimization": {
        "dosage_adjustments": "Recommendations based on patient factors",
        "timing_modifications": "Optimal treatment schedule",
        "adjuvant_therapies": ["Supportive therapy 1", "Supportive therapy 2"]
    },
    "overall_confidence": 0.88,
    "evidence_basis": "Multi-modal data integration with clinical evidence"
}

**INSTRUCTIONS:**
1. Integrate ALL available patient data (clinical, imaging, labs, genetics)
2. Consider patient-specific factors (age, comorbidities, previous treatments)
3. Provide realistic success probabilities with confidence intervals
4. Include specific biomarker predictions and monitoring recommendations
5. Suggest personalized optimization strategies
6. Base predictions on current evidence and similar patient outcomes

Generate the most accurate, evidence-based outcome prediction possible.
"""
    
    return prompt

def _generate_fallback_outcome_prediction(patient, therapy_plan):
    """Generate fallback outcome prediction when AI analysis fails"""
    
    # Basic prediction based on therapy type and patient age
    therapy_name = therapy_plan.get('therapy_name', 'regenerative therapy')
    patient_age = patient.get('demographics', {}).get('age', 50)
    
    # Age-adjusted success probability
    if patient_age < 40:
        base_success = 0.8
    elif patient_age < 60:
        base_success = 0.7
    else:
        base_success = 0.6
    
    # Therapy-specific adjustments
    therapy_multipliers = {
        'prp': 1.0,
        'bmac': 1.1,
        'stem cell': 1.2,
        'exosome': 0.9
    }
    
    therapy_key = next((key for key in therapy_multipliers.keys() if key in therapy_name.lower()), 'prp')
    adjusted_success = min(0.95, base_success * therapy_multipliers[therapy_key])
    
    return {
        "patient_id": patient.get('patient_id'),
        "therapy_plan": therapy_plan,
        "predictions": {
            "outcome_predictions": {
                "success_probability": adjusted_success,
                "confidence_interval": [max(0.1, adjusted_success - 0.15), min(0.95, adjusted_success + 0.1)],
                "timeline_to_improvement": {
                    "initial_response": "2-4 weeks",
                    "significant_improvement": "6-12 weeks",
                    "maximum_benefit": "3-6 months"
                },
                "expected_outcomes": [
                    f"Pain reduction: {int(adjusted_success * 50)}-{int(adjusted_success * 70)}%",
                    f"Functional improvement: {int(adjusted_success * 40)}-{int(adjusted_success * 60)}%",
                    "Quality of life enhancement: Moderate"
                ]
            },
            "risk_factors": {
                "positive_predictors": ["Localized condition", "Good general health"],
                "negative_predictors": ["Advanced age" if patient_age > 65 else "Systemic inflammation"],
                "overall_risk_score": "Low" if adjusted_success > 0.7 else "Moderate"
            },
            "biomarker_analysis": {
                "inflammatory_markers": "Expected reduction in CRP, ESR",
                "regenerative_indicators": "Anticipated growth factor elevation",
                "monitoring_recommendations": ["CRP", "ESR", "Pain scales"]
            },
            "personalized_optimization": {
                "dosage_adjustments": "Standard protocol appropriate",
                "timing_modifications": "Single treatment with 3-month follow-up",
                "adjuvant_therapies": ["Physical therapy", "Anti-inflammatory support"]
            },
            "overall_confidence": 0.7,
            "evidence_basis": "Clinical guidelines and age-adjusted outcomes"
        },
        "prediction_confidence": adjusted_success,
        "multi_modal_enhancement": False,
        "prediction_timestamp": datetime.utcnow().isoformat()
    }

def _parse_outcome_prediction_fallback(prediction_content, therapy_plan):
    """Parse outcome prediction when JSON parsing fails"""
    
    # Extract key information from text content
    success_probability = 0.75  # Default
    
    # Simple text parsing for success indicators
    if "excellent" in prediction_content.lower() or "high success" in prediction_content.lower():
        success_probability = 0.85
    elif "good" in prediction_content.lower() or "favorable" in prediction_content.lower():
        success_probability = 0.75
    elif "moderate" in prediction_content.lower():
        success_probability = 0.65
    elif "poor" in prediction_content.lower() or "low" in prediction_content.lower():
        success_probability = 0.45
    
    return {
        "outcome_predictions": {
            "success_probability": success_probability,
            "confidence_interval": [max(0.1, success_probability - 0.15), min(0.95, success_probability + 0.15)],
            "timeline_to_improvement": {
                "initial_response": "2-4 weeks",
                "significant_improvement": "6-12 weeks",
                "maximum_benefit": "3-6 months"
            },
            "expected_outcomes": [
                f"Pain reduction: {int(success_probability * 50)}-{int(success_probability * 70)}%",
                f"Functional improvement: {int(success_probability * 40)}-{int(success_probability * 60)}%",
                "Quality of life enhancement based on therapy response"
            ]
        },
        "risk_factors": {
            "positive_predictors": ["Patient-specific factors identified"],
            "negative_predictors": ["Individual risk assessment required"],
            "overall_risk_score": "Moderate"
        },
        "biomarker_analysis": {
            "inflammatory_markers": "Standard monitoring recommended",
            "regenerative_indicators": "Response tracking advised",
            "monitoring_recommendations": ["Standard biomarker panel"]
        },
        "personalized_optimization": {
            "dosage_adjustments": "Clinical judgment required",
            "timing_modifications": "Standard protocol",
            "adjuvant_therapies": ["Supportive care as indicated"]
        },
        "overall_confidence": 0.7,
        "evidence_basis": "Clinical assessment and standard protocols"
    }

@api_router.get("/patients/{patient_id}/comprehensive-analysis")
async def get_comprehensive_patient_analysis_v2(
    patient_id: str,
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Get comprehensive patient analysis including differential diagnosis and multi-modal insights"""
    
    try:
        # Get the most recent comprehensive analysis
        analysis = await db.comprehensive_analyses.find_one(
            {"patient_id": patient_id},
            sort=[("analysis_timestamp", -1)]
        )
        
        if not analysis:
            # If no analysis exists, generate one
            patient = await db.patients.find_one({"patient_id": patient_id})
            if not patient:
                raise HTTPException(status_code=404, detail="Patient not found")
            
            # Convert to PatientData object and analyze
            patient_data = PatientData(**patient)
            ai_engine = RegenerativeMedicineAI(OPENAI_API_KEY)
            diagnostic_results = await ai_engine.analyze_patient_data(patient_data)
            
            # Try to get the analysis that was just created
            analysis = await db.comprehensive_analyses.find_one(
                {"patient_id": patient_id},
                sort=[("analysis_timestamp", -1)]
            )
        
        if analysis:
            # Convert ObjectId to string for JSON serialization
            if '_id' in analysis:
                analysis['_id'] = str(analysis['_id'])
                
            return {
                "patient_id": patient_id,
                "analysis": analysis.get("comprehensive_analysis", {}),
                "multi_modal_files_used": analysis.get("multi_modal_files_used", 0),
                "file_categories": analysis.get("file_categories", []),
                "analysis_timestamp": analysis.get("analysis_timestamp"),
                "status": "completed"
            }
        else:
            return {
                "patient_id": patient_id,
                "analysis": {"status": "Analysis in progress"},
                "multi_modal_files_used": 0,
                "file_categories": [],
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "status": "generating"
            }
            
    except Exception as e:
        logging.error(f"Comprehensive analysis retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis retrieval failed: {str(e)}")

@api_router.post("/patients/{patient_id}/outcome-prediction")
async def predict_treatment_outcomes_advanced(
    patient_id: str,
    therapy_plan: Dict[str, Any],
    practitioner: Practitioner = Depends(get_current_practitioner)
):
    """Generate advanced outcome predictions with confidence intervals and biomarker analysis"""
    
    try:
        # Get patient data
        patient = await db.patients.find_one({"patient_id": patient_id})
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Get comprehensive analysis if available
        comprehensive_analysis = await db.comprehensive_analyses.find_one(
            {"patient_id": patient_id},
            sort=[("analysis_timestamp", -1)]
        )
        
        # Get uploaded files for enhanced predictions
        uploaded_files = {}
        if file_processor:
            try:
                file_summary = await file_processor.get_patient_file_summary(patient_id)
                uploaded_files = file_summary.get("files_by_category", {})
            except Exception as e:
                logging.warning(f"File summary retrieval failed: {str(e)}")
        
        # Build outcome prediction prompt
        prediction_prompt = _build_outcome_prediction_prompt(
            patient, comprehensive_analysis, therapy_plan, uploaded_files
        )
        
        # Generate AI-powered outcome prediction using the existing OpenAI integration
        try:
            ai_engine = RegenerativeMedicineAI(OPENAI_API_KEY)
            
            # Use the existing httpx client pattern
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{ai_engine.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {ai_engine.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4",
                        "messages": [
                            {
                                "role": "system",
                                "content": """You are a world-renowned expert in regenerative medicine outcomes research and predictive analytics. You have access to:

- 25+ years of clinical outcome data
- Advanced biomarker analysis and prognostic modeling
- Genetic variants affecting treatment response
- Multi-modal data integration for personalized predictions
- Statistical modeling for confidence intervals

Your expertise includes predicting treatment success rates, timeline to improvement, risk factors, and personalized optimization strategies based on patient-specific factors.

Provide evidence-based outcome predictions with statistical confidence intervals and detailed reasoning."""
                            },
                            {"role": "user", "content": prediction_prompt}
                        ],
                        "max_tokens": 3000,
                        "temperature": 0.3
                    }
                )
            
            if response.status_code != 200:
                logging.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return _generate_fallback_outcome_prediction(patient, therapy_plan)
            
            ai_response = response.json()
            prediction_content = ai_response['choices'][0]['message']['content']
            
            # Parse and structure outcome predictions
            try:
                prediction_data = json.loads(prediction_content)
            except json.JSONDecodeError:
                # Fallback parsing if JSON fails
                prediction_data = _parse_outcome_prediction_fallback(prediction_content, therapy_plan)
            
            # Store prediction in database
            prediction_doc = {
                "patient_id": patient_id,
                "therapy_plan": therapy_plan,
                "outcome_prediction": prediction_data,
                "prediction_timestamp": datetime.utcnow(),
                "multi_modal_enhancement": bool(uploaded_files),
                "files_integrated": sum(len(files) for files in uploaded_files.values()) if uploaded_files else 0
            }
            
            await db.outcome_predictions.insert_one(prediction_doc)
            
            return {
                "patient_id": patient_id,
                "therapy_plan": therapy_plan,
                "predictions": prediction_data,
                "prediction_confidence": prediction_data.get("overall_confidence", 0.8),
                "multi_modal_enhancement": bool(uploaded_files),
                "prediction_timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logging.error(f"AI outcome prediction failed: {str(e)}")
            # Generate fallback prediction
            fallback_prediction = _generate_fallback_outcome_prediction(patient, therapy_plan)
            return fallback_prediction
            
    except Exception as e:
        logging.error(f"Outcome prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Outcome prediction failed: {str(e)}")

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
    
    # Convert ObjectIds to strings for JSON serialization
    for outcome in recent_outcomes:
        if '_id' in outcome:
            outcome['_id'] = str(outcome['_id'])
    
    # Get audit trail
    recent_activities = await db.audit_log.find(
        {"practitioner_id": practitioner.id}
    ).sort("timestamp", -1).limit(20).to_list(20)
    
    # Convert ObjectIds to strings for JSON serialization
    for activity in recent_activities:
        if '_id' in activity:
            activity['_id'] = str(activity['_id'])
    
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
    global federated_service, pubmed_service, dicom_service, prediction_service, file_processor
    
    try:
        # Initialize advanced services
        federated_service = FederatedLearningService(db)
        pubmed_service = PubMedIntegrationService(db)
        dicom_service = DICOMProcessingService(db)
        prediction_service = OutcomePredictionService(db)
        file_processor = MedicalFileProcessor(db, OPENAI_API_KEY)
        
        # Initialize services
        await initialize_advanced_services(db)
        
        logger.info("Advanced AI services and file processing initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize advanced services: {str(e)}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)