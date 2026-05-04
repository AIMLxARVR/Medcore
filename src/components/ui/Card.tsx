import React from 'react';
import { C } from '../../constants/colors';

const Card=({children,style:sx={}}: {children: React.ReactNode, style?: React.CSSProperties})=>(
  <div style={{background:C.card,border:`1px solid ${C.border}`,borderRadius:12,padding:20,...sx}}>{children}</div>
);

export default Card;