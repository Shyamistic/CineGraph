import { useEffect, useMemo, useState, type FormEvent } from "react";
import WatchBuddy from "./WatchBuddy";
import {
  getHealth,
  getMe,
  getProduction,
  getSample,
  listProductions,
  loginAccount,
  logoutAccount,
  registerAccount,
  searchAssets,
  setAccountRole,
  startProduction,
  type Health,
  type Production,
  type Session,
} from "./api";

type Role = "director" | "fan";
type View = "home" | "watch" | "studio" | "discover" | "profile";
type StudioTab = "board" | "maven" | "library" | "qc" | "dub" | "nle" | "trace";
const PHASES = [
  { id: "director", label: "Director", role: "MAVEN" },
  { id: "producer", label: "Producer", role: "DSG loop" },
  { id: "studio_head", label: "Studio", role: "ClickHouse" },
  { id: "editorial", label: "Editorial", role: "NLE" },
  { id: "qc", label: "QC", role: "EBU / Netflix" },
  { id: "localization", label: "Localization", role: "EN → IN" },
  { id: "complete", label: "Observability", role: "OTel" },
];

function AuthPage({ onEnter }: { onEnter: (session: Session) => void }) {
  const [mode, setMode] = useState<"login" | "register">("register");
  const [role, setRole] = useState<Role>("director");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    setBusy(true);
    try {
      const session =
        mode === "register"
          ? await registerAccount({ name, email, password, role })
          : await loginAccount({ email, password });
      onEnter(session);
    } catch (err) {
      setError(err instanceof Error ? err.message.replace(/["{}]/g, " ").trim() : "Unable to sign in");
    } finally {
      setBusy(false);
    }
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
        <div className="eyebrow">GOVERNED FAN CINEMA</div>
        <h1>Stories that watch back.</h1>
        <p className="auth-copy">Directors define the world. Fans discover new paths through it. Every derivative is watermarked and logged.</p>
        <div className="role-picker auth-mode" aria-label="Account action">
          <button type="button" className={mode === "register" ? "role-option active" : "role-option"} onClick={() => setMode("register")}>
            <span className="role-icon">+</span>
            <span><strong>Create account</strong><small>Server-side session</small></span>
          </button>
          <button type="button" className={mode === "login" ? "role-option active" : "role-option"} onClick={() => setMode("login")}>
            <span className="role-icon">→</span>
            <span><strong>Sign in</strong><small>Existing account</small></span>
          </button>
        </div>
        <form onSubmit={submit}>
          {mode === "register" && (
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
          )}
          {mode === "register" && (
            <>
              <label htmlFor="name">Your name</label>
              <input id="name" value={name} onChange={(event) => setName(event.target.value)} placeholder={role === "director" ? "Ava Director" : "Arjun Fan"} required />
            </>
          )}
          <label htmlFor="email">Email address</label>
          <input id="email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@studio.film" required />
          <label htmlFor="password">Password</label>
          <input id="password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="At least 8 characters" minLength={8} required />
          {error && <p className="error-text">{error}</p>}
          <button className="primary-button auth-submit" type="submit" disabled={busy}>{busy ? "Connecting…" : mode === "register" ? "Create account →" : "Enter Watch Buddy →"}</button>
        </form>
        <p className="auth-note">HttpOnly session cookie · not stored in this browser’s localStorage</p>
      </main>
      <div className="auth-proof">
        <span>Powered by Gemini</span>
        <i />
        <span>ClickHouse provenance ledger</span>
      </div>
    </div>
  );
}

export default function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [authReady, setAuthReady] = useState(false);
  const [health, setHealth] = useState<Health | null>(null);
  const [title, setTitle] = useState("The Last Reel");
  const [script, setScript] = useState("");
  const [lang, setLang] = useState("hi");
  const [shotsN, setShotsN] = useState(4);
  const [prod, setProd] = useState<Production | null>(null);
  const [productions, setProductions] = useState<Production[]>([]);
  const [view, setView] = useState<View>("home");
  const [studioTab, setStudioTab] = useState<StudioTab>("board");
  const [busy, setBusy] = useState(false);
  const [query, setQuery] = useState("high-contrast lighting tracking shot");
  const [hits, setHits] = useState<Record<string, unknown>[]>([]);
  const [err, setErr] = useState("");
  const [notice, setNotice] = useState("");
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const [loadingWorkspace, setLoadingWorkspace] = useState(true);

  useEffect(() => {
    getMe().then((me) => {
      setSession(me);
      if (me?.role === "fan") setView("watch");
      setAuthReady(true);
    }).catch(() => setAuthReady(true));
  }, []);

  useEffect(() => {
    if (!session) return;
    setLoadingWorkspace(true);
    Promise.allSettled([getHealth(), getSample(), listProductions()]).then(([healthResult, sampleResult, productionsResult]) => {
      if (healthResult.status === "fulfilled") setHealth(healthResult.value);
      if (sampleResult.status === "fulfilled") {
        setTitle(sampleResult.value.title);
        setScript(sampleResult.value.script);
      }
      if (productionsResult.status === "fulfilled") {
        setProductions(productionsResult.value);
        const active = productionsResult.value.find((item) => item.status === "running") || productionsResult.value[0];
        if (active) setProd(active);
      }
      setLoadingWorkspace(false);
    });
  }, [session?.id]);

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
    if (title.trim().length < 3) {
      setErr("Give this production a title before sending it to the crew.");
      return;
    }
    if (script.trim().length < 120) {
      setErr("The crew needs at least 120 characters of screenplay context.");
      return;
    }
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

  async function signOut() {
    await logoutAccount();
    setSession(null);
    setProductions([]);
    setProd(null);
  }

  function chooseProduction(item: Production, destination: "watch" | "studio" = "watch") {
    setProd(item);
    setView(destination);
  }

  if (!authReady) {
    return <div className="workspace-loading"><span className="loading-reel" /><h2>Checking your session</h2><p>Connecting to the Watch Buddy API.</p></div>;
  }

  if (!session) return <AuthPage onEnter={(next) => { setSession(next); setView(next.role === "fan" ? "watch" : "home"); }} />;

  const isDirector = session.role === "director";
  const navItems: { id: View; label: string; meta: string }[] = [
    { id: "home", label: isDirector ? "Productions" : "For you", meta: "01" },
    ...(isDirector ? [{ id: "studio" as View, label: "Create & review", meta: "02" }] : []),
    { id: "discover", label: "Story library", meta: isDirector ? "03" : "02" },
    { id: "watch", label: "Screening room", meta: isDirector ? "04" : "03" },
    { id: "profile", label: "Settings", meta: isDirector ? "05" : "04" },
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
            {prod && <button className="active-production-chip" onClick={() => setView(prod.status === "complete" ? "watch" : "studio")}><span className={`status-dot ${prod.status === "complete" ? "good" : ""}`} />{prod.title}<b>{prod.status === "complete" ? "Ready" : `${Math.round(prod.progress * 100)}%`}</b></button>}
            {isDirector && <button className="topbar-create" onClick={() => { setProd(null); setView("studio"); }}>New production</button>}
            <button className="icon-button" onClick={() => setView("profile")} aria-label="Open profile">◎</button>
          </div>
        </header>

        {notice && <button className="toast" onClick={() => setNotice("")}>{notice}<span>×</span></button>}
        {view === "home" && (
          <HomeView
            session={session}
            prod={prod}
            productions={productions}
            health={health}
            loading={loadingWorkspace}
            onCreate={() => { setProd(null); setView("studio"); }}
            onDiscover={() => setView("discover")}
            onChoose={(item) => chooseProduction(item, isDirector && item.status !== "complete" ? "studio" : "watch")}
            onReview={(item) => chooseProduction(item, "studio")}
          />
        )}
        {view === "watch" && <WatchBuddy prod={prod} />}
        {view === "discover" && <DiscoverView productions={productions} onChoose={chooseProduction} />}
        {view === "profile" && <ProfileView session={session} health={health} onRoleSwitch={async (role) => {
          const next = await setAccountRole(role);
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

function HomeView({ session, prod, productions, health, loading, onCreate, onDiscover, onChoose, onReview }: {
  session: Session;
  prod: Production | null;
  productions: Production[];
  health: Health | null;
  loading: boolean;
  onCreate: () => void;
  onDiscover: () => void;
  onChoose: (production: Production) => void;
  onReview: (production: Production) => void;
}) {
  const isDirector = session.role === "director";
  const complete = productions.filter((item) => item.status === "complete");
  const running = productions.filter((item) => item.status === "running" || item.status === "queued");
  const failed = productions.filter((item) => item.status === "failed");
  const latestEvents = productions
    .flatMap((item) => item.events.slice(-2).map((event) => ({ ...event, title: item.title, id: item.id })))
    .slice(-6)
    .reverse();

  if (loading) {
    return <div className="workspace-loading"><span className="loading-reel" /><h2>Opening your studio</h2><p>Syncing productions, media, and agent activity.</p></div>;
  }

  return (
    <div className="overview-page production-home">
      <header className="workspace-intro">
        <div>
          <div className="eyebrow">{isDirector ? "DIRECTOR WORKSPACE" : "YOUR SCREENING QUEUE"}</div>
          <h1>{isDirector ? <>Good morning, {session.name.split(" ")[0]}.<br /><em>What are we making?</em></> : <>Your next story<br /><em>is already waiting.</em></>}</h1>
        </div>
        <div className="workspace-actions">
          <button className="primary-button" onClick={isDirector ? onCreate : onDiscover}>{isDirector ? "Create production" : "Explore stories"} <span>→</span></button>
          <div className="runtime-proof"><span className={`status-dot ${health?.gemini ? "good" : ""}`} /><strong>{health?.gemini ? "Gemini connected" : "Generation fallback"}</strong><small>{health?.generation}</small></div>
        </div>
      </header>

      <section className="workspace-metrics" aria-label="Workspace summary">
        <article><span>Productions</span><strong>{productions.length.toString().padStart(2, "0")}</strong><small>{isDirector ? `${running.length} active now` : `${complete.length} ready to watch`}</small></article>
        <article><span>Generated scenes</span><strong>{productions.reduce((sum, item) => sum + item.shots.length, 0).toString().padStart(2, "0")}</strong><small>Across your library</small></article>
        <article><span>Ready to screen</span><strong>{complete.length.toString().padStart(2, "0")}</strong><small>QC and localization complete</small></article>
        <article><span>Needs attention</span><strong>{failed.length.toString().padStart(2, "0")}</strong><small>{failed.length ? "Open to inspect failure" : "All systems moving"}</small></article>
      </section>

      <div className="workspace-grid">
        <section className="production-library">
          <div className="section-heading"><div><span className="section-kicker">{isDirector ? "YOUR SLATE" : "CONTINUE WATCHING"}</span><h2>{productions.length ? "Stories in motion" : "Your first world starts here"}</h2></div>{productions.length > 3 && <button className="text-button" onClick={onDiscover}>View full library →</button>}</div>
          {productions.length === 0 ? (
            <button className="empty-production" onClick={isDirector ? onCreate : onDiscover}><span className="empty-production-mark">+</span><div><strong>{isDirector ? "Create your first production" : "Browse the story library"}</strong><small>{isDirector ? "Bring a screenplay. The agent crew handles the production graph." : "Choose a finished story and meet your Watch Buddy."}</small></div></button>
          ) : (
            <div className="production-list">
              {productions.slice(0, 5).map((item, index) => <ProductionRow key={item.id} production={item} index={index} onOpen={() => onChoose(item)} onReview={isDirector ? () => onReview(item) : undefined} />)}
            </div>
          )}
        </section>

        <aside className="activity-console">
          <div className="section-heading"><div><span className="section-kicker">LIVE ACTIVITY</span><h2>Agent room</h2></div><span className="live-signal">LIVE</span></div>
          <div className="activity-stream">
            {latestEvents.length ? latestEvents.map((event, index) => <button key={`${event.id}-${index}`} onClick={() => onChoose(productions.find((item) => item.id === event.id)!)}><i /><span><strong>{event.title}</strong><small>{event.message}</small></span><b>{Math.round(event.progress * 100)}%</b></button>) : <div className="quiet-activity"><BuddyGlyph /><p>Agent activity will appear here as your production moves.</p></div>}
          </div>
          <div className="service-stack">
            <div><span><i className={`status-dot ${health?.gemini ? "good" : ""}`} />Gemini generation</span><b>{health?.gemini ? "Live" : "Fallback"}</b></div>
            <div><span><i className={`status-dot ${health?.clickhouse?.connected ? "good" : ""}`} />Asset ledger</span><b>{health?.clickhouse?.connected ? "Connected" : "Local"}</b></div>
            <div><span><i className="status-dot good" />Timeline engine</span><b>Synchronized</b></div>
          </div>
        </aside>
      </div>
    </div>
  );
}

function ProductionRow({ production, index, onOpen, onReview }: { production: Production; index: number; onOpen: () => void; onReview?: () => void }) {
  const image = production.shots.find((shot) => shot.media_path)?.media_path;
  const isReady = production.status === "complete";
  return (
    <article className="production-row">
      <button className={`production-poster poster-${index % 4}`} onClick={onOpen}>{image ? <img src={image} alt="" /> : <span>{String(index + 1).padStart(2, "0")}</span>}<i>{isReady ? "READY" : production.status.toUpperCase()}</i></button>
      <button className="production-summary" onClick={onOpen}><span className="production-meta">{production.shots.length || "—"} scenes · {production.generation_backend}</span><strong>{production.title}</strong><small>{production.error || production.events[production.events.length - 1]?.message || (isReady ? "Ready for the screening room" : "Waiting for the agent crew")}</small><div className="row-progress"><span style={{ width: `${Math.max(3, production.progress * 100)}%` }} /></div></button>
      <div className="production-actions"><b>{isReady ? "Published cut" : production.phase.replace(/_/g, " ")}</b>{onReview && <button onClick={onReview}>{isReady ? "Review" : "Open studio"} →</button>}<button onClick={onOpen}>{isReady ? "Watch" : "Details"} →</button></div>
    </article>
  );
}

function BuddyGlyph() {
  return <div className="glyph-inner"><div className="glyph-antenna" /><div className="glyph-face"><i /><i /><b /></div><div className="glyph-body-line" /></div>;
}

function DiscoverView({ productions, onChoose }: { productions: Production[]; onChoose: (production: Production) => void }) {
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState<"all" | "ready" | "making">("all");
  const visible = productions.filter((item) => {
    const matchesSearch = item.title.toLowerCase().includes(search.toLowerCase());
    const matchesFilter = filter === "all" || (filter === "ready" ? item.status === "complete" : item.status !== "complete");
    return matchesSearch && matchesFilter;
  });
  return (
    <div className="discover-page">
      <div className="page-heading"><div><div className="eyebrow">STORY LIBRARY</div><h1>Find your next<br /><em>living story.</em></h1><p>Every title here carries scene context, localized voice, and an ending you can reshape.</p></div><span className="heading-count">{visible.length.toString().padStart(2, "0")} stories</span></div>
      <div className="library-controls">
        <label><span>Search the library</span><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search by title" /></label>
        <div className="library-filters" aria-label="Filter stories">
          {(["all", "ready", "making"] as const).map((value) => <button key={value} className={filter === value ? "active" : ""} onClick={() => setFilter(value)}>{value === "all" ? "All stories" : value === "ready" ? "Ready to watch" : "In production"}</button>)}
        </div>
      </div>
      {visible.length === 0 ? <div className="empty-card"><span className="empty-icon">+</span><h2>No stories match this view.</h2><p>Change the filter or create a new production from the Director workspace.</p></div> : <div className="discover-grid">{visible.map((production, index) => {
        const image = production.shots.find((shot) => shot.media_path)?.media_path;
        return <button className="discover-card" key={production.id} onClick={() => onChoose(production)}><div className={`discover-art art-${index % 4}`}>{image ? <img src={image} alt="" /> : <span>{String(index + 1).padStart(2, "0")}</span>}<b>{production.status === "complete" ? "READY TO WATCH" : "IN PRODUCTION"}</b><i>{production.shots.length || "—"} SCENES</i></div><div className="discover-info"><strong>{production.title}</strong><span>{production.generation_backend} · {production.localization?.target_lang?.toUpperCase() || "VOICE PENDING"}</span><small>{production.status === "complete" ? "Enter screening room →" : `${Math.round(production.progress * 100)}% · ${production.phase.replace(/_/g, " ")}`}</small></div></button>;
      })}</div>}
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