import React from 'react';

const Av = ({ init, color, size = 40 }: { init: string; color: string; size?: number }) => (
  <div
    style={{
      width: size,
      height: size,
      borderRadius: "50%",
      background: `${color}22`,
      border: `2px solid ${color}44`,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: size * 0.3,
      fontWeight: 700,
      color,
      flexShrink: 0,
    }}
  >
    {init}
  </div>
);

export default Av;