import { useState, useEffect } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, ReferenceLine,
} from "recharts";
import { getForecasts } from "../api";

// recharts needs a custom tooltip so it doesnt look terrible
const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-xs">
      <p className="text-slate-400 mb-1">{label}</p>
      {payload.map((p) => (
        <p key={p.name} style={{ color: p.color }} className="font-medium">
          {p.name}: ${p.value?.toLocaleString()}
        </p>
      ))}
    </div>
  );
};

export default function RevenueChart({ kpi }) {
  const [forecast, setForecast] = useState(null);
  const [loading,  setLoading]  = useState(true);

  useEffect(() => {
    getForecasts()
      .then((r) => setForecast(r.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-slate-400">loading forecast...</p>;
  if (!forecast || forecast.error) return <p className="text-slate-400">not enough data to forecast yet</p>;

  // merge historical + forecast into one array for the chart
  const historical = (forecast.historical || []).map((d) => ({
    month:      d.month,
    actual:     d.revenue,
    forecast:   null,
  }));

  const future = (forecast.forecast || []).map((d) => ({
    month:      d.month,
    actual:     null,
    forecast:   d.predicted_revenue,
  }));

  const chartData = [...historical, ...future];
  const splitMonth = historical[historical.length - 1]?.month;

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-200">Revenue Forecast</h2>
        <div className="flex gap-3 text-xs">
          <span className={`px-2 py-1 rounded-full ${forecast.trend === "up" ? "bg-emerald-900/50 text-emerald-400" : "bg-red-900/50 text-red-400"}`}>
            trend: {forecast.trend} ${Math.abs(forecast.monthly_growth).toLocaleString()}/mo
          </span>
        </div>
      </div>

      <div className="bg-slate-800 rounded-xl border border-slate-700 p-4 mb-6">
        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={chartData} margin={{ top: 10, right: 20, left: 10, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="month" tick={{ fill: "#94a3b8", fontSize: 11 }} />
            <YAxis tick={{ fill: "#94a3b8", fontSize: 11 }} tickFormatter={(v) => `$${v?.toLocaleString()}`} />
            <Tooltip content={<CustomTooltip />} />
            <Legend wrapperStyle={{ fontSize: 12, color: "#94a3b8" }} />
            {splitMonth && <ReferenceLine x={splitMonth} stroke="#475569" strokeDasharray="4 4" label={{ value: "forecast →", fill: "#64748b", fontSize: 11 }} />}
            <Line type="monotone" dataKey="actual"   stroke="#3b82f6" strokeWidth={2} dot={{ r: 3 }} name="Actual Revenue"   connectNulls={false} />
            <Line type="monotone" dataKey="forecast" stroke="#a78bfa" strokeWidth={2} dot={{ r: 3 }} name="Forecast Revenue" connectNulls={false} strokeDasharray="5 5" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* forecast table */}
      <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
        <h3 className="text-sm font-semibold text-slate-300 mb-3">Monthly Forecast</h3>
        <div className="flex gap-4 flex-wrap">
          {forecast.forecast.map((f) => (
            <div key={f.month} className="bg-slate-700 rounded-lg px-4 py-3 min-w-32">
              <p className="text-xs text-slate-400">{f.month}</p>
              <p className="text-lg font-bold text-purple-400">${f.predicted_revenue.toLocaleString()}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
