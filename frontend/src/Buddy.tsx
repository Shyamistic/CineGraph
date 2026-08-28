/**
 * The Watch Buddy companion.
 *
 * A coded SVG/CSS character — no asset pipeline, crisp at any size. It has five
 * states that drive the whole watch-along interaction:
 *   idle       — gentle breathing, ambient
 *   thinking   — considering the scene
 *   whispering — leaning in to offer a suggestion
 *   excited    — a fork was chosen
 *   generating — minting the fork (animated ring)
 *
 * The buddy is the interface; the deterministic mint pipeline is the product.
 */

export type BuddyState = "idle" | "thinking" | "whispering" | "excited" | "generating";

const MOODS: Record<BuddyState, { ring: string; glow: string; eye: number }> = {
  idle: { ring: "#3a4256", glow: "#7f8aa8", eye: 1 },
  thinking: { ring: "#c9a24a", glow: "#c9a24a", eye: 0.7 },
  whispering: { ring: "#6fb2ff", glow: "#6fb2ff", eye: 1 },
  excited: { ring: "#ffcf5c", glow: "#ffcf5c", eye: 1.15 },
  generating: { ring: "#8b6fff", glow: "#8b6fff", eye: 0.9 },
};

export function Buddy({ state, size = 120 }: { state: BuddyState; size?: number }) {
  const mood = MOODS[state] ?? MOODS.idle;
  return (
    <div className={`buddy buddy-${state}`} style={{ width: size, height: size }}>
      <svg viewBox="0 0 120 120" width={size} height={size} aria-hidden>
        {/* halo / status ring */}
        <circle
          className="buddy-ring"
          cx="60"
          cy="60"
          r="52"
          fill="none"
          stroke={mood.ring}
          strokeWidth="2"
          strokeDasharray={state === "generating" ? "18 12" : "0 0"}
          opacity="0.7"
        />
        {/* soft glow */}
        <circle cx="60" cy="60" r="42" fill={mood.glow} opacity="0.10" className="buddy-glow" />

        {/* body: a friendly film-reel droid */}
        <g className="buddy-body">
          <rect x="30" y="34" width="60" height="52" rx="18" fill="#141824" stroke="#2b3142" strokeWidth="2" />
          {/* face screen */}
          <rect x="38" y="44" width="44" height="30" rx="10" fill="#0a0d15" stroke="#232a3a" />
          {/* eyes */}
          <g className="buddy-eyes" style={{ transform: `scaleY(${mood.eye})`, transformOrigin: "60px 59px" }}>
            <circle cx="51" cy="59" r="4.2" fill={mood.glow} />
            <circle cx="69" cy="59" r="4.2" fill={mood.glow} />
          </g>
          {/* mouth changes by mood */}
          {state === "excited" ? (
            <path d="M52 68 Q60 76 68 68" stroke={mood.glow} strokeWidth="2.2" fill="none" strokeLinecap="round" />
          ) : state === "whispering" ? (
            <ellipse cx="60" cy="69" rx="4" ry="2.6" fill={mood.glow} opacity="0.85" />
          ) : (
            <line x1="54" y1="69" x2="66" y2="69" stroke={mood.glow} strokeWidth="2" strokeLinecap="round" opacity="0.7" />
          )}
          {/* antenna: little reel */}
          <line x1="60" y1="34" x2="60" y2="22" stroke="#2b3142" strokeWidth="2" />
          <circle cx="60" cy="18" r="5" fill="#141824" stroke={mood.ring} strokeWidth="2" className="buddy-reel" />
        </g>
      </svg>
      {state === "generating" && <span className="buddy-caption">minting…</span>}
    </div>
  );
}
