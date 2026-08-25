"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Header } from "@/components/dashboard/Header";
import { MonthlySpending } from "@/components/dashboard/MonthlySpending";
import { RedeemModal } from "@/components/dashboard/RedeemModal";
import { RewardsSection } from "@/components/dashboard/RewardsSection";
import { SpendingByCategory } from "@/components/dashboard/SpendingByCategory";
import { StatsCards } from "@/components/dashboard/StatsCards";
import { TransactionDetailModal } from "@/components/dashboard/TransactionDetailModal";
import { TransactionFilters } from "@/components/dashboard/TransactionFilters";
import { TransactionPagination } from "@/components/dashboard/TransactionPagination";
import { TransactionTable } from "@/components/dashboard/TransactionTable";
import { Card } from "@/components/ui/Card";
import { ErrorState } from "@/components/ui/ErrorState";
import { ApiError, getCategorySpending, getDashboardSummary, getMonthlySpending, getRewards, getTransactions, getWallet, redeemReward } from "@/lib/api";
import type { CategorySpending, DashboardSummary, MonthlySpending as MonthlySpendingData, Pagination, Reward, Transaction, TransactionFilters as Filters, Wallet } from "@/lib/types";

const initialFilters: Filters = { page: 1, page_size: 25, sort_by: "timestamp", sort_order: "desc" };
const emptyPagination: Pagination = { page: 1, page_size: 25, total: 0, total_pages: 0 };

