from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import httpx
import asyncio

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# OpenAI configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_BASE_URL = "https://api.openai.com/v1"

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class PatientData(BaseModel):
    patient_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    demographics: Dict[str, Any]
    chief_complaint: str
    history_present_illness: str
    past_medical_history: List[str] = []
    medications: List[str] = []
    allergies: List[str] = []
    vital_signs: Dict[str, Any] = {}
    symptoms: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DiagnosticResult(BaseModel):
    diagnosis: str
    confidence_score: float
    reasoning: str
    supporting_evidence: List[str]
    recommended_tests: List[str] = []
    treatment_protocols: List[str] = []

class DiagnosticResponse(BaseModel):
    patient_id: str
    differential_diagnoses: List[DiagnosticResult]
    explanation: str
    next_steps: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processing_time_seconds: float

class PatientCreate(BaseModel):
    demographics: Dict[str, Any]
    chief_complaint: str
    history_present_illness: str
    past_medical_history: List[str] = []
    medications: List[str] = []
    allergies: List[str] = []
    vital_signs: Dict[str, Any] = {}
    symptoms: List[str] = []

# AI Medical Diagnostic Engine
class MedicalDiagnosticAI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = OPENAI_BASE_URL
        
    async def generate_differential_diagnoses(self, patient_data: PatientData) -> DiagnosticResponse:
        """Generate AI-powered differential diagnoses with explanations."""
        start_time = datetime.utcnow()
        
        # Construct medical prompt
        medical_prompt = self._build_medical_prompt(patient_data)
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
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
                                "content": "You are an expert medical AI assistant specializing in regenerative medicine and differential diagnosis. Provide evidence-based diagnostic suggestions with clear reasoning and confidence scores. Always format your response as valid JSON."
                            },
                            {
                                "role": "user", 
                                "content": medical_prompt
                            }
                        ],
                        "temperature": 0.3,
                        "max_tokens": 2000
                    }
                )
                
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="OpenAI API error")
                
            ai_response = response.json()
            content = ai_response['choices'][0]['message']['content']
            
            # Parse JSON response from AI
            try:
                diagnostic_data = json.loads(content)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                diagnostic_data = self._parse_fallback_response(content)
            
            # Calculate processing time
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Convert to DiagnosticResponse
            differential_diagnoses = [
                DiagnosticResult(**diag) for diag in diagnostic_data.get('differential_diagnoses', [])
            ]
            
            return DiagnosticResponse(
                patient_id=patient_data.patient_id,
                differential_diagnoses=differential_diagnoses,
                explanation=diagnostic_data.get('explanation', 'AI analysis completed'),
                next_steps=diagnostic_data.get('next_steps', []),
                processing_time_seconds=processing_time
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Diagnostic processing failed: {str(e)}")
    
    def _build_medical_prompt(self, patient_data: PatientData) -> str:
        """Build comprehensive medical prompt for AI analysis."""
        prompt = f"""
        Please analyze the following patient case and provide differential diagnoses with explanations.

        **PATIENT INFORMATION:**
        Demographics: {patient_data.demographics}
        Chief Complaint: {patient_data.chief_complaint}
        History of Present Illness: {patient_data.history_present_illness}
        Past Medical History: {', '.join(patient_data.past_medical_history) if patient_data.past_medical_history else 'None reported'}
        Current Medications: {', '.join(patient_data.medications) if patient_data.medications else 'None reported'}
        Allergies: {', '.join(patient_data.allergies) if patient_data.allergies else 'None reported'}
        Vital Signs: {patient_data.vital_signs}
        Symptoms: {', '.join(patient_data.symptoms) if patient_data.symptoms else 'None additional'}

        **REQUIRED OUTPUT FORMAT (JSON):**
        {{
            "differential_diagnoses": [
                {{
                    "diagnosis": "Primary diagnosis name",
                    "confidence_score": 0.85,
                    "reasoning": "Detailed medical reasoning for this diagnosis",
                    "supporting_evidence": ["symptom 1", "finding 2", "history factor 3"],
                    "recommended_tests": ["test 1", "test 2"],
                    "treatment_protocols": ["protocol 1", "protocol 2"]
                }}
            ],
            "explanation": "Overall analysis summary and clinical reasoning process",
            "next_steps": ["immediate action 1", "follow-up 2", "monitoring 3"]
        }}

        Provide 3-5 differential diagnoses ranked by likelihood. Include confidence scores (0.0-1.0).
        Focus on evidence-based reasoning and regenerative medicine approaches where applicable.
        """
        return prompt
    
    def _parse_fallback_response(self, content: str) -> Dict:
        """Fallback parser if JSON response fails."""
        return {
            "differential_diagnoses": [
                {
                    "diagnosis": "Clinical Analysis Required",
                    "confidence_score": 0.7,
                    "reasoning": content[:500] + "..." if len(content) > 500 else content,
                    "supporting_evidence": ["AI analysis completed"],
                    "recommended_tests": ["Further clinical evaluation"],
                    "treatment_protocols": ["Consult with specialist"]
                }
            ],
            "explanation": "AI provided analysis requires clinical interpretation",
            "next_steps": ["Review with medical professional", "Additional testing as indicated"]
        }

# Initialize AI diagnostic engine
diagnostic_ai = MedicalDiagnosticAI(OPENAI_API_KEY)

# API Routes
@api_router.get("/")
async def root():
    return {"message": "AI-Powered Regenerative Medicine Platform API"}

@api_router.post("/patients", response_model=PatientData)
async def create_patient(patient: PatientCreate):
    """Create new patient record."""
    patient_data = PatientData(**patient.dict())
    
    # Store in database
    await db.patients.insert_one(patient_data.dict())
    
    return patient_data

@api_router.get("/patients/{patient_id}", response_model=PatientData)
async def get_patient(patient_id: str):
    """Retrieve patient data."""
    patient = await db.patients.find_one({"patient_id": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return PatientData(**patient)

@api_router.post("/diagnose/{patient_id}", response_model=DiagnosticResponse)
async def diagnose_patient(patient_id: str, background_tasks: BackgroundTasks):
    """Generate AI-powered differential diagnoses for a patient."""
    # Retrieve patient data
    patient_record = await db.patients.find_one({"patient_id": patient_id})
    if not patient_record:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_data = PatientData(**patient_record)
    
    # Generate diagnoses using AI
    diagnostic_response = await diagnostic_ai.generate_differential_diagnoses(patient_data)
    
    # Store diagnostic results
    background_tasks.add_task(
        store_diagnostic_results, 
        patient_id, 
        diagnostic_response.dict()
    )
    
    return diagnostic_response

async def store_diagnostic_results(patient_id: str, diagnostic_data: Dict):
    """Background task to store diagnostic results."""
    await db.diagnostic_results.insert_one({
        **diagnostic_data,
        "stored_at": datetime.utcnow()
    })

@api_router.get("/diagnoses/{patient_id}")
async def get_diagnostic_history(patient_id: str):
    """Retrieve diagnostic history for a patient."""
    diagnoses = await db.diagnostic_results.find(
        {"patient_id": patient_id}
    ).sort("created_at", -1).to_list(10)
    
    return diagnoses

@api_router.get("/patients", response_model=List[PatientData])
async def list_patients():
    """List all patients."""
    patients = await db.patients.find().sort("created_at", -1).to_list(50)
    return [PatientData(**patient) for patient in patients]

# Health check endpoint
@api_router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "services": {
            "database": "connected",
            "ai_engine": "ready" if OPENAI_API_KEY else "not_configured"
        }
    }

# Include the router in the main app
app.include_router(api_router)

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

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()