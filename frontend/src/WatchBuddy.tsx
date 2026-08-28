/**
 * Watch Buddy — the couch-side watch-along surface.
 *
 * A viewer "watches" a CineGraph production as a sequence of scenes. At the
 * climax the buddy leans in and whispers "three ways this can end". The viewer
 * taps a branch (or types their own), and an alternate ending is minted live
 * through the same deterministic adherence loop the studio pipeline uses —
 * watermarked and logged to the ClickHouse provenance ledger.
 *
 * The rule this UI keeps visible: the buddy is how a human asks; CineGraph is
 * what actually executes.
 */

import { useEffect, useMemo, useRef, useState } from "react";
import { Buddy, type BuddyState } from "./Buddy";
import {
  getBranches,
  listForks,
  mintFork,
  type Branch,
  type Fork,
  type LineageSummary,
  type Production,
} from "./api";

type Props = { prod: Production | null };

export default function WatchBuddy({ prod }: Props) {
  const shots = useMemo(() => prod?.shots ?? [], [prod]);
  const [sceneIdx, setSceneIdx] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [buddyState, setBuddyState] = useState<BuddyState>("idle");
  const [whisper, setWhisper] = useState<string>("");
  const [branches, setBranches] = useState<Branch[]>([]);
  const [showBranches, setShowBranches] = useState(false);
  const [customWish, setCustomWish] = useState("");
  const [fork, setFork] = useState<Fork | null>(null);
  const [minting, setMinting] = useState(false);
  const [lineage, setLineage] = useState<LineageSummary | null>(null);
  const [err, setErr] = useState("");
  const timer = useRef<number | null>(null);

  const atClimax = shots.length > 0 && sceneIdx >= shots.length - 1;
  const current = shots[sceneIdx];

  // Reset when a new production loads.
  useEffect(() => {
    setSceneIdx(0);
    setFork(null);
    setShowBranches(false);
    setBranches([]);
    setWhisper("");
    setBuddyState("idle");
    if (prod?.id) listForks(prod.id).then((r) => setLineage(r.lineage)).catch(() => {});
  }, [prod?.id]);

  // Scene auto-advance while "playing".
  useEffect(() => {
    if (!playing || shots.length === 0) return;
    if (atClimax) {
      setPlaying(false);
      onReachClimax();
      return;
    }
    timer.current = window.setTimeout(() => setSceneIdx((i) => Math.min(i + 1, shots.length - 1)), 2600);
    return () => {
      if (timer.current) window.clearTimeout(timer.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playing, sceneIdx, shots.length]);

  async function onReachClimax() {
    if (!prod?.id || !current) return;
    setBuddyState("thinking");
    setWhisper("Hold on — this is where it turns. Three ways this can end…");
    try {
      const res = await getBranches(prod.id, current.shot_id);
      setBranches(res.branches);
      setShowBranches(true);
      setBuddyState("whispering");
    } catch {
      setBuddyState("idle");
    }
  }

  async function choose(prompt: string, label: string) {
    if (!prod?.id) return;
    setErr("");
    setMinting(true);
    setBuddyState("generating");
    setWhisper(`Minting your ending: "${label}"…`);
    setShowBranches(false);
    try {
      const minted = await mintFork({
        production_id: prod.id,
        shot_id: current?.shot_id,
        viewer_prompt: prompt,
        branch_label: label,
        origin: "fan",
      });
      setFork(minted);
      setBuddyState("excited");
      setWhisper(minted.whisper_text || `Here's how it ends when "${label}".`);
      // The buddy speaks the ending aloud (Hindi by default).
      if (minted.whisper_audio_path) {
        const audio = new Audio(minted.whisper_audio_path);
        audio.play().catch(() => {
          /* autoplay may be blocked until user gesture; caption still shows */
        });
      }
      const r = await listForks(prod.id);
      setLineage(r.lineage);
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Mint failed");
      setBuddyState("idle");
    } finally {
      setMinting(false);
    }
  }

  function startWatching() {
    setFork(null);
    setSceneIdx(0);
    setPlaying(true);
    setBuddyState("idle");
    setWhisper("Enjoy the show. I'll chime in if something interesting comes up.");
  }

  if (!prod || shots.length === 0) {
    return (
      <div className="wb-empty">
        <Buddy state="idle" size={140} />
        <h2>Your buddy is ready</h2>
        <p>Mint a production in the Studio tab, then come back to watch it together and fork the ending.</p>
      </div>
    );
  }

  return (
    <div className="wb">
      <div className="wb-stage">
        {/* The screen */}
        <div className="wb-screen">
          {fork ? (
            <figure className="wb-fork">
              {fork.media_kind === "video" ? (
                <video src={fork.media_path} poster={fork.poster_path} autoPlay loop muted controls />
              ) : (
                <img src={fork.media_path} alt={fork.branch_label} />
              )}
              <figcaption>
                <span className="wb-tag">FAN EDIT</span>
                <b>"{fork.branch_label}"</b>
                <em>
                  adherence {(fork.vta_score * 100).toFixed(0)}% · {fork.loop_iterations} loop
                  {fork.loop_iterations > 1 ? "s" : ""} · {fork.generation_backend}
                </em>
                {fork.whisper_text && (
                  <p className="wb-narration">
                    🔊 {fork.whisper_text}
                    {fork.whisper_lang && <span className="wb-lang"> · {fork.whisper_lang.toUpperCase()}</span>}
                  </p>
                )}
                <small>{fork.attribution}</small>
              </figcaption>
            </figure>
          ) : current?.media_path ? (
            <img className={`wb-frame ${playing ? "playing" : ""}`} src={current.media_path} alt={current.slugline} />
          ) : (
            <div className="wb-frame ph" />
          )}

          {/* scene ticker */}
          <div className="wb-ticker">
            {shots.map((s, i) => (
              <span
                key={s.shot_id}
                className={i === sceneIdx && !fork ? "on" : i < sceneIdx || fork ? "seen" : ""}
                title={s.slugline}
              />
            ))}
          </div>
        </div>

        {/* Buddy + whisper */}
        <div className="wb-side">
          <Buddy state={buddyState} size={132} />
          {whisper && <div className={`wb-whisper ${buddyState}`}>{whisper}</div>}

          {!playing && !showBranches && !fork && (
            <button className="wb-play" onClick={startWatching}>
              ▶ Watch with buddy
            </button>
          )}

          {showBranches && (
            <div className="wb-branches">
              {branches.map((b) => (
                <button key={b.label} disabled={minting} onClick={() => choose(b.prompt, b.label)}>
                  <b>{b.label}</b>
                  <span>{b.prompt}</span>
                </button>
              ))}
              <div className="wb-custom">
                <input
                  placeholder="…or type your own ending"
                  value={customWish}
                  onChange={(e) => setCustomWish(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && customWish.trim()) choose(customWish.trim(), customWish.trim().slice(0, 28));
                  }}
                />
              </div>
            </div>
          )}

          {fork && (
            <button className="wb-play" onClick={startWatching}>
              ↺ Watch again
            </button>
          )}
        </div>
      </div>

      {/* Now-playing caption */}
      <div className="wb-meta">
        {!fork && current && (
          <>
            <strong>
              SC {String(current.scene_number).padStart(2, "0")} · {current.slugline}
            </strong>
            <span>{current.action?.slice(0, 140)}</span>
          </>
        )}
        {err && <span className="wb-err">{err}</span>}
        {lineage && (
          <div className="wb-lineage" title="ClickHouse provenance ledger">
            ledger · {lineage.total_forks} forks · {lineage.fan_forks} fan · {lineage.watermarked_forks} watermarked · avg
            adherence {(lineage.avg_vta * 100).toFixed(0)}%
          </div>
        )}
      </div>
    </div>
  );
}
