import { useEffect, useMemo, useState } from "react";
import WatchBuddy from "./WatchBuddy";
import {
  getHealth,
  getProduction,
  getSample,
  searchAssets,
  startProduction,
  type Health,
  type Production,
} from "./api";

type Surface = "watch" | "studio";

const PHASES = [
  { id: "director", label: "01 Director", role: "MAVEN" },
  { id: "producer", label: "02 Producer", role: "DSG loop" },
  { id: "studio_head", label: "03 Studio Head", role: "ClickHouse" },
  { id: "editorial", label: "04 Editorial", role: "NLE" },
  { id: "qc", label: "05 QC", role: "EBU / Netflix" },
  { id: "localization", label: "06 Localization", role: "EN→HI" },
  { id: "complete", label: "07 Observability", role: "OTel" },
];

type Tab = "board" | "maven" | "library" | "qc" | "dub" | "nle" | "trace";

export default function App() {
  const [health, setHealth] = useState<Health | null>(null);
  const [title, setTitle] = useState("The Last Reel");
  const [script, setScript] = useState("");
  const [lang, setLang] = useState("hi");
  const [shotsN, setShotsN] = useState(4);
  const [prod, setProd] = useState<Production | null>(null);
  const [tab, setTab] = useState<Tab>("board");
  const [busy, setBusy] = useState(false);
  const [query, setQuery] = useState("high-contrast lighting tracking shot");
  const [hits, setHits] = useState<Record<string, unknown>[]>([]);
  const [err, setErr] = useState("");
  const [surface, setSurface] = useState<Surface>("watch");

  useEffect(() => {
    getHealth().then(setHealth).catch(() => setHealth(null));
    getSample().then((s) => {
      setTitle(s.title);
      setScript(s.script);
    });
  }, []);

  useEffect(() => {
    if (!prod?.id) return;
    if (prod.status === "complete" || prod.status === "failed") return;
    const t = setInterval(async () => {
      try {
        const next = await getProduction(prod.id);
        setProd(next);
      } catch {
        /* keep last */
      }
    }, 700);
    return () => clearInterval(t);
  }, [prod?.id, prod?.status]);

  const phaseIndex = useMemo(() => {
    const i = PHASES.findIndex((p) => p.id === prod?.phase);
    return i < 0 ? (prod?.status === "complete" ? PHASES.length - 1 : -1) : i;
  }, [prod]);

  async function run() {
    setErr("");
    setBusy(true);
    try {
      const created = await startProduction({
        title,
        script,
        target_lang: lang,
        max_shots: shotsN,
      });
      setProd(created);
      setTab("board");
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Failed to start");
    } finally {
      setBusy(false);
    }
  }

  async function doSearch() {
    const res = await searchAssets(query, prod?.id);
    setHits(res.hits);
    setTab("library");
  }

  return (
    <div className="shell">
      <header className="top">
        <div>
          <div className="mark">CINEGRAPH</div>
          <div className="sub">
            {surface === "watch"
              ? "Watch Buddy · watch along, fork the ending — minted by the CineGraph engine"
              : "Studio · deterministic pre-vis · NLE handoff · hyper-localization"}
          </div>
        </div>
        <div className="header-right">
          <div className="surface-toggle">
            <button className={surface === "watch" ? "on" : ""} onClick={() => setSurface("watch")}>
              Watch Buddy
            </button>
            <button className={surface === "studio" ? "on" : ""} onClick={() => setSurface("studio")}>
              Studio
            </button>
          </div>
          <div className="pills">
            <span className={health?.gemini ? "ok" : "dim"}>Gemini {health?.gemini ? "live" : "mock"}</span>
            <span className={health?.clickhouse.connected ? "ok" : "dim"}>
              ClickHouse {health?.clickhouse.mode ?? "—"}
            </span>
            <span className="dim">{health?.generation ?? "…"} gen</span>
          </div>
        </div>
      </header>

      {surface === "watch" && <WatchBuddy prod={prod} />}

      {surface === "studio" && (
        <>
      <section className="rail">
        {PHASES.map((p, i) => (
          <div key={p.id} className={`phase ${i <= phaseIndex ? "on" : ""}`}>
            <b>{p.label}</b>
            <em>{p.role}</em>
          </div>
        ))}
      </section>

      <main className="grid">
        <aside className="panel script">
          <h2>Screenplay ingest</h2>
          <label>Title</label>
          <input value={title} onChange={(e) => setTitle(e.target.value)} />
          <div className="row">
            <div>
              <label>Shots</label>
              <input
                type="number"
                min={2}
                max={8}
                value={shotsN}
                onChange={(e) => setShotsN(Number(e.target.value))}
              />
            </div>
            <div>
              <label>Dub target</label>
              <select value={lang} onChange={(e) => setLang(e.target.value)}>
                <option value="hi">Hindi</option>
                <option value="ta">Tamil</option>
                <option value="te">Telugu</option>
              </select>
            </div>
          </div>
          <label>Script</label>
          <textarea value={script} onChange={(e) => setScript(e.target.value)} />
          <button disabled={busy || !script.trim()} onClick={run}>
            {busy ? "Queuing…" : prod?.status === "running" ? "Pipeline running" : "Run full pipeline"}
          </button>
          {err && <p className="error">{err}</p>}
          {prod && (
            <p className="status">
              {prod.id} · {prod.status} · {Math.round(prod.progress * 100)}% · {prod.phase}
            </p>
          )}
          <ol className="log">
            {(prod?.events || []).slice(-8).reverse().map((e, i) => (
              <li key={i}>
                <span>{e.phase}</span> {e.message}
              </li>
            ))}
          </ol>
        </aside>

        <section className="panel stage">
          <nav>
            {(
              [
                ["board", "Storyboard"],
                ["maven", "MAVEN / DSG"],
                ["library", "Asset library"],
                ["qc", "QC"],
                ["dub", "Localization"],
                ["nle", "NLE export"],
                ["trace", "Traces"],
              ] as [Tab, string][]
            ).map(([id, label]) => (
              <button key={id} className={tab === id ? "active" : ""} onClick={() => setTab(id)}>
                {label}
              </button>
            ))}
          </nav>

          {tab === "board" && (
            <div className="board">
              {(prod?.shots || []).length === 0 && <p className="empty">Run the pipeline to generate IMAX pre-vis frames.</p>}
              {(prod?.shots || []).map((s) => (
                <figure key={s.shot_id}>
                  {s.media_path ? <img src={s.media_path} alt={s.slugline} /> : <div className="ph" />}
                  <figcaption>
                    <strong>
                      SC {String(s.scene_number).padStart(2, "0")} · {s.status}
                    </strong>
                    <span>{s.slugline}</span>
                    <em>
                      VTA {s.vta_score.toFixed(2)} · VQA {s.vqa_score.toFixed(2)} · loop {s.loop_iterations}
                    </em>
                  </figcaption>
                </figure>
              ))}
            </div>
          )}

          {tab === "maven" && (
            <div className="maven">
              {(prod?.shots || []).map((s) => (
                <article key={s.shot_id}>
                  <h3>
                    {s.slugline} · {s.camera}
                  </h3>
                  <p>
                    <b>Person</b> {s.maven.person}
                  </p>
                  <p>
                    <b>Action</b> {s.maven.action}
                  </p>
                  <p>
                    <b>Location</b> {s.maven.location}
                  </p>
                  <ul>
                    {s.dsg.nodes.map((n) => (
                      <li key={n.id}>{n.question}</li>
                    ))}
                  </ul>
                </article>
              ))}
            </div>
          )}

          {tab === "library" && (
            <div>
              <div className="search">
                <input value={query} onChange={(e) => setQuery(e.target.value)} />
                <button onClick={doSearch}>HNSW search</button>
              </div>
              <div className="board">
                {hits.map((h, i) => (
                  <figure key={i}>
                    {h.media_path ? <img src={String(h.media_path)} alt="" /> : <div className="ph" />}
                    <figcaption>
                      <strong>{String(h.title || h.shot_id)}</strong>
                      <em>dist {Number(h.dist || 0).toFixed(3)}</em>
                    </figcaption>
                  </figure>
                ))}
              </div>
            </div>
          )}

          {tab === "qc" && (
            <div className="qc">
              {!prod?.qc && <p className="empty">QC runs after editorial assembly.</p>}
              {prod?.qc && (
                <>
                  <p className={`badge ${prod.qc.overall}`}>{prod.qc.overall.toUpperCase()}</p>
                  <p>
                    Loudness {prod.qc.loudness_lufs ?? "—"} LUFS · True peak {prod.qc.true_peak_dbfs ?? "—"} dBFS
                  </p>
                  <table>
                    <tbody>
                      {prod.qc.findings.map((f) => (
                        <tr key={f.code + f.message}>
                          <td className={f.severity}>{f.severity}</td>
                          <td>{f.code}</td>
                          <td>{f.message}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </>
              )}
            </div>
          )}

          {tab === "dub" && (
            <div className="dub">
              {!prod?.localization && <p className="empty">Dubbing follows QC.</p>}
              {prod?.localization && (
                <>
                  <p>
                    {prod.localization.source_lang} → {prod.localization.target_lang} · MOS {prod.localization.mos_estimate} ·
                    LSE-D {prod.localization.lse_d_estimate}
                  </p>
                  {prod.localization.lines.map((l) => (
                    <article key={l.shot_id}>
                      <p className="src">{l.source}</p>
                      <p className="dst">{l.translated}</p>
                      {l.audio_path && <audio controls src={l.audio_path} />}
                    </article>
                  ))}
                </>
              )}
            </div>
          )}

          {tab === "nle" && (
            <div className="nle">
              {!prod?.editorial && <p className="empty">Editorial package appears after ingest.</p>}
              {prod?.editorial && (
                <>
                  <p>Sequence {prod.editorial.sequence_name}</p>
                  <p>Bins {prod.editorial.bins.join(" · ")}</p>
                  <p>
                    <a href={prod.editorial.fcpxml_path} download>
                      Download FCPXML
                    </a>
                    {" · "}
                    <a href={prod.editorial.otio_path} download>
                      Download OTIO
                    </a>
                  </p>
                  <p className="hint">Import the FCPXML into Premiere or Resolve. Live CEP/Lua plugins are stretch.</p>
                </>
              )}
            </div>
          )}

          {tab === "trace" && (
            <div className="trace">
              {(prod?.traces || []).length === 0 && <p className="empty">Spans stream as agents execute. Grafana Tempo on :3001 when docker compose is up.</p>}
              <ul>
                {(prod?.traces || []).map((t) => (
                  <li key={t.span_id}>
                    <span className="agent">{t.agent}</span>
                    <span>{t.name}</span>
                    <em>{t.duration_ms.toFixed(1)} ms</em>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      </main>
        </>
      )}
    </div>
  );
}
