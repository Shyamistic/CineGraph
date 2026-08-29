import { useEffect, useMemo, useState, type FormEvent } from "react";
import WatchBuddy from "./WatchBuddy";
import {
  getHealth,
  getProduction,
  getSample,
  listProductions,
  searchAssets,
  startProduction,
  type Health,
  type Production,
} from "./api";

type Role = "director" | "fan";
type View = "home" | "watch" | "studio" | "discover" | "profile";
type StudioTab = "board" | "maven" | "library" | "qc" | "dub" | "nle" | "trace";
type Session = { name: string; email: string; role: Role };

const SESSION_KEY = "watch-buddy-session";
const PHASES = [
  { id: "director", label: "Director", role: "MAVEN" },
  { id: "producer", label: "Producer", role: "DSG loop" },
  { id: "studio_head", label: "Studio", role: "ClickHouse" },
  { id: "editorial", label: "Editorial", role: "NLE" },
  { id: "qc", label: "QC", role: "EBU / Netflix" },
  { id: "localization", label: "Localization", role: "EN → IN" },
  { id: "complete", label: "Observability", role: "OTel" },
];

function readSession(): Session | null {
  const demoRole = new URLSearchParams(window.location.search).get("demo");
  if (demoRole === "director" || demoRole === "fan") {
    return {
      name: demoRole === "director" ? "Ava Director" : "Arjun Fan",
      email: `${demoRole}@watchbuddy.demo`,
      role: demoRole,
    };
  }
  try {
    const value = window.localStorage.getItem(SESSION_KEY);
    return value ? JSON.parse(value) : null;
  } catch {
    return null;
  }
}

function AuthPage({ onEnter }: { onEnter: (session: Session) => void }) {
  const [role, setRole] = useState<Role>("director");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  function submit(event: FormEvent) {
    event.preventDefault();
    const session = {
      name: name.trim() || (role === "director" ? "Ava Director" : "Arjun Fan"),
      email: email.trim() || `${role}@watchbuddy.demo`,
      role,
    };
    window.localStorage.setItem(SESSION_KEY, JSON.stringify(session));
    onEnter(session);
  }

  return (
    <div className="auth-page">
      <div className="auth-glow auth-glow-one" />
      <div className="auth-glow auth-glow-two" />
      <div className="auth-brand">
        <span className="brand-mark">W</span>
        <span>WATCH BUDDY</span>
      </div>
      <main className="auth-card">
        <div className="eyebrow">A NEW KIND OF WATCHING</div>
        <h1>Stories that watch back.</h1>
        <p className="auth-copy">Create a world, invite your audience in, and let every viewer leave a fingerprint on the ending.</p>
        <form onSubmit={submit}>
          <div className="role-picker" aria-label="Choose your experience">
            <button type="button" className={role === "director" ? "role-option active" : "role-option"} onClick={() => setRole("director")}>
              <span className="role-icon">D</span>
              <span><strong>Director</strong><small>Build cinematic worlds</small></span>
            </button>
            <button type="button" className={role === "fan" ? "role-option active" : "role-option"} onClick={() => setRole("fan")}>
              <span className="role-icon">F</span>
              <span><strong>Fan</strong><small>Watch beyond the frame</small></span>
            </button>
          </div>
          <label htmlFor="name">Your name</label>
          <input id="name" value={name} onChange={(event) => setName(event.target.value)} placeholder={role === "director" ? "Ava Director" : "Arjun Fan"} />
          <label htmlFor="email">Email address</label>
          <input id="email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder={`${role}@watchbuddy.demo`} />
          <button className="primary-button auth-submit" type="submit">Enter Watch Buddy <span>→</span></button>
        </form>
        <p className="auth-note">Demo access · no password required</p>
      </main>
      <div className="auth-proof">
        <span>Powered by Gemini</span>
        <i />
        <span>Built for Agentic Cinema</span>
      </div>
    </div>
  );
}

