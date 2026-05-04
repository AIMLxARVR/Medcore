import React from 'react';
import { Stethoscope } from 'lucide-react';
import { C } from '../../constants/colors';

function NavBar({view,onNav}:{view: string, onNav: (view: string) => void}){
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

export default NavBar;