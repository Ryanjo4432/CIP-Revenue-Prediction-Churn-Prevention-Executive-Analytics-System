import axios from "axios";

const api = axios.create({
  // goes through vite proxy to backend
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
});

export const getKPI          = ()      => api.get("/analytics/kpi");
export const getCustomers    = ()      => api.get("/customers");
export const getTransactions = ()      => api.get("/transactions");
export const getForecasts    = ()      => api.get("/predictions/run/forecast");
export const runChurn        = ()      => api.post("/predictions/run/churn");
export const runCLV          = ()      => api.post("/predictions/run/clv");
export const getRecommendations       = ()      => api.get("/recommendations");
export const generateRecommendations  = ()      => api.post("/recommendations/generate");
export const getCustomerRecs = (id)   => api.get(`/recommendations/customer/${id}`);

export default api;
