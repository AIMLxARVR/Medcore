import React from 'react';
import Badge from './Badge';
import { C } from '../../constants/colors';

const StatusBadge=({status}: {status: string})=>{
  const m={confirmed:{bg:C.greenLight,c:C.green,l:"Confirmed"},pending:{bg:C.amberLight,c:C.amber,l:"Pending"},completed:{bg:"#F1F5F9",c:C.muted,l:"Completed"},cancelled:{bg:C.redLight,c:C.red,l:"Cancelled"},success:{bg:C.greenLight,c:C.green,l:"Success"},warning:{bg:C.amberLight,c:C.amber,l:"Warning"},error:{bg:C.redLight,c:C.red,l:"Error"},syncing:{bg:C.primaryLight,c:C.primaryMid,l:"Syncing"},connected:{bg:C.greenLight,c:C.green,l:"Connected"},disconnected:{bg:C.redLight,c:C.red,l:"Disconnected"}};
  const s=m[status]||m.pending;
  return <Badge text={s.l} color={s.c} bg={s.bg}/>;
};

export default StatusBadge;