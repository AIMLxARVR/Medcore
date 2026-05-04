import React, { useRef, useEffect } from 'react';
import { Bot, Send, RefreshCw } from 'lucide-react';
import { C } from '../../constants/colors';
import TypingDots from '../../components/shared/TypingDots';
import { Button, Card } from '../../components/ui';
import { useChat } from '../../hooks/useChat';

const quickReplies=[
  {label:"📅 Book appointment",msg:"I want to book an appointment"},
  {label:"🗓️ My appointment",msg:"Show my upcoming appointment"},
  {label:"👨‍⚕️ Available doctors",msg:"Which doctors are available today?"},
  {label:"📄 My reports",msg:"Show my recent reports"},
  {label:"🤒 I have fever",msg:"I have fever and cough"},
  {label:"💔 Chest pain",msg:"I'm having chest pain"},
];

function ChatbotView(){
  const { msgs, input, typing, error, setInput, send, reset } = useChat();
  const bottom=useRef(null);
  useEffect(()=>{bottom.current?.scrollIntoView({behavior:"smooth"});},[msgs,typing]);

  return(
    <div style={{maxWidth:680,margin:"0 auto",padding:"16px 12px 40px"}}>
      <div style={{display:"flex",alignItems:"center",gap:10,marginBottom:14}}>
        <div style={{width:40,height:40,borderRadius:12,background:C.primaryLight,display:"flex",alignItems:"center",justifyContent:"center"}}><Bot size={20} color={C.primary}/></div>
        <div>
          <div style={{fontSize:15,fontWeight:800,color:C.text}}>MedBot — AI Assistant</div>
          <div style={{fontSize:11,color:C.green,display:"flex",alignItems:"center",gap:4}}>
            <div style={{width:6,height:6,borderRadius:"50%",background:C.green}}/>Online
          </div>
        </div>
        <Button onClick={reset} variant="ghost" size="sm" style={{marginLeft:"auto"}}><RefreshCw size={12}/> Reset</Button>
      </div>
      <Card style={{height:400,display:"flex",flexDirection:"column",padding:0}}>
        <div style={{flex:1,overflowY:"auto",padding:"14px"}}>
          {msgs.map((m,i)=>(
            <div key={i} style={{display:"flex",justifyContent:m.from==="bot"?"flex-start":"flex-end",marginBottom:10}}>
              <div style={{background:m.from==="bot"?C.bg:C.primary,color:m.from==="bot"?C.text:"#fff",padding:"8px 12px",borderRadius:12,maxWidth:"85%",fontSize:13,lineHeight:1.5,whiteSpace:"pre-wrap"}}>
                {m.text}
              </div>
            </div>
          ))}
          {typing && <TypingDots/>}
          <div ref={bottom}/>
        </div>
        <div style={{borderTop:`1px solid ${C.border}`,padding:"8px",background:C.card,borderBottomLeftRadius:12,borderBottomRightRadius:12}}>
          <div style={{display:"flex",gap:4,marginBottom:6,flexWrap:"wrap"}}>
            {quickReplies.map(qr=>(
              <button key={qr.label} onClick={()=>send(qr.msg)} style={{background:C.bg,border:`1px solid ${C.border}`,color:C.muted,padding:"4px 8px",borderRadius:12,fontSize:11,cursor:"pointer",fontFamily:"inherit"}}>
                {qr.label}
              </button>
            ))}
          </div>
          <div style={{display:"flex",alignItems:"center",gap:8}}>
            <input value={input} onChange={e=>setInput(e.target.value)} onKeyPress={e=>e.key==="Enter"&&send()} placeholder="Ask MedBot..." style={{flex:1,border:`1px solid ${C.border}`,borderRadius:8,padding:"8px 12px",fontSize:13,fontFamily:"inherit"}}/>
            <Button onClick={()=>send()} disabled={typing}><Send size={14}/></Button>
          </div>
          {error && <div style={{color:C.red,fontSize:11,marginTop:6,textAlign:"center"}}>{error}</div>}
        </div>
      </Card>
    </div>
  );
}

export default ChatbotView;