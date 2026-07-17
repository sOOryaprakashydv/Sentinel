import { NavLink } from "react-router-dom";
import {
  LuLayoutDashboard, LuUpload, LuSearch, LuFileText, LuSettings, LuShieldCheck,
} from "react-icons/lu";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", icon: LuLayoutDashboard, end: true },
  { to: "/upload", label: "Upload", icon: LuUpload },
  { to: "/investigations", label: "Investigations", icon: LuSearch },
  { to: "/reports", label: "Reports", icon: LuFileText },
  { to: "/settings", label: "Settings", icon: LuSettings },
];

export default function Sidebar() {
  return (
    <aside className="w-64 shrink-0 h-full bg-ink-900 text-ink-100 flex flex-col">
      <div className="flex items-center gap-2.5 px-6 py-6">
        <div className="w-9 h-9 rounded-lg bg-primary-600 flex items-center justify-center">
          <LuShieldCheck className="text-white" size={20} />
        </div>
        <div>
          <div className="font-display font-bold text-white text-lg leading-none">Sentinel</div>
          <div className="text-[11px] text-ink-300 tracking-wide mt-0.5">Investigation Platform</div>
        </div>
      </div>

      <nav className="flex-1 px-3 mt-4 space-y-1">
        {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? "bg-primary-600 text-white"
                  : "text-ink-300 hover:bg-white/5 hover:text-white"
              }`
            }
          >
            <Icon size={18} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="px-6 py-5 border-t border-white/10 text-[11px] text-ink-300">
        Demo build · v1.0
      </div>
    </aside>
  );
}