export default function DashboardPage() {
  const [filters, setFilters] = useState<Filters>(initialFilters);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [pagination, setPagination] = useState<Pagination>(emptyPagination);
  const [wallet, setWallet] = useState<Wallet>();
  const [rewards, setRewards] = useState<Reward[]>([]);
  const [categoryData, setCategoryData] = useState<CategorySpending[]>([]);
  const [monthlyData, setMonthlyData] = useState<MonthlySpendingData[]>([]);
  const [summary, setSummary] = useState<DashboardSummary>();
  const [transactionLoading, setTransactionLoading] = useState(true);
  const [transactionError, setTransactionError] = useState<string>();
  const [overviewLoading, setOverviewLoading] = useState(true);
  const [overviewError, setOverviewError] = useState<string>();
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null);
  const [selectedReward, setSelectedReward] = useState<Reward | null>(null);
  const [redeeming, setRedeeming] = useState(false);
  const [redeemError, setRedeemError] = useState<string>();
  const [redeemSuccess, setRedeemSuccess] = useState(false);

  const loadOverview = useCallback(async () => {
    setOverviewLoading(true); setOverviewError(undefined);
    try {
      const [nextWallet, nextRewards, categories, months, nextSummary] = await Promise.all([getWallet(), getRewards(), getCategorySpending(), getMonthlySpending(), getDashboardSummary()]);
      setWallet(nextWallet); setRewards(nextRewards); setCategoryData(categories); setMonthlyData(months); setSummary(nextSummary);
    } catch (error) { setOverviewError(error instanceof Error ? error.message : "Could not load the dashboard overview."); }
    finally { setOverviewLoading(false); }
  }, []);
  useEffect(() => { void loadOverview(); }, [loadOverview]);

  useEffect(() => {
    const controller = new AbortController();
    const timer = window.setTimeout(async () => {
      setTransactionLoading(true); setTransactionError(undefined);
      try { const result = await getTransactions(filters, controller.signal); setTransactions(result.data); setPagination(result.pagination); }
      catch (error) { if ((error as Error).name !== "AbortError") setTransactionError(error instanceof Error ? error.message : "Could not load transactions."); }
      finally { if (!controller.signal.aborted) setTransactionLoading(false); }
    }, filters.search !== undefined ? 300 : 0);
    return () => { controller.abort(); window.clearTimeout(timer); };
  }, [filters]);

  const updateFilters = (changes: Partial<Filters>) => setFilters((current) => ({ ...current, ...changes, page: changes.page ?? 1 }));
  const categories = useMemo(() => categoryData.map((item) => item.category), [categoryData]);
  const focusTransactions = () => document.getElementById("transactions")?.scrollIntoView({ behavior: "smooth" });
  const handleSort = (sortBy: "timestamp" | "amount") => setFilters((current) => ({ ...current, page: 1, sort_by: sortBy, sort_order: current.sort_by === sortBy && current.sort_order === "desc" ? "asc" : "desc" }));
  const selectMonth = (month: string) => { const [year, monthNumber] = month.split("-").map(Number); updateFilters({ start_date: `${month}-01`, end_date: new Date(year, monthNumber, 0).toISOString().slice(0, 10) }); focusTransactions(); };
  const confirmRedeem = async () => {
    if (!selectedReward) return;
    setRedeeming(true); setRedeemError(undefined);
    try { await redeemReward(selectedReward.id); const [nextWallet, nextRewards] = await Promise.all([getWallet(), getRewards()]); setWallet(nextWallet); setRewards(nextRewards); setRedeemSuccess(true); }
    catch (error) { setRedeemError(error instanceof ApiError && error.status === 409 ? "You do not have enough coins for this reward." : error instanceof Error ? error.message : "Redemption could not be completed."); try { setWallet(await getWallet()); } catch { /* Preserve last confirmed balance. */ } }
    finally { setRedeeming(false); }
  };

  return <><Header balance={wallet?.coin_balance} /><main className="mx-auto max-w-7xl space-y-10 px-4 py-7 sm:px-6 lg:px-8">
    <section><p className="text-xs font-bold uppercase tracking-[0.16em] text-[#4a7f62]">Financial overview</p><h1 className="mt-1 text-3xl font-bold tracking-tight text-[#142536] sm:text-4xl">Your money, in focus.</h1><p className="mt-2 text-sm text-[#63736d]">Review activity, discover patterns, and get more from every transaction.</p></section>
    <StatsCards totalSpending={Number(summary?.total_spending ?? 0)} successfulTransactions={summary?.successful_transactions ?? 0} coinBalance={wallet?.coin_balance} transactionCount={summary?.transaction_count ?? 0} />
    <section id="insights" className="scroll-mt-6"><div className="mb-5"><p className="text-xs font-bold uppercase tracking-[0.16em] text-[#4a7f62]">Insights</p><h2 className="mt-1 text-2xl font-bold text-[#142536]">A clearer spending picture</h2></div>{overviewError ? <ErrorState message={overviewError} onRetry={loadOverview} /> : <div className="grid gap-5 lg:grid-cols-2"><SpendingByCategory data={categoryData} loading={overviewLoading} onSelect={(category) => { updateFilters({ category }); focusTransactions(); }} /><MonthlySpending data={monthlyData} loading={overviewLoading} onSelect={selectMonth} /></div>}</section>
    <section id="transactions" className="scroll-mt-6"><div className="mb-5"><p className="text-xs font-bold uppercase tracking-[0.16em] text-[#4a7f62]">Activity</p><h2 className="mt-1 text-2xl font-bold text-[#142536]">Transactions</h2></div><Card className="overflow-hidden"><TransactionFilters filters={filters} categories={categories} onChange={updateFilters} onClear={() => setFilters(initialFilters)} />{transactionError ? <ErrorState message={transactionError} onRetry={() => setFilters((current) => ({ ...current }))} /> : <><TransactionTable records={transactions} loading={transactionLoading} filters={filters} onSort={handleSort} onSelect={setSelectedTransaction} /><TransactionPagination pagination={pagination} onPageChange={(page) => updateFilters({ page })} /></>}</Card></section>
    <RewardsSection rewards={rewards} balance={wallet?.coin_balance} loading={overviewLoading} error={overviewError} onRetry={loadOverview} onRedeem={(reward) => { setSelectedReward(reward); setRedeemError(undefined); setRedeemSuccess(false); }} />
  </main><TransactionDetailModal transaction={selectedTransaction} onClose={() => setSelectedTransaction(null)} /><RedeemModal reward={selectedReward} balance={wallet?.coin_balance} loading={redeeming} error={redeemError} success={redeemSuccess} onConfirm={confirmRedeem} onClose={() => { setSelectedReward(null); setRedeemSuccess(false); setRedeemError(undefined); }} /></>;
}
