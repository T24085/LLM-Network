export type AgentStatus = 'active' | 'idle' | 'error';
export type TaskStatus = 'queued' | 'running' | 'done' | 'failed';

export const dashboardStatus = {
  project: 'OpenClaw Local Rig',
  openClaw: 'Connected',
  localServer: 'Localhost only',
  currentModel: 'gpt-4.1-mini',
};

export const agents = [
  { name: 'CaptainClaw', role: 'Planner', status: 'active', activeTask: 'Route tasks', model: 'gpt-4.1', tokenUsage: 440, uptime: '4h 12m', health: 95, lastAction: 'Spawned worker' },
  { name: 'BarnacleBot', role: 'Coder', status: 'idle', activeTask: 'Patch parser', model: 'gpt-4.1-mini', tokenUsage: 220, uptime: '2h 40m', health: 88, lastAction: 'Completed task #117' },
  { name: 'ReefWatch', role: 'Monitor', status: 'error', activeTask: 'Inspect loop', model: 'gpt-4.1-nano', tokenUsage: 180, uptime: '7h 09m', health: 61, lastAction: 'Loop warning emitted' },
] as const;

export const tasks = [
  { id: 'T-117', name: 'Fix routing logic', assignedAgent: 'BarnacleBot', status: 'running', startedTime: '10:41', duration: '00:12:44', tokenUsage: 1320, errors: 0 },
  { id: 'T-118', name: 'Scrape worker stats', assignedAgent: 'CaptainClaw', status: 'queued', startedTime: '10:53', duration: '00:00:00', tokenUsage: 0, errors: 0 },
  { id: 'T-119', name: 'Generate summary', assignedAgent: 'ReefWatch', status: 'failed', startedTime: '09:21', duration: '00:18:12', tokenUsage: 1560, errors: 2 },
] as const;

export const workers = [{ health: 91 }, { health: 84 }, { health: 77 }];
export const memoryStats = { usedGb: 9.8, totalGb: 16 };

export const tokenUsage = [
  { time: '10:00', tokens: 1200, cpu: 35 },
  { time: '10:10', tokens: 1900, cpu: 48 },
  { time: '10:20', tokens: 2300, cpu: 51 },
  { time: '10:30', tokens: 1700, cpu: 44 },
  { time: '10:40', tokens: 2600, cpu: 63 },
  { time: '10:50', tokens: 2900, cpu: 68 },
];

export const logs = [
  { event: 'task started', detail: 'T-117 by BarnacleBot' },
  { event: 'task completed', detail: 'T-114 complete' },
  { event: 'agent spawned', detail: 'CaptainClaw child worker online' },
  { event: 'error detected', detail: 'ReefWatch token parser' },
  { event: 'loop warning', detail: 'Retry cycle > 8' },
  { event: 'worker connected', detail: 'worker-07 attached' },
  { event: 'memory updated', detail: '9.8GB used' },
];

export const alerts = [
  'loop detected',
  'high token burn',
  'failed task',
  'disconnected worker',
  'memory limit warning',
];

export const networkNodes = ['Planner', 'Coder', 'Monitor', 'Worker-1', 'Worker-2'];
