import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import { Textarea } from "./components/ui/textarea";
import { Badge } from "./components/ui/badge";
import { Separator } from "./components/ui/separator";
import { Alert, AlertDescription } from "./components/ui/alert";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { Brain, User, FileText, Activity, Loader2, Stethoscope, TestTube, Pill } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [activeTab, setActiveTab] = useState("patient-input");
  const [loading, setLoading] = useState(false);
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [diagnosticResults, setDiagnosticResults] = useState(null);
  
  // Patient form state
  const [patientForm, setPatientForm] = useState({
    demographics: {
      name: "",
      age: "",
      gender: "",
      occupation: ""
    },
    chief_complaint: "",
    history_present_illness: "",
    past_medical_history: [],
    medications: [],
    allergies: [],
    vital_signs: {
      temperature: "",
      blood_pressure: "",
      heart_rate: "",
      respiratory_rate: "",
      oxygen_saturation: ""
    },
    symptoms: []
  });

  const [newSymptom, setNewSymptom] = useState("");
  const [newMedication, setNewMedication] = useState("");
  const [newAllergy, setNewAllergy] = useState("");
  const [newHistory, setNewHistory] = useState("");

  // Load patients on component mount
  useEffect(() => {
    loadPatients();
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const response = await axios.get(`${API}/health`);
      console.log("System Health:", response.data);
    } catch (error) {
      console.error("Health check failed:", error);
    }
  };

  const loadPatients = async () => {
    try {
      const response = await axios.get(`${API}/patients`);
      setPatients(response.data);
    } catch (error) {
      console.error("Failed to load patients:", error);
    }
  };

  const handleCreatePatient = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await axios.post(`${API}/patients`, patientForm);
      setSelectedPatient(response.data);
      setActiveTab("diagnostic");
      await loadPatients();
    } catch (error) {
      console.error("Failed to create patient:", error);
      alert("Failed to create patient record");
    } finally {
      setLoading(false);
    }
  };

  const handleDiagnose = async (patientId) => {
    setLoading(true);
    setDiagnosticResults(null);
    
    try {
      const response = await axios.post(`${API}/diagnose/${patientId}`);
      setDiagnosticResults(response.data);
    } catch (error) {
      console.error("Diagnostic failed:", error);
      alert("Diagnostic analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const addToList = (listName, value, setter) => {
    if (value.trim()) {
      setPatientForm(prev => ({
        ...prev,
        [listName]: [...prev[listName], value.trim()]
      }));
      setter("");
    }
  };

  const removeFromList = (listName, index) => {
    setPatientForm(prev => ({
      ...prev,
      [listName]: prev[listName].filter((_, i) => i !== index)
    }));
  };

  const getConfidenceColor = (score) => {
    if (score >= 0.8) return "bg-green-500";
    if (score >= 0.6) return "bg-yellow-500";
    return "bg-red-500";
  };

  const getConfidenceText = (score) => {
    if (score >= 0.8) return "High Confidence";
    if (score >= 0.6) return "Moderate Confidence";
    return "Low Confidence";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-lg border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl">
                <Brain className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
                  AI Medical Diagnostics
                </h1>
                <p className="text-sm text-slate-600">Regenerative Medicine Knowledge Platform</p>
              </div>
            </div>
            <Badge variant="outline" className="px-3 py-1">
              <Activity className="h-4 w-4 mr-2" />
              System Active
            </Badge>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-3 bg-white/70 backdrop-blur-sm">
            <TabsTrigger value="patient-input" className="flex items-center gap-2">
              <User className="h-4 w-4" />
              Patient Input
            </TabsTrigger>
            <TabsTrigger value="diagnostic" className="flex items-center gap-2">
              <Brain className="h-4 w-4" />
              AI Diagnosis
            </TabsTrigger>
            <TabsTrigger value="patients" className="flex items-center gap-2">
              <FileText className="h-4 w-4" />
              Patient Records
            </TabsTrigger>
          </TabsList>

          {/* Patient Input Tab */}
          <TabsContent value="patient-input" className="space-y-6">
            <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Stethoscope className="h-5 w-5 text-blue-600" />
                  New Patient Assessment
                </CardTitle>
                <CardDescription>
                  Enter comprehensive patient information for AI-powered diagnostic analysis
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleCreatePatient} className="space-y-6">
                  {/* Demographics */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="name">Patient Name</Label>
                      <Input
                        id="name"
                        value={patientForm.demographics.name}
                        onChange={(e) => setPatientForm(prev => ({
                          ...prev,
                          demographics: { ...prev.demographics, name: e.target.value }
                        }))}
                        placeholder="Enter patient name"
                        required
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-2">
                      <div className="space-y-2">
                        <Label htmlFor="age">Age</Label>
                        <Input
                          id="age"
                          type="number"
                          value={patientForm.demographics.age}
                          onChange={(e) => setPatientForm(prev => ({
                            ...prev,
                            demographics: { ...prev.demographics, age: e.target.value }
                          }))}
                          placeholder="Age"
                          required
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="gender">Gender</Label>
                        <select
                          id="gender"
                          className="w-full px-3 py-2 bg-background border border-input rounded-md"
                          value={patientForm.demographics.gender}
                          onChange={(e) => setPatientForm(prev => ({
                            ...prev,
                            demographics: { ...prev.demographics, gender: e.target.value }
                          }))}
                          required
                        >
                          <option value="">Select</option>
                          <option value="Male">Male</option>
                          <option value="Female">Female</option>
                          <option value="Other">Other</option>
                        </select>
                      </div>
                    </div>
                  </div>

                  {/* Chief Complaint */}
                  <div className="space-y-2">
                    <Label htmlFor="chief_complaint">Chief Complaint</Label>
                    <Textarea
                      id="chief_complaint"
                      value={patientForm.chief_complaint}
                      onChange={(e) => setPatientForm(prev => ({
                        ...prev,
                        chief_complaint: e.target.value
                      }))}
                      placeholder="Primary reason for visit..."
                      required
                      className="min-h-[80px]"
                    />
                  </div>

                  {/* History of Present Illness */}
                  <div className="space-y-2">
                    <Label htmlFor="hpi">History of Present Illness</Label>
                    <Textarea
                      id="hpi"
                      value={patientForm.history_present_illness}
                      onChange={(e) => setPatientForm(prev => ({
                        ...prev,
                        history_present_illness: e.target.value
                      }))}
                      placeholder="Detailed description of current condition..."
                      required
                      className="min-h-[120px]"
                    />
                  </div>

                  {/* Vital Signs */}
                  <div className="space-y-3">
                    <Label>Vital Signs</Label>
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                      <div className="space-y-1">
                        <Label className="text-xs">Temperature (°F)</Label>
                        <Input
                          placeholder="98.6"
                          value={patientForm.vital_signs.temperature}
                          onChange={(e) => setPatientForm(prev => ({
                            ...prev,
                            vital_signs: { ...prev.vital_signs, temperature: e.target.value }
                          }))}
                        />
                      </div>
                      <div className="space-y-1">
                        <Label className="text-xs">BP (mmHg)</Label>
                        <Input
                          placeholder="120/80"
                          value={patientForm.vital_signs.blood_pressure}
                          onChange={(e) => setPatientForm(prev => ({
                            ...prev,
                            vital_signs: { ...prev.vital_signs, blood_pressure: e.target.value }
                          }))}
                        />
                      </div>
                      <div className="space-y-1">
                        <Label className="text-xs">HR (bpm)</Label>
                        <Input
                          placeholder="72"
                          value={patientForm.vital_signs.heart_rate}
                          onChange={(e) => setPatientForm(prev => ({
                            ...prev,
                            vital_signs: { ...prev.vital_signs, heart_rate: e.target.value }
                          }))}
                        />
                      </div>
                      <div className="space-y-1">
                        <Label className="text-xs">RR (bpm)</Label>
                        <Input
                          placeholder="16"
                          value={patientForm.vital_signs.respiratory_rate}
                          onChange={(e) => setPatientForm(prev => ({
                            ...prev,
                            vital_signs: { ...prev.vital_signs, respiratory_rate: e.target.value }
                          }))}
                        />
                      </div>
                      <div className="space-y-1">
                        <Label className="text-xs">O2 Sat (%)</Label>
                        <Input
                          placeholder="98"
                          value={patientForm.vital_signs.oxygen_saturation}
                          onChange={(e) => setPatientForm(prev => ({
                            ...prev,
                            vital_signs: { ...prev.vital_signs, oxygen_saturation: e.target.value }
                          }))}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Dynamic Lists */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Symptoms */}
                    <div className="space-y-3">
                      <Label>Symptoms</Label>
                      <div className="flex gap-2">
                        <Input
                          value={newSymptom}
                          onChange={(e) => setNewSymptom(e.target.value)}
                          placeholder="Add symptom..."
                          onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addToList('symptoms', newSymptom, setNewSymptom))}
                        />
                        <Button 
                          type="button" 
                          onClick={() => addToList('symptoms', newSymptom, setNewSymptom)}
                          size="sm"
                        >
                          Add
                        </Button>
                      </div>
                      <div className="flex flex-wrap gap-2 max-h-24 overflow-y-auto">
                        {patientForm.symptoms.map((symptom, index) => (
                          <Badge
                            key={index}
                            variant="secondary"
                            className="cursor-pointer hover:bg-destructive hover:text-destructive-foreground"
                            onClick={() => removeFromList('symptoms', index)}
                          >
                            {symptom} ×
                          </Badge>
                        ))}
                      </div>
                    </div>

                    {/* Medications */}
                    <div className="space-y-3">
                      <Label>Current Medications</Label>
                      <div className="flex gap-2">
                        <Input
                          value={newMedication}
                          onChange={(e) => setNewMedication(e.target.value)}
                          placeholder="Add medication..."
                          onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addToList('medications', newMedication, setNewMedication))}
                        />
                        <Button 
                          type="button" 
                          onClick={() => addToList('medications', newMedication, setNewMedication)}
                          size="sm"
                        >
                          Add
                        </Button>
                      </div>
                      <div className="flex flex-wrap gap-2 max-h-24 overflow-y-auto">
                        {patientForm.medications.map((med, index) => (
                          <Badge
                            key={index}
                            variant="secondary"
                            className="cursor-pointer hover:bg-destructive hover:text-destructive-foreground"
                            onClick={() => removeFromList('medications', index)}
                          >
                            {med} ×
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>

                  <Button type="submit" disabled={loading} className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700">
                    {loading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Creating Patient Record...
                      </>
                    ) : (
                      <>
                        <User className="mr-2 h-4 w-4" />
                        Create Patient & Start Diagnosis
                      </>
                    )}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </TabsContent>

          {/* AI Diagnosis Tab */}
          <TabsContent value="diagnostic" className="space-y-6">
            {selectedPatient ? (
              <>
                <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span className="flex items-center gap-2">
                        <Brain className="h-5 w-5 text-indigo-600" />
                        AI Diagnostic Analysis
                      </span>
                      <Button
                        onClick={() => handleDiagnose(selectedPatient.patient_id)}
                        disabled={loading}
                        className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700"
                      >
                        {loading ? (
                          <>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Analyzing...
                          </>
                        ) : (
                          <>
                            <Brain className="mr-2 h-4 w-4" />
                            Generate Diagnosis
                          </>
                        )}
                      </Button>
                    </CardTitle>
                    <CardDescription>
                      Patient: {selectedPatient.demographics.name} | 
                      Age: {selectedPatient.demographics.age} | 
                      Gender: {selectedPatient.demographics.gender}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <h4 className="font-semibold mb-2">Chief Complaint:</h4>
                        <p className="text-slate-700 bg-slate-50 p-3 rounded-lg">{selectedPatient.chief_complaint}</p>
                      </div>
                      
                      {diagnosticResults && (
                        <div className="space-y-6 mt-6">
                          <Separator />
                          
                          <div>
                            <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                              <TestTube className="h-5 w-5 text-green-600" />
                              Differential Diagnoses
                            </h3>
                            
                            <div className="space-y-4">
                              {diagnosticResults.differential_diagnoses.map((diagnosis, index) => (
                                <Card key={index} className="border-l-4 border-l-blue-500">
                                  <CardContent className="pt-4">
                                    <div className="flex items-start justify-between mb-3">
                                      <h4 className="text-lg font-semibold">{diagnosis.diagnosis}</h4>
                                      <div className="flex items-center gap-2">
                                        <div className={`w-3 h-3 rounded-full ${getConfidenceColor(diagnosis.confidence_score)}`}></div>
                                        <Badge variant="outline">
                                          {Math.round(diagnosis.confidence_score * 100)}% - {getConfidenceText(diagnosis.confidence_score)}
                                        </Badge>
                                      </div>
                                    </div>
                                    
                                    <p className="text-slate-700 mb-3">{diagnosis.reasoning}</p>
                                    
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                                      <div>
                                        <h5 className="font-medium mb-2">Supporting Evidence:</h5>
                                        <ul className="list-disc list-inside text-slate-600 space-y-1">
                                          {diagnosis.supporting_evidence.map((evidence, i) => (
                                            <li key={i}>{evidence}</li>
                                          ))}
                                        </ul>
                                      </div>
                                      
                                      <div>
                                        <h5 className="font-medium mb-2 flex items-center gap-1">
                                          <TestTube className="h-4 w-4" />
                                          Recommended Tests:
                                        </h5>
                                        <ul className="list-disc list-inside text-slate-600 space-y-1">
                                          {diagnosis.recommended_tests.map((test, i) => (
                                            <li key={i}>{test}</li>
                                          ))}
                                        </ul>
                                      </div>
                                      
                                      <div>
                                        <h5 className="font-medium mb-2 flex items-center gap-1">
                                          <Pill className="h-4 w-4" />
                                          Treatment Protocols:
                                        </h5>
                                        <ul className="list-disc list-inside text-slate-600 space-y-1">
                                          {diagnosis.treatment_protocols.map((protocol, i) => (
                                            <li key={i}>{protocol}</li>
                                          ))}
                                        </ul>
                                      </div>
                                    </div>
                                  </CardContent>
                                </Card>
                              ))}
                            </div>
                          </div>
                          
                          <div>
                            <h4 className="font-semibold mb-2">Clinical Summary:</h4>
                            <p className="text-slate-700 bg-blue-50 p-4 rounded-lg">{diagnosticResults.explanation}</p>
                          </div>
                          
                          <div>
                            <h4 className="font-semibold mb-2">Recommended Next Steps:</h4>
                            <ul className="list-disc list-inside text-slate-700 space-y-1 bg-green-50 p-4 rounded-lg">
                              {diagnosticResults.next_steps.map((step, index) => (
                                <li key={index}>{step}</li>
                              ))}
                            </ul>
                          </div>
                          
                          <Alert>
                            <Brain className="h-4 w-4" />
                            <AlertDescription>
                              Processing completed in {diagnosticResults.processing_time_seconds.toFixed(2)} seconds. 
                              This AI analysis is for educational purposes and should be validated by medical professionals.
                            </AlertDescription>
                          </Alert>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </>
            ) : (
              <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
                <CardContent className="text-center py-12">
                  <Brain className="h-16 w-16 mx-auto text-slate-400 mb-4" />
                  <h3 className="text-xl font-semibold mb-2">No Patient Selected</h3>
                  <p className="text-slate-600">
                    Create a new patient record or select an existing patient to start diagnostic analysis.
                  </p>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Patient Records Tab */}
          <TabsContent value="patients" className="space-y-6">
            <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5 text-slate-600" />
                  Patient Records
                </CardTitle>
                <CardDescription>
                  View and manage patient records and diagnostic history
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {patients.map((patient) => (
                    <Card 
                      key={patient.patient_id} 
                      className="cursor-pointer hover:shadow-md transition-shadow border-l-4 border-l-blue-500"
                      onClick={() => {
                        setSelectedPatient(patient);
                        setActiveTab("diagnostic");
                      }}
                    >
                      <CardContent className="pt-4">
                        <div className="flex items-start justify-between mb-2">
                          <h4 className="font-semibold">{patient.demographics.name}</h4>
                          <Badge variant="outline">{patient.demographics.age}y</Badge>
                        </div>
                        <p className="text-sm text-slate-600 mb-2">{patient.chief_complaint}</p>
                        <p className="text-xs text-slate-500">
                          Created: {new Date(patient.created_at).toLocaleDateString()}
                        </p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
                
                {patients.length === 0 && (
                  <div className="text-center py-12">
                    <User className="h-16 w-16 mx-auto text-slate-400 mb-4" />
                    <h3 className="text-xl font-semibold mb-2">No Patient Records</h3>
                    <p className="text-slate-600">
                      Start by creating your first patient record in the Patient Input tab.
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}

export default App;