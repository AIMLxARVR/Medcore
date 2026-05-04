import { C } from './colors';

export const DOCTORS=[
  {id:1,name:"Dr. Fatima Rahman",title:"MBBS, MD (Cardiology)",spec:"Cardiologist",dept:"Cardiology",rating:4.9,reviews:312,patients:"1,200+",fee:1500,init:"FR",color:"#0369A1",avail:"Today 3:00 PM",slots:["3:00 PM","3:30 PM","5:00 PM","5:30 PM"]},
  {id:2,name:"Dr. Ahmed Hossain",title:"MBBS, MD (Neurology)",spec:"Neurologist",dept:"Neurology",rating:4.8,reviews:198,patients:"980+",fee:2000,init:"AH",color:"#7C3AED",avail:"Tomorrow 10:00 AM",slots:["10:00 AM","10:30 AM","11:00 AM","2:00 PM"]},
  {id:3,name:"Dr. Nasrin Khatun",title:"MBBS, DCH (Pediatrics)",spec:"Pediatrician",dept:"Pediatrics",rating:4.9,reviews:445,patients:"1,500+",fee:1200,init:"NK",color:"#059669",avail:"Today 5:00 PM",slots:["5:00 PM","5:30 PM","6:00 PM"]},
  {id:4,name:"Dr. Karim Uddin",title:"MBBS, MS (Ortho)",spec:"Orthopedist",dept:"Orthopedics",rating:4.7,reviews:167,patients:"876+",fee:1800,init:"KU",color:"#B45309",avail:"Thu 11:00 AM",slots:["11:00 AM","11:30 AM","2:30 PM","3:00 PM"]},
  {id:5,name:"Dr. Sultana Begum",title:"MBBS, DDV (Dermatology)",spec:"Dermatologist",dept:"Dermatology",rating:4.8,reviews:289,patients:"1,100+",fee:1500,init:"SB",color:"#DB2777",avail:"Today 6:30 PM",slots:["6:00 PM","6:30 PM","7:00 PM"]},
];

export const DAYS=[{label:"Today",date:"4 May"},{label:"Tomorrow",date:"5 May"},{label:"Thu",date:"6 May"},{label:"Fri",date:"7 May"},{label:"Sat",date:"8 May"}];

export const CHART_DATA=[
  {day:"Mon",booked:24,completed:22},{day:"Tue",booked:31,completed:28},
  {day:"Wed",booked:28,completed:25},{day:"Thu",booked:35,completed:33},
  {day:"Fri",booked:42,completed:38},{day:"Sat",booked:56,completed:51},
  {day:"Sun",booked:18,completed:16},
];

export const AI_DIAGNOSES = {
  "chest pain shortness of breath": {conditions:[{name:"Angina Pectoris",conf:78,icd:"I20"},{name:"Acute MI (rule out)",conf:62,icd:"I21"},{name:"Costochondritis",conf:41,icd:"M94.0"}],tests:["ECG","Troponin I/T","Chest X-Ray","CBC"],urgency:"high",recommendation:"Refer to cardiology. ECG immediately."},
  "fever cough fatigue": {conditions:[{name:"Viral URI",conf:85,icd:"J06.9"},{name:"Influenza",conf:72,icd:"J11"},{name:"COVID-19",conf:55,icd:"U07.1"}],tests:["CBC","CRP","COVID Antigen","Chest X-Ray"],urgency:"medium",recommendation:"Symptomatic management. Isolate if COVID suspected."},
  "headache dizziness nausea": {conditions:[{name:"Migraine",conf:82,icd:"G43"},{name:"Tension Headache",conf:68,icd:"G44.2"},{name:"Hypertension",conf:45,icd:"I10"}],tests:["BP monitoring","CBC","Blood glucose"],urgency:"low",recommendation:"Analgesics PRN. Monitor BP. Neuro referral if recurrent."},
  "joint pain swelling stiffness": {conditions:[{name:"Rheumatoid Arthritis",conf:71,icd:"M06"},{name:"Osteoarthritis",conf:65,icd:"M19"},{name:"Gout",conf:48,icd:"M10"}],tests:["ESR","CRP","RF","Uric Acid","X-Ray joints"],urgency:"medium",recommendation:"NSAIDs. Rheumatology referral recommended."},
};

export const LAB_MOCK = {
  "CBC": [{param:"Hemoglobin",val:11.2,unit:"g/dL",ref:"13.5–17.5",status:"low"},{param:"WBC",val:11800,unit:"/cumm",ref:"4500–11000",status:"high"},{param:"Platelets",val:285000,unit:"/cumm",ref:"150000–400000",status:"normal"},{param:"Hematocrit",val:34,unit:"%",ref:"41–53",status:"low"}],
  "Lipid Panel": [{param:"Total Cholesterol",val:215,unit:"mg/dL",ref:"<200",status:"high"},{param:"LDL",val:142,unit:"mg/dL",ref:"<130",status:"high"},{param:"HDL",val:38,unit:"mg/dL",ref:">40",status:"low"},{param:"Triglycerides",val:178,unit:"mg/dL",ref:"<150",status:"high"}],
  "Blood Glucose": [{param:"Fasting Glucose",val:112,unit:"mg/dL",ref:"70–100",status:"high"},{param:"HbA1c",val:6.1,unit:"%",ref:"<5.7",status:"high"}],
};

export const ERP_SYSTEMS = [
  {name:"MySoft ERP",status:"connected",lastSync:"2 min ago",records:1247,icon:"🔗",color:C.green},
  {name:"Lab Information System",status:"connected",lastSync:"5 min ago",records:834,icon:"🧪",color:C.green},
  {name:"Pharmacy System",status:"syncing",lastSync:"Syncing...",records:0,icon:"💊",color:C.accent},
  {name:"Insurance TPA",status:"disconnected",lastSync:"Never",records:0,icon:"🏥",color:C.red},
];

export const ETL_LOGS = [
  {time:"10:42 AM",event:"MySoft patient import",status:"success",count:"+12 records"},
  {time:"10:38 AM",event:"Lab results sync (HL7)",status:"success",count:"+4 reports"},
  {time:"10:35 AM",event:"Appointment export to ERP",status:"success",count:"8 records"},
  {time:"10:20 AM",event:"Pharmacy order sync",status:"warning",count:"2 conflicts"},
  {time:"09:55 AM",event:"Insurance eligibility check",status:"error",count:"Connection failed"},
];