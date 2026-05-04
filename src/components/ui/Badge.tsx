import React from 'react';
import { C } from '../../constants/colors';

const Badge=({text,color=C.primaryMid,bg=C.primaryLight}: {text: string, color?: string, bg?: string})=>(
  <span style={{display:"inline-block",padding:"2px 8px",borderRadius:12,background:bg,color,fontSize:11,fontWeight:700,whiteSpace:"nowrap"}}>{text}</span>
);

export default Badge;