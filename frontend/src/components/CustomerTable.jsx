import { useState, useEffect } from "react";
import { getCustomers, runChurn } from "../api";

const riskColor = (prob) => {
  if (prob == null) return "text-slate-400";
  if (prob >= 0.70)  return "text-red-400";
  if (prob >= 0.40)  return "text-yellow-400";
  return "text-green-400";
};

const riskLabel = (prob) => {
  if (prob == null) return "unknown";
  if (prob >= 0.70)  return "high";
  if (prob >= 0.40)  return "medium";
  return "low";
};

export default function CustomerTable() {
  const [customers, setCustomers] = useState([]);
  const [churnMap,  setChurnMap]  = useState({});
  const [loading,   setLoading]   = useState(true);
  const [search,    setSearch]    = useState("");

  useEffect(() => {
    getCustomers()
      .then((r) => setCustomers(r.data))
      .catch(console.error)
      .finally(() => setLoading(false));

    // pull latest churn predictions
    runChurn()
      .then((r) => {
        const map = {};
        r.data.predictions?.forEach((p) => { map[p.customer_id] = p.churn_probability; });
        setChurnMap(map);
      })
      .catch(console.error);
  }, []);

  const filtered = customers.filter(
    (c) =>
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      c.email.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) return <p className="text-slate-400">loading customers...</p>;

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-200">Customer Insights</h2>
        <input
          type="text"
          placeholder="search name or email..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="bg-slate-700 border border-slate-600 rounded-lg px-3 py-1.5 text-sm text-slate-200 placeholder-slate-400 focus:outline-none focus:border-blue-500 w-60"
        />
      </div>

      <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-slate-400 text-left border-b border-slate-700 bg-slate-800/80">
              <th className="px-4 py-3">ID</th>
              <th className="px-4 py-3">Name</th>
              <th className="px-4 py-3">Email</th>
              <th className="px-4 py-3">Location</th>
              <th className="px-4 py-3">Joined</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Churn Risk</th>
              <th className="px-4 py-3">Churn Prob</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((c) => {
              const prob = churnMap[c.customer_id] ?? null;
              return (
                <tr key={c.customer_id} className="border-b border-slate-700/50 hover:bg-slate-700/30 transition">
                  <td className="px-4 py-3 text-slate-400">{c.customer_id}</td>
                  <td className="px-4 py-3 font-medium text-slate-200">{c.name}</td>
                  <td className="px-4 py-3 text-slate-400">{c.email}</td>
                  <td className="px-4 py-3 text-slate-400">{c.location ?? "—"}</td>
                  <td className="px-4 py-3 text-slate-400">{c.join_date ?? "—"}</td>
                  <td className="px-4 py-3">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${c.is_active ? "bg-emerald-900/50 text-emerald-400" : "bg-red-900/50 text-red-400"}`}>
                      {c.is_active ? "active" : "inactive"}
                    </span>
                  </td>
                  <td className={`px-4 py-3 font-medium ${riskColor(prob)}`}>
                    {riskLabel(prob)}
                  </td>
                  <td className={`px-4 py-3 font-mono ${riskColor(prob)}`}>
                    {prob != null ? `${(prob * 100).toFixed(1)}%` : "—"}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>

        {filtered.length === 0 && (
          <p className="text-center text-slate-400 py-8">no customers found</p>
        )}
      </div>
    </div>
  );
}
