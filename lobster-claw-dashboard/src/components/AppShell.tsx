import { useEffect, useMemo, useState } from 'react';
import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { agents, alerts, logs, networkNodes, tasks, tokenUsage } from '../data/mockDashboardData';
import ActivityFeed from './ActivityFeed';
import AgentCard from './AgentCard';
import AlertsPanel from './AlertsPanel';
import ChartFrame from './ChartFrame';
import DashboardGrid from './DashboardGrid';
import MascotWidget from './MascotWidget';
import Sidebar from './Sidebar';
import TaskTable from './TaskTable';
import TopBar from './TopBar';

export default function AppShell() {
  const [tick, setTick] = useState(0);
  const [paused, setPaused] = useState(false);
  const [agentFilter, setAgentFilter] = useState('all');
  const [taskFilter, setTaskFilter] = useState('all');

  useEffect(() => {
    if (paused) return;
    const timer = setInterval(() => setTick((v) => v + 1), 5000);
    return () => clearInterval(timer);
  }, [paused]);

  const filteredAgents = useMemo(() => agents.filter((a) => agentFilter === 'all' || a.status === agentFilter), [agentFilter, tick]);
  const filteredTasks = useMemo(() => tasks.filter((t) => taskFilter === 'all' || t.status === taskFilter), [taskFilter, tick]);
  const pieData = useMemo(() => ['queued', 'running', 'done', 'failed'].map((s) => ({ name: s, value: tasks.filter((t) => t.status === s).length })), [tick]);

  return <div className="min-h-screen bg-ocean p-4 text-slate-100"><div className="mx-auto grid max-w-[1600px] gap-4 xl:grid-cols-[260px_1fr]"><Sidebar /><main><div className="top-dashboard-frame mb-3 h-8 rounded bg-brass/10"/><TopBar />
    <div className="mb-3 flex flex-wrap items-center gap-2">
      <select className="ocean-card rounded px-2 py-1" value={agentFilter} onChange={(e) => setAgentFilter(e.target.value)}><option value="all">All Agents</option><option value="active">Active</option><option value="idle">Idle</option><option value="error">Error</option></select>
      <select className="ocean-card rounded px-2 py-1" value={taskFilter} onChange={(e) => setTaskFilter(e.target.value)}><option value="all">All Tasks</option><option value="queued">Queued</option><option value="running">Running</option><option value="done">Done</option><option value="failed">Failed</option></select>
      <button className="rounded border border-tube px-3 py-1" onClick={() => setPaused((p) => !p)}>{paused ? 'Resume Monitoring' : 'Pause Monitoring'}</button>
      <button className="rounded border border-claw px-3 py-1 text-claw">Emergency Stop Agents</button>
    </div>
    <DashboardGrid />
    <section className="mt-4 grid gap-3 lg:grid-cols-2">
      <ChartFrame title="Token usage over time"><ResponsiveContainer width="100%" height={220}><LineChart data={tokenUsage}><CartesianGrid strokeDasharray="3 3" stroke="#234" /><XAxis dataKey="time" /><YAxis /><Tooltip /><Line type="monotone" dataKey="tokens" stroke="#2ad8ca" strokeWidth={2} /></LineChart></ResponsiveContainer></ChartFrame>
      <ChartFrame title="Task completion pie chart"><ResponsiveContainer width="100%" height={220}><PieChart><Pie data={pieData} dataKey="value" nameKey="name" outerRadius={70}>{pieData.map((_,i)=><Cell key={i} fill={['#2ad8ca','#cf9c42','#4ade80','#dc3b34'][i]} />)}</Pie><Tooltip /></PieChart></ResponsiveContainer></ChartFrame>
      <ChartFrame title="Agent network/node map placeholder"><div className="grid grid-cols-3 gap-2 p-4 text-xs">{networkNodes.map((n)=><div key={n} className="rounded border border-tube/30 p-2 text-center">{n}</div>)}</div></ChartFrame>
      <ChartFrame title="CPU/token usage combo chart"><ResponsiveContainer width="100%" height={220}><BarChart data={tokenUsage}><CartesianGrid strokeDasharray="3 3" stroke="#234" /><XAxis dataKey="time" /><YAxis /><Tooltip /><Bar dataKey="cpu" fill="#cf9c42" /><Line type="monotone" dataKey="tokens" stroke="#dc3b34"/></BarChart></ResponsiveContainer></ChartFrame>
    </section>
    <section className="mt-4 grid gap-3 xl:grid-cols-3"><ActivityFeed logs={logs} /><AlertsPanel alerts={alerts} /><div><h3 className="mb-2 text-sm text-brass">Settings Placeholder</h3><div className="lobster-panel space-y-2 p-3 text-xs">{['sound effects','desktop notifications','daily status reports','auto-refresh','compact mode','streamer overlay mode'].map(s=><label key={s} className="flex items-center justify-between"><span>{s}</span><input type="checkbox" defaultChecked className="accent-cyan-400"/></label>)}</div></div></section>
    <section className="mt-4"><h3 className="mb-2 text-brass">Agents</h3><div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">{filteredAgents.map((a)=><AgentCard key={a.name} agent={a as any} />)}</div></section>
    <section className="mt-4"><h3 className="mb-2 text-brass">Task Monitor</h3><TaskTable tasks={filteredTasks as any[]} /></section>
    <div className="fixed bottom-4 right-4 w-72"><MascotWidget /></div>
  </main></div></div>;
}
