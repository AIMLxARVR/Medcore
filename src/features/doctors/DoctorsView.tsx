import React from 'react';
import { Star } from 'lucide-react';
import { C } from '../../constants/colors';
import { DOCTORS } from '../../constants/data';
import { Button, Card, Avatar, Badge } from '../../components/ui';

function DoctorsView({onNav, onPick}: {onNav: (view: string) => void, onPick: (doctor: any) => void}){
  return(
    <div style={{maxWidth:960,margin:"0 auto",padding:"16px 12px 40px"}}>
      <h1 style={{fontSize:20,fontWeight:800,color:C.text,marginBottom:16}}>Our Doctors</h1>
      <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:12}}>
        {DOCTORS.map(doc=>(
          <Card key={doc.id} style={{padding:16}}>
            <div style={{display:"flex",alignItems:"center",gap:12,marginBottom:12}}>
              <Avatar init={doc.init} color={doc.color} size={50}/>
              <div>
                <div style={{fontSize:14,fontWeight:700,color:C.text,lineHeight:1.3}}>{doc.name}</div>
                <div style={{fontSize:11,color:C.muted,marginTop:2}}>{doc.title}</div>
              </div>
            </div>
            <div style={{display:"flex",gap:6,marginBottom:10}}>
              <Badge text={doc.spec} />
              <Badge text={doc.dept} />
            </div>
            <div style={{display:"flex",alignItems:"center",gap:12,fontSize:11,color:C.muted,marginBottom:12}}>
              <div style={{display:"flex",alignItems:"center",gap:3}}><Star size={12} color={C.accent} fill={C.accent}/> <span style={{color:C.text,fontWeight:700}}>{doc.rating}</span> ({doc.reviews} reviews)</div>
              <div><span style={{color:C.text,fontWeight:700}}>{doc.patients}</span> patients</div>
            </div>
            <div style={{borderTop:`1px solid ${C.border}`,paddingTop:12,display:"flex",alignItems:"center",justifyContent:"space-between"}}>
              <div>
                <div style={{fontSize:11,color:C.muted}}>Booking Fee</div>
                <div style={{fontSize:16,fontWeight:800,color:C.primary}}>৳{doc.fee.toLocaleString()}</div>
              </div>
              <Button onClick={()=>{onPick(doc);onNav("book");}} size="md">Book Now</Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default DoctorsView;