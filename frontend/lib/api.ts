import type {
  CategorySpending,
  DashboardSummary,
  MonthlySpending,
  RedemptionResponse,
  Reward,
  TransactionFilters,
  TransactionListResponse,
  Wallet,
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  constructor(message: string, public readonly status?: number) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: { Accept: "application/json", ...options.headers },
    });
  } catch {
    throw new ApiError("Unable to reach the Coinly API. Check that the backend is running.");
  }

  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new ApiError(payload?.detail ?? "The request could not be completed.", response.status);
  }
  return response.json() as Promise<T>;
}

export function getTransactions(filters: TransactionFilters, signal?: AbortSignal) {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== "") params.set(key, String(value));
  });
  return request<TransactionListResponse>(`/api/transactions?${params}`, { signal });
}

export const getWallet = (signal?: AbortSignal) => request<Wallet>("/api/wallet", { signal });
export const getRewards = (signal?: AbortSignal) => request<Reward[]>("/api/rewards", { signal });
export const getCategorySpending = (signal?: AbortSignal) =>
  request<CategorySpending[]>("/api/analytics/category-spending", { signal });
export const getMonthlySpending = (signal?: AbortSignal) =>
  request<MonthlySpending[]>("/api/analytics/monthly-spending", { signal });
export const getDashboardSummary = (signal?: AbortSignal) =>
  request<DashboardSummary>("/api/analytics/summary", { signal });
export const redeemReward = (rewardId: number) =>
  request<RedemptionResponse>(`/api/rewards/${rewardId}/redeem`, { method: "POST" });
