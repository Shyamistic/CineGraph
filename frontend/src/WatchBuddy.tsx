import { useEffect, useMemo, useRef, useState } from "react";
import { Buddy, type BuddyState } from "./Buddy";
import {
  getBranches,
  getTimeline,
  listForks,
  mintFork,
  type Branch,
  type Fork,
  type LineageSummary,
  type Production,
  type TimelineItem,
} from "./api";

type Props = { prod: Production | null };

export default function WatchBuddy({ prod }: Props) {
  const shots = useMemo(() => prod?.shots ?? [], [prod]);
  const [sceneIdx, setSceneIdx] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const [buddyState, setBuddyState] = useState<BuddyState>("idle");
  const [whisper, setWhisper] = useState("");
  const [branches, setBranches] = useState<Branch[]>([]);
  const [showBranches, setShowBranches] = useState(false);
  const [customWish, setCustomWish] = useState("");
  const [fork, setFork] = useState<Fork | null>(null);
  const [minting, setMinting] = useState(false);
  const [lineage, setLineage] = useState<LineageSummary | null>(null);
  const [timeline, setTimeline] = useState<TimelineItem[]>([]);
  const [captions, setCaptions] = useState(true);
  const [sound, setSound] = useState(true);
  const [castStatus, setCastStatus] = useState("");
  const [err, setErr] = useState("");
  const timer = useRef<number | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [audioDuration, setAudioDuration] = useState(0);

  const atClimax = shots.length > 0 && sceneIdx >= shots.length - 1;
  const current = shots[sceneIdx];
  const currentTiming = timeline.find((item) => item.shot_id === current?.shot_id);
  const duration = Math.max(2.4, audioDuration || ((currentTiming?.end_ms ?? 4000) - (currentTiming?.start_ms ?? 0)) / 1000);
  const progress = Math.min(100, (elapsed / duration) * 100);

  useEffect(() => {
    setSceneIdx(0);
    setElapsed(0);
    setFork(null);
    setShowBranches(false);
    setBranches([]);
    setWhisper("");
    setBuddyState("idle");
    setTimeline([]);
    if (!prod?.id) return;
    getTimeline(prod.id).then((r) => setTimeline(r.items)).catch(() => {});
    listForks(prod.id).then((r) => setLineage(r.lineage)).catch(() => {});
  }, [prod?.id]);

  useEffect(() => {
    if (!playing || shots.length === 0 || fork || (sound && currentTiming?.audio_path)) return;
    timer.current = window.setInterval(() => {
      setElapsed((value) => {
        const next = value + 0.1;
        if (next < duration) return next;
        if (atClimax) {
          window.setTimeout(() => onReachClimax(), 0);
          setPlaying(false);
          return duration;
        }
        setSceneIdx((index) => Math.min(index + 1, shots.length - 1));
        return 0;
      });
    }, 100);
    return () => {
      if (timer.current) window.clearInterval(timer.current);
    };
  }, [playing, sceneIdx, shots.length, duration, atClimax, fork, sound, currentTiming?.audio_path]);

  useEffect(() => {
    setAudioDuration(0);
    setElapsed(0);
  }, [sceneIdx, currentTiming?.audio_path]);

  useEffect(() => {
    if (!sound || !currentTiming?.audio_path || !audioRef.current) return;
    const audio = audioRef.current;
    if (playing) {
      audio.play().catch(() => setSound(false));
    } else {
      audio.pause();
    }
  }, [playing, sound, currentTiming?.audio_path]);

  async function onReachClimax() {
    if (!prod?.id || !current || showBranches) return;
    setBuddyState("thinking");
    setWhisper("This is the turning point. How should the story continue?");
    try {
      const res = await getBranches(prod.id, current.shot_id);
      setBranches(res.branches);
      setShowBranches(true);
      setBuddyState("whispering");
    } catch {
      setBuddyState("idle");
      setErr("The story branches are temporarily unavailable.");
    }
  }

  async function choose(prompt: string, label: string) {
    if (!prod?.id || !current) return;
    setErr("");
    setMinting(true);
    setBuddyState("generating");
    setWhisper(`Creating your version: ${label}`);
    setShowBranches(false);
    try {
      const minted = await mintFork({
        production_id: prod.id,
        shot_id: current.shot_id,
        viewer_prompt: prompt,
        branch_label: label,
        origin: "fan",
      });
      setFork(minted);
      setBuddyState("excited");
      setWhisper(minted.whisper_text || `Here is the story when you choose ${label}.`);
      if (minted.whisper_audio_path && sound) {
        const audio = new Audio(minted.whisper_audio_path);
        audio.play().catch(() => {});
      } else if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(new SpeechSynthesisUtterance(minted.whisper_text || label));
      }
      const r = await listForks(prod.id);
      setLineage(r.lineage);
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Unable to create that branch.");
      setBuddyState("idle");
    } finally {
      setMinting(false);
    }
  }

  function startWatching() {
    setFork(null);
    setSceneIdx(0);
    setElapsed(0);
    setPlaying(true);
    setBuddyState("idle");
    setWhisper("I am right here. I will chime in when the story turns.");
  }

  function togglePlayback() {
    if (playing) {
      setPlaying(false);
    } else if (fork) {
      startWatching();
    } else {
      setPlaying(true);
    }
  }

  function advanceAfterNarration() {
    if (atClimax) {
      setPlaying(false);
      void onReachClimax();
    } else {
      setSceneIdx((index) => Math.min(index + 1, shots.length - 1));
    }
  }

  function showTvRoadmap() {
    setCastStatus("TV handoff is a roadmap preview. This build does not send or inspect media on another app or device.");
  }

  if (!prod || shots.length === 0) {
    return (
      <div className="watch-empty">
        <div className="eyebrow">THE WATCH ROOM</div>
        <Buddy state="idle" size={170} />
        <h2>Your companion is ready</h2>
        <p>Start a production in Studio, then return here to watch it scene by scene and shape a different ending.</p>
      </div>
    );
  }

  return (
    <div className="watch-room">
      <div className="watch-room-head">
        <div>
          <div className="eyebrow">WATCHING WITH BUDDY</div>
          <h1>{prod.title}</h1>
          <p className="watch-sub">{shots.length} scenes · interactive story · {prod.generation_backend}</p>
        </div>
        <div className="watch-actions">
          <button className="soft-button" onClick={showTvRoadmap}>TV roadmap</button>
          <button className={`soft-button ${captions ? "selected" : ""}`} onClick={() => setCaptions((value) => !value)}>
            Captions {captions ? "on" : "off"}
          </button>
        </div>
      </div>

      <div className="watch-grid">
        <section className="cinema-panel">
          <div className="screen-frame">
            {fork ? (
              <figure className="fork-media">
                {fork.media_kind === "video" ? (
                  <video src={fork.media_path} poster={fork.poster_path} autoPlay loop muted controls />
                ) : (
                  <img src={fork.media_path} alt={fork.branch_label} />
                )}
                <figcaption>
                  <span className="media-chip">FAN BRANCH</span>
                  <strong>{fork.branch_label}</strong>
                  <small>Adherence {(fork.vta_score * 100).toFixed(0)}% · {fork.loop_iterations} validation pass{fork.loop_iterations > 1 ? "es" : ""}</small>
                </figcaption>
              </figure>
            ) : current?.media_path ? (
              <img className={`screen-image ${playing ? "screen-playing" : ""}`} src={current.media_path} alt={current.slugline} />
            ) : (
              <div className="screen-placeholder">Generating scene frame</div>
            )}
            <div className="screen-topline">
              <span>SCENE {String(current?.scene_number ?? 0).padStart(2, "0")}</span>
              <span>{playing ? "LIVE WATCH" : fork ? "BRANCH PREVIEW" : "PAUSED"}</span>
            </div>
            <div className="scene-progress"><span style={{ width: `${fork ? 100 : progress}%` }} /></div>
          </div>
          <div className="watch-controls">
            <button className="play-button" onClick={togglePlayback} aria-label={playing ? "Pause watching" : "Play watching"}>
              {playing ? "Pause" : elapsed > 0 ? "Resume" : "Play story"}
            </button>
            <button className="control-button" onClick={() => { setPlaying(false); setSceneIdx((index) => Math.max(0, index - 1)); }}>Previous</button>
            <button className="control-button" onClick={() => { setPlaying(false); setSceneIdx((index) => Math.min(shots.length - 1, index + 1)); }}>Next scene</button>
            <button className={`control-button ${sound ? "active-control" : ""}`} onClick={() => setSound((value) => !value)}>
              Voice {sound ? "on" : "off"}
            </button>
            <span className="control-time">{Math.floor(elapsed)}s / {Math.ceil(duration)}s</span>
          </div>
          <audio
            ref={audioRef}
            src={sound ? currentTiming?.audio_path : undefined}
            onLoadedMetadata={(event) => setAudioDuration(Number.isFinite(event.currentTarget.duration) ? event.currentTarget.duration : 0)}
            onTimeUpdate={(event) => setElapsed(event.currentTarget.currentTime)}
            onEnded={advanceAfterNarration}
            hidden
          />
          {captions && !fork && currentTiming && (
            <div className="caption-card">
              <span>{currentTiming.slugline}</span>
              <strong>{currentTiming.narration}</strong>
            </div>
          )}
        </section>

        <aside className="buddy-panel">
          <div className="buddy-panel-label">YOUR WATCH BUDDY</div>
          <Buddy state={buddyState} size={185} />
          <div className={`buddy-message ${buddyState}`}>{whisper || "Press play and I will watch with you."}</div>
          {showBranches && (
            <div className="branch-list">
              <div className="branch-heading">Choose the next beat</div>
              {branches.map((branch) => (
                <button key={branch.label} disabled={minting} onClick={() => choose(branch.prompt, branch.label)}>
                  <strong>{branch.label}</strong>
                  <span>{branch.prompt}</span>
                </button>
              ))}
              <div className="custom-branch">
                <input
                  placeholder="Describe your own ending"
                  value={customWish}
                  onChange={(event) => setCustomWish(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter" && customWish.trim()) choose(customWish.trim(), customWish.trim().slice(0, 28));
                  }}
                />
              </div>
            </div>
          )}
          {fork && <button className="watch-again" onClick={startWatching}>Watch the canonical cut again</button>}
          {castStatus && <p className="cast-status">{castStatus}</p>}
        </aside>
      </div>

      <div className="watch-footer">
        <div className="scene-strip">
          {shots.map((shot, index) => (
            <button
              key={shot.shot_id}
              className={index === sceneIdx && !fork ? "current-scene" : index < sceneIdx || fork ? "seen-scene" : ""}
              onClick={() => { setFork(null); setSceneIdx(index); setElapsed(0); setPlaying(false); }}
              title={shot.slugline}
            >
              <span>{String(shot.scene_number).padStart(2, "0")}</span>
              <small>{shot.slugline.replace(/^(INT\.|EXT\.|INT\/EXT\.)\s*/i, "").slice(0, 22)}</small>
            </button>
          ))}
        </div>
        <div className="watch-meta">
          <strong>{fork ? `Branch: ${fork.branch_label}` : current?.slugline}</strong>
          <span>{fork ? fork.attribution : current?.action}</span>
          {err && <span className="error-text">{err}</span>}
          {lineage && <small>Provenance ledger · {lineage.total_forks} fan branch{lineage.total_forks === 1 ? "" : "es"} · average adherence {(lineage.avg_vta * 100).toFixed(0)}%</small>}
        </div>
      </div>
    </div>
  );
}