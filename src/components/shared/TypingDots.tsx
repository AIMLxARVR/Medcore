import React, { useState, useEffect } from 'react';
import { C } from '../../constants/colors';

const TypingDots=()=>{
  const [dot,setDot]=useState(0);
  useEffect(()=>{const t=setInterval(()=>setDot(d=>(d+1)%4),400);return()=>clearInterval(t);},[]);
  const labels=["Thinking","Thinking.","Thinking..","Thinking..."];
  return <span style={{color:C.muted,fontSize:12}}>{labels[dot]}</span>;
};

export default TypingDots;