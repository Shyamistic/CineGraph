export type BuddyState = "idle" | "thinking" | "whispering" | "excited" | "generating";

const MOODS: Record<BuddyState, { ring: string; glow: string; eye: number; label: string }> = {
  idle: { ring: "#756bff", glow: "#a8a2ff", eye: 1, label: "ready" },
  thinking: { ring: "#ffb86b", glow: "#ffd39d", eye: 0.72, label: "thinking" },
  whispering: { ring: "#63d7e5", glow: "#a7f1f2", eye: 1, label: "speaking" },
  excited: { ring: "#ff7e9b", glow: "#ffc0cb", eye: 1.15, label: "excited" },
  generating: { ring: "#b58cff", glow: "#d4c3ff", eye: 0.9, label: "creating" },
};

export function Buddy({ state, size = 120 }: { state: BuddyState; size?: number }) {
  const mood = MOODS[state] ?? MOODS.idle;
  return (
    <div className={`buddy buddy-${state}`} style={{ width: size, height: size }} aria-label={`Watch Buddy is ${mood.label}`}>
      <svg viewBox="0 0 160 160" width={size} height={size} role="img" aria-hidden>
        <defs>
          <radialGradient id="buddyAura" cx="50%" cy="38%" r="64%">
            <stop offset="0%" stopColor={mood.glow} stopOpacity="0.46" />
            <stop offset="72%" stopColor={mood.ring} stopOpacity="0.08" />
            <stop offset="100%" stopColor={mood.ring} stopOpacity="0" />
          </radialGradient>
          <linearGradient id="buddyShell" x1="20%" y1="10%" x2="90%" y2="100%">
            <stop offset="0%" stopColor="#303b63" />
            <stop offset="48%" stopColor="#171d3b" />
            <stop offset="100%" stopColor="#0c1024" />
          </linearGradient>
          <linearGradient id="buddyFace" x1="15%" y1="0%" x2="85%" y2="100%">
            <stop offset="0%" stopColor="#172448" />
            <stop offset="100%" stopColor="#070a18" />
          </linearGradient>
          <filter id="buddyShadow" x="-30%" y="-30%" width="160%" height="180%">
            <feDropShadow dx="0" dy="10" stdDeviation="8" floodColor="#000" floodOpacity="0.42" />
          </filter>
        </defs>
        <ellipse cx="80" cy="84" rx="72" ry="72" fill="url(#buddyAura)" />
        <ellipse cx="80" cy="143" rx="42" ry="8" fill="#02030b" opacity="0.7" />
        <circle
          className="buddy-ring"
          cx="80"
          cy="80"
          r="68"
          fill="none"
          stroke={mood.ring}
          strokeWidth="1.5"
          strokeDasharray={state === "generating" ? "18 12" : "0 0"}
          opacity="0.7"
        />
        <g className="buddy-body" filter="url(#buddyShadow)">
          <path d="M39 115 C34 105 32 93 34 73 L42 47 C45 35 56 27 69 25 L91 25 C105 27 116 35 119 47 L126 74 C128 94 125 105 120 115 C108 129 52 129 39 115Z" fill="url(#buddyShell)" stroke="#5c6da4" strokeWidth="1.4" />
          <path d="M48 91 C43 76 46 57 53 47 C63 39 96 38 107 47 C115 58 118 77 112 92 C104 105 57 105 48 91Z" fill="url(#buddyFace)" stroke="#51639d" strokeWidth="1" />
          <path d="M54 47 C62 39 99 39 106 48" fill="none" stroke="#93a3e2" strokeWidth="1.4" opacity="0.42" />
          <g className="buddy-eyes" style={{ transform: `scaleY(${mood.eye})`, transformOrigin: "80px 69px" }}>
            <circle cx="66" cy="68" r="6" fill={mood.glow} opacity="0.18" />
            <circle cx="94" cy="68" r="6" fill={mood.glow} opacity="0.18" />
            <circle cx="66" cy="68" r="3.2" fill={mood.glow} />
            <circle cx="94" cy="68" r="3.2" fill={mood.glow} />
          </g>
          {state === "excited" ? (
            <path d="M68 82 Q80 94 92 82" stroke={mood.glow} strokeWidth="2.8" fill="none" strokeLinecap="round" />
          ) : state === "whispering" ? (
            <ellipse cx="80" cy="84" rx="6" ry="4" fill={mood.glow} opacity="0.85" />
          ) : (
            <path d="M73 84 Q80 88 87 84" stroke={mood.glow} strokeWidth="2.2" fill="none" strokeLinecap="round" opacity="0.7" />
          )}
          <path d="M80 27 L80 14" stroke="#6e7db5" strokeWidth="2" />
          <circle cx="80" cy="10" r="7" fill="#182044" stroke={mood.ring} strokeWidth="2" className="buddy-reel" />
          <path d="M44 105 Q34 114 32 126" fill="none" stroke="#52639c" strokeWidth="4" strokeLinecap="round" />
          <path d="M116 105 Q126 114 128 126" fill="none" stroke="#52639c" strokeWidth="4" strokeLinecap="round" />
          <circle cx="31" cy="128" r="5" fill={mood.ring} opacity="0.8" />
          <circle cx="129" cy="128" r="5" fill={mood.ring} opacity="0.8" />
        </g>
      </svg>
      {state === "generating" && <span className="buddy-caption">creating</span>}
    </div>
  );
}
