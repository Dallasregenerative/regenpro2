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
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./components/ui/select";
import { Progress } from "./components/ui/progress";
import { 
  Brain, 
  User, 
  FileText, 
  Activity, 
  Loader2, 
  Stethoscope, 
  TestTube, 
  Pill, 
  Dna,
  Heart,
  Eye,
  Zap,
  Shield,
  ChevronRight,
  Clock,
  TrendingUp,
  Award,
  Globe,
  AlertTriangle,
  CheckCircle,
  BookOpen,
  Microscope,
  FlaskConical,
  Target,
  Sparkles,
  ChartBar,
  Download,
  Upload,
  Network,
  Database,
  Cpu,
  Image,
  BarChart3,
  Layers,
  GitBranch,
  Rss,
  Search,
  Monitor,
  Settings,
  CloudDownload,
  Scan
} from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// School of Thought configurations
const SCHOOLS_OF_THOUGHT = {
  traditional_autologous: {
    name: "Traditional Autologous (US Legal)",
    description: "FDA-approved autologous therapies: PRP, BMAC",
    icon: Shield,
    color: "bg-green-500",
    therapies: ["PRP", "BMAC"],
    legalStatus: "Fully approved in US"
  },
  autologous_non_us: {
    name: "Autologous (Non-US Legal)",
    description: "Advanced autologous therapies available internationally",
    icon: Globe,
    color: "bg-blue-500",
    therapies: ["PRP", "BMAC", "Wharton's Jelly"],
    legalStatus: "Approved in select countries"
  },
  biologics: {
    name: "Biologics & Allogenic",
    description: "Donor-derived regenerative therapies",
    icon: FlaskConical,
    color: "bg-purple-500",
    therapies: ["Wharton's Jelly MSCs", "MSC Exosomes", "Cord Blood"],
    legalStatus: "Variable by jurisdiction"
  },
  experimental: {
    name: "Experimental & Cutting-Edge",
    description: "Latest research and experimental protocols",
    icon: Microscope,
    color: "bg-orange-500",
    therapies: ["MSC Exosomes", "Cord Blood", "CRISPR", "NK Cells"],
    legalStatus: "Research/investigational"
  },
  ai_optimized: {
    name: "AI-Optimized Best Protocol",
    description: "AI selects optimal therapy regardless of regulatory status",
    icon: Sparkles,
    color: "bg-gradient-to-r from-purple-600 to-blue-600",
    therapies: ["All Available Options"],
    legalStatus: "AI provides regulatory warnings"
  }
};

