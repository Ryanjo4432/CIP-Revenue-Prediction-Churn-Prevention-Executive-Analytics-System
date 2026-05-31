import { useState, useEffect } from "react";
import KPICards            from "./components/KPICards";
import CustomerTable       from "./components/CustomerTable";
import RevenueChart        from "./components/RevenueChart";
import RecommendationCenter from "./components/RecommendationCenter";
import { getKPI, runChurn, runCLV, generateRecommendations } from "./api";

const TABS = ["Overview", "Customers", "Forecast", "Recommendations"];

export default function App() {
  const [tab,     setTab]     = useState("Overview");
  const [kpi,     setKpi]     = useState(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [toast,   setToast]   = useState("");

  useEffect(() => {
    getKPI()
      .then((r) => setKpi(r.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(""), 3000);
  };

  // runs churn + clv + recommendations in sequence then refreshes kpi
  const runAllModels = async () => {
    setRunning(true);
    try {
      await runChurn();
      await runCLV();
      await generateRecommendations();
      const kpiRes = await getKPI();
      setKpi(kpiRes.data);
      showToast("models ran successfully");
    } catch (e) {
      showToast("something went wrong running models");
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">

      {/* navbar */}
      <header className="bg-slate-800 border-b border-slate-700 px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-blue-400">CIP</h1>
          <p className="text-xs text-slate-400">Customer Intelligence Platform</p>
        </div>
        <button
          onClick={runAllModels}
          disabled={running}
          className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-sm px-4 py-2 rounded-lg transition"
        >
          {running ? "Running..." : "Run Models"}
        </button>
      </header>

      {/* tabs */}
      <nav className="bg-slate-800 border-b border-slate-700 px-6 flex gap-1">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-3 text-sm font-medium transition border-b-2 ${
              tab === t
                ? "border-blue-500 text-blue-400"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            {t}
          </button>
        ))}
      </nav>

      {/* content */}
      <main className="p-6 max-w-7xl mx-auto">
        {loading ? (
          <div className="flex items-center justify-center h-64 text-slate-400">loading...</div>
        ) : (
          <>
            {tab === "Overview"         && <KPICards kpi={kpi} />}
            {tab === "Customers"        && <CustomerTable />}
            {tab === "Forecast"         && <RevenueChart kpi={kpi} />}
            {tab === "Recommendations"  && <RecommendationCenter />}
          </>
        )}
      </main>

      {/* toast */}
      {toast && (
        <div className="fixed bottom-6 right-6 bg-blue-600 text-white px-4 py-2 rounded-lg shadow-lg text-sm">
          {toast}
        </div>
      )}
    </div>
  );
}
