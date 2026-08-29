import { useEffect, useMemo, useRef, useState } from "react";
import { Buddy, type BuddyState } from "./Buddy";
import {
  getBranches,
  getCastMedia,
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
type CastConnection = { context: any; player: any; controller: any };

declare global {
  interface Window {
    __watchBuddyCastApiAvailable?: boolean;
    cast?: any;
    chrome: any;
  }
}

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
  const [castReady, setCastReady] = useState(false);
  const [castConnected, setCastConnected] = useState(false);
  const [castLoaded, setCastLoaded] = useState(false);
  const [castVerified, setCastVerified] = useState(false);
  const [castLoading, setCastLoading] = useState(false);
  const [err, setErr] = useState("");
  const timer = useRef<number | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const forkVideoRef = useRef<HTMLVideoElement | null>(null);
  const [audioDuration, setAudioDuration] = useState(0);
  const castRef = useRef<CastConnection | null>(null);
  const prodRef = useRef(prod);
  const playbackRef = useRef({ sceneIdx, playing, elapsed, fork });
  const lastCastPlayerState = useRef("");
  const lastRemoteTime = useRef(0);
  const remoteWasPlaying = useRef(false);
  const hadCastConnection = useRef(false);
  const castLoadSequence = useRef(0);
  const castLoadQueue = useRef<Promise<unknown>>(Promise.resolve());
  const onReachClimaxRef = useRef<(() => void) | null>(null);

  const atClimax = shots.length > 0 && sceneIdx >= shots.length - 1;
  const current = shots[sceneIdx];
  const currentTiming = timeline.find((item) => item.shot_id === current?.shot_id);
  const duration = Math.max(2.4, audioDuration || ((currentTiming?.end_ms ?? 4000) - (currentTiming?.start_ms ?? 0)) / 1000);
  const progress = Math.min(100, (elapsed / duration) * 100);

  useEffect(() => {
    prodRef.current = prod;
    playbackRef.current = { sceneIdx, playing, elapsed, fork };
  }, [prod, sceneIdx, playing, elapsed, fork]);

  useEffect(() => {
    const onCastReady = (event: Event) => {
      if ((event as CustomEvent<boolean>).detail) setCastReady(true);
    };
    window.addEventListener("watch-buddy-cast-ready", onCastReady);
    if (window.__watchBuddyCastApiAvailable && window.cast?.framework) setCastReady(true);
    return () => window.removeEventListener("watch-buddy-cast-ready", onCastReady);
  }, []);

  useEffect(() => {
    if (!castReady || !window.cast?.framework || !window.chrome?.cast) return;
    const framework = window.cast.framework;
    const context = framework.CastContext.getInstance();
    const player = new framework.RemotePlayer();
    const controller = new framework.RemotePlayerController(player);
    castRef.current = { context, player, controller };
    context.setOptions({
      receiverApplicationId: window.chrome.cast.media.DEFAULT_MEDIA_RECEIVER_APP_ID,
      autoJoinPolicy: window.chrome.cast.AutoJoinPolicy.ORIGIN_SCOPED,
    });

    const syncRemoteState = () => {
      const connected = Boolean(player.isConnected);
      setCastConnected(connected);
      if (!connected) {
        setCastLoaded(false);
        setCastVerified(false);
        if (!hadCastConnection.current) return;
        hadCastConnection.current = false;
        const resumeAt = lastRemoteTime.current;
        if (playbackRef.current.fork && forkVideoRef.current) {
          forkVideoRef.current.currentTime = Math.min(
            resumeAt,
            Number.isFinite(forkVideoRef.current.duration) ? forkVideoRef.current.duration : resumeAt,
          );
        } else if (audioRef.current) {
          audioRef.current.currentTime = Math.min(
            resumeAt,
            Number.isFinite(audioRef.current.duration) ? audioRef.current.duration : resumeAt,
          );
        }
        setElapsed(resumeAt);
        setPlaying(remoteWasPlaying.current);
        setCastStatus(
          remoteWasPlaying.current
            ? "TV disconnected. Continuing this CineGraph scene in the Watch Room."
            : "TV disconnected. This CineGraph scene is paused in the Watch Room.",
        );
        return;
      }
      hadCastConnection.current = true;
      if (player.isMediaLoaded) {
        setCastLoaded(true);
        if (Number.isFinite(player.currentTime)) {
          lastRemoteTime.current = Math.max(0, player.currentTime);
          setElapsed(lastRemoteTime.current);
        }
        if (player.playerState === "PLAYING") {
          remoteWasPlaying.current = true;
          setPlaying(true);
        }
        if (player.playerState === "PAUSED") {
          remoteWasPlaying.current = false;
          setPlaying(false);
        }
      }
    };
    const onPlayerStateChanged = () => {
      const state = player.playerState || "";
      const previous = lastCastPlayerState.current;
      lastCastPlayerState.current = state;
      syncRemoteState();
      if (previous === "PLAYING" && state === "IDLE" && (!player.idleReason || player.idleReason === "FINISHED")) {
        handleCastMediaFinished();
      }
    };
    const onSessionChanged = () => {
      syncRemoteState();
    };
    const remoteEvents = framework.RemotePlayerEventType || {};
    const contextEvents = framework.CastContextEventType || {};
    controller.addEventListener(remoteEvents.IS_CONNECTED_CHANGED || "IS_CONNECTED_CHANGED", syncRemoteState);
    controller.addEventListener(remoteEvents.IS_MEDIA_LOADED_CHANGED || "IS_MEDIA_LOADED_CHANGED", syncRemoteState);
    controller.addEventListener(remoteEvents.CURRENT_TIME_CHANGED || "CURRENT_TIME_CHANGED", syncRemoteState);
    controller.addEventListener(remoteEvents.PLAYER_STATE_CHANGED || "PLAYER_STATE_CHANGED", onPlayerStateChanged);
    context.addEventListener(contextEvents.SESSION_STATE_CHANGED || "SESSION_STATE_CHANGED", onSessionChanged);
    syncRemoteState();

    return () => {
      controller.removeEventListener(remoteEvents.IS_CONNECTED_CHANGED || "IS_CONNECTED_CHANGED", syncRemoteState);
      controller.removeEventListener(remoteEvents.IS_MEDIA_LOADED_CHANGED || "IS_MEDIA_LOADED_CHANGED", syncRemoteState);
      controller.removeEventListener(remoteEvents.CURRENT_TIME_CHANGED || "CURRENT_TIME_CHANGED", syncRemoteState);
      controller.removeEventListener(remoteEvents.PLAYER_STATE_CHANGED || "PLAYER_STATE_CHANGED", onPlayerStateChanged);
      context.removeEventListener(contextEvents.SESSION_STATE_CHANGED || "SESSION_STATE_CHANGED", onSessionChanged);
      castRef.current = null;
    };
  }, [castReady]);

  useEffect(() => {
    setSceneIdx(0);
    setElapsed(0);
    setFork(null);
    setShowBranches(false);
    setBranches([]);
    setWhisper("");
    setBuddyState("idle");
    setTimeline([]);
    setCastVerified(false);
    if (!prod?.id) return;
    getTimeline(prod.id).then((r) => setTimeline(r.items)).catch(() => {});
    listForks(prod.id).then((r) => setLineage(r.lineage)).catch(() => {});
  }, [prod?.id]);

  useEffect(() => {
    if (!playing || castConnected || shots.length === 0 || fork || (sound && currentTiming?.audio_path)) return;
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
  }, [playing, castConnected, shots.length, duration, atClimax, fork, sound, currentTiming?.audio_path]);

  useEffect(() => {
    setAudioDuration(0);
    setElapsed(0);
  }, [sceneIdx, currentTiming?.audio_path]);

  useEffect(() => {
    if (castConnected || !sound || !currentTiming?.audio_path || !audioRef.current) return;
    const audio = audioRef.current;
    if (playing) {
      audio.play().catch(() => setSound(false));
    } else {
      audio.pause();
    }
  }, [playing, castConnected, sound, currentTiming?.audio_path]);

  useEffect(() => {
    const video = forkVideoRef.current;
    if (!video) return;
    if (castConnected || !playing) {
      video.pause();
    } else {
      video.play().catch(() => {});
    }
  }, [castConnected, playing, fork?.fork_id]);

  function loadCastMedia(shotId?: string, forkId?: string, autoplay = true, startAt = 0): Promise<boolean> {
    const requestSequence = ++castLoadSequence.current;
    setCastVerified(false);
    const queuedLoad = castLoadQueue.current.then(
      () => performCastMediaLoad(requestSequence, shotId, forkId, autoplay, startAt),
      () => performCastMediaLoad(requestSequence, shotId, forkId, autoplay, startAt),
    );
    castLoadQueue.current = queuedLoad;
    return queuedLoad;
  }

  async function performCastMediaLoad(requestSequence: number, shotId?: string, forkId?: string, autoplay = true, startAt = 0) {
    const connection = castRef.current;
    const production = prodRef.current;
    if (!connection || !production?.id) return false;
    const session = connection.context.getCastSession();
    if (!session) return false;
    setCastLoading(true);
    setCastStatus("Loading CineGraph media on Google TV…");
    try {
      const item = await getCastMedia(production.id, shotId, forkId);
      if (requestSequence !== castLoadSequence.current) return false;
      const mediaInfo = new window.chrome.cast.media.MediaInfo(
        new URL(item.media_url, window.location.origin).toString(),
        item.content_type,
      );
      const metadata = new window.chrome.cast.media.GenericMediaMetadata();
      metadata.title = item.title;
      metadata.subtitle = `${item.source_label} · Scene ${String(item.scene_number).padStart(2, "0")}`;
      metadata.artist = item.attribution;
      if (item.visual_url) {
        metadata.images = [new window.chrome.cast.Image(new URL(item.visual_url, window.location.origin).toString())];
      }
      mediaInfo.metadata = metadata;
      if (item.duration_ms > 0) mediaInfo.duration = item.duration_ms / 1000;
      if (item.media_kind !== "image") {
        mediaInfo.streamType = window.chrome.cast.media.StreamType.BUFFERED;
      }
      const request = new window.chrome.cast.media.LoadRequest(mediaInfo);
      request.autoplay = autoplay;
      request.currentTime = Math.max(0, startAt);
      const loaded = await session.loadMedia(request);
      if (loaded === false) throw new Error("The receiver rejected this CineGraph media item.");
      if (requestSequence !== castLoadSequence.current) return false;
      setCastLoaded(true);
      setCastVerified(true);
      setCastConnected(true);
      setPlaying(autoplay);
      setCastStatus(`${item.source_label} · ${autoplay ? "playing" : "paused"} on Google TV. CineGraph media only; third-party apps are not inspected.`);
      return true;
    } catch (error) {
      setCastLoaded(false);
      setCastVerified(false);
      setCastStatus(error instanceof Error ? error.message : "Unable to load CineGraph media on Google TV.");
      return false;
    } finally {
      if (requestSequence === castLoadSequence.current) setCastLoading(false);
    }
  }

  function handleCastMediaFinished() {
    const production = prodRef.current;
    const state = playbackRef.current;
    if (!production || state.fork) {
      setPlaying(false);
      setCastLoaded(false);
      setCastVerified(false);
      return;
    }
    const nextIndex = state.sceneIdx + 1;
    if (nextIndex < production.shots.length) {
      const nextShot = production.shots[nextIndex];
      setSceneIdx(nextIndex);
      setElapsed(0);
      setPlaying(true);
      void loadCastMedia(nextShot.shot_id, undefined, true, 0);
    } else {
      setPlaying(false);
      setCastLoaded(false);
      setCastVerified(false);
      onReachClimaxRef.current?.();
    }
  }

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
      setPlaying(true);
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
      if (castConnected) void loadCastMedia(undefined, minted.fork_id, true, 0);
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Unable to create that branch.");
      setBuddyState("idle");
    } finally {
      setMinting(false);
    }
  }

  function selectScene(index: number) {
    const nextIndex = Math.max(0, Math.min(shots.length - 1, index));
    const autoplay = castConnected && playing;
    setFork(null);
    setSceneIdx(nextIndex);
    setElapsed(0);
    setPlaying(autoplay);
    if (castConnected && shots[nextIndex]) {
      void loadCastMedia(shots[nextIndex].shot_id, undefined, autoplay, 0);
    }
  }

  function startWatching() {
    setFork(null);
    setSceneIdx(0);
    setElapsed(0);
    setPlaying(true);
    setBuddyState("idle");
    setWhisper("I am right here. I will chime in when the story turns.");
    if (castConnected && prod?.shots[0]) void loadCastMedia(prod.shots[0].shot_id, undefined, true, 0);
  }

  function togglePlayback() {
    if (castConnected && castLoaded && castRef.current) {
      castRef.current.controller.playOrPause();
      return;
    }
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
    if (!castReady) {
      setCastStatus("TV handoff is a roadmap preview until the Cast sender is available. CineGraph never inspects third-party apps.");
      return;
    }
    const context = castRef.current?.context;
    if (!context) return;
    setCastStatus("Choose a Google TV receiver for this CineGraph story.");
    void (async () => {
      try {
        if (!context.getCastSession()) await context.requestSession();
        const state = playbackRef.current;
        await loadCastMedia(
          state.fork?.fork_id ? undefined : prod?.shots[state.sceneIdx]?.shot_id,
          state.fork?.fork_id,
          state.playing,
          state.elapsed,
        );
      } catch (error) {
        setCastStatus(error instanceof Error ? error.message : "Google TV connection was cancelled.");
      }
    })();
  }

  onReachClimaxRef.current = onReachClimax;

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
          <button className="soft-button" onClick={showTvRoadmap} disabled={castLoading}>
            {castConnected ? (castVerified ? "Google TV media verified" : "Google TV connected") : castReady ? "Continue on Google TV" : "TV roadmap"}
          </button>
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
                  <video ref={forkVideoRef} src={fork.media_path} poster={fork.poster_path} autoPlay={!castConnected} loop={!castConnected} muted controls />
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
            <button className="control-button" onClick={() => selectScene(Math.max(0, sceneIdx - 1))}>Previous</button>
            <button className="control-button" onClick={() => selectScene(Math.min(shots.length - 1, sceneIdx + 1))}>Next scene</button>
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
              onClick={() => selectScene(index)}
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