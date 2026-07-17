import type { IconType } from "react-icons";

interface Props {
  label: string;
  value: string | number;
  icon: IconType;
  tone?: "primary" | "success" | "warning" | "critical" | "neutral";
}

const TONE_STYLES: Record<string, string> = {
  primary: "bg-primary-50 text-primary-700",
  success: "bg-success-50 text-success-700",
  warning: "bg-warning-50 text-warning-700",
  critical: "bg-critical-50 text-critical-700",
  neutral: "bg-ink-100 text-ink-700",
};

export default function StatCard({ label, value, icon: Icon, tone = "neutral" }: Props) {
  return (
    <div className="panel p-5 flex items-start justify-between">
      <div>
        <div className="text-xs font-medium text-ink-500 uppercase tracking-wide">{label}</div>
        <div className="text-3xl font-display font-bold text-ink-900 mt-2">{value}</div>
      </div>
      <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${TONE_STYLES[tone]}`}>
        <Icon size={20} />
      </div>
    </div>
  );
}
