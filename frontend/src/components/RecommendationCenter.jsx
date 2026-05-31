import { useState, useEffect } from "react";
import { getRecommendations, generateRecommendations } from "../api";

const priorityStyle = {
  high:   "bg-red-900/50 text-red-400 border-red-800",
  medium: "bg-yellow-900/50 text-yellow-400 border-yellow-800",
  low:    "bg-emerald-900/50 text-emerald-400 border-emerald-800",
};

const priorityOrder = { high: 0, medium: 1, low: 2 };

export default function RecommendationCenter() {
  const [recs,      setRecs]      = useState([]);
  const [loading,   setLoading]   = useState(true);
  const [running,   setRunning]   = useState(false);
  const [filter,    setFilter]    = useState("all");

  const load = () => {
    setLoading(true);
    getRecommendations()
      .then((r) => setRecs(r.data || []))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const regenerate = async () => {
    setRunning(true);
    try {
      await generateRecommendations();
      load();
    } catch (e) {
      console.error(e);
    } finally {
      setRunning(false);
    }
  };

  const filtered = recs
    .filter((r) => filter === "all" || r.priority === filter)
    .sort((a, b) => (priorityOrder[a.priority] ?? 3) - (priorityOrder[b.priority] ?? 3));

  const counts = {
    high:   recs.filter((r) => r.priority === "high").length,
    medium: recs.filter((r) => r.priority === "medium").length,
    low:    recs.filter((r) => r.priority === "low").length,
  };

  if (loading) return <p className="text-slate-400">loading recommendations...</p>;

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-200">Recommendation Center</h2>
        <button
          onClick={regenerate}
          disabled={running}
          className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-xs px-3 py-1.5 rounded-lg transition"
        >
          {running ? "generating..." : "Regenerate"}
        </button>
      </div>

      {/* summary chips */}
      <div className="flex gap-3 mb-5">
        {["all", "high", "medium", "low"].map((p) => (
          <button
            key={p}
            onClick={() => setFilter(p)}
            className={`text-xs px-3 py-1 rounded-full border transition ${
              filter === p
                ? "bg-blue-600 text-white border-blue-500"
                : "bg-slate-800 text-slate-400 border-slate-600 hover:border-slate-400"
            }`}
          >
            {p === "all" ? `all (${recs.length})` : `${p} (${counts[p]})`}
          </button>
        ))}
      </div>

      {filtered.length === 0 ? (
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-8 text-center">
          <p className="text-slate-400 mb-2">no recommendations yet</p>
          <p className="text-slate-500 text-sm">run models first then click regenerate</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filtered.map((rec, i) => (
            <div key={i} className="bg-slate-800 rounded-xl border border-slate-700 p-4 hover:border-slate-500 transition">
              <div className="flex items-start justify-between mb-2">
                <span className="text-sm font-semibold text-slate-200">Customer #{rec.customer_id}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full border ${priorityStyle[rec.priority] ?? "bg-slate-700 text-slate-400 border-slate-600"}`}>
                  {rec.priority}
                </span>
              </div>
              <p className="text-sm text-slate-300 leading-relaxed">{rec.recommendation}</p>
              {rec.created_at && (
                <p className="text-xs text-slate-500 mt-2">{new Date(rec.created_at).toLocaleDateString()}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
