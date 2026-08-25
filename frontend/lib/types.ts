export type TransactionStatus = "SUCCESS" | "FAILED" | "PENDING";

export interface Transaction {
  id: number;
  source_transaction_id: string;
  timestamp: string;
  merchant: string;
  category: string | null;
  amount: string | number;
  currency: string;
  status: TransactionStatus;
  payment_method: string;
  created_at: string;
}

export interface Pagination {
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

export interface TransactionListResponse {
  data: Transaction[];
  pagination: Pagination;
}

export interface TransactionFilters {
  page: number;
  page_size: number;
  search?: string;
  category?: string;
  status?: TransactionStatus;
  min_amount?: string;
  max_amount?: string;
  start_date?: string;
  end_date?: string;
  sort_by: "timestamp" | "amount";
  sort_order: "asc" | "desc";
}

export interface Wallet {
  id: number;
  coin_balance: number;
  updated_at: string;
}

export interface Reward {
  id: number;
  name: string;
  description: string;
  coin_cost: number;
  reward_type: string;
  active: boolean;
}

export interface RedemptionResponse {
  redemption_id: number;
  reward: Reward;
  updated_balance: number;
}

export interface CategorySpending {
  category: string;
  total: string | number;
}

export interface MonthlySpending {
  month: string;
  total: string | number;
}

export interface DashboardSummary {
  total_spending: string | number;
  successful_transactions: number;
  transaction_count: number;
}
