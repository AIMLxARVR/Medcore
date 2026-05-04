import { useState, useRef, useEffect } from "react";
import { Search, Calendar, Star, ChevronRight, Check, Users, FileText, Activity, Bell, LogOut, Stethoscope, Download, X, Shield, MessageCircle, CheckCircle, QrCode, ArrowRight, Plus, Clock, Brain, Upload, Database, Zap, AlertTriangle, TrendingUp, RefreshCw, Send, Bot, User, ChevronDown, Eye, Pill, FlaskConical, History, ArrowUpDown } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from "recharts";

const C = {
  primary:"#0C4A6E",primaryMid:"#0369A1",primaryLight:"#E0F2FE",
  accent:"#D97706",accentLight:"#FEF3C7",
  green:"#059669",greenLight:"#ECFDF5",
  red:"#DC2626",redLight:"#FEF2F2",
  amber:"#B45309",amberLight:"#FFFBEB",
  purple:"#7C3AED",purpleLight:"#EDE9FE",
  teal:"#0F766E",tealLight:"#F0FDFA",
  bg:"#F0F4F8",card:"#FFFFFF",border:"#E2E8F0",
  text:"#0F172A",muted:"#64748B",light:"#94A3B8",
};

const DOCTORS=[
  {id:1,name:"Dr. Fatima Rahman",title:"MBBS, MD (Cardiology)",spec:"Cardiologist",dept:"Cardiology",rating:4.9,reviews:312,patients:"1,200+",fee:1500,init:"FR",color:"#0369A1",avail:"Today 3:00 PM",slots:["3:00 PM","3:30 PM","5:00 PM","5:30 PM"]},
  {id:2,name:"Dr. Ahmed Hossain",title:"MBBS, MD (Neurology)",spec:"Neurologist",dept:"Neurology",rating:4.8,reviews:198,patients:"980+",fee:2000,init:"AH",color:"#7C3AED",avail:"Tomorrow 10:00 AM",slots:["10:00 AM","10:30 AM","11:00 AM","2:00 PM"]},
  {id:3,name:"Dr. Nasrin Khatun",title:"MBBS, DCH (Pediatrics)",spec:"Pediatrician",dept:"Pediatrics",rating:4.9,reviews:445,patients:"1,500+",fee:1200,init:"NK",color:"#059669",avail:"Today 5:00 PM",slots:["5:00 PM","5:30 PM","6:00 PM"]},
  {id:4,name:"Dr. Karim Uddin",title:"MBBS, MS (Ortho)",spec:"Orthopedist",dept:"Orthopedics",rating:4.7,reviews:167,patients:"876+",fee:1800,init:"KU",color:"#B45309",avail:"Thu 11:00 AM",slots:["11:00 AM","11:30 AM","2:30 PM","3:00 PM"]},
  {id:5,name:"Dr. Sultana Begum",title:"MBBS, DDV (Dermatology)",spec:"Dermatologist",dept:"Dermatology",rating:4.8,reviews:289,patients:"1,100+",fee:1500,init:"SB",color:"#DB2777",avail:"Today 6:30 PM",slots:["6:00 PM","6:30 PM","7:00 PM"]},
];

const DAYS=[{label:"Today",date:"4 May"},{label:"Tomorrow",date:"5 May"},{label:"Thu",date:"6 May"},{label:"Fri",date:"7 May"},{label:"Sat",date:"8 May"}];

const CHART_DATA=[
  {day:"Mon",booked:24,completed:22},{day:"Tue",booked:31,completed:28},
  {day:"Wed",booked:28,completed:25},{day:"Thu",booked:35,completed:33},
  {day:"Fri",booked:42,completed:38},{day:"Sat",booked:56,completed:51},
  {day:"Sun",booked:18,completed:16},
];

const AI_DIAGNOSES = {
  "chest pain shortness of breath": {conditions:[{name:"Angina Pectoris",conf:78,icd:"I20"},{name:"Acute MI (rule out)",conf:62,icd:"I21"},{name:"Costochondritis",conf:41,icd:"M94.0"}],tests:["ECG","Troponin I/T","Chest X-Ray","CBC"],urgency:"high",recommendation:"Refer to cardiology. ECG immediately."},
  "fever cough fatigue": {conditions:[{name:"Viral URI",conf:85,icd:"J06.9"},{name:"Influenza",conf:72,icd:"J11"},{name:"COVID-19",conf:55,icd:"U07.1"}],tests:["CBC","CRP","COVID Antigen","Chest X-Ray"],urgency:"medium",recommendation:"Symptomatic management. Isolate if COVID suspected."},
  "headache dizziness nausea": {conditions:[{name:"Migraine",conf:82,icd:"G43"},{name:"Tension Headache",conf:68,icd:"G44.2"},{name:"Hypertension",conf:45,icd:"I10"}],tests:["BP monitoring","CBC","Blood glucose"],urgency:"low",recommendation:"Analgesics PRN. Monitor BP. Neuro referral if recurrent."},
  "joint pain swelling stiffness": {conditions:[{name:"Rheumatoid Arthritis",conf:71,icd:"M06"},{name:"Osteoarthritis",conf:65,icd:"M19"},{name:"Gout",conf:48,icd:"M10"}],tests:["ESR","CRP","RF","Uric Acid","X-Ray joints"],urgency:"medium",recommendation:"NSAIDs. Rheumatology referral recommended."},
};

const LAB_MOCK = {
  "CBC": [{param:"Hemoglobin",val:11.2,unit:"g/dL",ref:"13.5–17.5",status:"low"},{param:"WBC",val:11800,unit:"/cumm",ref:"4500–11000",status:"high"},{param:"Platelets",val:285000,unit:"/cumm",ref:"150000–400000",status:"normal"},{param:"Hematocrit",val:34,unit:"%",ref:"41–53",status:"low"}],
  "Lipid Panel": [{param:"Total Cholesterol",val:215,unit:"mg/dL",ref:"<200",status:"high"},{param:"LDL",val:142,unit:"mg/dL",ref:"<130",status:"high"},{param:"HDL",val:38,unit:"mg/dL",ref:">40",status:"low"},{param:"Triglycerides",val:178,unit:"mg/dL",ref:"<150",status:"high"}],
  "Blood Glucose": [{param:"Fasting Glucose",val:112,unit:"mg/dL",ref:"70–100",status:"high"},{param:"HbA1c",val:6.1,unit:"%",ref:"<5.7",status:"high"}],
};

// ─── MedBot system prompt (compact, token-optimised) ──────────────
const MEDBOT_SYSTEM = `You are MedBot, the AI assistant for MedCore Diagnostic Centre in Dhaka, Bangladesh. Be concise, warm, and helpful. Use plain text only (no markdown, no asterisks, no headers) - format with line breaks, bullet points (•), and emojis only.

CLINIC DATA (answer questions using this):
Doctors: 1) Dr. Fatima Rahman – Cardiologist, MBBS MD, fee ৳1500, today 3:00PM/3:30PM/5:00PM/5:30PM | 2) Dr. Ahmed Hossain – Neurologist, MBBS MD, fee ৳2000, tomorrow 10:00AM/10:30AM/11:00AM/2:00PM | 3) Dr. Nasrin Khatun – Pediatrician, MBBS DCH, fee ৳1200, today 5:00PM/5:30PM/6:00PM | 4) Dr. Karim Uddin – Orthopedist, MBBS MS, fee ৳1800, Thu 11:00AM/11:30AM/2:30PM/3:00PM | 5) Dr. Sultana Begum – Dermatologist, MBBS DDV, fee ৳1500, today 6:00PM/6:30PM/7:00PM
Patient on record: Farhan Ahmed, PAT-00142, blood group B+
Appointment on record: APT-2847, Dr. Fatima Rahman, May 8 2026 3:00PM, Serial #7, Chamber 2B, Status: Confirmed
Recent reports: CBC (Apr 28, flagged: Low Hb 11.2 g/dL, High WBC 11800), ECG (Apr 15), Chest X-Ray (Mar 20)
Emergency: Call 999. Hotline: 01700-000000. Address: House 7, Road 12, Dhanmondi, Dhaka.

RULES:
• When user says yes/no or picks a number (1,2,3 etc), understand it in context of your last question
• For appointments: confirm doctor, date, time, then ask for name & phone to complete
• For symptoms: give brief guidance, suggest relevant doctor, ask if they want to book
• For cancellation: ask "yes" to confirm, warn about ৳500 fee if <24h
• Keep responses under 120 words
• Always end with a clear next action or question when the conversation is ongoing
• NEVER say you cannot help — always guide them to the right option`;

const ERP_SYSTEMS = [
  {name:"MySoft ERP",status:"connected",lastSync:"2 min ago",records:1247,icon:"🔗",color:C.green},
  {name:"Lab Information System",status:"connected",lastSync:"5 min ago",records:834,icon:"🧪",color:C.green},
  {name:"Pharmacy System",status:"syncing",lastSync:"Syncing...",records:0,icon:"💊",color:C.accent},
  {name:"Insurance TPA",status:"disconnected",lastSync:"Never",records:0,icon:"🏥",color:C.red},
];

const ETL_LOGS = [
  {time:"10:42 AM",event:"MySoft patient import",status:"success",count:"+12 records"},
  {time:"10:38 AM",event:"Lab results sync (HL7)",status:"success",count:"+4 reports"},
  {time:"10:35 AM",event:"Appointment export to ERP",status:"success",count:"8 records"},
  {time:"10:20 AM",event:"Pharmacy order sync",status:"warning",count:"2 conflicts"},
  {time:"09:55 AM",event:"Insurance eligibility check",status:"error",count:"Connection failed"},
];

