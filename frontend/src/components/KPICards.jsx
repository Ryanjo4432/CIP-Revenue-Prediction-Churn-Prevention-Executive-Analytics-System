export default function KPICards({ kpi }) {
  if (!kpi) return <p className="text-slate-400">no data yet — click Run Models</p>;

  const cards = [
    { label: "Total Revenue",     value: `$${kpi.total_revenue?.toLocaleString() ?? 0}`,  color: "text-green-400"  },
    { label: "Avg Order Value",   value: `$${kpi.avg_order_value ?? 0}`,                   color: "text-blue-400"   },
    { label: "Churn Rate",        value: `${kpi.churn_rate ?? 0}%`,                        color: "text-red-400"    },
    { label: "Retention Rate",    value: `${kpi.retention_rate ?? 0}%`,                    color: "text-emerald-400"},
    { label: "Avg Customer CLV",  value: `$${kpi.customer_lifetime_value?.toLocaleString() ?? 0}`, color: "text-purple-400" },
  ];

  return (
    <div>
      <h2 className="text-lg font-semibold mb-4 text-slate-200">Executive Overview</h2>

      {/* kpi cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-8">
        {cards.map((c) => (
          <div key={c.label} className="bg-slate-800 rounded-xl p-4 border border-slate-700">
            <p className="text-xs text-slate-400 mb-1">{c.label}</p>
            <p className={`text-2xl font-bold ${c.color}`}>{c.value}</p>
          </div>
        ))}
      </div>

      {/* top customers table */}
      {kpi.top_customers?.length > 0 && (
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-4 mb-6">
          <h3 className="text-sm font-semibold text-slate-300 mb-3">Top Customers by Spend</h3>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-slate-400 text-left border-b border-slate-700">
                <th className="pb-2">Name</th>
                <th className="pb-2">Email</th>
                <th className="pb-2 text-right">Total Spent</th>
              </tr>
            </thead>
            <tbody>
              {kpi.top_customers.map((c) => (
                <tr key={c.customer_id} className="border-b border-slate-700/50 hover:bg-slate-700/30">
                  <td className="py-2 text-slate-200">{c.name}</td>
                  <td className="py-2 text-slate-400">{c.email}</td>
                  <td className="py-2 text-right text-green-400 font-medium">${c.total_spent.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* revenue by category */}
      {kpi.revenue_by_category?.length > 0 && (
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
          <h3 className="text-sm font-semibold text-slate-300 mb-3">Revenue by Category</h3>
          <div className="flex flex-wrap gap-3">
            {kpi.revenue_by_category.map((c) => (
              <div key={c.category} className="bg-slate-700 rounded-lg px-3 py-2">
                <p className="text-xs text-slate-400 capitalize">{c.category}</p>
                <p className="text-sm font-bold text-blue-400">${c.total.toLocaleString()}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
