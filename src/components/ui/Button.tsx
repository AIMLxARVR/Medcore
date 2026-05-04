import React from 'react';
import { C } from '../../constants/colors';

const Btn=({children,onClick,variant="primary",size="md",full=false,style:sx={}}: {children: React.ReactNode, onClick?: () => void, variant?: string, size?: string, full?: boolean, style?: React.CSSProperties})=>{
  const vs={primary:{background:C.primary,color:"#fff",border:`1px solid ${C.primary}`},outline:{background:"transparent",color:C.primary,border:`1px solid ${C.primary}`},ghost:{background:"transparent",color:C.muted,border:`1px solid ${C.border}`},success:{background:C.green,color:"#fff",border:`1px solid ${C.green}`},danger:{background:C.red,color:"#fff",border:`1px solid ${C.red}`},purple:{background:C.purple,color:"#fff",border:`1px solid ${C.purple}`}};
  const ss={sm:{padding:"5px 11px",fontSize:12},md:{padding:"8px 16px",fontSize:13},lg:{padding:"11px 22px",fontSize:14}};
  return <button onClick={onClick} style={{...vs[variant],...ss[size],borderRadius:8,fontWeight:700,cursor:"pointer",display:"inline-flex",alignItems:"center",gap:5,width:full?"100%":"auto",justifyContent:"center",fontFamily:"inherit",...sx}}>{children}</button>;
};

export default Btn;