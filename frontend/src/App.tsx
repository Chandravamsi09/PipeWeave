import React, { useState } from 'react';
import { 
  GitBranch, 
  Activity, 
  Database, 
  Layers, 
  FileText, 
  Plug, 
  Play, 
  CheckCircle2, 
  Clock, 
  Cpu, 
  ShieldCheck, 
  ArrowRight,
  Zap,
  HardDrive
} from 'lucide-react';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'canvas' | 'sql' | 'metrics' | 'schema' | 'lineage' | 'connectors' | 'runs'>('canvas');
  const [executing, setExecuting] = useState(false);
  const [runSuccess, setRunSuccess] = useState(false);
  const [sqlQuery, setSqlQuery] = useState(`SELECT 
    customer_id,
    COUNT(order_id) AS total_orders,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_val
FROM kafka_orders_stream
WHERE status = 'COMPLETED'
GROUP BY customer_id
ORDER BY total_revenue DESC;`);

  const nodes = [
    { id: 'source_kafka', name: 'Kafka Orders Stream', type: 'SOURCE', desc: 'Real-time JSON/Avro events topic' },
    { id: 'clean_nulls', name: 'Null Sanitizer & Imputer', type: 'TRANSFORM', desc: 'Cleanse & normalize payload fields' },
    { id: 'quality_gate', name: 'Great Expectations Gate', type: 'QUALITY_GATE', desc: 'Rule check: amount > 0, valid email' },
    { id: 'revenue_agg', name: 'Tumbling Revenue Window', type: 'TRANSFORM', desc: 'Vectorized 60s sliding window aggregate' },
    { id: 'sink_clickhouse', name: 'ClickHouse Columnar Mart', type: 'SINK', desc: 'Fast columnar analytics warehouse' },
  ];

  const handleExecute = () => {
    setExecuting(true);
    setRunSuccess(false);
    setTimeout(() => {
      setExecuting(false);
      setRunSuccess(true);
      setTimeout(() => setRunSuccess(false), 4000);
    }, 1200);
  };

  const tabs = [
    { id: 'canvas', label: 'DAG Canvas', icon: GitBranch },
    { id: 'sql', label: 'Transform IDE', icon: Layers },
    { id: 'metrics', label: 'Stream Telemetry', icon: Activity },
    { id: 'schema', label: 'Schema Registry', icon: FileText },
    { id: 'lineage', label: 'Column Lineage', icon: Database },
    { id: 'connectors', label: 'Connectors', icon: Plug },
    { id: 'runs', label: 'Execution Runs', icon: Cpu },
  ] as const;

  return (
    <div className="h-screen w-screen flex flex-col bg-slate-950 text-slate-100 overflow-hidden font-sans">
      {/* Top Navbar */}
      <header className="h-16 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-6 select-none shrink-0 shadow-lg">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center font-bold text-slate-950 shadow-lg shadow-emerald-500/20">
            <GitBranch className="w-5 h-5 stroke-[2.5]" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-base tracking-tight text-white">PipeWeave Studio</span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-semibold border border-emerald-500/20">v1.0</span>
            </div>
            <span className="text-xs text-slate-400 font-mono">E-Commerce Real-Time Order Stream</span>
          </div>
        </div>

        <nav className="flex space-x-1 bg-slate-950/80 p-1 rounded-xl border border-slate-800">
          {tabs.map((t) => {
            const Icon = t.icon;
            const isActive = activeTab === t.id;
            return (
              <button
                key={t.id}
                onClick={() => setActiveTab(t.id)}
                className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-emerald-500 text-slate-950 font-bold shadow-md shadow-emerald-500/20'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{t.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="flex items-center space-x-3">
          {runSuccess && (
            <span className="flex items-center space-x-1 text-emerald-400 text-xs font-semibold animate-pulse">
              <CheckCircle2 className="w-4 h-4" />
              <span>Executed 50,000 records successfully!</span>
            </span>
          )}
          <button
            onClick={handleExecute}
            disabled={executing}
            className="flex items-center space-x-2 bg-emerald-500 hover:bg-emerald-400 active:scale-95 text-slate-950 font-bold px-4 py-2 rounded-lg text-xs shadow-lg shadow-emerald-500/20 transition-all cursor-pointer"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>{executing ? 'Executing Pipeline...' : 'Execute Pipeline'}</span>
          </button>
        </div>
      </header>

      {/* Main View Area */}
      <main className="flex-1 overflow-y-auto bg-slate-950 p-8">
        {/* VIEW 1: DAG CANVAS */}
        {activeTab === 'canvas' && (
          <div className="h-full flex flex-col justify-between">
            <div className="flex items-center justify-between bg-slate-900/90 border border-slate-800 px-6 py-3 rounded-2xl shadow-xl mb-8">
              <div className="flex space-x-6 text-xs font-mono">
                <span className="text-slate-400">Topology: <strong className="text-emerald-400">Linear DAG (5 Nodes)</strong></span>
                <span className="text-slate-400">Throughput: <strong className="text-white">14,500 rec/sec</strong></span>
                <span className="text-slate-400">State: <strong className="text-emerald-400">ACTIVE STREAMING</strong></span>
              </div>
              <span className="text-xs text-slate-500 font-mono">Engine: DuckDB Vectorized + Celery Pool</span>
            </div>

            <div className="flex items-center justify-center space-x-4 my-auto overflow-x-auto py-8">
              {nodes.map((node, idx) => (
                <React.Fragment key={node.id}>
                  <div className="bg-slate-900 border-2 border-emerald-500/40 hover:border-emerald-400 hover:scale-105 transition-all duration-200 rounded-2xl p-5 w-64 shadow-2xl backdrop-blur-sm">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-slate-950 text-emerald-400 font-mono">{node.type}</span>
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    </div>
                    <h3 className="text-sm font-semibold text-white mb-1 truncate">{node.name}</h3>
                    <p className="text-xs text-slate-400 mb-3">{node.desc}</p>
                    <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400 font-mono">
                      <span>Latency</span>
                      <span className="text-emerald-400">1.2ms</span>
                    </div>
                  </div>

                  {idx < nodes.length - 1 && (
                    <div className="flex flex-col items-center">
                      <div className="h-0.5 w-8 bg-gradient-to-r from-emerald-500 to-teal-400" />
                      <ArrowRight className="w-4 h-4 text-emerald-400 -mt-2" />
                    </div>
                  )}
                </React.Fragment>
              ))}
            </div>
            
            <div className="text-center text-xs text-slate-500 font-mono pt-4">
              Click on any node to view configuration parameters or click "Execute Pipeline" to run in real-time.
            </div>
          </div>
        )}

        {/* VIEW 2: TRANSFORM IDE */}
        {activeTab === 'sql' && (
          <div className="h-full flex flex-col space-y-4">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-lg font-bold text-white flex items-center space-x-2">
                  <Layers className="w-5 h-5 text-purple-400" />
                  <span>Vectorized SQL Transformation IDE (DuckDB Engine)</span>
                </h2>
                <p className="text-xs text-slate-400">Write zero-copy ANSI SQL queries executed directly in-memory.</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 flex-1 min-h-0">
              <div className="bg-slate-900 border border-slate-800 rounded-xl flex flex-col overflow-hidden shadow-xl">
                <div className="bg-slate-950 px-4 py-2 text-xs font-mono text-slate-400 border-b border-slate-800 flex justify-between">
                  <span>order_revenue_agg.sql</span>
                  <span className="text-purple-400">DuckDB 0.10.0</span>
                </div>
                <textarea
                  value={sqlQuery}
                  onChange={(e) => setSqlQuery(e.target.value)}
                  className="flex-1 w-full bg-slate-900 text-slate-200 font-mono text-xs p-4 resize-none focus:outline-none leading-relaxed"
                />
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-xl flex flex-col overflow-hidden shadow-xl">
                <div className="bg-slate-950 px-4 py-2 text-xs font-mono text-slate-400 border-b border-slate-800 flex justify-between">
                  <span>Result Preview (3 rows)</span>
                  <span className="text-emerald-400 flex items-center space-x-1">
                    <CheckCircle2 className="w-3 h-3" />
                    <span>Vectorized Execution: 1.4ms</span>
                  </span>
                </div>
                <div className="p-4 overflow-auto">
                  <table className="w-full text-left text-xs font-mono">
                    <thead className="text-slate-400 border-b border-slate-800">
                      <tr>
                        <th className="pb-2">customer_id</th>
                        <th className="pb-2">total_orders</th>
                        <th className="pb-2">total_revenue</th>
                        <th className="pb-2">avg_order_val</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/60">
                      <tr className="hover:bg-slate-800/40">
                        <td className="py-2.5 text-emerald-400 font-bold">CUST-104</td>
                        <td className="py-2.5">14</td>
                        <td className="py-2.5">$4,250.00</td>
                        <td className="py-2.5">$303.57</td>
                      </tr>
                      <tr className="hover:bg-slate-800/40">
                        <td className="py-2.5 text-emerald-400 font-bold">CUST-389</td>
                        <td className="py-2.5">9</td>
                        <td className="py-2.5">$2,980.50</td>
                        <td className="py-2.5">$331.16</td>
                      </tr>
                      <tr className="hover:bg-slate-800/40">
                        <td className="py-2.5 text-emerald-400 font-bold">CUST-212</td>
                        <td className="py-2.5">6</td>
                        <td className="py-2.5">$1,420.00</td>
                        <td className="py-2.5">$236.66</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* VIEW 3: TELEMETRY */}
        {activeTab === 'metrics' && (
          <div className="space-y-6">
            <h2 className="text-lg font-bold text-white flex items-center space-x-2">
              <Activity className="w-5 h-5 text-emerald-400" />
              <span>Real-Time Observability & Stream Telemetry</span>
            </h2>

            <div className="grid grid-cols-4 gap-6">
              {[
                { title: 'Throughput Rate', value: '14,500 rps', sub: 'Peak: 24,000 rps', icon: Zap, color: 'text-emerald-400' },
                { title: 'p95 Latency', value: '24.1 ms', sub: 'p99: 68.9 ms', icon: Activity, color: 'text-cyan-400' },
                { title: 'Engine CPU Load', value: '34.2%', sub: '8 Cores Active', icon: Cpu, color: 'text-amber-400' },
                { title: 'Worker Memory', value: '512 MB', sub: 'Allocated 2048 MB', icon: HardDrive, color: 'text-purple-400' },
              ].map((c) => {
                const Icon = c.icon;
                return (
                  <div key={c.title} className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
                    <div className="flex justify-between items-center mb-4">
                      <span className="text-xs text-slate-400">{c.title}</span>
                      <Icon className={`w-4 h-4 ${c.color}`} />
                    </div>
                    <div className="text-2xl font-bold text-white font-mono">{c.value}</div>
                    <div className="text-xs text-slate-500 mt-1 font-mono">{c.sub}</div>
                  </div>
                );
              })}
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
              <h3 className="text-sm font-semibold text-white mb-4">Throughput Histogram (Last 60 Minutes)</h3>
              <div className="h-40 flex items-end justify-between space-x-2 pt-6">
                {[45, 60, 75, 90, 85, 95, 70, 80, 100, 88, 92, 98, 85, 90, 94, 99].map((h, i) => (
                  <div key={i} className="flex-1 bg-gradient-to-t from-emerald-600 to-teal-400 rounded-t-md transition-all hover:opacity-80" style={{ height: `${h}%` }} />
                ))}
              </div>
            </div>
          </div>
        )}

        {/* VIEW 4: SCHEMA REGISTRY */}
        {activeTab === 'schema' && (
          <div className="space-y-6">
            <h2 className="text-lg font-bold text-white flex items-center space-x-2">
              <FileText className="w-5 h-5 text-cyan-400" />
              <span>Schema Registry & Evolution Governance</span>
            </h2>
            <div className="grid grid-cols-2 gap-6">
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
                <h3 className="text-sm font-bold text-slate-300 mb-4 pb-2 border-b border-slate-800">Version 1.0 (Baseline Schema)</h3>
                <div className="space-y-2 text-xs font-mono">
                  <div className="p-3 bg-slate-950 rounded-lg flex justify-between"><span>order_id</span><span className="text-slate-400">STRING (Required)</span></div>
                  <div className="p-3 bg-slate-950 rounded-lg flex justify-between"><span>customer_id</span><span className="text-slate-400">STRING (Required)</span></div>
                  <div className="p-3 bg-slate-950 rounded-lg flex justify-between"><span>amount</span><span className="text-slate-400">FLOAT (Required)</span></div>
                </div>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
                <h3 className="text-sm font-bold text-emerald-400 mb-4 pb-2 border-b border-slate-800">Version 2.0 (Active Evolution)</h3>
                <div className="space-y-2 text-xs font-mono">
                  <div className="p-3 bg-slate-950 rounded-lg flex justify-between"><span>order_id</span><span className="text-slate-400">STRING</span></div>
                  <div className="p-3 bg-slate-950 rounded-lg flex justify-between"><span>customer_id</span><span className="text-slate-400">STRING</span></div>
                  <div className="p-3 bg-slate-950 rounded-lg flex justify-between"><span>amount</span><span className="text-slate-400">FLOAT</span></div>
                  <div className="p-3 bg-emerald-950/20 border border-emerald-500/30 text-emerald-300 rounded-lg flex justify-between"><span>currency</span><span>STRING (default: USD)</span></div>
                  <div className="p-3 bg-emerald-950/20 border border-emerald-500/30 text-emerald-300 rounded-lg flex justify-between"><span>status</span><span>STRING (default: PENDING)</span></div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* VIEW 5: LINEAGE */}
        {activeTab === 'lineage' && (
          <div className="space-y-6">
            <h2 className="text-lg font-bold text-white flex items-center space-x-2">
              <Database className="w-5 h-5 text-indigo-400" />
              <span>Column-Level Data Lineage & Impact Analysis</span>
            </h2>
            <div className="flex items-center justify-center space-x-6 py-12 overflow-x-auto">
              {[
                { table: 'raw_kafka_orders', cols: ['order_id', 'customer_id', 'amount', 'timestamp'] },
                { table: 'stg_orders_clean', cols: ['order_id', 'customer_id', 'gross_amount', 'event_time'] },
                { table: 'fct_daily_revenue', cols: ['date_key', 'total_orders', 'total_revenue', 'avg_ticket'] },
              ].map((s, idx) => (
                <React.Fragment key={s.table}>
                  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 w-72 shadow-xl">
                    <div className="text-xs font-mono text-indigo-400 font-bold mb-4 pb-2 border-b border-slate-800">{s.table}</div>
                    <div className="space-y-2 text-xs font-mono">
                      {s.cols.map((c) => (
                        <div key={c} className="p-2.5 bg-slate-950 rounded-lg text-slate-300 flex justify-between items-center">
                          <span>{c}</span>
                          <span className="w-2 h-2 rounded-full bg-indigo-500" />
                        </div>
                      ))}
                    </div>
                  </div>
                  {idx < 2 && <ArrowRight className="w-6 h-6 text-indigo-400 animate-pulse" />}
                </React.Fragment>
              ))}
            </div>
          </div>
        )}

        {/* VIEW 6: CONNECTORS */}
        {activeTab === 'connectors' && (
          <div className="space-y-6">
            <h2 className="text-lg font-bold text-white flex items-center space-x-2">
              <Plug className="w-5 h-5 text-emerald-400" />
              <span>Ingestion & Sink Connectors Vault</span>
            </h2>
            <div className="grid grid-cols-2 gap-6">
              {[
                { name: 'Production Kafka Broker', type: 'KAFKA', host: 'kafka.prod.internal:9092', status: 'ONLINE' },
                { name: 'PostgreSQL Read Replica', type: 'POSTGRESQL', host: 'pg-replica.internal:5432', status: 'ONLINE' },
                { name: 'ClickHouse Columnar Sink', type: 'CLICKHOUSE', host: 'clickhouse.cluster:8123', status: 'ONLINE' },
                { name: 'S3 Parquet Data Lake', type: 'S3_PARQUET', host: 's3://production-lakehouse/', status: 'ONLINE' },
              ].map((conn) => (
                <div key={conn.name} className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
                  <div className="flex justify-between items-center">
                    <div>
                      <h3 className="text-sm font-bold text-white">{conn.name}</h3>
                      <span className="text-xs text-slate-400 font-mono">{conn.type}</span>
                    </div>
                    <span className="text-emerald-400 text-xs font-semibold bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
                      {conn.status}
                    </span>
                  </div>
                  <div className="p-3 bg-slate-950 rounded-xl text-xs font-mono text-slate-400">
                    Endpoint: <strong className="text-slate-200">{conn.host}</strong>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* VIEW 7: RUNS */}
        {activeTab === 'runs' && (
          <div className="space-y-6">
            <h2 className="text-lg font-bold text-white flex items-center space-x-2">
              <Cpu className="w-5 h-5 text-emerald-400" />
              <span>Pipeline Execution History & Logs</span>
            </h2>
            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
              <table className="w-full text-left text-xs font-mono">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-4">Run ID</th>
                    <th className="p-4">Pipeline</th>
                    <th className="p-4">Status</th>
                    <th className="p-4">Records</th>
                    <th className="p-4">Duration</th>
                    <th className="p-4">Time</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {[
                    { id: 'run-9021', name: 'E-Commerce Order Stream', state: 'SUCCESS', rec: '50,000', dur: '1.45s', time: '10:15:00 UTC' },
                    { id: 'run-9020', name: 'E-Commerce Order Stream', state: 'SUCCESS', rec: '50,000', dur: '1.38s', time: '10:10:00 UTC' },
                    { id: 'run-9019', name: 'IoT Telemetry Stream', state: 'SUCCESS', rec: '25,000', dur: '0.92s', time: '10:05:00 UTC' },
                  ].map((r) => (
                    <tr key={r.id} className="hover:bg-slate-800/40">
                      <td className="p-4 text-emerald-400 font-bold">{r.id}</td>
                      <td className="p-4 text-white">{r.name}</td>
                      <td className="p-4 text-emerald-400 font-bold">{r.state}</td>
                      <td className="p-4 text-slate-300">{r.rec}</td>
                      <td className="p-4 text-slate-300">{r.dur}</td>
                      <td className="p-4 text-slate-500">{r.time}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};
export default App;