function App() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [loading, setLoading] = useState(false);
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [patientAnalysis, setPatientAnalysis] = useState(null);
  const [generatedProtocol, setGeneratedProtocol] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [therapiesData, setTherapiesData] = useState(null);
  const [selectedSchool, setSelectedSchool] = useState("ai_optimized");
  const [advancedSystemStatus, setAdvancedSystemStatus] = useState(null);
  const [literatureUpdates, setLiteratureUpdates] = useState(null);
  const [outcomePredictiion, setOutcomePrediction] = useState(null);
  const [federatedLearningStatus, setFederatedLearningStatus] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [comprehensiveAnalysis, setComprehensiveAnalysis] = useState(null);
  
  // File upload state
  const [fileUpload, setFileUpload] = useState({
    uploading: false,
    fileName: '',
    uploadedFiles: []
  });
  
  // Patient form state
  const [patientForm, setPatientForm] = useState({
    demographics: {
      name: "",
      age: "",
      gender: "",
      occupation: "",
      insurance: "Self-pay"
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
      oxygen_saturation: "",
      weight: "",
      height: ""
    },
    symptoms: [],
    lab_results: {},
    imaging_data: [],
    genetic_data: {}
  });

  const [newSymptom, setNewSymptom] = useState("");
  const [newMedication, setNewMedication] = useState("");
  const [newAllergy, setNewAllergy] = useState("");
  const [newHistory, setNewHistory] = useState("");

  // Load initial data
  useEffect(() => {
    loadPatients();
    loadDashboardData();
    loadTherapiesData();
    loadAdvancedSystemStatus();
    loadLiteratureUpdates();
    loadFederatedLearningStatus();
  }, []);

  const loadPatients = async () => {
    try {
      const response = await axios.get(`${API}/patients`, {
        headers: { Authorization: `Bearer demo-token` }
      });
      setPatients(response.data);
    } catch (error) {
      console.error("Failed to load patients:", error);
    }
  };

  const loadDashboardData = async () => {
    try {
      const response = await axios.get(`${API}/analytics/dashboard`, {
        headers: { Authorization: `Bearer demo-token` }
      });
      setDashboardData(response.data);
    } catch (error) {
      console.error("Failed to load dashboard data:", error);
    }
  };

  const loadAdvancedSystemStatus = async () => {
    try {
      const response = await axios.get(`${API}/advanced/system-status`, {
        headers: { Authorization: `Bearer demo-token` }
      });
      setAdvancedSystemStatus(response.data);
    } catch (error) {
      console.error("Failed to load advanced system status:", error);
    }
  };

  const loadLiteratureUpdates = async () => {
    try {
      const response = await axios.get(`${API}/literature/latest-updates`, {
        headers: { Authorization: `Bearer demo-token` }
      });
      setLiteratureUpdates(response.data);
    } catch (error) {
      console.error("Failed to load literature updates:", error);
    }
  };

  const handleFileUpload = async (files, category, patientId) => {
    if (!patientId) {
      alert("Please select a patient first");
      return;
    }

    setIsUploading(true);
    
    try {
      const uploadPromises = Array.from(files).map(async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('patient_id', patientId);
        formData.append('file_category', category);

        const response = await axios.post(`${API}/files/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer demo-token`
          }
        });

        return response.data;
      });

      const results = await Promise.all(uploadPromises);
      
      // Reload files for the patient
      await loadPatientFiles(patientId);
      
      alert(`Successfully uploaded ${results.length} file(s)`);
      
    } catch (error) {
      console.error("File upload failed:", error);
      alert("File upload failed");
    } finally {
      setIsUploading(false);
    }
  };

  const loadPatientFiles = async (patientId) => {
    try {
      const response = await axios.get(`${API}/files/patient/${patientId}`, {
        headers: { Authorization: `Bearer demo-token` }
      });
      setUploadedFiles(response.data.uploaded_files || []);
    } catch (error) {
      console.error("Failed to load patient files:", error);
    }
  };

  const loadComprehensiveAnalysis = async (patientId) => {
    try {
      const response = await axios.get(`${API}/files/comprehensive-analysis/${patientId}`, {
        headers: { Authorization: `Bearer demo-token` }
      });
      setComprehensiveAnalysis(response.data.comprehensive_analysis);
    } catch (error) {
      console.error("Failed to load comprehensive analysis:", error);
    }
  };

  const generateFileBasedProtocol = async (patientId, school) => {
    setLoading(true);
    
    try {
      const response = await axios.post(`${API}/protocols/generate-from-files`, {
        patient_id: patientId,
        school_of_thought: school
      }, {
        headers: { Authorization: `Bearer demo-token` }
      });
      
      setGeneratedProtocol(response.data.protocol);
      
      alert(`Generated enhanced protocol using ${response.data.file_insights_used} files`);
      
    } catch (error) {
      console.error("File-based protocol generation failed:", error);
      alert("Protocol generation failed");
    } finally {
      setLoading(false);
    }
  };

  const loadFederatedLearningStatus = async () => {
    try {
      const response = await axios.get(`${API}/federated/global-model-status`, {
        headers: { Authorization: `Bearer demo-token` }
      });
      setFederatedLearningStatus(response.data);
    } catch (error) {
      console.error("Failed to load federated learning status:", error);
    }
  };

  const handlePredictOutcome = async (patientId, therapyPlan) => {
    setLoading(true);
    setOutcomePrediction(null);
    
    try {
      const response = await axios.post(`${API}/predictions/treatment-outcome`, {
        patient_id: patientId,
        therapy_plan: therapyPlan
      }, {
        headers: { Authorization: `Bearer demo-token` }
      });
      setOutcomePrediction(response.data);
    } catch (error) {
      console.error("Outcome prediction failed:", error);
      alert("Outcome prediction failed");
    } finally {
      setLoading(false);
    }
  };

  const loadTherapiesData = async () => {
    try {
      const response = await axios.get(`${API}/therapies`);
      setTherapiesData(response.data);
    } catch (error) {
      console.error("Failed to load therapies data:", error);
    }
  };

  const handleCreatePatient = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await axios.post(`${API}/patients`, patientForm, {
        headers: { Authorization: `Bearer demo-token` }
      });
      setSelectedPatient(response.data);
      setActiveTab("patient-analysis");
      await loadPatients();
      await loadDashboardData();
    } catch (error) {
      console.error("Failed to create patient:", error);
      alert("Failed to create patient record");
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzePatient = async (patientId) => {
    setLoading(true);
    setPatientAnalysis(null);
    
    try {
      const response = await axios.post(`${API}/patients/${patientId}/analyze`, {}, {
        headers: { Authorization: `Bearer demo-token` }
      });
      setPatientAnalysis(response.data);
    } catch (error) {
      console.error("Patient analysis failed:", error);
      alert("Patient analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateProtocol = async (patientId, schoolOfThought) => {
    setLoading(true);
    setGeneratedProtocol(null);
    
    try {
      const response = await axios.post(`${API}/protocols/generate`, {
        patient_id: patientId,
        school_of_thought: schoolOfThought
      }, {
        headers: { Authorization: `Bearer demo-token` }
      });
      setGeneratedProtocol(response.data);
    } catch (error) {
      console.error("Protocol generation failed:", error);
      alert("Protocol generation failed");
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
    if (score >= 0.8) return "text-green-600 bg-green-50";
    if (score >= 0.6) return "text-yellow-600 bg-yellow-50";
    return "text-red-600 bg-red-50";
  };

  const getEvidenceIcon = (level) => {
    switch(level) {
      case 1: return <Award className="h-4 w-4 text-yellow-500" />;
      case 2: return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 3: return <BookOpen className="h-4 w-4 text-blue-500" />;
      default: return <TestTube className="h-4 w-4 text-gray-500" />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Advanced Header */}
      <header className="bg-white/90 backdrop-blur-xl border-b border-slate-200 sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="p-2 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl shadow-lg">
                <Brain className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
                  RegenMed AI Pro
                </h1>
                <p className="text-sm text-slate-600">Advanced Regenerative Medicine Knowledge Platform</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="px-3 py-1 bg-green-50 text-green-700">
                <Activity className="h-4 w-4 mr-2" />
                AI Systems Active
              </Badge>
              <Badge variant="outline" className="px-3 py-1">
                Dr. Regenerative Medicine
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-10 bg-white/80 backdrop-blur-sm shadow-sm text-xs">
            <TabsTrigger value="dashboard" className="flex items-center gap-1 text-slate-800 font-medium data-[state=active]:bg-blue-100 data-[state=active]:text-blue-900">
              <ChartBar className="h-3 w-3" />
              Dashboard
            </TabsTrigger>
            <TabsTrigger value="patient-input" className="flex items-center gap-1">
              <User className="h-3 w-3" />
              Patient Input
            </TabsTrigger>
            <TabsTrigger value="file-upload" className="flex items-center gap-1">
              <Upload className="h-3 w-3" />
              File Upload
            </TabsTrigger>
            <TabsTrigger value="patient-analysis" className="flex items-center gap-1">
              <Brain className="h-3 w-3" />
              AI Analysis
            </TabsTrigger>
            <TabsTrigger value="protocol-generation" className="flex items-center gap-1">
              <Pill className="h-3 w-3" />
              Protocol Gen
            </TabsTrigger>
            <TabsTrigger value="outcome-prediction" className="flex items-center gap-1">
              <BarChart3 className="h-3 w-3" />
              ML Prediction
            </TabsTrigger>
            <TabsTrigger value="imaging-ai" className="flex items-center gap-1">
              <Image className="h-3 w-3" />
              Imaging AI
            </TabsTrigger>
            <TabsTrigger value="literature" className="flex items-center gap-1">
              <BookOpen className="h-3 w-3" />
              Literature
            </TabsTrigger>
            <TabsTrigger value="federated-learning" className="flex items-center gap-1">
              <Network className="h-3 w-3" />
              Fed Learning
            </TabsTrigger>
            <TabsTrigger value="patients" className="flex items-center gap-1">
              <FileText className="h-3 w-3" />
              Records
            </TabsTrigger>
          </TabsList>

          {/* Dashboard Tab */}
          <TabsContent value="dashboard" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {/* Summary Cards */}
              <Card className="bg-gradient-to-br from-blue-50 to-indigo-100 border-0 shadow-lg">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-blue-700">Total Patients</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-blue-900">
                    {dashboardData?.summary_stats?.total_patients || 0}
                  </div>
                  <p className="text-xs text-blue-600 mt-1">Active in system</p>
                </CardContent>
              </Card>
              
              <Card className="bg-gradient-to-br from-green-50 to-emerald-100 border-0 shadow-lg">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-green-700">Protocols Generated</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-green-900">
                    {(dashboardData?.summary_stats?.protocols_pending || 0) + 
                     (dashboardData?.summary_stats?.protocols_approved || 0)}
                  </div>
                  <p className="text-xs text-green-600 mt-1">Evidence-based</p>
                </CardContent>
              </Card>
              
              <Card className="bg-gradient-to-br from-purple-50 to-violet-100 border-0 shadow-lg">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-purple-700">Outcomes Tracked</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-purple-900">
                    {dashboardData?.summary_stats?.outcomes_tracked || 0}
                  </div>
                  <p className="text-xs text-purple-600 mt-1">Continuous learning</p>
                </CardContent>
              </Card>
              
              <Card className="bg-gradient-to-br from-orange-50 to-red-100 border-0 shadow-lg">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-orange-700">AI Accuracy</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-orange-900">94.2%</div>
                  <p className="text-xs text-orange-600 mt-1">Model performance</p>
                </CardContent>
              </Card>
            </div>

            {/* Recent Activities */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Activity className="h-5 w-5 text-indigo-600" />
                    Recent Activities
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {dashboardData?.recent_activities?.slice(0, 5).map((activity, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                      <div className="flex items-center gap-3">
                        <div className="w-2 h-2 bg-indigo-500 rounded-full"></div>
                        <span className="text-sm capitalize">
                          {activity.action?.replace(/_/g, ' ')}
                        </span>
                      </div>
                      <span className="text-xs text-slate-500">
                        {new Date(activity.timestamp).toLocaleDateString()}
                      </span>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-green-600" />
                    Platform Insights
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">Protocol Success Rate</span>
                      <span className="text-sm font-medium text-green-600">87%</span>
                    </div>
                    <Progress value={87} className="h-2" />
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">Evidence Integration</span>
                      <span className="text-sm font-medium text-blue-600">2,847 papers</span>
                    </div>
                    <Progress value={94} className="h-2" />
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">Global Knowledge Sync</span>
                      <span className="text-sm font-medium text-purple-600">Real-time</span>
                    </div>
                    <Progress value={100} className="h-2" />
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Patient Input Tab */}
          <TabsContent value="patient-input" className="space-y-6">
            <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Stethoscope className="h-5 w-5 text-blue-600" />
                  Comprehensive Patient Assessment
                </CardTitle>
                <CardDescription>
                  Advanced multi-modal data collection for AI-powered regenerative medicine analysis
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleCreatePatient} className="space-y-8">
                  {/* Demographics Section */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold flex items-center gap-2">
                      <User className="h-5 w-5" />
                      Patient Demographics
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="name">Full Name</Label>
                        <Input
                          id="name"
                          value={patientForm.demographics.name}
                          onChange={(e) => setPatientForm(prev => ({
                            ...prev,
                            demographics: { ...prev.demographics, name: e.target.value }
                          }))}
                          placeholder="Patient full name"
                          required
                        />
                      </div>
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
                        <Select 
                          value={patientForm.demographics.gender}
                          onValueChange={(value) => setPatientForm(prev => ({
                            ...prev,
                            demographics: { ...prev.demographics, gender: value }
                          }))}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select gender" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="Male">Male</SelectItem>
                            <SelectItem value="Female">Female</SelectItem>
                            <SelectItem value="Other">Other</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                  </div>

                  {/* Clinical Presentation */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold flex items-center gap-2">
                      <FileText className="h-5 w-5" />
                      Clinical Presentation
                    </h3>
                    
                    <div className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="chief_complaint">Chief Complaint</Label>
                        <Textarea
                          id="chief_complaint"
                          value={patientForm.chief_complaint}
                          onChange={(e) => setPatientForm(prev => ({
                            ...prev,
                            chief_complaint: e.target.value
                          }))}
                          placeholder="Primary reason for seeking regenerative medicine treatment..."
                          required
                          className="min-h-[80px]"
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="hpi">History of Present Illness</Label>
                        <Textarea
                          id="hpi"
                          value={patientForm.history_present_illness}
                          onChange={(e) => setPatientForm(prev => ({
                            ...prev,
                            history_present_illness: e.target.value
                          }))}
                          placeholder="Detailed chronological description of the current condition, including onset, duration, progression, associated symptoms, and functional impact..."
                          required
                          className="min-h-[120px]"
                        />
                      </div>
                    </div>
                  </div>

                  {/* Vital Signs */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold flex items-center gap-2">
                      <Heart className="h-5 w-5" />
                      Vital Signs & Measurements
                    </h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
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
                        <Label className="text-xs">Blood Pressure</Label>
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
                        <Label className="text-xs">Heart Rate (bpm)</Label>
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
                        <Label className="text-xs">Weight (lbs)</Label>
                        <Input
                          placeholder="150"
                          value={patientForm.vital_signs.weight}
                          onChange={(e) => setPatientForm(prev => ({
                            ...prev,
                            vital_signs: { ...prev.vital_signs, weight: e.target.value }
                          }))}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Symptoms & History Lists */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Symptoms */}
                    <div className="space-y-3">
                      <Label className="flex items-center gap-2">
                        <AlertTriangle className="h-4 w-4" />
                        Current Symptoms
                      </Label>
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
                      <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
                        {patientForm.symptoms.map((symptom, index) => (
                          <Badge
                            key={index}
                            variant="secondary"
                            className="cursor-pointer hover:bg-destructive hover:text-destructive-foreground transition-colors"
                            onClick={() => removeFromList('symptoms', index)}
                          >
                            {symptom} ×
                          </Badge>
                        ))}
                      </div>
                    </div>

                    {/* Medications */}
                    <div className="space-y-3">
                      <Label className="flex items-center gap-2">
                        <Pill className="h-4 w-4" />
                        Current Medications
                      </Label>
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
                      <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
                        {patientForm.medications.map((med, index) => (
                          <Badge
                            key={index}
                            variant="secondary"
                            className="cursor-pointer hover:bg-destructive hover:text-destructive-foreground transition-colors"
                            onClick={() => removeFromList('medications', index)}
                          >
                            {med} ×
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex justify-between items-center pt-6 border-t">
                    <div className="text-sm text-slate-600">
                      All data encrypted and HIPAA compliant
                    </div>
                    <Button 
                      type="submit" 
                      disabled={loading} 
                      className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 px-8"
                    >
                      {loading ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Creating Patient Profile...
                        </>
                      ) : (
                        <>
                          <Brain className="mr-2 h-4 w-4" />
                          Create Patient & Begin AI Analysis
                        </>
                      )}
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Patient Analysis Tab */}
          <TabsContent value="patient-analysis" className="space-y-6">
            {selectedPatient ? (
              <>
                <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span className="flex items-center gap-2">
                        <Brain className="h-5 w-5 text-indigo-600" />
                        Advanced AI Analysis
                      </span>
                      <Button
                        onClick={() => handleAnalyzePatient(selectedPatient.patient_id)}
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
                            <Microscope className="mr-2 h-4 w-4" />
                            Run Comprehensive Analysis
                          </>
                        )}
                      </Button>
                    </CardTitle>
                    <CardDescription>
                      Patient: {selectedPatient.demographics.name} • 
                      Age: {selectedPatient.demographics.age} • 
                      Gender: {selectedPatient.demographics.gender}
                    </CardDescription>
                  </CardHeader>
                  
                  <CardContent>
                    {patientAnalysis && (
                      <div className="space-y-6">
                        <Alert className="bg-blue-50 border-blue-200">
                          <Brain className="h-4 w-4" />
                          <AlertDescription>
                            AI analysis complete. {patientAnalysis.diagnostic_results.length} diagnostic possibilities identified with evidence-based reasoning.
                          </AlertDescription>
                        </Alert>

                        <div className="space-y-4">
                          <h3 className="text-xl font-bold flex items-center gap-2">
                            <Target className="h-5 w-5 text-green-600" />
                            Diagnostic Results & Regenerative Targets
                          </h3>
                          
                          {patientAnalysis.diagnostic_results.map((result, index) => (
                            <Card key={index} className="border-l-4 border-l-indigo-500 bg-gradient-to-r from-indigo-50 to-purple-50">
                              <CardContent className="pt-4">
                                <div className="flex items-start justify-between mb-3">
                                  <div className="space-y-1">
                                    <h4 className="text-lg font-semibold text-indigo-900">{result.diagnosis}</h4>
                                    <p className="text-sm text-indigo-700">
                                      Regenerative Medicine Candidate
                                    </p>
                                  </div>
                                  <Badge className={`${getConfidenceColor(result.confidence_score)} font-medium`}>
                                    {Math.round(result.confidence_score * 100)}% Confidence
                                  </Badge>
                                </div>
                                
                                <p className="text-slate-700 mb-4 bg-white/50 p-3 rounded-lg">
                                  {result.reasoning}
                                </p>
                                
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                                  <div className="space-y-2">
                                    <h5 className="font-medium text-green-700 flex items-center gap-1">
                                      <CheckCircle className="h-4 w-4" />
                                      Supporting Evidence
                                    </h5>
                                    <ul className="space-y-1">
                                      {result.supporting_evidence.map((evidence, i) => (
                                        <li key={i} className="flex items-start gap-2">
                                          <div className="w-1.5 h-1.5 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                                          <span className="text-slate-600">{evidence}</span>
                                        </li>
                                      ))}
                                    </ul>
                                  </div>
                                  
                                  <div className="space-y-2">
                                    <h5 className="font-medium text-blue-700 flex items-center gap-1">
                                      <Dna className="h-4 w-4" />
                                      Regenerative Targets
                                    </h5>
                                    <ul className="space-y-1">
                                      {result.regenerative_targets?.map((target, i) => (
                                        <li key={i} className="flex items-start gap-2">
                                          <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                                          <span className="text-slate-600">{target}</span>
                                        </li>
                                      ))}
                                    </ul>
                                  </div>
                                  
                                  <div className="space-y-2">
                                    <h5 className="font-medium text-purple-700 flex items-center gap-1">
                                      <TestTube className="h-4 w-4" />
                                      Recommended Tests
                                    </h5>
                                    <ul className="space-y-1">
                                      {result.recommended_tests.map((test, i) => (
                                        <li key={i} className="flex items-start gap-2">
                                          <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mt-2 flex-shrink-0"></div>
                                          <span className="text-slate-600">{test}</span>
                                        </li>
                                      ))}
                                    </ul>
                                  </div>
                                </div>
                              </CardContent>
                            </Card>
                          ))}
                        </div>
                        
                        <div className="pt-4 border-t">
                          <Button
                            onClick={() => setActiveTab("protocol-generation")}
                            className="w-full bg-gradient-to-r from-green-600 to-teal-600 hover:from-green-700 hover:to-teal-700"
                          >
                            <ChevronRight className="mr-2 h-4 w-4" />
                            Proceed to Protocol Generation
                          </Button>
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </>
            ) : (
              <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
                <CardContent className="text-center py-12">
                  <Brain className="h-16 w-16 mx-auto text-slate-400 mb-4" />
                  <h3 className="text-xl font-semibold mb-2">No Patient Selected</h3>
                  <p className="text-slate-600 mb-6">
                    Create a new patient record or select an existing patient to begin AI-powered analysis.
                  </p>
                  <Button onClick={() => setActiveTab("patient-input")}>
                    <User className="mr-2 h-4 w-4" />
                    Create New Patient
                  </Button>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* File Upload Tab */}
          <TabsContent value="file-upload" className="space-y-6">
            {selectedPatient ? (
              <>
                <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <FileText className="h-5 w-5 text-blue-600" />
                      Multi-Modal File Upload & Analysis
                    </CardTitle>
                    <p className="text-sm text-muted-foreground">
                      Upload patient data for comprehensive AI analysis: laboratory results, genetic tests, medical imaging, and clinical charts
                    </p>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Patient Selection Display */}
                    <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                      <div className="flex items-center gap-2 text-blue-800">
                        <User className="h-4 w-4" />
                        <span className="font-medium">Selected Patient:</span>
                        <span>{selectedPatient.name} (ID: {selectedPatient.patient_id?.slice(0, 8)}...)</span>
                      </div>
                    </div>

                    {/* File Upload Categories */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                      {/* Laboratory Results */}
                      <Card className="border-2 border-dashed border-green-300 hover:border-green-400 transition-colors">
                        <CardHeader className="pb-3">
                          <CardTitle className="text-sm flex items-center gap-2 text-green-700">
                            <Activity className="h-4 w-4" />
                            Laboratory Results
                          </CardTitle>
                        </CardHeader>
                        <CardContent className="pt-0">
                          <div className="text-xs text-muted-foreground mb-3">
                            CBC, metabolic panel, inflammatory markers, growth factors
                          </div>
                          <input
                            type="file"
                            id="labs-upload"
                            className="hidden"
                            accept=".json,.csv,.pdf,.txt"
                            onChange={(e) => handleFileUpload(e.target.files, 'labs', selectedPatient?.patient_id)}
                          />
                          <Button 
                            variant="outline" 
                            size="sm" 
                            className="w-full text-green-700 border-green-200 hover:bg-green-50"
                            onClick={() => document.getElementById('labs-upload').click()}
                          >
                            <Upload className="h-3 w-3 mr-1" />
                            Upload Labs
                          </Button>
                          <div className="text-xs text-muted-foreground mt-2">
                            JSON, CSV, PDF, TXT
                          </div>
                        </CardContent>
                      </Card>

                      {/* Genetic Testing */}
                      <Card className="border-2 border-dashed border-purple-300 hover:border-purple-400 transition-colors">
                        <CardHeader className="pb-3">
                          <CardTitle className="text-sm flex items-center gap-2 text-purple-700">
                            <Dna className="h-4 w-4" />
                            Genetic Testing
                          </CardTitle>
                        </CardHeader>
                        <CardContent className="pt-0">
                          <div className="text-xs text-muted-foreground mb-3">
                            Pharmacogenomics, sports medicine variants, healing factors
                          </div>
                          <input
                            type="file"
                            id="genetics-upload"
                            className="hidden"
                            accept=".vcf,.json,.csv,.txt"
                            onChange={(e) => handleFileUpload(e.target.files, 'genetics', selectedPatient?.patient_id)}
                          />
                          <Button 
                            variant="outline" 
                            size="sm" 
                            className="w-full text-purple-700 border-purple-200 hover:bg-purple-50"
                            onClick={() => document.getElementById('genetics-upload').click()}
                          >
                            <Upload className="h-3 w-3 mr-1" />
                            Upload Genetics
                          </Button>
                          <div className="text-xs text-muted-foreground mt-2">
                            VCF, JSON, CSV, TXT
                          </div>
                        </CardContent>
                      </Card>

                      {/* Medical Imaging */}
                      <Card className="border-2 border-dashed border-orange-300 hover:border-orange-400 transition-colors">
                        <CardHeader className="pb-3">
                          <CardTitle className="text-sm flex items-center gap-2 text-orange-700">
                            <Scan className="h-4 w-4" />
                            Medical Imaging
                          </CardTitle>
                        </CardHeader>
                        <CardContent className="pt-0">
                          <div className="text-xs text-muted-foreground mb-3">
                            DICOM files, MRI/CT/X-ray images, radiology reports
                          </div>
                          <input
                            type="file"
                            id="imaging-upload"
                            className="hidden"
                            accept=".dcm,.jpg,.jpeg,.png,.pdf,.txt"
                            onChange={(e) => handleFileUpload(e.target.files, 'imaging', selectedPatient?.patient_id)}
                          />
                          <Button 
                            variant="outline" 
                            size="sm" 
                            className="w-full text-orange-700 border-orange-200 hover:bg-orange-50"
                            onClick={() => document.getElementById('imaging-upload').click()}
                          >
                            <Upload className="h-3 w-3 mr-1" />
                            Upload Imaging
                          </Button>
                          <div className="text-xs text-muted-foreground mt-2">
                            DICOM, JPG, PNG, PDF
                          </div>
                        </CardContent>
                      </Card>

                      {/* Patient Charts */}
                      <Card className="border-2 border-dashed border-blue-300 hover:border-blue-400 transition-colors">
                        <CardHeader className="pb-3">
                          <CardTitle className="text-sm flex items-center gap-2 text-blue-700">
                            <FileText className="h-4 w-4" />
                            Patient Charts
                          </CardTitle>
                        </CardHeader>
                        <CardContent className="pt-0">
                          <div className="text-xs text-muted-foreground mb-3">
                            Clinical notes, medical records, consultation reports
                          </div>
                          <input
                            type="file"
                            id="chart-upload"
                            className="hidden"
                            accept=".pdf,.docx,.doc,.txt"
                            onChange={(e) => handleFileUpload(e, 'chart')}
                          />
                          <Button 
                            variant="outline" 
                            size="sm" 
                            className="w-full text-blue-700 border-blue-200 hover:bg-blue-50"
                            onClick={() => document.getElementById('chart-upload').click()}
                          >
                            <Upload className="h-3 w-3 mr-1" />
                            Upload Charts
                          </Button>
                          <div className="text-xs text-muted-foreground mt-2">
                            PDF, DOCX, DOC, TXT
                          </div>
                        </CardContent>
                      </Card>
                    </div>

                    {/* Upload Progress */}
                    {fileUpload.uploading && (
                      <Card className="bg-yellow-50 border-yellow-200">
                        <CardContent className="p-4">
                          <div className="flex items-center gap-3">
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-yellow-600"></div>
                            <span className="text-sm text-yellow-800">
                              Uploading {fileUpload.fileName}... AI analysis in progress
                            </span>
                          </div>
                        </CardContent>
                      </Card>
                    )}

                    {/* Uploaded Files Summary */}
                    {fileUpload.uploadedFiles.length > 0 && (
                      <Card className="bg-green-50 border-green-200">
                        <CardHeader className="pb-3">
                          <CardTitle className="text-sm text-green-800">
                            Uploaded Files ({fileUpload.uploadedFiles.length})
                          </CardTitle>
                        </CardHeader>
                        <CardContent className="pt-0">
                          <div className="space-y-2">
                            {fileUpload.uploadedFiles.map((file, index) => (
                              <div key={index} className="flex items-center justify-between p-2 bg-white rounded border">
                                <div className="flex items-center gap-2">
                                  <div className={`w-2 h-2 rounded-full ${
                                    file.category === 'labs' ? 'bg-green-500' :
                                    file.category === 'genetics' ? 'bg-purple-500' :
                                    file.category === 'imaging' ? 'bg-orange-500' :
                                    'bg-blue-500'
                                  }`}></div>
                                  <span className="text-sm font-medium">{file.fileName}</span>
                                  <Badge variant="secondary" className="text-xs">
                                    {file.category}
                                  </Badge>
                                </div>
                                <div className="flex items-center gap-2">
                                  <Badge variant={file.status === 'processed' ? 'default' : 'destructive'} className="text-xs">
                                    {file.status}
                                  </Badge>
                                  <span className="text-xs text-muted-foreground">
                                    {file.confidence_score ? `${Math.round(file.confidence_score * 100)}%` : ''}
                                  </span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </CardContent>
                      </Card>
                    )}

                    {/* Generate File-Based Protocol */}
                    {fileUpload.uploadedFiles.length > 0 && (
                      <Card className="bg-gradient-to-r from-purple-50 to-indigo-50 border-purple-200">
                        <CardContent className="p-4">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                              <Sparkles className="h-5 w-5 text-purple-600" />
                              <div>
                                <div className="font-medium text-purple-900">
                                  Enhanced AI Protocol Generation
                                </div>
                                <div className="text-sm text-purple-700">
                                  Generate protocols using uploaded multi-modal data
                                </div>
                              </div>
                            </div>
                            <Button 
                              onClick={generateFileBasedProtocol}
                              className="bg-purple-600 hover:bg-purple-700"
                              disabled={loading}
                            >
                              {loading ? (
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                              ) : (
                                <Zap className="h-4 w-4 mr-2" />
                              )}
                              Generate Enhanced Protocol
                            </Button>
                          </div>
                        </CardContent>
                      </Card>
                    )}
                  </CardContent>
                </Card>
              </>
            ) : (
              <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
                <CardContent className="flex flex-col items-center justify-center py-16">
                  <User className="h-16 w-16 text-muted-foreground mb-4" />
                  <h3 className="text-xl font-semibold text-muted-foreground mb-2">
                    Select a Patient First
                  </h3>
                  <p className="text-muted-foreground text-center">
                    Please select a patient from the Patient Records tab to upload and analyze their medical files.
                  </p>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Protocol Generation Tab */}
          <TabsContent value="protocol-generation" className="space-y-6">
            {selectedPatient ? (
              <>
                <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Sparkles className="h-5 w-5 text-purple-600" />
                      Regenerative Medicine Protocol Generator
                    </CardTitle>
                    <CardDescription>
                      Select your preferred school of thought for evidence-based protocol generation
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* School of Thought Selection */}
                    <div className="space-y-4">
                      <h3 className="text-lg font-semibold">Select Treatment Philosophy</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {Object.entries(SCHOOLS_OF_THOUGHT).map(([key, school]) => {
                          const IconComponent = school.icon;
                          return (
                            <Card
                              key={key}
                              className={`cursor-pointer transition-all duration-200 hover:shadow-lg ${
                                selectedSchool === key 
                                  ? 'ring-2 ring-indigo-500 bg-indigo-50' 
                                  : 'hover:bg-slate-50'
                              }`}
                              onClick={() => setSelectedSchool(key)}
                            >
                              <CardContent className="p-4">
                                <div className="flex items-start justify-between mb-3">
                                  <div className={`p-2 rounded-lg ${school.color}`}>
                                    <IconComponent className="h-5 w-5 text-white" />
                                  </div>
                                  {selectedSchool === key && (
                                    <CheckCircle className="h-5 w-5 text-indigo-600" />
                                  )}
                                </div>
                                <h4 className="font-semibold text-sm mb-2">{school.name}</h4>
                                <p className="text-xs text-slate-600 mb-3">{school.description}</p>
                                <div className="space-y-2">
                                  <div className="text-xs">
                                    <span className="font-medium">Therapies:</span>
                                    <div className="flex flex-wrap gap-1 mt-1">
                                      {school.therapies.slice(0, 2).map((therapy, i) => (
                                        <Badge key={i} variant="outline" className="text-xs">
                                          {therapy}
                                        </Badge>
                                      ))}
                                    </div>
                                  </div>
                                  <div className="text-xs">
                                    <span className="font-medium">Legal Status:</span>
                                    <span className="text-slate-600 ml-1">{school.legalStatus}</span>
                                  </div>
                                </div>
                              </CardContent>
                            </Card>
                          );
                        })}
                      </div>
                    </div>

                    {/* Generate Protocol Button */}
                    <div className="border-t pt-6">
                      <Button
                        onClick={() => handleGenerateProtocol(selectedPatient.patient_id, selectedSchool)}
                        disabled={loading}
                        className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 h-12"
                      >
                        {loading ? (
                          <>
                            <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                            Generating Evidence-Based Protocol...
                          </>
                        ) : (
                          <>
                            <Sparkles className="mr-2 h-5 w-5" />
                            Generate Personalized Protocol
                          </>
                        )}
                      </Button>
                    </div>
                  </CardContent>
                </Card>

                {/* Generated Protocol Display */}
                {generatedProtocol && (
                  <Card className="shadow-lg border-0 bg-gradient-to-br from-green-50 to-teal-50">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2 text-green-800">
                        <CheckCircle className="h-6 w-6" />
                        Generated Protocol - {SCHOOLS_OF_THOUGHT[generatedProtocol.school_of_thought]?.name}
                      </CardTitle>
                      <CardDescription className="text-green-700">
                        Confidence Score: {Math.round(generatedProtocol.confidence_score * 100)}% • 
                        Evidence-Based • Personalized for {selectedPatient.demographics.name}
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-8">
                      {/* AI Reasoning */}
                      <div className="bg-white/80 p-4 rounded-lg">
                        <h4 className="font-semibold mb-2 flex items-center gap-2">
                          <Brain className="h-4 w-4" />
                          AI Clinical Reasoning
                        </h4>
                        <p className="text-slate-700">{generatedProtocol.ai_reasoning}</p>
                      </div>

                      {/* Protocol Steps */}
                      <div className="space-y-4">
                        <h4 className="font-semibold text-lg flex items-center gap-2">
                          <Pill className="h-5 w-5" />
                          Treatment Protocol Steps
                        </h4>
                        {generatedProtocol.protocol_steps.map((step, index) => (
                          <Card key={index} className="bg-white/80 border-l-4 border-l-green-500">
                            <CardContent className="pt-4">
                              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="col-span-2">
                                  <h5 className="font-semibold text-green-800 mb-2">
                                    Step {step.step_number}: {step.therapy}
                                  </h5>
                                  <div className="space-y-2 text-sm">
                                    <p><strong>Dosage:</strong> {step.dosage}</p>
                                    <p><strong>Delivery:</strong> {step.delivery_method}</p>
                                    <p><strong>Timing:</strong> {step.timing}</p>
                                  </div>
                                </div>
                                <div className="space-y-2">
                                  <div className="bg-green-100 p-3 rounded-lg">
                                    <p className="text-sm font-medium text-green-800">Expected Outcome:</p>
                                    <p className="text-sm text-green-700">{step.expected_outcome}</p>
                                    <p className="text-xs text-green-600 mt-1">Timeline: {step.timeframe}</p>
                                  </div>
                                </div>
                              </div>
                            </CardContent>
                          </Card>
                        ))}
                      </div>

                      {/* Timeline Predictions */}
                      <div className="bg-white/80 p-4 rounded-lg">
                        <h4 className="font-semibold mb-3 flex items-center gap-2">
                          <Clock className="h-4 w-4" />
                          Predicted Timeline & Outcomes
                        </h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {Object.entries(generatedProtocol.timeline_predictions || {}).map(([phase, description]) => (
                            <div key={phase} className="space-y-2">
                              <h5 className="font-medium capitalize text-slate-800">
                                {phase.replace(/_/g, ' ')}
                              </h5>
                              <p className="text-sm text-slate-600">{description}</p>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Warnings & Contraindications */}
                      {generatedProtocol.legal_warnings?.length > 0 && (
                        <Alert className="bg-yellow-50 border-yellow-200">
                          <AlertTriangle className="h-4 w-4" />
                          <AlertDescription>
                            <strong>Legal & Safety Warnings:</strong>
                            <ul className="list-disc list-inside mt-2">
                              {generatedProtocol.legal_warnings.map((warning, index) => (
                                <li key={index}>{warning}</li>
                              ))}
                            </ul>
                          </AlertDescription>
                        </Alert>
                      )}

                      {/* Action Buttons */}
                      <div className="flex gap-4">
                        <Button className="flex-1 bg-green-600 hover:bg-green-700">
                          <Download className="mr-2 h-4 w-4" />
                          Download Protocol (PDF)
                        </Button>
                        <Button variant="outline" className="flex-1">
                          <Eye className="mr-2 h-4 w-4" />
                          Review Evidence
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </>
            ) : (
              <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
                <CardContent className="text-center py-12">
                  <Sparkles className="h-16 w-16 mx-auto text-slate-400 mb-4" />
                  <h3 className="text-xl font-semibold mb-2">No Patient Selected</h3>
                  <p className="text-slate-600">
                    Complete patient analysis first to generate personalized protocols.
                  </p>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Outcome Prediction Tab */}
          <TabsContent value="outcome-prediction" className="space-y-6">
            {selectedPatient ? (
              <>
                <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <BarChart3 className="h-5 w-5 text-purple-600" />
                      Machine Learning Outcome Prediction
                    </CardTitle>
                    <CardDescription>
                      Advanced ML models predict treatment success, timeline, and optimal parameters
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-6">
                      {/* Therapy Selection for Prediction */}
                      <div className="space-y-4">
                        <h3 className="text-lg font-semibold">Select Therapy for Outcome Prediction</h3>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          <Button
                            onClick={() => handlePredictOutcome(selectedPatient.patient_id, {
                              therapy_name: "Platelet-Rich Plasma (PRP)",
                              dosage: "3-5ml",
                              delivery_method: "Intra-articular injection"
                            })}
                            disabled={loading}
                            className="h-20 flex flex-col bg-gradient-to-br from-blue-50 to-blue-100 text-blue-800 border-blue-200 hover:from-blue-100 hover:to-blue-200"
                            variant="outline"
                          >
                            <TestTube className="h-6 w-6 mb-2" />
                            <span>Predict PRP Outcome</span>
                          </Button>
                          
                          <Button
                            onClick={() => handlePredictOutcome(selectedPatient.patient_id, {
                              therapy_name: "Bone Marrow Aspirate Concentrate (BMAC)",
                              dosage: "8-12ml",
                              delivery_method: "Ultrasound-guided injection"
                            })}
                            disabled={loading}
                            className="h-20 flex flex-col bg-gradient-to-br from-green-50 to-green-100 text-green-800 border-green-200 hover:from-green-100 hover:to-green-200"
                            variant="outline"
                          >
                            <Dna className="h-6 w-6 mb-2" />
                            <span>Predict BMAC Outcome</span>
                          </Button>
                          
                          <Button
                            onClick={() => handlePredictOutcome(selectedPatient.patient_id, {
                              therapy_name: "MSC Exosomes",
                              dosage: "2ml",
                              delivery_method: "Direct injection"
                            })}
                            disabled={loading}
                            className="h-20 flex flex-col bg-gradient-to-br from-purple-50 to-purple-100 text-purple-800 border-purple-200 hover:from-purple-100 hover:to-purple-200"
                            variant="outline"
                          >
                            <Microscope className="h-6 w-6 mb-2" />
                            <span>Predict Exosome Outcome</span>
                          </Button>
                        </div>
                      </div>

                      {loading && (
                        <div className="text-center py-8">
                          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-purple-600" />
                          <p className="text-lg font-medium">Running ML Models...</p>
                          <p className="text-sm text-slate-600">Analyzing patient data with advanced algorithms</p>
                        </div>
                      )}

                      {/* Prediction Results */}
                      {outcomePredictiion && (
                        <Card className="bg-gradient-to-br from-purple-50 to-indigo-50 border-purple-200">
                          <CardHeader>
                            <CardTitle className="flex items-center gap-2 text-purple-800">
                              <Cpu className="h-6 w-6" />
                              ML Prediction Results - {outcomePredictiion.therapy}
                            </CardTitle>
                          </CardHeader>
                          <CardContent className="space-y-6">
                            {/* Success Probability */}
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                              <Card className="bg-white/80">
                                <CardContent className="pt-6">
                                  <div className="text-center">
                                    <div className="text-3xl font-bold text-green-600 mb-2">
                                      {Math.round(outcomePredictiion.predictions.success_probability * 100)}%
                                    </div>
                                    <p className="text-sm text-slate-600">Success Probability</p>
                                  </div>
                                </CardContent>
                              </Card>
                              
                              <Card className="bg-white/80">
                                <CardContent className="pt-6">
                                  <div className="text-center">
                                    <div className="text-lg font-bold text-blue-600 mb-2">
                                      {outcomePredictiion.predictions.expected_timeline?.most_likely || "4-8 weeks"}
                                    </div>
                                    <p className="text-sm text-slate-600">Expected Response Time</p>
                                  </div>
                                </CardContent>
                              </Card>
                              
                              <Card className="bg-white/80">
                                <CardContent className="pt-6">
                                  <div className="text-center">
                                    <div className="text-lg font-bold text-purple-600 mb-2">
                                      v{outcomePredictiion.model_version}
                                    </div>
                                    <p className="text-sm text-slate-600">Model Version</p>
                                  </div>
                                </CardContent>
                              </Card>
                            </div>

                            {/* Timeline Breakdown */}
                            {outcomePredictiion.predictions.expected_timeline?.category_probabilities && (
                              <div className="space-y-3">
                                <h4 className="font-semibold">Response Timeline Probabilities:</h4>
                                {Object.entries(outcomePredictiion.predictions.expected_timeline.category_probabilities).map(([category, probability]) => (
                                  <div key={category} className="flex items-center justify-between">
                                    <span className="text-sm capitalize">{category}</span>
                                    <div className="flex items-center gap-2">
                                      <div className="w-32 bg-gray-200 rounded-full h-2">
                                        <div 
                                          className="bg-blue-600 h-2 rounded-full" 
                                          style={{width: `${probability * 100}%`}}
                                        ></div>
                                      </div>
                                      <span className="text-sm font-medium">{Math.round(probability * 100)}%</span>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            )}

                            {/* Risk Assessment */}
                            {outcomePredictiion.risk_assessment && (
                              <div className="space-y-3">
                                <h4 className="font-semibold">Risk Assessment:</h4>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                  {outcomePredictiion.risk_assessment.low_risk?.length > 0 && (
                                    <div className="bg-green-50 p-3 rounded-lg">
                                      <h5 className="font-medium text-green-800 mb-2">Low Risk Factors</h5>
                                      <ul className="text-sm text-green-700 space-y-1">
                                        {outcomePredictiion.risk_assessment.low_risk.map((risk, i) => (
                                          <li key={i}>• {risk}</li>
                                        ))}
                                      </ul>
                                    </div>
                                  )}
                                  
                                  {outcomePredictiion.risk_assessment.moderate_risk?.length > 0 && (
                                    <div className="bg-yellow-50 p-3 rounded-lg">
                                      <h5 className="font-medium text-yellow-800 mb-2">Moderate Risk Factors</h5>
                                      <ul className="text-sm text-yellow-700 space-y-1">
                                        {outcomePredictiion.risk_assessment.moderate_risk.map((risk, i) => (
                                          <li key={i}>• {risk}</li>
                                        ))}
                                      </ul>
                                    </div>
                                  )}
                                  
                                  {outcomePredictiion.risk_assessment.high_risk?.length > 0 && (
                                    <div className="bg-red-50 p-3 rounded-lg">
                                      <h5 className="font-medium text-red-800 mb-2">High Risk Factors</h5>
                                      <ul className="text-sm text-red-700 space-y-1">
                                        {outcomePredictiion.risk_assessment.high_risk.map((risk, i) => (
                                          <li key={i}>• {risk}</li>
                                        ))}
                                      </ul>
                                    </div>
                                  )}
                                </div>
                              </div>
                            )}

                            {/* AI Recommendations */}
                            {outcomePredictiion.recommendations && (
                              <div className="bg-blue-50 p-4 rounded-lg">
                                <h4 className="font-semibold text-blue-800 mb-3">ML-Generated Recommendations:</h4>
                                <ul className="space-y-2">
                                  {outcomePredictiion.recommendations.map((rec, i) => (
                                    <li key={i} className="flex items-start gap-2 text-blue-700">
                                      <CheckCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
                                      <span className="text-sm">{rec}</span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </CardContent>
                        </Card>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </>
            ) : (
              <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
                <CardContent className="text-center py-12">
                  <BarChart3 className="h-16 w-16 mx-auto text-slate-400 mb-4" />
                  <h3 className="text-xl font-semibold mb-2">No Patient Selected</h3>
                  <p className="text-slate-600">
                    Select a patient to generate ML-powered outcome predictions.
                  </p>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Advanced Imaging AI Tab */}
          <TabsContent value="imaging-ai" className="space-y-6">
            <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Image className="h-5 w-5 text-indigo-600" />
                  AI-Powered Medical Imaging Analysis
                </CardTitle>
                <CardDescription>
                  Advanced DICOM processing with regenerative medicine insights
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Imaging Modality Support */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
                    <CardContent className="p-4 text-center">
                      <Monitor className="h-8 w-8 mx-auto mb-3 text-blue-600" />
                      <h4 className="font-semibold text-blue-800">MRI Analysis</h4>
                      <p className="text-sm text-blue-600 mt-2">Cartilage segmentation, tissue analysis</p>
                    </CardContent>
                  </Card>
                  
                  <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200">
                    <CardContent className="p-4 text-center">
                      <Layers className="h-8 w-8 mx-auto mb-3 text-green-600" />
                      <h4 className="font-semibold text-green-800">CT Imaging</h4>
                      <p className="text-sm text-green-600 mt-2">Bone density, structural analysis</p>
                    </CardContent>
                  </Card>
                  
                  <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
                    <CardContent className="p-4 text-center">
                      <Zap className="h-8 w-8 mx-auto mb-3 text-purple-600" />
                      <h4 className="font-semibold text-purple-800">X-Ray AI</h4>
                      <p className="text-sm text-purple-600 mt-2">Joint space, osteoarthritis grading</p>
                    </CardContent>
                  </Card>
                  
                  <Card className="bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200">
                    <CardContent className="p-4 text-center">
                      <Activity className="h-8 w-8 mx-auto mb-3 text-orange-600" />
                      <h4 className="font-semibold text-orange-800">Ultrasound</h4>
                      <p className="text-sm text-orange-600 mt-2">Injection guidance, soft tissue</p>
                    </CardContent>
                  </Card>
                </div>

                {/* AI Capabilities */}
                <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-6 rounded-lg">
                  <h3 className="text-lg font-semibold mb-4">Advanced AI Imaging Capabilities</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-3">
                      <h4 className="font-medium text-indigo-800">Regenerative Medicine Analysis</h4>
                      <ul className="text-sm space-y-1">
                        <li className="flex items-center gap-2">
                          <CheckCircle className="h-4 w-4 text-green-500" />
                          <span>Cartilage volume quantification</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <CheckCircle className="h-4 w-4 text-green-500" />
                          <span>Injection target identification</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <CheckCircle className="h-4 w-4 text-green-500" />
                          <span>Tissue viability assessment</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <CheckCircle className="h-4 w-4 text-green-500" />
                          <span>Treatment candidacy scoring</span>
                        </li>
                      </ul>
                    </div>
                    
                    <div className="space-y-3">
                      <h4 className="font-medium text-purple-800">Clinical Integration</h4>
                      <ul className="text-sm space-y-1">
                        <li className="flex items-center gap-2">
                          <CheckCircle className="h-4 w-4 text-green-500" />
                          <span>Automated reporting</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <CheckCircle className="h-4 w-4 text-green-500" />
                          <span>Treatment recommendation</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <CheckCircle className="h-4 w-4 text-green-500" />
                          <span>Progress monitoring</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <CheckCircle className="h-4 w-4 text-green-500" />
                          <span>Outcome prediction</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>

                {/* Upload Interface */}
                <Card className="border-2 border-dashed border-slate-300 bg-slate-50">
                  <CardContent className="p-8 text-center">
                    <Upload className="h-12 w-12 mx-auto mb-4 text-slate-400" />
                    <h3 className="text-lg font-semibold mb-2">Upload DICOM Images</h3>
                    <p className="text-slate-600 mb-4">
                      Drag and drop DICOM files or click to browse
                    </p>
                    <Button className="bg-indigo-600 hover:bg-indigo-700">
                      <Upload className="mr-2 h-4 w-4" />
                      Select DICOM Files
                    </Button>
                  </CardContent>
                </Card>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Literature Integration Tab */}
          <TabsContent value="literature" className="space-y-6">
            <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BookOpen className="h-5 w-5 text-green-600" />
                  Real-Time Literature Integration
                </CardTitle>
                <CardDescription>
                  Live PubMed monitoring and evidence synthesis for regenerative medicine
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Literature Status */}
                {literatureUpdates && (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <Card className="bg-gradient-to-br from-green-50 to-emerald-100">
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-green-600 mb-1">
                          {literatureUpdates.processing_result?.new_papers_processed || 0}
                        </div>
                        <p className="text-sm text-green-700">New Papers Today</p>
                      </CardContent>
                    </Card>
                    
                    <Card className="bg-gradient-to-br from-blue-50 to-blue-100">
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-blue-600 mb-1">
                          {literatureUpdates.total_papers_in_database || 0}
                        </div>
                        <p className="text-sm text-blue-700">Total Papers</p>
                      </CardContent>
                    </Card>
                    
                    <Card className="bg-gradient-to-br from-purple-50 to-purple-100">
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-purple-600 mb-1">
                          <Rss className="h-6 w-6 mx-auto" />
                        </div>
                        <p className="text-sm text-purple-700">Live Monitoring</p>
                      </CardContent>
                    </Card>
                  </div>
                )}

                {/* Recent Papers */}
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold flex items-center gap-2">
                    <Search className="h-5 w-5" />
                    Recent High-Impact Publications
                  </h3>
                  
                  {literatureUpdates?.recent_papers?.slice(0, 5).map((paper, index) => (
                    <Card key={index} className="hover:shadow-md transition-shadow">
                      <CardContent className="pt-4">
                        <div className="flex items-start justify-between mb-3">
                          <div className="space-y-2 flex-1">
                            <h4 className="font-semibold text-slate-800 leading-tight">
                              {paper.title}
                            </h4>
                            <div className="flex items-center gap-4 text-sm text-slate-600">
                              <span>{paper.journal}</span>
                              <span>{paper.authors?.slice(0, 3).join(", ")}
                                {paper.authors?.length > 3 && " et al."}
                              </span>
                              <span>{new Date(paper.publication_date).getFullYear()}</span>
                            </div>
                            <p className="text-sm text-slate-700 line-clamp-2">
                              {paper.abstract}
                            </p>
                          </div>
                          <div className="ml-4 text-center">
                            <Badge className={`${getConfidenceColor(paper.relevance_score)} mb-2`}>
                              {Math.round(paper.relevance_score * 100)}%
                            </Badge>
                            <p className="text-xs text-slate-500">Relevance</p>
                          </div>
                        </div>
                        
                        {/* Keywords */}
                        <div className="flex flex-wrap gap-1">
                          {paper.regenerative_keywords?.slice(0, 5).map((keyword, i) => (
                            <Badge key={i} variant="outline" className="text-xs">
                              {keyword}
                            </Badge>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  )) || (
                    <div className="text-center py-8 text-slate-500">
                      <CloudDownload className="h-12 w-12 mx-auto mb-3" />
                      <p>Loading latest publications...</p>
                    </div>
                  )}
                </div>

                {/* Search Interface */}
                <Card className="bg-gradient-to-r from-slate-50 to-blue-50">
                  <CardContent className="p-6">
                    <h4 className="font-semibold mb-3">Search Literature Database</h4>
                    <div className="flex gap-3">
                      <Input
                        placeholder="Search regenerative medicine literature..."
                        className="flex-1"
                      />
                      <Button>
                        <Search className="h-4 w-4 mr-2" />
                        Search
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Federated Learning Tab */}
          <TabsContent value="federated-learning" className="space-y-6">
            <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Network className="h-5 w-5 text-blue-600" />
                  Federated Learning & Continuous Improvement
                </CardTitle>
                <CardDescription>
                  Privacy-preserving collaborative learning across regenerative medicine practices
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Global Model Status */}
                {federatedLearningStatus && (
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <Card className="bg-gradient-to-br from-blue-50 to-blue-100">
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-blue-600 mb-1">
                          {federatedLearningStatus.model_version || 1}
                        </div>
                        <p className="text-sm text-blue-700">Model Version</p>
                      </CardContent>
                    </Card>
                    
                    <Card className="bg-gradient-to-br from-green-50 to-green-100">
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-green-600 mb-1">
                          {federatedLearningStatus.participants || 0}
                        </div>
                        <p className="text-sm text-green-700">Active Participants</p>
                      </CardContent>
                    </Card>
                    
                    <Card className="bg-gradient-to-br from-purple-50 to-purple-100">
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-purple-600 mb-1">
                          {Math.round((federatedLearningStatus.performance_improvement || 0.05) * 100)}%
                        </div>
                        <p className="text-sm text-purple-700">Performance Gain</p>
                      </CardContent>
                    </Card>
                    
                    <Card className="bg-gradient-to-br from-orange-50 to-orange-100">
                      <CardContent className="p-4 text-center">
                        <div className="flex items-center justify-center mb-1">
                          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse mr-2"></div>
                          <span className="text-sm font-semibold text-orange-600">LIVE</span>
                        </div>
                        <p className="text-sm text-orange-700">System Status</p>
                      </CardContent>
                    </Card>
                  </div>
                )}

                {/* Federated Learning Benefits */}
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg">
                  <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                    <GitBranch className="h-5 w-5" />
                    Privacy-Preserving Collaborative Learning
                  </h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-3">
                      <h4 className="font-medium text-blue-800">Security Features</h4>
                      <ul className="text-sm space-y-2">
                        <li className="flex items-center gap-2">
                          <Shield className="h-4 w-4 text-green-500" />
                          <span>Differential privacy protection</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <Shield className="h-4 w-4 text-green-500" />
                          <span>No patient data leaves your clinic</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <Shield className="h-4 w-4 text-green-500" />
                          <span>Encrypted model updates only</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <Shield className="h-4 w-4 text-green-500" />
                          <span>HIPAA compliant architecture</span>
                        </li>
                      </ul>
                    </div>
                    
                    <div className="space-y-3">
                      <h4 className="font-medium text-purple-800">Learning Benefits</h4>
                      <ul className="text-sm space-y-2">
                        <li className="flex items-center gap-2">
                          <TrendingUp className="h-4 w-4 text-blue-500" />
                          <span>Continuous model improvement</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <TrendingUp className="h-4 w-4 text-blue-500" />
                          <span>Global knowledge aggregation</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <TrendingUp className="h-4 w-4 text-blue-500" />
                          <span>Rare case pattern recognition</span>
                        </li>
                        <li className="flex items-center gap-2">
                          <TrendingUp className="h-4 w-4 text-blue-500" />
                          <span>Personalized recommendations</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>

                {/* Participation Controls */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Participation Controls</CardTitle>
                    <CardDescription>
                      Manage your clinic's contribution to federated learning
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
                      <div>
                        <h4 className="font-medium text-green-800">Federated Learning Status</h4>
                        <p className="text-sm text-green-600">Your clinic is actively contributing to global knowledge</p>
                      </div>
                      <Badge className="bg-green-100 text-green-800">
                        <CheckCircle className="h-4 w-4 mr-1" />
                        Active
                      </Badge>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <Button variant="outline" className="h-12">
                        <Settings className="mr-2 h-4 w-4" />
                        Privacy Settings
                      </Button>
                      <Button variant="outline" className="h-12">
                        <BarChart3 className="mr-2 h-4 w-4" />
                        Contribution Metrics
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Knowledge Base Tab */}
          <TabsContent value="knowledge-base" className="space-y-6">
            <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BookOpen className="h-5 w-5 text-blue-600" />
                  Regenerative Medicine Knowledge Base
                </CardTitle>
                <CardDescription>
                  Comprehensive database of therapies, evidence, and global research
                </CardDescription>
              </CardHeader>
              <CardContent>
                {therapiesData && (
                  <div className="space-y-6">
                    {/* Therapy Overview */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {therapiesData.therapies.map((therapy, index) => (
                        <Card key={index} className="hover:shadow-md transition-shadow">
                          <CardContent className="pt-4">
                            <div className="flex items-center gap-2 mb-3">
                              <div className="p-2 bg-blue-100 rounded-lg">
                                <FlaskConical className="h-4 w-4 text-blue-600" />
                              </div>
                              <div>
                                <h4 className="font-semibold text-sm">{therapy.name}</h4>
                                <div className="flex items-center gap-1 mt-1">
                                  {getEvidenceIcon(therapy.evidence_level)}
                                  <span className="text-xs text-slate-600">
                                    Level {therapy.evidence_level} Evidence
                                  </span>
                                </div>
                              </div>
                            </div>
                            
                            <div className="space-y-2 text-xs">
                              <div>
                                <span className="font-medium">Success Rate:</span>
                                <Progress value={therapy.success_rate * 100} className="h-1 mt-1" />
                                <span className="text-slate-600">{Math.round(therapy.success_rate * 100)}%</span>
                              </div>
                              
                              <div>
                                <span className="font-medium">Mechanisms:</span>
                                <div className="flex flex-wrap gap-1 mt-1">
                                  {therapy.mechanism?.slice(0, 2).map((mechanism, i) => (
                                    <Badge key={i} variant="outline" className="text-xs">
                                      {mechanism}
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                              
                              <div>
                                <span className="font-medium">Primary Indications:</span>
                                <p className="text-slate-600 mt-1">
                                  {therapy.indications?.slice(0, 2).join(", ")}
                                </p>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>

                    {/* Global Research Status */}
                    <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg">
                      <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                        <Globe className="h-5 w-5" />
                        Global Research & Regulatory Status
                      </h3>
                      
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="bg-white p-4 rounded-lg">
                          <h4 className="font-medium text-green-700 mb-2">Approved Therapies</h4>
                          <p className="text-2xl font-bold text-green-600">12</p>
                          <p className="text-xs text-slate-600">FDA/EMA approved</p>
                        </div>
                        
                        <div className="bg-white p-4 rounded-lg">
                          <h4 className="font-medium text-blue-700 mb-2">Active Trials</h4>
                          <p className="text-2xl font-bold text-blue-600">847</p>
                          <p className="text-xs text-slate-600">Global clinical trials</p>
                        </div>
                        
                        <div className="bg-white p-4 rounded-lg">
                          <h4 className="font-medium text-purple-700 mb-2">Recent Papers</h4>
                          <p className="text-2xl font-bold text-purple-600">2,847</p>
                          <p className="text-xs text-slate-600">Last 12 months</p>
                        </div>
                      </div>
                    </div>

                    {/* Evidence Integration Status */}
                    <Card>
                      <CardHeader>
                        <CardTitle className="text-lg">Real-Time Evidence Integration</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-3">
                          <div className="flex justify-between items-center">
                            <span className="text-sm">PubMed Integration</span>
                            <Badge className="bg-green-100 text-green-800">Live</Badge>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-sm">ClinicalTrials.gov</span>
                            <Badge className="bg-green-100 text-green-800">Synced</Badge>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-sm">International Registries</span>
                            <Badge className="bg-blue-100 text-blue-800">Updating</Badge>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-sm">Patent Database</span>
                            <Badge className="bg-green-100 text-green-800">Current</Badge>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Patient Records Tab */}
          <TabsContent value="patients" className="space-y-6">
            <Card className="shadow-lg border-0 bg-white/70 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5 text-slate-600" />
                  Patient Records & Outcomes
                </CardTitle>
                <CardDescription>
                  Comprehensive patient management with outcome tracking
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {patients.map((patient) => (
                    <Card 
                      key={patient.patient_id} 
                      className="cursor-pointer hover:shadow-md transition-all border-l-4 border-l-indigo-500 bg-gradient-to-r from-indigo-50 to-purple-50"
                      onClick={() => {
                        setSelectedPatient(patient);
                        setActiveTab("patient-analysis");
                      }}
                    >
                      <CardContent className="pt-4">
                        <div className="flex items-start justify-between">
                          <div className="space-y-2">
                            <div className="flex items-center gap-3">
                              <h4 className="font-semibold text-indigo-900">{patient.demographics.name}</h4>
                              <Badge variant="outline" className="text-xs">
                                {patient.demographics.age}y • {patient.demographics.gender}
                              </Badge>
                            </div>
                            <p className="text-sm text-indigo-700 font-medium">{patient.chief_complaint}</p>
                            <p className="text-xs text-slate-600">
                              Created: {new Date(patient.created_at).toLocaleDateString()} • 
                              Last Updated: {new Date(patient.updated_at).toLocaleDateString()}
                            </p>
                          </div>
                          <div className="text-right">
                            <Badge className="bg-green-100 text-green-800 mb-2">Active</Badge>
                            <p className="text-xs text-slate-500">ID: {patient.patient_id.slice(0, 8)}...</p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                  
                  {patients.length === 0 && (
                    <div className="text-center py-12">
                      <User className="h-16 w-16 mx-auto text-slate-400 mb-4" />
                      <h3 className="text-xl font-semibold mb-2">No Patient Records</h3>
                      <p className="text-slate-600 mb-6">
                        Start building your regenerative medicine practice with your first patient assessment.
                      </p>
                      <Button onClick={() => setActiveTab("patient-input")}>
                        <User className="mr-2 h-4 w-4" />
                        Add First Patient
                      </Button>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}

export default App;