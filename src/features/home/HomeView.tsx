import React from 'react';
import { Brain, Database, Bot, ArrowRight, ChevronRight, FlaskConical } from 'lucide-react';
import { C } from '../../constants/colors';
import { DOCTORS } from '../../constants/data';
import { Button, Card, Avatar } from '../../components/ui';

function HomeView({onNav,onPick}:{onNav: (view: string) => void, onPick: (doctor: any) => void}){
  return(
    <div style={{maxWidth:960,margin:"0 auto",padding:"0 12px 40px"}}>
      <div style={{background:C.primary,borderRadius:16,padding:"28px 28px",color:"#fff",margin:"16px 0 16px"}}>
        <div style={{fontSize:9,fontWeight:800,letterSpacing:"0.12em",opacity:0.65,marginBottom:6}}>DHAKA MEDICARE — AI-ENHANCED MVP</div>
        <h1 style={{fontSize:22,fontWeight:800,lineHeight:1.2,margin:"0 0 8px"}}>Intelligent Healthcare Management</h1>
        <p style={{opacity:0.8,marginBottom:18,fontSize:12,lineHeight:1.6}}>AI diagnosis assistance · Public chatbot · ETL pipeline · Report analysis · Full EMR</p>
        <div style={{display:"flex",gap:8,flexWrap:"wrap"}}>
          <Button onClick={()=>onNav("chatbot")} size="sm" sx={{background:"#fff",color:C.primary,border:"none"}}><Bot size={12}/> AI Chatbot</Button>
          <Button onClick={()=>onNav("ai-clinical")} size="sm" sx={{background:"rgba(255,255,255,0.15)",color:"#fff",borderColor:"rgba(255,255,255,0.3)"}}><Brain size={12}/> AI Clinical Panel</Button>
          <Button onClick={()=>onNav("etl")} size="sm" sx={{background:"rgba(255,255,255,0.15)",color:"#fff",borderColor:"rgba(255,255,255,0.3)"}}><Database size={12}/> ETL Hub</Button>
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
        <Button onClick={()=>onNav("doctors")} variant="ghost" size="sm">View All <ChevronRight size={12}/></Button>
      </div>
      <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:10}}>
        {DOCTORS.slice(0,3).map(doc=>(
          <Card key={doc.id} style={{padding:14}}>
            <div style={{display:"flex",alignItems:"center",gap:8,marginBottom:8}}>
              <Avatar init={doc.init} color={doc.color} size={38}/>
              <div><div style={{fontSize:12,fontWeight:700,color:C.text,lineHeight:1.2}}>{doc.name}</div><div style={{fontSize:10,color:C.muted,marginTop:2}}>{doc.spec}</div></div>
            </div>
            <div style={{fontSize:10,color:C.green,fontWeight:700,marginBottom:8}}><span style={{color:C.muted}}>Next: </span>{doc.avail}</div>
            <div style={{display:"flex",alignItems:"center",justifyContent:"space-between"}}>
              <span style={{fontSize:13,fontWeight:800,color:C.primary}}>৳{doc.fee.toLocaleString()}</span>
              <Button onClick={()=>{onPick(doc);onNav("book");}} size="sm">Book</Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default HomeView;