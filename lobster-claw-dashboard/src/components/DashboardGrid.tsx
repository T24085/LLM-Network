import { agents, memoryStats, tasks, tokenUsage, workers } from '../data/mockDashboardData';
import StatCard from './StatCard';
export default function DashboardGrid(){
  const activeAgents = agents.filter(a=>a.status==='active').length;
  const openTasks = tasks.filter(t=>t.status==='queued'||t.status==='running').length;
  const tpm = tokenUsage[tokenUsage.length-1].tokens;
  const total = tokenUsage.reduce((s,t)=>s+t.tokens,0);
  const errors = tasks.reduce((s,t)=>s+t.errors,0);
  const loops = 1;
  const health = Math.round(workers.reduce((s,w)=>s+w.health,0)/workers.length);
  const mem = `${memoryStats.usedGb}/${memoryStats.totalGb} GB`;
  return <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4"><StatCard label="Active Agents" value={activeAgents}/><StatCard label="Open Tasks" value={openTasks}/><StatCard label="Tokens / Minute" value={tpm}/><StatCard label="Total Tokens Today" value={total}/><StatCard label="Errors Today" value={errors}/><StatCard label="Loop Warnings" value={loops}/><StatCard label="Worker Health" value={`${health}%`}/><StatCard label="Memory Usage" value={mem}/></section>}