export default function App() {
  const [session, setSession] = useState<Session | null>(() => readSession());
  const [health, setHealth] = useState<Health | null>(null);
  const [title, setTitle] = useState("The Last Reel");
  const [script, setScript] = useState("");
  const [lang, setLang] = useState("hi");
  const [shotsN, setShotsN] = useState(4);
  const [prod, setProd] = useState<Production | null>(null);
  const [productions, setProductions] = useState<Production[]>([]);
  const [view, setView] = useState<View>(() => readSession()?.role === "fan" ? "watch" : "home");
  const [studioTab, setStudioTab] = useState<StudioTab>("board");
  const [busy, setBusy] = useState(false);
  const [query, setQuery] = useState("high-contrast lighting tracking shot");
  const [hits, setHits] = useState<Record<string, unknown>[]>([]);
  const [err, setErr] = useState("");
  const [notice, setNotice] = useState("");
  const [mobileNavOpen, setMobileNavOpen] = useState(false);

  useEffect(() => {
    getHealth().then(setHealth).catch(() => setHealth(null));
    getSample().then((sample) => {
      setTitle(sample.title);
      setScript(sample.script);
    }).catch(() => {});
    listProductions().then(setProductions).catch(() => {});
  }, []);

  useEffect(() => {
    if (!prod?.id || prod.status === "complete" || prod.status === "failed") return;
    const timer = window.setInterval(async () => {
      try {
        const next = await getProduction(prod.id);
        setProd(next);
        setProductions((items) => items.some((item) => item.id === next.id) ? items.map((item) => item.id === next.id ? next : item) : [next, ...items]);
      } catch {
        // Keep the last known state visible while a job is running.
      }
    }, 800);
    return () => window.clearInterval(timer);
  }, [prod?.id, prod?.status]);

  const phaseIndex = useMemo(() => {
    const index = PHASES.findIndex((phase) => phase.id === prod?.phase);
    return index < 0 ? (prod?.status === "complete" ? PHASES.length - 1 : -1) : index;
  }, [prod]);

  async function run() {
    setErr("");
    setNotice("");
    setBusy(true);
    try {
      const created = await startProduction({ title, script, target_lang: lang, max_shots: shotsN });
      setProd(created);
      setProductions((items) => [created, ...items.filter((item) => item.id !== created.id)]);
      setView(session?.role === "fan" ? "watch" : "studio");
      setStudioTab("board");
      setNotice("Your production is now moving through the agent crew.");
    } catch (error) {
      setErr(error instanceof Error ? error.message : "Unable to start production");
    } finally {
      setBusy(false);
    }
  }

  async function runSearch() {
    try {
      const result = await searchAssets(query, prod?.id);
      setHits(result.hits);
      setStudioTab("library");
    } catch {
      setErr("Semantic search is unavailable while the asset index is offline.");
    }
  }

  function signOut() {
    window.localStorage.removeItem(SESSION_KEY);
    setSession(null);
  }

  function chooseProduction(item: Production) {
    setProd(item);
    setView("watch");
  }

  if (!session) return <AuthPage onEnter={setSession} />;

  const isDirector = session.role === "director";
  const navItems: { id: View; label: string; meta: string }[] = [
    { id: "home", label: "Overview", meta: "01" },
    { id: "watch", label: "Watch room", meta: "02" },
    ...(isDirector ? [{ id: "studio" as View, label: "Director studio", meta: "03" }] : []),
    { id: "discover", label: "Discover", meta: "04" },
    { id: "profile", label: "My profile", meta: "05" },
  ];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <span className="brand-mark">W</span>
          <div><strong>WATCH BUDDY</strong><small>Stories that watch back</small></div>
        </div>
        <button
          className="mobile-nav-toggle"
          type="button"
          aria-label="Toggle navigation"
          aria-expanded={mobileNavOpen}
          onClick={() => setMobileNavOpen((open) => !open)}
        >
          {mobileNavOpen ? "Close" : "Menu"}
        </button>
        <div className="sidebar-profile">
          <span className={`avatar ${session.role}`}>{session.name.slice(0, 1).toUpperCase()}</span>
          <div><strong>{session.name}</strong><small>{isDirector ? "Director account" : "Fan account"}</small></div>
          <span className="online-dot" />
        </div>
        <nav className={`main-nav ${mobileNavOpen ? "open" : ""}`} aria-label="Main navigation">
          <span className="nav-heading">Workspace</span>
          {navItems.map((item) => (
            <button key={item.id} className={view === item.id ? "nav-item active" : "nav-item"} onClick={() => { setView(item.id); setMobileNavOpen(false); }}>
              <span className="nav-index">{item.meta}</span>{item.label}<span className="nav-arrow">↗</span>
            </button>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="service-mini"><span className={health?.gemini ? "status-dot good" : "status-dot"} /><span>Gemini engine</span><small>{health?.gemini ? "LIVE" : "DEMO"}</small></div>
          <div className="service-mini"><span className={health?.clickhouse?.connected ? "status-dot good" : "status-dot"} /><span>Asset ledger</span><small>{health?.clickhouse?.connected ? "LIVE" : "LOCAL"}</small></div>
          <button className="sign-out" onClick={signOut}>Sign out <span>⌁</span></button>
        </div>
      </aside>

      <main className="content">
        <header className="topbar">
          <div className="breadcrumb"><span>WATCH BUDDY</span><b>/</b><strong>{view === "home" ? "Overview" : navItems.find((item) => item.id === view)?.label}</strong></div>
          <div className="topbar-actions">
            <span className="build-label">BUILD 0.4 · AGENTIC CINEMA</span>
            <button className="icon-button" onClick={() => setView("profile")} aria-label="Open profile">◎</button>
          </div>
        </header>

        {notice && <button className="toast" onClick={() => setNotice("")}>{notice}<span>×</span></button>}
        {view === "home" && (
          <HomeView session={session} prod={prod} productions={productions} health={health} onStart={() => setView(isDirector ? "studio" : "watch")} onDemo={run} onChoose={chooseProduction} />
        )}
        {view === "watch" && <WatchBuddy prod={prod} />}
        {view === "discover" && <DiscoverView productions={productions} onChoose={chooseProduction} />}
        {view === "profile" && <ProfileView session={session} health={health} onRoleSwitch={(role) => {
          const next = { ...session, role };
          window.localStorage.setItem(SESSION_KEY, JSON.stringify(next));
          setSession(next);
          setView(role === "director" ? "home" : "watch");
        }} />}
        {view === "studio" && isDirector && (
          <StudioView
            title={title}
            setTitle={setTitle}
            script={script}
            setScript={setScript}
            lang={lang}
            setLang={setLang}
            shotsN={shotsN}
            setShotsN={setShotsN}
            prod={prod}
            phaseIndex={phaseIndex}
            busy={busy}
            err={err}
            run={run}
            studioTab={studioTab}
            setStudioTab={setStudioTab}
            query={query}
            setQuery={setQuery}
            runSearch={runSearch}
            hits={hits}
          />
        )}
      </main>
    </div>
  );
}

function HomeView({ session, prod, productions, health, onStart, onDemo, onChoose }: {
  session: Session;
  prod: Production | null;
  productions: Production[];
  health: Health | null;
  onStart: () => void;
  onDemo: () => void;
  onChoose: (production: Production) => void;
}) {
  const isDirector = session.role === "director";
  return (
    <div className="overview-page">
      <section className="welcome-hero">
        <div className="hero-copy">
          <div className="eyebrow">{isDirector ? "DIRECTOR CONTROL ROOM" : "YOUR PRIVATE WATCH ROOM"}</div>
          <h1>{isDirector ? <>Make a world.<br /><em>Let it move.</em></> : <>Tonight, watch<br /><em>something alive.</em></>}</h1>
          <p>{isDirector ? "A cinematic production system where every frame is understood, tested, and ready to become interactive." : "A story is more fun when your companion remembers the details and leaves room for your choices."}</p>
          <div className="hero-actions">
            <button className="primary-button" onClick={onStart}>{isDirector ? "Open director studio" : "Enter watch room"} <span>→</span></button>
            <button className="text-button" onClick={onDemo}>Try the demo story <span>↗</span></button>
          </div>
        </div>
        <div className="hero-orbit">
          <div className="orbit orbit-one" /><div className="orbit orbit-two" />
          <div className="hero-buddy"><BuddyGlyph /></div>
          <div className="orbit-label label-top">SCENE AWARE</div>
          <div className="orbit-label label-bottom">ALWAYS WITH YOU</div>
        </div>
      </section>
      <section className="stat-row">
        <div><span>Active productions</span><strong>{productions.length.toString().padStart(2, "0")}</strong><small>{productions.length ? "Ready to continue" : "Start your first story"}</small></div>
        <div><span>Agent crew</span><strong>07</strong><small>Specialists working in sync</small></div>
        <div><span>Engine status</span><strong className="stat-live">{health?.gemini ? "LIVE" : "DEMO"}</strong><small>{health?.clickhouse?.connected ? "Cloud services connected" : "Local fallback active"}</small></div>
        <div><span>Latest milestone</span><strong>{prod?.status === "complete" ? "100%" : prod ? `${Math.round(prod.progress * 100)}%` : "—"}</strong><small>{prod ? prod.phase : "No story in progress"}</small></div>
      </section>
      {prod && (
        <section className="continue-card">
          <div className="section-kicker">CONTINUE YOUR STORY</div>
          <div className="continue-content"><div><h2>{prod.title}</h2><p>{prod.status === "complete" ? "Your production is ready for the watch room." : "Your agent crew is still shaping the film."}</p></div><button className="soft-button" onClick={() => onChoose(prod)}>Open production <span>→</span></button></div>
          <div className="mini-progress"><span style={{ width: `${Math.max(5, prod.progress * 100)}%` }} /></div>
        </section>
      )}
      <section className="principles">
        <div className="section-kicker">THE WATCH BUDDY PROMISE</div>
        <div className="principle-grid"><div><b>01</b><strong>It sees the story</strong><p>Scene-aware context makes every nudge feel earned, not random.</p></div><div><b>02</b><strong>It respects the cut</strong><p>Every fan branch is labeled, scored, watermarked, and traceable.</p></div><div><b>03</b><strong>It speaks your language</strong><p>English, Hindi, Tamil, and Telugu are first-class ways to watch.</p></div></div>
      </section>
    </div>
  );
}

function BuddyGlyph() {
  return <div className="glyph-inner"><div className="glyph-antenna" /><div className="glyph-face"><i /><i /><b /></div><div className="glyph-body-line" /></div>;
}

function DiscoverView({ productions, onChoose }: { productions: Production[]; onChoose: (production: Production) => void }) {
  return (
    <div className="discover-page">
      <div className="page-heading"><div><div className="eyebrow">THE COMMUNITY CUT</div><h1>Stories in motion.</h1><p>Explore productions made with the Watch Buddy engine.</p></div><span className="heading-count">{productions.length.toString().padStart(2, "0")} stories</span></div>
      {productions.length === 0 ? <div className="empty-card"><span className="empty-icon">✦</span><h2>The gallery is waiting.</h2><p>Run the demo story to create the first world in your library.</p></div> : <div className="discover-grid">{productions.map((production, index) => <button className="discover-card" key={production.id} onClick={() => onChoose(production)}><div className={`discover-art art-${index % 4}`}><span>{String(index + 1).padStart(2, "0")}</span><b>{production.status === "complete" ? "READY TO WATCH" : "IN PRODUCTION"}</b></div><div className="discover-info"><strong>{production.title}</strong><span>{production.shots.length || "—"} scenes · {production.generation_backend}</span><small>{production.status === "complete" ? "Open watch room →" : `${Math.round(production.progress * 100)}% complete`}</small></div></button>)}</div>}
    </div>
  );
}

function ProfileView({ session, health, onRoleSwitch }: { session: Session; health: Health | null; onRoleSwitch: (role: Role) => void }) {
  return <div className="profile-page"><div className="page-heading"><div><div className="eyebrow">ACCOUNT SPACE</div><h1>Your profile.</h1><p>Shape how Watch Buddy meets you inside the story.</p></div></div><section className="profile-card"><div className={`profile-avatar-large ${session.role}`}>{session.name.slice(0, 1).toUpperCase()}</div><div className="profile-details"><span className="eyebrow">{session.role} ACCOUNT</span><h2>{session.name}</h2><p>{session.email}</p><div className="profile-tags"><span>English</span><span>Hindi-ready</span><span>Watch Buddy beta</span></div></div></section><section className="settings-grid"><div><span className="section-kicker">EXPERIENCE</span><h3>Switch perspective</h3><p>Use the same account to preview the Director Studio or Fan Watch Room.</p><div className="role-switch"><button className={session.role === "director" ? "selected" : ""} onClick={() => onRoleSwitch("director")}>Director</button><button className={session.role === "fan" ? "selected" : ""} onClick={() => onRoleSwitch("fan")}>Fan</button></div></div><div><span className="section-kicker">SERVICE CONNECTIONS</span><h3>Live product signals</h3><div className="connection-row"><span className={health?.gemini ? "status-dot good" : "status-dot"} />Gemini reasoning <b>{health?.gemini ? "Connected" : "Demo mode"}</b></div><div className="connection-row"><span className={health?.clickhouse?.connected ? "status-dot good" : "status-dot"} />ClickHouse ledger <b>{health?.clickhouse?.mode || "Memory fallback"}</b></div><div className="connection-row"><span className="status-dot good" />Timeline sync <b>Enabled</b></div></div></section></div>;
}

function StudioView(props: {
  title: string; setTitle: (value: string) => void; script: string; setScript: (value: string) => void; lang: string; setLang: (value: string) => void; shotsN: number; setShotsN: (value: number) => void; prod: Production | null; phaseIndex: number; busy: boolean; err: string; run: () => void; studioTab: StudioTab; setStudioTab: (value: StudioTab) => void; query: string; setQuery: (value: string) => void; runSearch: () => void; hits: Record<string, unknown>[];
}) {
  const { title, setTitle, script, setScript, lang, setLang, shotsN, setShotsN, prod, phaseIndex, busy, err, run, studioTab, setStudioTab, query, setQuery, runSearch, hits } = props;
  const tabs: [StudioTab, string][] = [["board", "Storyboard"], ["maven", "MAVEN / DSG"], ["library", "Asset library"], ["qc", "QC"], ["dub", "Localization"], ["nle", "NLE export"], ["trace", "Traces"]];
  return <div className="studio-page"><div className="page-heading studio-heading"><div><div className="eyebrow">DIRECTOR CONTROL ROOM</div><h1>Make the impossible<br /><em>feel inevitable.</em></h1><p>One script. Seven specialist agents. A world that knows why every frame exists.</p></div><div className="studio-badges"><span><i className="status-dot good" /> {prod?.status === "complete" ? "Production ready" : prod ? "Crew in motion" : "Ready to direct"}</span><span>Google ADK pipeline</span></div></div><div className="phase-rail">{PHASES.map((phase, index) => <div key={phase.id} className={index <= phaseIndex ? "phase-item on" : "phase-item"}><span>{String(index + 1).padStart(2, "0")}</span><div><strong>{phase.label}</strong><small>{phase.role}</small></div></div>)}</div><div className="studio-workspace"><aside className="script-card"><div className="section-kicker">01 · SCRIPT INGEST</div><h2>Start with a world.</h2><p className="card-help">Give the crew enough detail to find the emotional center of your film.</p><label htmlFor="production-title">Production title</label><input id="production-title" value={title} onChange={(event) => setTitle(event.target.value)} /><div className="input-row"><div><label htmlFor="shot-count">Scenes</label><input id="shot-count" type="number" min={2} max={8} value={shotsN} onChange={(event) => setShotsN(Number(event.target.value))} /></div><div><label htmlFor="dub-language">Voice language</label><select id="dub-language" value={lang} onChange={(event) => setLang(event.target.value)}><option value="hi">Hindi</option><option value="ta">Tamil</option><option value="te">Telugu</option></select></div></div><label htmlFor="screenplay">Screenplay</label><textarea id="screenplay" value={script} onChange={(event) => setScript(event.target.value)} /><button className="primary-button full-width" disabled={busy || !script.trim()} onClick={run}>{busy ? "Queueing the crew…" : prod?.status === "running" ? "Pipeline in motion" : "Run full pipeline"} <span>→</span></button>{err && <p className="error-text">{err}</p>}<div className="ingest-foot"><span>Mock-safe runtime</span><span>{healthLabel(prod)}</span></div></aside><section className="studio-stage"><div className="stage-toolbar"><div className="tabs">{tabs.map(([id, label]) => <button key={id} className={studioTab === id ? "active" : ""} onClick={() => setStudioTab(id)}>{label}</button>)}</div>{prod && <span className="stage-id">{prod.id} · {Math.round(prod.progress * 100)}%</span>}</div>{studioTab === "board" && <div className="board-view">{(prod?.shots || []).length === 0 ? <div className="stage-empty"><span>✦</span><h2>Your storyboard will appear here.</h2><p>Run the pipeline and watch seven agents turn a script into a world.</p></div> : <div className="board-grid">{prod?.shots.map((shot) => <figure key={shot.shot_id} className="shot-card">{shot.media_path ? <img src={shot.media_path} alt={shot.slugline} /> : <div className="shot-placeholder" />}<figcaption><div><strong>SC {String(shot.scene_number).padStart(2, "0")}</strong><span className={`shot-status ${shot.status}`}>{shot.status}</span></div><b>{shot.slugline}</b><small>{shot.camera} · VTA {shot.vta_score.toFixed(2)}</small></figcaption></figure>)}</div>}</div>}{studioTab === "maven" && <div className="detail-list">{(prod?.shots || []).map((shot) => <article key={shot.shot_id}><span className="detail-number">SC {String(shot.scene_number).padStart(2, "0")}</span><div><h3>{shot.slugline} <small>{shot.camera}</small></h3><p><b>Person</b>{shot.maven.person}</p><p><b>Action</b>{shot.maven.action}</p><p><b>Location</b>{shot.maven.location}</p><div className="node-row">{shot.dsg.nodes.map((node) => <span key={node.id}>{node.question}</span>)}</div></div></article>)}</div>}{studioTab === "library" && <div className="library-view"><div className="search-bar"><input value={query} onChange={(event) => setQuery(event.target.value)} /><button className="soft-button" onClick={runSearch}>Search assets</button></div><div className="board-grid">{hits.map((hit, index) => <figure className="shot-card" key={index}>{hit.media_path ? <img src={String(hit.media_path)} alt="" /> : <div className="shot-placeholder" />}<figcaption><b>{String(hit.title || hit.shot_id || "Asset")}</b><small>Semantic distance {Number(hit.dist || 0).toFixed(3)}</small></figcaption></figure>)}</div></div>}{studioTab === "qc" && <QcView prod={prod} />}{studioTab === "dub" && <DubView prod={prod} />}{studioTab === "nle" && <div className="stage-empty"><span>↗</span><h2>{prod?.editorial?.sequence_name || "Editorial package"}</h2><p>{prod?.editorial ? "Your rough cut is ready for the NLE." : "FCPXML and OTIO exports appear after the pipeline seals."}</p>{prod?.editorial && <p><a href={prod.editorial.fcpxml_path} download>Download FCPXML</a> · <a href={prod.editorial.otio_path} download>Download OTIO</a></p>}</div>}{studioTab === "trace" && <div className="trace-view">{(prod?.traces || []).map((trace) => <div key={trace.span_id}><span>{trace.agent}</span><b>{trace.name}</b><small>{trace.duration_ms.toFixed(0)} ms</small></div>)}</div>}</section></div></div>;
}

function healthLabel(prod: Production | null) {
  if (!prod) return "No active job";
  return prod.status === "complete" ? "Sealed" : `${Math.round(prod.progress * 100)}% complete`;
}

function QcView({ prod }: { prod: Production | null }) {
  if (!prod?.qc) return <div className="stage-empty"><span>✓</span><h2>QC arrives after the cut.</h2><p>Compliance agents will check every frame and audio handoff.</p></div>;
  return <div className="qc-view"><div className={`qc-score ${prod.qc.overall}`}><strong>{prod.qc.overall.toUpperCase()}</strong><span>Overall compliance</span></div><div className="qc-metrics"><span>Loudness <b>{prod.qc.loudness_lufs ?? "—"} LUFS</b></span><span>True peak <b>{prod.qc.true_peak_dbfs ?? "—"} dBFS</b></span></div>{prod.qc.findings.map((finding) => <div className="finding" key={finding.code + finding.message}><span className={finding.severity}>{finding.severity}</span><b>{finding.code}</b><p>{finding.message}</p></div>)}</div>;
}

function DubView({ prod }: { prod: Production | null }) {
  if (!prod?.localization) return <div className="stage-empty"><span>◌</span><h2>Give the story a voice.</h2><p>Localization follows quality control and keeps the original timing contract.</p></div>;
  return <div className="dub-view"><div className="dub-summary"><span>{prod.localization.source_lang.toUpperCase()} → {prod.localization.target_lang.toUpperCase()}</span><b>Voice quality {prod.localization.mos_estimate.toFixed(1)} / 5</b></div>{prod.localization.lines.map((line) => <article key={line.shot_id}><span>{line.shot_id.slice(-6)}</span><div><p>{line.source}</p><strong>{line.translated}</strong></div>{line.audio_path && <audio controls src={line.audio_path} />}</article>)}</div>;
}