// ─── Shared components ────────────────────────────────────────────
const Av=({init,color,size=40})=>(
  <div style={{width:size,height:size,borderRadius:"50%",background:color+"22",border:`2px solid ${color}44`,display:"flex",alignItems:"center",justifyContent:"center",fontSize:size*0.3,fontWeight:700,color,flexShrink:0}}>{init}</div>
);
const Badge=({text,color=C.primaryMid,bg=C.primaryLight})=>(
  <span style={{display:"inline-block",padding:"2px 8px",borderRadius:12,background:bg,color,fontSize:11,fontWeight:700,whiteSpace:"nowrap"}}>{text}</span>
);
const Btn=({children,onClick,variant="primary",size="md",full=false,style:sx={}})=>{
  const vs={primary:{background:C.primary,color:"#fff",border:`1px solid ${C.primary}`},outline:{background:"transparent",color:C.primary,border:`1px solid ${C.primary}`},ghost:{background:"transparent",color:C.muted,border:`1px solid ${C.border}`},success:{background:C.green,color:"#fff",border:`1px solid ${C.green}`},danger:{background:C.red,color:"#fff",border:`1px solid ${C.red}`},purple:{background:C.purple,color:"#fff",border:`1px solid ${C.purple}`}};
  const ss={sm:{padding:"5px 11px",fontSize:12},md:{padding:"8px 16px",fontSize:13},lg:{padding:"11px 22px",fontSize:14}};
  return <button onClick={onClick} style={{...vs[variant],...ss[size],borderRadius:8,fontWeight:700,cursor:"pointer",display:"inline-flex",alignItems:"center",gap:5,width:full?"100%":"auto",justifyContent:"center",fontFamily:"inherit",...sx}}>{children}</button>;
};
const Card=({children,style:sx={}})=>(
  <div style={{background:C.card,border:`1px solid ${C.border}`,borderRadius:12,padding:20,...sx}}>{children}</div>
);
const StatusBadge=({status})=>{
  const m={confirmed:{bg:C.greenLight,c:C.green,l:"Confirmed"},pending:{bg:C.amberLight,c:C.amber,l:"Pending"},completed:{bg:"#F1F5F9",c:C.muted,l:"Completed"},cancelled:{bg:C.redLight,c:C.red,l:"Cancelled"},success:{bg:C.greenLight,c:C.green,l:"Success"},warning:{bg:C.amberLight,c:C.amber,l:"Warning"},error:{bg:C.redLight,c:C.red,l:"Error"},syncing:{bg:C.primaryLight,c:C.primaryMid,l:"Syncing"},connected:{bg:C.greenLight,c:C.green,l:"Connected"},disconnected:{bg:C.redLight,c:C.red,l:"Disconnected"}};
  const s=m[status]||m.pending;
  return <Badge text={s.l} color={s.c} bg={s.bg}/>;
};

// ─── NavBar ───────────────────────────────────────────────────────
function NavBar({view,onNav}){
  const tabs=[{k:"home",l:"Home"},{k:"doctors",l:"Doctors"},{k:"chatbot",l:"AI Chatbot"},{k:"portal",l:"My Portal"},{k:"ai-clinical",l:"AI Clinical"},{k:"etl",l:"ETL Hub"},{k:"admin",l:"Admin"}];
  return(
    <nav style={{background:C.card,borderBottom:`1px solid ${C.border}`,position:"sticky",top:0,zIndex:100}}>
      <div style={{maxWidth:960,margin:"0 auto",padding:"0 12px",display:"flex",alignItems:"center",height:48,gap:2}}>
        <div onClick={()=>onNav("home")} style={{display:"flex",alignItems:"center",gap:6,cursor:"pointer",marginRight:"auto",flexShrink:0}}>
          <div style={{width:28,height:28,borderRadius:8,background:C.primary,display:"flex",alignItems:"center",justifyContent:"center"}}><Stethoscope size={14} color="#fff"/></div>
          <div>
            <div style={{fontSize:13,fontWeight:800,color:C.text,letterSpacing:"-0.02em"}}>MedCore</div>
            <div style={{fontSize:8,color:C.muted,letterSpacing:"0.08em"}}>AI-ENHANCED MVP</div>
          </div>
        </div>
        {tabs.map(({k,l})=>(
          <button key={k} onClick={()=>onNav(k)} style={{padding:"4px 8px",border:"none",background:"none",cursor:"pointer",fontSize:11,fontWeight:view===k?800:400,color:view===k?C.primary:C.muted,borderBottom:`2px solid ${view===k?C.primary:"transparent"}`,height:48,fontFamily:"inherit",whiteSpace:"nowrap"}}>
            {l}
          </button>
        ))}
        <div style={{marginLeft:4,display:"flex",alignItems:"center",gap:4,flexShrink:0}}>
          <div style={{width:6,height:6,borderRadius:"50%",background:C.green}}/>
          <span style={{fontSize:8,color:C.green,fontWeight:800,letterSpacing:"0.08em"}}>LIVE</span>
        </div>
      </div>
    </nav>
  );
}

