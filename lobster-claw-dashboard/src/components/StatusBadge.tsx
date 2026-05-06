interface Props { label: string; tone?: 'ok'|'warn'|'bad'; }
export default function StatusBadge({ label, tone='ok' }: Props) {
  const cls = tone === 'ok' ? 'bg-emerald-500/20 text-emerald-200' : tone === 'warn' ? 'bg-amber-500/20 text-amber-200' : 'bg-red-500/20 text-red-200';
  return <span className={`rounded-full px-2 py-1 text-xs font-semibold ${cls}`}>{label}</span>;
}