// ─── Home ─────────────────────────────────────────────────────────
function HomeView({onNav,onPick}){
  return(
    <div style={{maxWidth:960,margin:"0 auto",padding:"0 12px 40px"}}>
      <div style={{background:C.primary,borderRadius:16,padding:"28px 28px",color:"#fff",margin:"16px 0 16px"}}>
        <div style={{fontSize:9,fontWeight:800,letterSpacing:"0.12em",opacity:0.65,marginBottom:6}}>DHAKA MEDICARE — AI-ENHANCED MVP</div>
        <h1 style={{fontSize:22,fontWeight:800,lineHeight:1.2,margin:"0 0 8px"}}>Intelligent Healthcare Management</h1>
        <p style={{opacity:0.8,marginBottom:18,fontSize:12,lineHeight:1.6}}>AI diagnosis assistance · Public chatbot · ETL pipeline · Report analysis · Full EMR</p>
        <div style={{display:"flex",gap:8,flexWrap:"wrap"}}>
          <Btn onClick={()=>onNav("chatbot")} size="sm" sx={{background:"#fff",color:C.primary,border:"none"}}><Bot size={12}/> AI Chatbot</Btn>
          <Btn onClick={()=>onNav("ai-clinical")} size="sm" sx={{background:"rgba(255,255,255,0.15)",color:"#fff",borderColor:"rgba(255,255,255,0.3)"}}><Brain size={12}/> AI Clinical Panel</Btn>
          <Btn onClick={()=>onNav("etl")} size="sm" sx={{background:"rgba(255,255,255,0.15)",color:"#fff",borderColor:"rgba(255,255,255,0.3)"}}><Database size={12}/> ETL Hub</Btn>
        </div>
      </div>
      <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:10,marginBottom:16}}>
        {[{l:"AI Diagnoses Today",v:"47",icon:Brain,c:C.purple},{l:"ETL Records Synced",v:"1,081",icon:Database,c:C.teal},{l:"Lab Reports Analyzed",v:"23",icon:FlaskConical,c:C.green},{l:"Chatbot Sessions",v:"142",icon:Bot,c:C.accent}].map(({l,v,icon:I,c})=>(
          <Card key={l} style={{textAlign:"center",padding:"14px 8px"}}>
            <div style={{width:32,height:32,borderRadius:8,background:c+"18",display:"flex",alignItems:"center",justifyContent:"center",margin:"0 auto 6px"}}><I size={15} color={c}/></div>
            <div style={{fontSize:18,fontWeight:800,color:C.text,lineHeight:1}}>{v}</div>
            <div style={{fontSize:10,color:C.muted,marginTop:3,lineHeight:1.3}}>{l}</div>
          </Card>
        ))}
      </div>
      <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:12,marginBottom:16}}>
        {[
          {title:"Public AI Chatbot",desc:"Symptom check, booking & appointment tracking for patients",icon:Bot,color:C.primaryMid,nav:"chatbot"},
          {title:"AI Clinical Analysis",desc:"Diagnosis assistance, lab report analysis & prescription review",icon:Brain,color:C.purple,nav:"ai-clinical"},
          {title:"ETL Integration Hub",desc:"Real-time sync with MySoft ERP, Lab systems & Insurance",icon:Database,color:C.teal,nav:"etl"},
        ].map(({title,desc,icon:I,color,nav})=>(
          <Card key={title} style={{cursor:"pointer",padding:16}} onClick={()=>onNav(nav)}>
            <div style={{width:38,height:38,borderRadius:10,background:color+"18",display:"flex",alignItems:"center",justifyContent:"center",marginBottom:10}}><I size={18} color={color}/></div>
            <div style={{fontSize:13,fontWeight:700,color:C.text,marginBottom:4}}>{title}</div>
            <div style={{fontSize:11,color:C.muted,lineHeight:1.5,marginBottom:10}}>{desc}</div>
            <div style={{fontSize:11,color:color,fontWeight:700,display:"flex",alignItems:"center",gap:4}}>Explore <ArrowRight size={11}/></div>
          </Card>
        ))}
      </div>
      <div style={{marginBottom:12,display:"flex",alignItems:"center",justifyContent:"space-between"}}>
        <h2 style={{fontSize:16,fontWeight:800,color:C.text,margin:0}}>Available Doctors</h2>
        <Btn onClick={()=>onNav("doctors")} variant="ghost" size="sm">View All <ChevronRight size={12}/></Btn>
      </div>
      <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:10}}>
        {DOCTORS.slice(0,3).map(doc=>(
          <Card key={doc.id} style={{padding:14}}>
            <div style={{display:"flex",alignItems:"center",gap:8,marginBottom:8}}>
              <Av init={doc.init} color={doc.color} size={38}/>
              <div><div style={{fontSize:12,fontWeight:700,color:C.text,lineHeight:1.2}}>{doc.name}</div><div style={{fontSize:10,color:C.muted,marginTop:2}}>{doc.spec}</div></div>
            </div>
            <div style={{fontSize:10,color:C.green,fontWeight:700,marginBottom:8}}><span style={{color:C.muted}}>Next: </span>{doc.avail}</div>
            <div style={{display:"flex",alignItems:"center",justifyContent:"space-between"}}>
              <span style={{fontSize:13,fontWeight:800,color:C.primary}}>৳{doc.fee.toLocaleString()}</span>
              <Btn onClick={()=>{onPick(doc);onNav("book");}} size="sm">Book</Btn>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

// ─── Typing dots animation ────────────────────────────────────────
const TypingDots=()=>{
  const [dot,setDot]=useState(0);
  useEffect(()=>{const t=setInterval(()=>setDot(d=>(d+1)%4),400);return()=>clearInterval(t);},[]);
  const labels=["Thinking","Thinking.","Thinking..","Thinking..."];
  return <span style={{color:C.muted,fontSize:12}}>{labels[dot]}</span>;
};

// ─── AI PUBLIC CHATBOT ────────────────────────────────────────────
function ChatbotView(){
  const INIT_MSG={from:"bot",text:"Hello! 👋 I'm MedBot, your MedCore AI assistant.\n\nI can help you:\n• 📅 Book or manage appointments\n• 🩺 Check doctor availability\n• 📊 View your reports & history\n• 💊 Symptom guidance\n• 🔔 Check appointment status\n\nWhat do you need today?"};
  const [msgs,setMsgs]=useState([INIT_MSG]);
  const [apiHistory,setApiHistory]=useState([]); // tracks {role,content} for Claude API
  const [input,setInput]=useState("");
  const [typing,setTyping]=useState(false);
  const [error,setError]=useState(null);
  const bottom=useRef(null);
  useEffect(()=>{bottom.current?.scrollIntoView({behavior:"smooth"});},[msgs,typing]);

  const callClaude=async(userText,history)=>{
    const newHistory=[...history,{role:"user",content:userText}];
    const res=await fetch("https://api.anthropic.com/v1/messages",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({
        model:"claude-sonnet-4-20250514",
        max_tokens:200,
        system:MEDBOT_SYSTEM,
        messages:newHistory,
      })
    });
    if(!res.ok) throw new Error("API error "+res.status);
    const data=await res.json();
    const replyText=data.content?.map(b=>b.type==="text"?b.text:"").join("")||"Sorry, I couldn't process that. Please try again.";
    const updatedHistory=[...newHistory,{role:"assistant",content:replyText}];
    return{replyText,updatedHistory};
  };

  const send=async(text)=>{
    const txt=(text||input).trim();
    if(!txt||typing) return;
    setInput("");
    setError(null);
    setMsgs(p=>[...p,{from:"user",text:txt}]);
    setTyping(true);
    try{
      const{replyText,updatedHistory}=await callClaude(txt,apiHistory);
      setApiHistory(updatedHistory);
      setMsgs(p=>[...p,{from:"bot",text:replyText}]);
    }catch(e){
      setError("MedBot is temporarily unavailable. Please try again.");
      setMsgs(p=>[...p,{from:"bot",text:"⚠️ I'm having a brief connectivity issue. Please try again in a moment.",isError:true}]);
    }finally{
      setTyping(false);
    }
  };

  // Quick replies auto-send (not just fill input)
  const quickReplies=[
    {label:"📅 Book appointment",msg:"I want to book an appointment"},
    {label:"🗓️ My appointment",msg:"Show my upcoming appointment"},
    {label:"👨‍⚕️ Available doctors",msg:"Which doctors are available today?"},
    {label:"📄 My reports",msg:"Show my recent reports"},
    {label:"🤒 I have fever",msg:"I have fever and cough"},
    {label:"💔 Chest pain",msg:"I'm having chest pain"},
  ];

  const reset=()=>{setMsgs([INIT_MSG]);setApiHistory([]);setInput("");setError(null);};

  return(
    <div style={{maxWidth:680,margin:"0 auto",padding:"16px 12px 40px"}}>
      <div style={{display:"flex",alignItems:"center",gap:10,marginBottom:14}}>
        <div style={{width:40,height:40,borderRadius:12,background:C.primaryLight,display:"flex",alignItems:"center",justifyContent:"center"}}><Bot size={20} color={C.primary}/></div>
        <div>
          <div style={{fontSize:15,fontWeight:800,color:C.text}}>MedBot — AI Assistant</div>
          <div style={{fontSize:11,color:C.green,display:"flex",alignItems:"center",gap:4}}>
            <span style={{width:6,height:6,borderRadius:"50%",background:C.green,display:"inline-block"}}/>
            Live AI · Understands Yes/No & numbered replies
          </div>
        </div>
        <div style={{marginLeft:"auto",display:"flex",gap:6,alignItems:"center"}}>
          <Badge text="Claude Powered" color={C.purple} bg={C.purpleLight}/>
          <button onClick={reset} title="New chat" style={{border:`1px solid ${C.border}`,background:"transparent",borderRadius:6,padding:"3px 7px",cursor:"pointer",fontSize:10,color:C.muted,fontFamily:"inherit"}}>↺ Reset</button>
        </div>
      </div>
      <div style={{background:C.primaryLight,border:`1px solid ${C.primaryMid}30`,borderRadius:10,padding:"8px 12px",marginBottom:12,fontSize:11,color:C.primaryMid}}>
        ⚠️ General guidance only. For medical emergencies, call 999. Not a substitute for professional diagnosis.
      </div>
      <Card style={{padding:0,overflow:"hidden"}}>
        {/* Chat messages */}
        <div style={{height:380,overflowY:"auto",padding:14,display:"flex",flexDirection:"column",gap:10}}>
          {msgs.map((m,i)=>(
            <div key={i} style={{display:"flex",justifyContent:m.from==="user"?"flex-end":"flex-start",gap:8,alignItems:"flex-end"}}>
              {m.from==="bot"&&<div style={{width:28,height:28,borderRadius:"50%",background:m.isError?C.redLight:C.primaryLight,display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}><Bot size={14} color={m.isError?C.red:C.primary}/></div>}
              <div style={{maxWidth:"78%",padding:"10px 13px",borderRadius:m.from==="user"?"12px 12px 2px 12px":"12px 12px 12px 2px",background:m.from==="user"?C.primary:m.isError?C.redLight:C.bg,color:m.from==="user"?"#fff":m.isError?C.red:C.text,fontSize:12,lineHeight:1.7,whiteSpace:"pre-line"}}>{m.text}</div>
              {m.from==="user"&&<div style={{width:28,height:28,borderRadius:"50%",background:C.accentLight,display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}><User size={14} color={C.accent}/></div>}
            </div>
          ))}
          {typing&&(
            <div style={{display:"flex",gap:8,alignItems:"flex-end"}}>
              <div style={{width:28,height:28,borderRadius:"50%",background:C.primaryLight,display:"flex",alignItems:"center",justifyContent:"center"}}><Bot size={14} color={C.primary}/></div>
              <div style={{padding:"10px 14px",borderRadius:"12px 12px 12px 2px",background:C.bg,minWidth:90}}><TypingDots/></div>
            </div>
          )}
          <div ref={bottom}/>
        </div>

        {/* Quick reply chips — auto-send on click */}
        <div style={{padding:"8px 10px",borderTop:`1px solid ${C.border}`,display:"flex",flexWrap:"wrap",gap:5}}>
          {quickReplies.map(q=>(
            <button key={q.label} onClick={()=>!typing&&send(q.msg)} disabled={typing} style={{padding:"4px 10px",borderRadius:16,border:`1px solid ${C.border}`,background:typing?C.bg:C.card,cursor:typing?"not-allowed":"pointer",fontSize:11,color:typing?C.light:C.primaryMid,fontFamily:"inherit",fontWeight:600,transition:"all 0.15s",opacity:typing?0.6:1}}>{q.label}</button>
          ))}
        </div>

        {/* Input row */}
        <div style={{padding:"8px 10px",borderTop:`1px solid ${C.border}`,display:"flex",gap:8}}>
          <input
            value={input}
            onChange={e=>setInput(e.target.value)}
            onKeyDown={e=>e.key==="Enter"&&!e.shiftKey&&send()}
            placeholder={typing?"MedBot is responding...":"Type 'yes', 'no', a number, or anything..."}
            disabled={typing}
            style={{flex:1,padding:"8px 12px",border:`1px solid ${typing?C.border:C.primaryMid}30`,borderRadius:8,fontSize:12,color:C.text,background:typing?"#FAFAFA":C.card,outline:"none",fontFamily:"inherit",transition:"border-color 0.2s"}}
          />
          <Btn onClick={()=>send()} size="sm" sx={{opacity:(!input.trim()||typing)?0.5:1}}><Send size={13}/></Btn>
        </div>
      </Card>
      <div style={{marginTop:8,fontSize:10,color:C.light,textAlign:"center"}}>
        Context-aware AI · Understands Yes/No, numbered choices, and free-text · Powered by Claude
      </div>
    </div>
  );
}

// ─── AI CLINICAL PANEL ────────────────────────────────────────────
function AIClinicalView(){
  const [aiTab,setAiTab]=useState("diagnosis");
  const [symptoms,setSymptoms]=useState("");
  const [aiResult,setAiResult]=useState(null);
  const [loading,setLoading]=useState(false);
  const [selectedReport,setSelectedReport]=useState(null);
  const [uploadedFile,setUploadedFile]=useState(null);
  const [prescInput,setPrescInput]=useState("");
  const [prescResult,setPrescResult]=useState(null);

  const runDiagnosis=()=>{
    if(!symptoms.trim()) return;
    setLoading(true);
    setTimeout(()=>{
      const key=Object.keys(AI_DIAGNOSES).find(k=>k.split(" ").some(w=>symptoms.toLowerCase().includes(w)));
      setAiResult(key?AI_DIAGNOSES[key]:{conditions:[{name:"Unspecified Condition",conf:35,icd:"R69"}],tests:["CBC","CMP","Urinalysis"],urgency:"low",recommendation:"Full clinical workup recommended."});
      setLoading(false);
    },1500);
  };

  const analyzeReport=(name)=>{
    setSelectedReport({name,data:LAB_MOCK[name]||LAB_MOCK["CBC"]});
  };

  const checkPrescription=()=>{
    if(!prescInput.trim()) return;
    setPrescResult({interactions:[{drugs:"Aspirin + Warfarin",severity:"high",note:"Increased bleeding risk — monitor INR closely"},{drugs:"Metformin + Contrast dye",severity:"medium",note:"Hold Metformin 48h before/after contrast procedures"}],allergies:[],dosageWarnings:["Metformin 1000mg twice daily — confirm eGFR >30"],recommendation:"Interaction alert found. Physician review required before dispensing."});
  };

  const historyData=[
    {date:"Apr 28",dx:"Viral URI",doctor:"Dr. Khatun",bp:"118/74",weight:72},
    {date:"Apr 15",dx:"Tension Headache",doctor:"Dr. Hossain",bp:"120/78",weight:71.5},
    {date:"Mar 20",dx:"Hypertension (monitoring)",doctor:"Dr. Rahman",bp:"138/88",weight:72},
    {date:"Feb 10",dx:"Lipid Profile Review",doctor:"Dr. Rahman",bp:"135/85",weight:73},
  ];

  const urgColor={high:C.red,medium:C.amber,low:C.green};

  return(
    <div style={{maxWidth:960,margin:"0 auto",padding:"16px 12px 40px"}}>
      <div style={{display:"flex",alignItems:"center",gap:10,marginBottom:14}}>
        <div style={{width:40,height:40,borderRadius:12,background:C.purpleLight,display:"flex",alignItems:"center",justifyContent:"center"}}><Brain size={20} color={C.purple}/></div>
        <div><div style={{fontSize:15,fontWeight:800,color:C.text}}>AI Clinical Panel</div><div style={{fontSize:11,color:C.muted}}>For doctors, admins & authorized practitioners</div></div>
        <div style={{marginLeft:"auto"}}><Badge text="Restricted Access" color={C.red} bg={C.redLight}/></div>
      </div>
      <div style={{background:C.redLight,border:`1px solid ${C.red}30`,borderRadius:8,padding:"8px 12px",marginBottom:14,fontSize:11,color:C.red,fontWeight:600}}>
        ⚕️ Clinical AI is a decision-support tool. All diagnoses must be confirmed by a licensed physician. AI suggestions do not replace clinical judgment.
      </div>

      <div style={{display:"flex",gap:2,borderBottom:`2px solid ${C.border}`,marginBottom:14}}>
        {[{k:"diagnosis",l:"Symptom Analysis",icon:Brain},{k:"labanalysis",l:"Lab Report Analysis",icon:FlaskConical},{k:"prescription",l:"Prescription Check",icon:Pill},{k:"history",l:"Patient History",icon:History}].map(({k,l,icon:I})=>(
          <button key={k} onClick={()=>setAiTab(k)} style={{padding:"6px 14px",border:"none",background:"none",cursor:"pointer",fontSize:12,fontWeight:aiTab===k?800:400,color:aiTab===k?C.primary:C.muted,borderBottom:`2px solid ${aiTab===k?C.primary:"transparent"}`,marginBottom:-2,fontFamily:"inherit",display:"flex",alignItems:"center",gap:5}}>
            <I size={12}/>{l}
          </button>
        ))}
      </div>

      {aiTab==="diagnosis"&&(
        <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:14}}>
          <div>
            <Card>
              <div style={{fontSize:13,fontWeight:800,color:C.text,marginBottom:10}}>Enter Patient Symptoms</div>
              <textarea value={symptoms} onChange={e=>setSymptoms(e.target.value)} placeholder="e.g. chest pain shortness of breath, fever cough fatigue, headache dizziness nausea..." style={{width:"100%",height:100,padding:"10px 12px",border:`1px solid ${C.border}`,borderRadius:8,fontSize:12,color:C.text,resize:"none",boxSizing:"border-box",fontFamily:"inherit",lineHeight:1.5,outline:"none"}}/>
              <div style={{display:"flex",gap:8,marginTop:8,flexWrap:"wrap"}}>
                {["chest pain shortness of breath","fever cough fatigue","headache dizziness nausea","joint pain swelling stiffness"].map(s=>(
                  <button key={s} onClick={()=>setSymptoms(s)} style={{padding:"3px 8px",borderRadius:10,border:`1px solid ${C.border}`,background:C.bg,cursor:"pointer",fontSize:10,color:C.muted,fontFamily:"inherit"}}>{s}</button>
                ))}
              </div>
              <div style={{marginTop:10}}><Btn onClick={runDiagnosis} full variant="purple" size="sm"><Brain size={12}/> {loading?"Analyzing...":"Run AI Diagnosis"}</Btn></div>
            </Card>
          </div>
          <div>
            {!aiResult&&!loading&&(
              <Card style={{background:C.bg,border:`1px dashed ${C.border}`,textAlign:"center",padding:40}}>
                <Brain size={32} color={C.light} style={{margin:"0 auto 10px",display:"block"}}/>
                <div style={{fontSize:12,color:C.muted}}>Enter symptoms and click "Run AI Diagnosis" to see differential diagnosis with ICD-10 codes, recommended tests, and clinical guidance.</div>
              </Card>
            )}
            {loading&&<Card style={{textAlign:"center",padding:40}}><div style={{fontSize:12,color:C.muted}}>🧠 Analyzing symptoms via AI model...</div></Card>}
            {aiResult&&!loading&&(
              <Card>
                <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:12}}>
                  <div style={{fontSize:13,fontWeight:800,color:C.text}}>Differential Diagnosis</div>
                  <span style={{padding:"3px 8px",borderRadius:8,background:urgColor[aiResult.urgency]+"18",color:urgColor[aiResult.urgency],fontSize:11,fontWeight:800,textTransform:"capitalize"}}>⚑ {aiResult.urgency} urgency</span>
                </div>
                {aiResult.conditions.map((c,i)=>(
                  <div key={i} style={{padding:"8px 10px",borderRadius:8,background:C.bg,marginBottom:6,display:"flex",alignItems:"center",gap:10}}>
                    <div style={{width:32,height:32,borderRadius:"50%",background:C.primaryLight,display:"flex",alignItems:"center",justifyContent:"center",fontSize:12,fontWeight:800,color:C.primary,flexShrink:0}}>{i+1}</div>
                    <div style={{flex:1}}>
                      <div style={{fontSize:12,fontWeight:700,color:C.text}}>{c.name}</div>
                      <div style={{fontSize:10,color:C.muted}}>ICD-10: {c.icd}</div>
                    </div>
                    <div>
                      <div style={{fontSize:13,fontWeight:800,color:c.conf>70?C.green:c.conf>50?C.amber:C.muted}}>{c.conf}%</div>
                      <div style={{fontSize:9,color:C.muted}}>confidence</div>
                    </div>
                  </div>
                ))}
                <div style={{marginTop:10,padding:"8px 10px",background:C.primaryLight,borderRadius:8}}>
                  <div style={{fontSize:11,fontWeight:700,color:C.primary,marginBottom:4}}>Recommended Tests</div>
                  <div style={{display:"flex",flexWrap:"wrap",gap:4}}>{aiResult.tests.map(t=><Badge key={t} text={t} color={C.primaryMid} bg="#fff"/>)}</div>
                </div>
                <div style={{marginTop:8,fontSize:11,color:C.muted,fontStyle:"italic",borderTop:`1px solid ${C.border}`,paddingTop:8}}>💊 {aiResult.recommendation}</div>
              </Card>
            )}
          </div>
        </div>
      )}

      {aiTab==="labanalysis"&&(
        <div style={{display:"grid",gridTemplateColumns:"200px 1fr",gap:14}}>
          <Card style={{padding:12}}>
            <div style={{fontSize:12,fontWeight:800,color:C.text,marginBottom:10}}>Patient Reports</div>
            {Object.keys(LAB_MOCK).map(name=>(
              <div key={name} onClick={()=>analyzeReport(name)} style={{padding:"8px 10px",borderRadius:8,cursor:"pointer",background:selectedReport?.name===name?C.primaryLight:"transparent",marginBottom:4,display:"flex",alignItems:"center",gap:8}}>
                <FlaskConical size={13} color={selectedReport?.name===name?C.primary:C.muted}/>
                <span style={{fontSize:12,color:selectedReport?.name===name?C.primary:C.text}}>{name}</span>
              </div>
            ))}
            <div style={{borderTop:`1px solid ${C.border}`,paddingTop:10,marginTop:4}}>
              <div style={{fontSize:10,color:C.muted,marginBottom:6}}>Upload new report</div>
              <label style={{display:"block",padding:"8px",borderRadius:8,border:`1.5px dashed ${C.border}`,textAlign:"center",cursor:"pointer",fontSize:10,color:C.muted}}>
                <Upload size={16} color={C.muted} style={{display:"block",margin:"0 auto 4px"}}/>
                {uploadedFile||"Drop PDF/Image"}
                <input type="file" style={{display:"none"}} onChange={e=>setUploadedFile(e.target.files[0]?.name||null)}/>
              </label>
              {uploadedFile&&<div style={{fontSize:10,color:C.green,marginTop:4,textAlign:"center"}}>✓ OCR extracting...</div>}
            </div>
          </Card>
          <div>
            {!selectedReport&&<Card style={{background:C.bg,border:`1px dashed ${C.border}`,textAlign:"center",padding:40}}><FlaskConical size={32} color={C.light} style={{margin:"0 auto 10px",display:"block"}}/><div style={{fontSize:12,color:C.muted}}>Select a report from the left panel to run AI analysis on lab values, flag abnormals, and get clinical interpretation.</div></Card>}
            {selectedReport&&(
              <Card>
                <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:12}}>
                  <div style={{fontSize:13,fontWeight:800,color:C.text}}>{selectedReport.name} — AI Analysis</div>
                  <Badge text="AI Interpreted" color={C.purple} bg={C.purpleLight}/>
                </div>
                <table style={{width:"100%",borderCollapse:"collapse",fontSize:12,marginBottom:12}}>
                  <thead><tr style={{background:C.bg}}>{["Parameter","Value","Unit","Reference","Status"].map(h=><th key={h} style={{padding:"6px 8px",textAlign:"left",color:C.muted,fontSize:11,fontWeight:700,borderBottom:`1px solid ${C.border}`}}>{h}</th>)}</tr></thead>
                  <tbody>{selectedReport.data.map((row,i)=>{
                    const sc={normal:C.green,high:C.red,low:C.amber}[row.status];
                    return <tr key={i} style={{background:row.status!=="normal"?sc+"08":"transparent"}}>
                      <td style={{padding:"7px 8px",color:C.text,fontWeight:row.status!=="normal"?700:400}}>{row.param}</td>
                      <td style={{padding:"7px 8px",fontWeight:800,color:sc}}>{row.val.toLocaleString()}</td>
                      <td style={{padding:"7px 8px",color:C.muted}}>{row.unit}</td>
                      <td style={{padding:"7px 8px",color:C.muted}}>{row.ref}</td>
                      <td style={{padding:"7px 8px"}}><Badge text={row.status.toUpperCase()} color={sc} bg={sc+"15"}/></td>
                    </tr>;
                  })}</tbody>
                </table>
                <div style={{background:C.purpleLight,border:`1px solid ${C.purple}30`,borderRadius:8,padding:"10px 12px"}}>
                  <div style={{fontSize:11,fontWeight:800,color:C.purple,marginBottom:6}}>🧠 AI Clinical Interpretation</div>
                  <div style={{fontSize:11,color:C.text,lineHeight:1.6}}>
                    {selectedReport.name==="CBC"&&"Findings suggest anemia (low Hb, low Hct) with mild leukocytosis. Differential: iron deficiency anemia vs. infection. Recommend peripheral smear, serum ferritin, TIBC. Follow-up CBC in 4 weeks post-treatment."}
                    {selectedReport.name==="Lipid Panel"&&"Dyslipidemia pattern: elevated LDL, low HDL, borderline triglycerides. 10-year ASCVD risk assessment recommended. Consider lifestyle modification + statin therapy. Repeat lipid panel in 3 months."}
                    {selectedReport.name==="Blood Glucose"&&"Pre-diabetic range: IFG (impaired fasting glucose) + borderline HbA1c. Lifestyle intervention recommended. OGTT to confirm. Diabetologist referral if no improvement in 3 months. Monitor HbA1c quarterly."}
                  </div>
                </div>
              </Card>
            )}
          </div>
        </div>
      )}

      {aiTab==="prescription"&&(
        <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:14}}>
          <Card>
            <div style={{fontSize:13,fontWeight:800,color:C.text,marginBottom:10}}>Prescription Review</div>
            <div style={{fontSize:11,color:C.muted,marginBottom:8}}>Enter or paste prescription text, or list medications:</div>
            <textarea value={prescInput} onChange={e=>setPrescInput(e.target.value)} placeholder="e.g.&#10;Aspirin 100mg OD&#10;Warfarin 5mg OD&#10;Metformin 500mg BD&#10;Atorvastatin 20mg OD" style={{width:"100%",height:120,padding:"10px 12px",border:`1px solid ${C.border}`,borderRadius:8,fontSize:12,color:C.text,resize:"none",boxSizing:"border-box",fontFamily:"monospace",lineHeight:1.7,outline:"none"}}/>
            <div style={{marginTop:8,display:"flex",gap:8}}>
              <Btn onClick={checkPrescription} full variant="purple" size="sm"><Pill size={12}/> Check Interactions</Btn>
              <Btn onClick={()=>{setPrescInput("Aspirin 100mg OD\nWarfarin 5mg OD\nMetformin 500mg BD");}} variant="ghost" size="sm">Load Example</Btn>
            </div>
          </Card>
          <div>
            {!prescResult&&<Card style={{background:C.bg,border:`1px dashed ${C.border}`,textAlign:"center",padding:40}}><Pill size={32} color={C.light} style={{margin:"0 auto 10px",display:"block"}}/><div style={{fontSize:12,color:C.muted}}>Paste prescription to check drug-drug interactions, allergy conflicts, dosage alerts, and patient-specific safety flags.</div></Card>}
            {prescResult&&(
              <Card>
                <div style={{fontSize:13,fontWeight:800,color:C.text,marginBottom:12}}>Safety Analysis</div>
                {prescResult.interactions.map((ix,i)=>(
                  <div key={i} style={{padding:"8px 10px",borderRadius:8,background:ix.severity==="high"?C.redLight:C.amberLight,marginBottom:8,borderLeft:`3px solid ${ix.severity==="high"?C.red:C.amber}`}}>
                    <div style={{fontSize:12,fontWeight:700,color:ix.severity==="high"?C.red:C.amber,marginBottom:3}}>{ix.severity==="high"?"🔴":"🟡"} {ix.drugs}</div>
                    <div style={{fontSize:11,color:C.text}}>{ix.note}</div>
                  </div>
                ))}
                {prescResult.dosageWarnings.map((w,i)=>(
                  <div key={i} style={{padding:"8px 10px",borderRadius:8,background:C.primaryLight,marginBottom:8,borderLeft:`3px solid ${C.primaryMid}`}}>
                    <div style={{fontSize:11,color:C.primaryMid}}>ℹ️ {w}</div>
                  </div>
                ))}
                <div style={{padding:"8px 10px",background:C.redLight,borderRadius:8,marginTop:4}}>
                  <div style={{fontSize:11,fontWeight:700,color:C.red}}>⚕️ {prescResult.recommendation}</div>
                </div>
              </Card>
            )}
          </div>
        </div>
      )}

      {aiTab==="history"&&(
        <div>
          <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:10,marginBottom:14}}>
            {[{l:"Total Visits",v:"7"},{l:"Unique Doctors",v:"3"},{l:"Open Follow-ups",v:"1"},{l:"Avg BP",v:"128/81"}].map(({l,v})=>(
              <Card key={l} style={{padding:12,textAlign:"center"}}>
                <div style={{fontSize:18,fontWeight:800,color:C.primary}}>{v}</div>
                <div style={{fontSize:10,color:C.muted,marginTop:3}}>{l}</div>
              </Card>
            ))}
          </div>
          <Card style={{marginBottom:14}}>
            <div style={{fontSize:13,fontWeight:800,color:C.text,marginBottom:12}}>Vital Signs Trend</div>
            <ResponsiveContainer width="100%" height={130}>
              <LineChart data={[{visit:"Feb",bp:135},{visit:"Mar",bp:138},{visit:"Apr 15",bp:120},{visit:"Apr 28",bp:118}]}>
                <CartesianGrid strokeDasharray="3 3" stroke={C.border} vertical={false}/>
                <XAxis dataKey="visit" tick={{fontSize:10,fill:C.muted}} axisLine={false} tickLine={false}/>
                <YAxis tick={{fontSize:10,fill:C.muted}} axisLine={false} tickLine={false} domain={[100,150]}/>
                <Tooltip contentStyle={{fontSize:11,borderRadius:8,border:`1px solid ${C.border}`}}/>
                <Line type="monotone" dataKey="bp" stroke={C.primary} strokeWidth={2} dot={{r:4,fill:C.primary}}/>
              </LineChart>
            </ResponsiveContainer>
          </Card>
          {historyData.map((h,i)=>(
            <Card key={i} style={{marginBottom:8,padding:14}}>
              <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:6}}>
                <div style={{fontSize:12,fontWeight:700,color:C.text}}>{h.dx}</div>
                <div style={{display:"flex",gap:6}}><Badge text={h.date} color={C.muted} bg={C.bg}/><Badge text={h.doctor} color={C.primaryMid} bg={C.primaryLight}/></div>
              </div>
              <div style={{display:"flex",gap:16,fontSize:11,color:C.muted}}>
                <span>BP: <strong style={{color:C.text}}>{h.bp}</strong></span>
                <span>Weight: <strong style={{color:C.text}}>{h.weight} kg</strong></span>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

// ─── ETL HUB ─────────────────────────────────────────────────────
function ETLView(){
  const [syncing,setSyncing]=useState(null);
  const [etlTab,setEtlTab]=useState("integrations");
  const [mapExpanded,setMapExpanded]=useState(false);

  const doSync=(name)=>{
    setSyncing(name);
    setTimeout(()=>setSyncing(null),2000);
  };

  const mappingRules=[
    {source:"MySoft: patient_name",target:"patients.full_name",transform:"Trim + Title Case",status:"active"},
    {source:"MySoft: dob",target:"patients.date_of_birth",transform:"dd/mm/yyyy → ISO 8601",status:"active"},
    {source:"LIS: test_result",target:"lab_reports.value",transform:"Parse float, validate range",status:"active"},
    {source:"LIS: ref_range",target:"lab_reports.reference",transform:"String normalization",status:"active"},
    {source:"MySoft: appt_date",target:"appointments.datetime",transform:"UTC offset correction",status:"active"},
    {source:"Insurance: policy_id",target:"patients.insurance_id",transform:"Prefix PAY- → strip",status:"review"},
  ];

  return(
    <div style={{maxWidth:960,margin:"0 auto",padding:"16px 12px 40px"}}>
      <div style={{display:"flex",alignItems:"center",gap:10,marginBottom:14}}>
        <div style={{width:40,height:40,borderRadius:12,background:C.tealLight,display:"flex",alignItems:"center",justifyContent:"center"}}><Database size={20} color={C.teal}/></div>
        <div><div style={{fontSize:15,fontWeight:800,color:C.text}}>ETL Integration Hub</div><div style={{fontSize:11,color:C.muted}}>Extract · Transform · Load — ERP / LIS / Insurance sync</div></div>
        <div style={{marginLeft:"auto",display:"flex",gap:8}}>
          <Badge text="HL7 Ready" color={C.teal} bg={C.tealLight}/>
          <Badge text="FHIR R4" color={C.purple} bg={C.purpleLight}/>
        </div>
      </div>

      <div style={{display:"flex",gap:2,borderBottom:`2px solid ${C.border}`,marginBottom:14}}>
        {[{k:"integrations",l:"Integrations"},{k:"mapping",l:"Field Mapping"},{k:"logs",l:"ETL Logs"},{k:"pipeline",l:"AI Pipeline"}].map(({k,l})=>(
          <button key={k} onClick={()=>setEtlTab(k)} style={{padding:"6px 14px",border:"none",background:"none",cursor:"pointer",fontSize:12,fontWeight:etlTab===k?800:400,color:etlTab===k?C.primary:C.muted,borderBottom:`2px solid ${etlTab===k?C.primary:"transparent"}`,marginBottom:-2,fontFamily:"inherit"}}>{l}</button>
        ))}
      </div>

      {etlTab==="integrations"&&(
        <div>
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12,marginBottom:14}}>
            {ERP_SYSTEMS.map(sys=>(
              <Card key={sys.name} style={{padding:14}}>
                <div style={{display:"flex",alignItems:"center",gap:10,marginBottom:10}}>
                  <div style={{fontSize:20}}>{sys.icon}</div>
                  <div style={{flex:1}}>
                    <div style={{fontSize:13,fontWeight:700,color:C.text}}>{sys.name}</div>
                    <div style={{fontSize:10,color:C.muted}}>Last sync: {sys.lastSync}</div>
                  </div>
                  <StatusBadge status={sys.status}/>
                </div>
                <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginTop:6}}>
                  <div style={{fontSize:11,color:C.muted}}>{sys.records>0?`${sys.records.toLocaleString()} records synced`:"Not synced"}</div>
                  <Btn onClick={()=>doSync(sys.name)} variant={sys.status==="disconnected"?"outline":"ghost"} size="sm">
                    <RefreshCw size={11} style={{animation:syncing===sys.name?"spin 1s linear infinite":undefined}}/>{syncing===sys.name?"Syncing...":sys.status==="disconnected"?"Connect":"Sync"}
                  </Btn>
                </div>
              </Card>
            ))}
          </div>
          <Card>
            <div style={{fontSize:13,fontWeight:800,color:C.text,marginBottom:10}}>ETL Architecture</div>
            <div style={{display:"grid",gridTemplateColumns:"repeat(5,1fr)",gap:8,alignItems:"center"}}>
              {[{l:"Source Systems",items:["MySoft ERP","Lab LIS","Insurance TPA","Pharmacy"],color:C.teal},{l:"Extract",items:["HL7 v2.5 parser","FHIR API client","CSV/JSON reader","REST adapter"],color:C.primaryMid},{l:"Transform",items:["Field mapping","Data cleaning","Type casting","Deduplication"],color:C.purple},{l:"Validate",items:["Schema check","Constraint check","Conflict detect","AI anomaly flag"],color:C.accent},{l:"Load",items:["PostgreSQL","Redis cache","Audit log","Event bus"],color:C.green}].map(({l,items,color})=>(
                <div key={l} style={{background:color+"10",border:`1px solid ${color}30`,borderRadius:8,padding:"10px 8px"}}>
                  <div style={{fontSize:10,fontWeight:800,color,marginBottom:6,textAlign:"center"}}>{l}</div>
                  {items.map(item=><div key={item} style={{fontSize:9,color:C.muted,padding:"2px 0",borderBottom:`1px solid ${color}20`,lineHeight:1.4}}>{item}</div>)}
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}

      {etlTab==="mapping"&&(
        <Card>
          <div style={{fontSize:13,fontWeight:800,color:C.text,marginBottom:12}}>Field Mapping Rules — {mappingRules.length} active mappings</div>
          <table style={{width:"100%",borderCollapse:"collapse",fontSize:12}}>
            <thead><tr style={{background:C.bg}}>
              {["Source Field","→","Target Field","Transform","Status"].map(h=><th key={h} style={{padding:"7px 10px",textAlign:"left",color:C.muted,fontSize:11,fontWeight:700,borderBottom:`1px solid ${C.border}`}}>{h}</th>)}
            </tr></thead>
            <tbody>{mappingRules.map((r,i)=>(
              <tr key={i} style={{borderBottom:`1px solid ${C.border}`}}>
                <td style={{padding:"8px 10px",fontFamily:"monospace",fontSize:11,color:C.primaryMid}}>{r.source}</td>
                <td style={{padding:"8px 4px",color:C.muted}}>→</td>
                <td style={{padding:"8px 10px",fontFamily:"monospace",fontSize:11,color:C.text}}>{r.target}</td>
                <td style={{padding:"8px 10px",fontSize:11,color:C.muted}}>{r.transform}</td>
                <td style={{padding:"8px 10px"}}><Badge text={r.status} color={r.status==="active"?C.green:C.amber} bg={r.status==="active"?C.greenLight:C.amberLight}/></td>
              </tr>
            ))}</tbody>
          </table>
          <div style={{marginTop:10,padding:"8px 12px",background:C.primaryLight,borderRadius:8,fontSize:11,color:C.primaryMid}}>
            💡 Conflict resolution strategy: <strong>Last-write-wins</strong> for non-clinical fields. Clinical data (diagnosis, prescriptions) requires manual review on conflict.
          </div>
        </Card>
      )}

      {etlTab==="logs"&&(
        <Card>
          <div style={{fontSize:13,fontWeight:800,color:C.text,marginBottom:12}}>Real-Time ETL Event Log</div>
          {ETL_LOGS.map((log,i)=>(
            <div key={i} style={{display:"flex",alignItems:"center",gap:10,padding:"8px 0",borderBottom:i<ETL_LOGS.length-1?`1px solid ${C.border}`:"none"}}>
              <div style={{fontSize:10,color:C.muted,width:60,flexShrink:0}}>{log.time}</div>
              <div style={{width:6,height:6,borderRadius:"50%",background:{success:C.green,warning:C.accent,error:C.red}[log.status],flexShrink:0}}/>
              <div style={{flex:1,fontSize:12,color:C.text}}>{log.event}</div>
              <div style={{fontSize:11,color:C.muted}}>{log.count}</div>
              <StatusBadge status={log.status}/>
            </div>
          ))}
          <div style={{marginTop:10,fontSize:11,color:C.muted,textAlign:"center"}}>Auto-refreshes every 30 seconds · Last 50 events shown</div>
        </Card>
      )}

      {etlTab==="pipeline"&&(
        <div>
          <Card style={{marginBottom:12}}>
            <div style={{fontSize:13,fontWeight:800,color:C.text,marginBottom:10}}>AI-Augmented ETL Pipeline</div>
            <div style={{fontSize:11,color:C.muted,marginBottom:12,lineHeight:1.6}}>The AI layer runs post-extraction to flag anomalies, suggest deduplication matches, and enrich records before loading into the clinical database.</div>
            <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:10}}>
              {[
                {title:"Anomaly Detection",desc:"Flags lab values >3σ from patient baseline. Auto-alerts doctor.",status:"Active",icon:AlertTriangle,color:C.red},
                {title:"Deduplication AI",desc:"Fuzzy name + DOB matching to prevent duplicate patient records.",status:"Active",icon:Users,color:C.purple},
                {title:"Record Enrichment",desc:"ICD-10 code suggestion from free-text diagnosis during import.",status:"Active",icon:Brain,color:C.teal},
                {title:"HL7 → FHIR Bridge",desc:"Converts legacy HL7 v2.5 messages to FHIR R4 resources.",status:"Active",icon:ArrowUpDown,color:C.primaryMid},
                {title:"Conflict Resolver",desc:"AI scores conflicting records and routes high-risk to manual review.",status:"Active",icon:Zap,color:C.accent},
                {title:"Compliance Checker",desc:"Auto-redacts PII in logs. Flags non-HIPAA fields before storage.",status:"Beta",icon:Shield,color:C.green},
              ].map(({title,desc,status,icon:I,color})=>(
                <div key={title} style={{padding:12,borderRadius:8,border:`1px solid ${C.border}`,background:color+"06"}}>
                  <div style={{display:"flex",alignItems:"center",gap:6,marginBottom:6}}>
                    <I size={14} color={color}/>
                    <span style={{fontSize:12,fontWeight:700,color:C.text}}>{title}</span>
                    <Badge text={status} color={status==="Active"?C.green:C.amber} bg={status==="Active"?C.greenLight:C.amberLight}/>
                  </div>
                  <div style={{fontSize:10,color:C.muted,lineHeight:1.5}}>{desc}</div>
                </div>
              ))}
            </div>
          </Card>
          <Card style={{background:C.bg}}>
            <div style={{fontSize:12,fontWeight:800,color:C.text,marginBottom:8}}>MVP Constraints Reminder</div>
            <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:8,fontSize:11}}>
              {[
                {l:"✅ Included in MVP",items:["MySoft ERP CSV/API sync","HL7 v2.5 parser (basic)","Field mapping engine","AI anomaly flagging","Conflict manual review queue","ETL audit log"]},
                {l:"🔜 Phase 2 (post-launch)",items:["FHIR R4 full implementation","Real-time streaming (Kafka)","Auto-conflict resolution","Multi-tenant ETL","Pharmacy live sync","Blockchain audit trail"]},
              ].map(({l,items})=>(
                <div key={l} style={{padding:10,borderRadius:8,background:C.card,border:`1px solid ${C.border}`}}>
                  <div style={{fontWeight:700,color:C.text,marginBottom:6}}>{l}</div>
                  {items.map(item=><div key={item} style={{padding:"2px 0",color:C.muted,borderBottom:`1px solid ${C.border}`,lineHeight:1.6}}>{item}</div>)}
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}

// ─── Patient Portal (preserved, compact) ─────────────────────────
function PortalView({onNav}){
  const [loggedIn,setLoggedIn]=useState(false);
  const [otp,setOtp]=useState("");
  const [sent,setSent]=useState(false);
  const [phone,setPhone]=useState("");
  const [tab,setTab]=useState("appointments");

  if(!loggedIn) return(
    <div style={{maxWidth:380,margin:"44px auto",padding:"0 12px"}}>
      <Card style={{padding:28}}>
        <div style={{textAlign:"center",marginBottom:20}}>
          <div style={{width:48,height:48,borderRadius:12,background:C.primaryLight,display:"flex",alignItems:"center",justifyContent:"center",margin:"0 auto 10px"}}><Shield size={22} color={C.primary}/></div>
          <h2 style={{fontSize:16,fontWeight:800,color:C.text,margin:"0 0 4px"}}>Patient Portal</h2>
          <p style={{fontSize:11,color:C.muted,margin:0}}>Login with your registered mobile number</p>
        </div>
        <div style={{marginBottom:10}}>
          <input value={phone} onChange={e=>setPhone(e.target.value)} placeholder="01XXXXXXXXX" style={{width:"100%",padding:"9px 11px",border:`1px solid ${C.border}`,borderRadius:8,fontSize:13,boxSizing:"border-box",outline:"none",fontFamily:"inherit"}}/>
        </div>
        {sent&&(
          <div style={{marginBottom:12}}>
            <input value={otp} onChange={e=>setOtp(e.target.value)} placeholder="Enter OTP (1234)" maxLength={4} style={{width:"100%",padding:"10px",border:`1px solid ${C.border}`,borderRadius:8,fontSize:20,fontWeight:800,boxSizing:"border-box",textAlign:"center",letterSpacing:"0.4em",outline:"none",fontFamily:"inherit"}}/>
            <div style={{fontSize:10,color:C.green,marginTop:3,fontWeight:700,textAlign:"center"}}>Demo OTP → 1234</div>
          </div>
        )}
        {!sent?<Btn onClick={()=>setSent(true)} full size="md">Send OTP</Btn>:<Btn onClick={()=>otp==="1234"&&setLoggedIn(true)} full size="md" sx={{opacity:otp.length===4?1:0.5}}>Verify & Login</Btn>}
      </Card>
    </div>
  );

  const myApts=[{id:"APT-2847",doctor:"Dr. Fatima Rahman",spec:"Cardiologist",date:"8 May 2026",time:"3:00 PM",status:"confirmed",serial:5,fee:1500},{id:"APT-2801",doctor:"Dr. Nasrin Khatun",spec:"Pediatrician",date:"28 Apr 2026",time:"5:00 PM",status:"completed",serial:12,fee:1200}];
  const myReports=[{id:"RPT-001",name:"CBC Report",date:"28 Apr 2026",type:"Blood Test",flagged:true},{id:"RPT-002",name:"ECG Report",date:"15 Apr 2026",type:"Cardiac",flagged:false}];

  return(
    <div style={{maxWidth:800,margin:"0 auto",padding:"16px 12px 40px"}}>
      <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:14}}>
        <div><h2 style={{fontSize:16,fontWeight:800,color:C.text,margin:"0 0 2px"}}>Welcome, Farhan Ahmed</h2><p style={{fontSize:11,color:C.muted,margin:0}}>PAT-00142 · B+ · Last visit Apr 28</p></div>
        <div style={{display:"flex",gap:8}}><Btn onClick={()=>onNav("chatbot")} variant="outline" size="sm"><Bot size={11}/> MedBot</Btn><Btn onClick={()=>setLoggedIn(false)} variant="ghost" size="sm"><LogOut size={11}/> Logout</Btn></div>
      </div>
      <div style={{display:"flex",gap:2,borderBottom:`2px solid ${C.border}`,marginBottom:12}}>
        {[{k:"appointments",l:"Appointments"},{k:"reports",l:"Reports"},{k:"aicheck",l:"AI Symptom Check"}].map(({k,l})=>(
          <button key={k} onClick={()=>setTab(k)} style={{padding:"6px 14px",border:"none",background:"none",cursor:"pointer",fontSize:12,fontWeight:tab===k?800:400,color:tab===k?C.primary:C.muted,borderBottom:`2px solid ${tab===k?C.primary:"transparent"}`,marginBottom:-2,fontFamily:"inherit"}}>{l}</button>
        ))}
      </div>
      {tab==="appointments"&&myApts.map(apt=>(
        <Card key={apt.id} style={{marginBottom:8,display:"flex",alignItems:"center",gap:10,padding:12}}>
          <Calendar size={18} color={apt.status==="confirmed"?C.primary:C.muted}/>
          <div style={{flex:1}}><div style={{fontSize:12,fontWeight:700,color:C.text}}>{apt.doctor} <StatusBadge status={apt.status}/></div><div style={{fontSize:10,color:C.muted}}>{apt.spec} · {apt.date} at {apt.time} · Serial #{apt.serial}</div></div>
          <span style={{fontSize:13,fontWeight:800,color:C.primary}}>৳{apt.fee.toLocaleString()}</span>
        </Card>
      ))}
      {tab==="reports"&&myReports.map(rep=>(
        <Card key={rep.id} style={{marginBottom:8,display:"flex",alignItems:"center",gap:10,padding:12}}>
          <FileText size={18} color={rep.flagged?C.red:C.green}/>
          <div style={{flex:1}}><div style={{fontSize:12,fontWeight:700,color:C.text}}>{rep.name} {rep.flagged&&<Badge text="Abnormal values" color={C.red} bg={C.redLight}/>}</div><div style={{fontSize:10,color:C.muted}}>{rep.type} · {rep.date}</div></div>
          <Btn size="sm" variant="outline"><Download size={11}/></Btn>
        </Card>
      ))}
      {tab==="aicheck"&&(
        <Card style={{background:C.primaryLight,border:`1px solid ${C.primaryMid}30`,textAlign:"center",padding:28}}>
          <Bot size={28} color={C.primary} style={{margin:"0 auto 8px",display:"block"}}/>
          <div style={{fontSize:13,fontWeight:700,color:C.text,marginBottom:6}}>Quick Symptom Check</div>
          <div style={{fontSize:11,color:C.muted,marginBottom:14,lineHeight:1.5}}>Describe your symptoms to our AI for preliminary guidance. Not a substitute for medical diagnosis.</div>
          <Btn onClick={()=>alert("MedBot symptom check — in a real deployment this opens the chatbot with symptom-check mode pre-loaded")} variant="primary" size="sm"><Bot size={12}/> Open MedBot Symptom Check</Btn>
        </Card>
      )}
    </div>
  );
}

// ─── Doctors view (compact) ───────────────────────────────────────
function DoctorsView({onNav,onPick}){
  const [q,setQ]=useState("");
  const filtered=DOCTORS.filter(d=>d.name.toLowerCase().includes(q.toLowerCase())||d.spec.toLowerCase().includes(q.toLowerCase()));
  return(
    <div style={{maxWidth:960,margin:"0 auto",padding:"16px 12px 40px"}}>
      <div style={{display:"flex",gap:8,marginBottom:14}}>
        <div style={{flex:1,position:"relative"}}>
          <Search size={13} style={{position:"absolute",left:10,top:"50%",transform:"translateY(-50%)",color:C.muted}}/>
          <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search doctor or specialty..." style={{width:"100%",padding:"9px 12px 9px 30px",border:`1px solid ${C.border}`,borderRadius:8,fontSize:13,background:C.card,color:C.text,boxSizing:"border-box",outline:"none",fontFamily:"inherit"}}/>
        </div>
      </div>
      <div style={{display:"grid",gridTemplateColumns:"repeat(2,1fr)",gap:10}}>
        {filtered.map(doc=>(
          <Card key={doc.id} style={{display:"flex",gap:10,padding:14}}>
            <Av init={doc.init} color={doc.color} size={46}/>
            <div style={{flex:1,minWidth:0}}>
              <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:4}}>
                <div><div style={{fontSize:12,fontWeight:700,color:C.text}}>{doc.name}</div><div style={{fontSize:10,color:C.muted}}>{doc.title}</div></div>
                <Badge text={doc.spec} color={doc.color} bg={doc.color+"18"}/>
              </div>
              <div style={{display:"flex",alignItems:"center",gap:8,marginBottom:6}}>
                <Star size={11} fill={C.accent} color={C.accent}/><span style={{fontSize:11,fontWeight:700,color:C.text}}>{doc.rating}</span><span style={{fontSize:10,color:C.light}}>({doc.reviews})</span>
              </div>
              <div style={{display:"flex",alignItems:"center",justifyContent:"space-between"}}>
                <div><div style={{fontSize:9,color:C.muted}}>Next available</div><div style={{fontSize:10,fontWeight:700,color:C.green}}>{doc.avail}</div></div>
                <div style={{textAlign:"right"}}><div style={{fontSize:13,fontWeight:800,color:C.primary}}>৳{doc.fee.toLocaleString()}</div><Btn onClick={()=>{onPick(doc);onNav("book");}} size="sm" sx={{marginTop:3}}>Book</Btn></div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

// ─── Booking View (compact) ───────────────────────────────────────
function BookView({doctor,onNav}){
  const [step,setStep]=useState(1);
  const [day,setDay]=useState(0);
  const [slot,setSlot]=useState(null);
  const [form,setForm]=useState({name:"",phone:""});
  const [done,setDone]=useState(false);
  if(!doctor) return <div style={{maxWidth:500,margin:"60px auto",padding:"0 12px",textAlign:"center"}}><div style={{fontSize:13,color:C.muted,marginBottom:12}}>No doctor selected.</div><Btn onClick={()=>onNav("doctors")}>Browse Doctors</Btn></div>;
  if(done) return(
    <div style={{maxWidth:440,margin:"32px auto",padding:"0 12px"}}>
      <Card style={{textAlign:"center",padding:28}}>
        <CheckCircle size={36} color={C.green} style={{margin:"0 auto 10px",display:"block"}}/>
        <h2 style={{fontSize:16,fontWeight:800,color:C.text,margin:"0 0 6px"}}>Appointment Confirmed!</h2>
        <p style={{color:C.muted,fontSize:12,margin:"0 0 16px"}}>Confirmation sent to {form.phone}</p>
        <div style={{background:C.primaryLight,borderRadius:8,padding:12,marginBottom:14,textAlign:"left",fontSize:11}}>
          {[["Doctor",doctor.name],["Date",`${DAYS[day].label}, ${DAYS[day].date} · ${slot}`],["Patient",form.name],["Serial","#7"]].map(([l,v])=>(
            <div key={l} style={{display:"flex",justifyContent:"space-between",padding:"4px 0",borderBottom:`1px solid ${C.border}`}}><span style={{color:C.muted}}>{l}</span><span style={{fontWeight:700,color:C.text}}>{v}</span></div>
          ))}
        </div>
        <div style={{display:"flex",gap:8}}><Btn onClick={()=>onNav("home")} variant="outline" full>Home</Btn><Btn onClick={()=>onNav("portal")} full>My Portal</Btn></div>
      </Card>
    </div>
  );
  return(
    <div style={{maxWidth:560,margin:"16px auto",padding:"0 12px 40px"}}>
      <Card>
        <div style={{display:"flex",alignItems:"center",gap:8,marginBottom:14}}>
          <Av init={doctor.init} color={doctor.color} size={34}/>
          <div><div style={{fontSize:12,fontWeight:700,color:C.text}}>{doctor.name}</div><div style={{fontSize:10,color:C.muted}}>{doctor.spec} · ৳{doctor.fee.toLocaleString()}</div></div>
          <Btn onClick={()=>onNav("doctors")} variant="ghost" size="sm" sx={{marginLeft:"auto"}}><X size={11}/></Btn>
        </div>
        {step===1&&(<>
          <div style={{display:"flex",gap:5,marginBottom:12}}>
            {DAYS.map((d,i)=>(
              <button key={i} onClick={()=>setDay(i)} style={{flex:1,padding:"7px 3px",borderRadius:7,border:`1.5px solid ${day===i?C.primary:C.border}`,background:day===i?C.primaryLight:C.card,cursor:"pointer",fontFamily:"inherit"}}>
                <div style={{fontSize:8,fontWeight:700,color:day===i?C.primary:C.muted}}>{d.label.toUpperCase()}</div>
                <div style={{fontSize:11,fontWeight:700,color:day===i?C.primary:C.text}}>{d.date}</div>
              </button>
            ))}
          </div>
          <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:6,marginBottom:12}}>
            {doctor.slots.map(s=>(
              <button key={s} onClick={()=>setSlot(s)} style={{padding:"7px 3px",borderRadius:7,border:`1.5px solid ${slot===s?C.primary:C.border}`,background:slot===s?C.primary:C.card,cursor:"pointer",color:slot===s?"#fff":C.text,fontSize:11,fontWeight:700,fontFamily:"inherit"}}>{s}</button>
            ))}
          </div>
          <Btn onClick={()=>slot&&setStep(2)} full sx={{opacity:slot?1:0.45}}>Continue →</Btn>
        </>)}
        {step===2&&(<>
          {[{k:"name",l:"Full Name",ph:"Mohammad Ali"},{k:"phone",l:"Mobile",ph:"01XXXXXXXXX"}].map(({k,l,ph})=>(
            <div key={k} style={{marginBottom:10}}>
              <label style={{display:"block",fontSize:11,fontWeight:700,color:C.text,marginBottom:3}}>{l}</label>
              <input value={form[k]} onChange={e=>setForm(p=>({...p,[k]:e.target.value}))} placeholder={ph} style={{width:"100%",padding:"8px 10px",border:`1px solid ${C.border}`,borderRadius:7,fontSize:12,color:C.text,boxSizing:"border-box",outline:"none",fontFamily:"inherit"}}/>
            </div>
          ))}
          <div style={{display:"flex",gap:8}}><Btn onClick={()=>setStep(1)} variant="outline">Back</Btn><Btn onClick={()=>(form.name&&form.phone)&&setDone(true)} full sx={{opacity:(form.name&&form.phone)?1:0.45}}><CheckCircle size={12}/> Confirm</Btn></div>
        </>)}
      </Card>
    </div>
  );
}

// ─── Admin (compact) ─────────────────────────────────────────────
function AdminView(){
  const appts=[
    {id:"APT-2851",patient:"Mohammad Ali",doctor:"Dr. F. Rahman",time:"9:00 AM",status:"confirmed",serial:1},
    {id:"APT-2850",patient:"Sumaiya Akter",doctor:"Dr. N. Khatun",time:"9:30 AM",status:"confirmed",serial:2},
    {id:"APT-2849",patient:"Rashed Khan",doctor:"Dr. A. Hossain",time:"10:00 AM",status:"pending",serial:3},
    {id:"APT-2848",patient:"Fatema Begum",doctor:"Dr. K. Uddin",time:"10:30 AM",status:"pending",serial:4},
  ];
  const [adminTab,setAdminTab]=useState("schedule");
  return(
    <div style={{maxWidth:960,margin:"0 auto",padding:"16px 12px 40px"}}>
      <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:14}}>
        <div><h2 style={{fontSize:16,fontWeight:800,color:C.text,margin:"0 0 2px"}}>Admin Dashboard</h2><p style={{fontSize:11,color:C.muted,margin:0}}>May 4, 2026 · MedCore</p></div>
        <div style={{display:"flex",gap:8}}>
          <Btn onClick={()=>alert("Navigate to AI Clinical Panel in the nav")} variant="outline" size="sm"><Brain size={11}/> AI Panel</Btn>
          <Btn onClick={()=>alert("Navigate to ETL Hub in the nav")} variant="outline" size="sm"><Database size={11}/> ETL</Btn>
        </div>
      </div>
      <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:10,marginBottom:14}}>
        {[{l:"Today's Appts",v:"6",c:C.primary},{l:"Confirmed",v:"4",c:C.green},{l:"Pending",v:"2",c:C.accent},{l:"ETL Synced",v:"1,081",c:C.teal}].map(({l,v,c})=>(
          <Card key={l} style={{padding:12}}>
            <div style={{fontSize:20,fontWeight:800,color:c,lineHeight:1}}>{v}</div>
            <div style={{fontSize:10,color:C.muted,marginTop:3}}>{l}</div>
          </Card>
        ))}
      </div>
      <div style={{display:"flex",gap:2,borderBottom:`2px solid ${C.border}`,marginBottom:12}}>
        {[{k:"schedule",l:"Schedule"},{k:"analytics",l:"Analytics"}].map(({k,l})=>(
          <button key={k} onClick={()=>setAdminTab(k)} style={{padding:"6px 14px",border:"none",background:"none",cursor:"pointer",fontSize:12,fontWeight:adminTab===k?800:400,color:adminTab===k?C.primary:C.muted,borderBottom:`2px solid ${adminTab===k?C.primary:"transparent"}`,marginBottom:-2,fontFamily:"inherit"}}>{l}</button>
        ))}
      </div>
      {adminTab==="schedule"&&(
        <table style={{width:"100%",borderCollapse:"collapse",fontSize:12}}>
          <thead><tr style={{background:C.bg}}>{["#","ID","Patient","Doctor","Time","Status"].map(h=><th key={h} style={{padding:"7px 10px",textAlign:"left",color:C.muted,fontSize:11,fontWeight:700,borderBottom:`1px solid ${C.border}`}}>{h}</th>)}</tr></thead>
          <tbody>{appts.map((a,i)=>(
            <tr key={a.id} style={{background:i%2?"#FAFAFA":C.card}}>
              <td style={{padding:"8px 10px",fontWeight:800,color:C.primaryMid}}>#{a.serial}</td>
              <td style={{padding:"8px 10px",color:C.muted,fontSize:11}}>{a.id}</td>
              <td style={{padding:"8px 10px",fontWeight:700}}>{a.patient}</td>
              <td style={{padding:"8px 10px",color:C.text}}>{a.doctor}</td>
              <td style={{padding:"8px 10px"}}><Badge text={a.time} color={C.primaryMid} bg={C.primaryLight}/></td>
              <td style={{padding:"8px 10px"}}><StatusBadge status={a.status}/></td>
            </tr>
          ))}</tbody>
        </table>
      )}
      {adminTab==="analytics"&&(
        <Card>
          <div style={{fontSize:13,fontWeight:800,color:C.text,marginBottom:12}}>Weekly Appointment Trends</div>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={CHART_DATA} barGap={3} barCategoryGap="30%">
              <CartesianGrid strokeDasharray="3 3" stroke={C.border} vertical={false}/>
              <XAxis dataKey="day" tick={{fontSize:10,fill:C.muted}} axisLine={false} tickLine={false}/>
              <YAxis tick={{fontSize:10,fill:C.muted}} axisLine={false} tickLine={false}/>
              <Tooltip contentStyle={{fontSize:11,borderRadius:8,border:`1px solid ${C.border}`}}/>
              <Bar dataKey="booked" name="Booked" fill={C.primaryMid} radius={[3,3,0,0]}/>
              <Bar dataKey="completed" name="Completed" fill={C.green} radius={[3,3,0,0]}/>
            </BarChart>
          </ResponsiveContainer>
        </Card>
      )}
    </div>
  );
}

// ─── App root ─────────────────────────────────────────────────────
export default function App(){
  const [view,setView]=useState("home");
  const [doc,setDoc]=useState(null);
  return(
    <div style={{minHeight:"100vh",background:C.bg,fontFamily:"'Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',sans-serif"}}>
      <NavBar view={view} onNav={setView}/>
      {view==="home"&&<HomeView onNav={setView} onPick={setDoc}/>}
      {view==="doctors"&&<DoctorsView onNav={setView} onPick={setDoc}/>}
      {view==="book"&&<BookView doctor={doc} onNav={setView}/>}
      {view==="chatbot"&&<ChatbotView/>}
      {view==="ai-clinical"&&<AIClinicalView/>}
      {view==="etl"&&<ETLView/>}
      {view==="portal"&&<PortalView onNav={setView}/>}
      {view==="admin"&&<AdminView/>}
    </div>
  );
}
