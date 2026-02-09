import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, BookOpen, GraduationCap, Settings, Menu, TrendingUp, LogOut } from 'lucide-react';
import clsx from 'clsx';
import { useState } from 'react';
import { useStudent } from '../../context/StudentContext';

const SidebarItem = ({ icon: Icon, label, path, active }) => (
  <Link
    to={path}
    className={clsx(
      "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group",
      active
        ? "bg-blue-600 text-white shadow-lg shadow-blue-500/30"
        : "text-slate-500 hover:bg-white hover:text-blue-600"
    )}
  >
    <Icon size={20} className={active ? "text-white" : "text-slate-400 group-hover:text-blue-600"} />
    <span className="font-medium">{label}</span>
  </Link>
);

export default function Layout({ children }) {
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { logout } = useStudent();

  const navItems = [
    { label: 'Dashboard', path: '/', icon: LayoutDashboard },
    { label: 'Günlük Plan', path: '/plan', icon: BookOpen },
    { label: 'Müfredat Takip', path: '/curriculum', icon: BookOpen },
    { label: 'Deneme Sınavları', path: '/exams', icon: GraduationCap },
    { label: 'Gelişim Analizi', path: '/analytics', icon: TrendingUp },
    { label: 'Ayarlar', path: '/settings', icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-slate-50 flex font-sans">
      {/* Sidebar */}
      <aside className={clsx(
        "fixed inset-y-0 left-0 z-50 w-72 bg-slate-50/50 backdrop-blur-xl border-r border-slate-200/60 p-6 transition-transform duration-300 lg:translate-x-0 lg:static",
        isMobileMenuOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex items-center gap-3 px-2 mb-10">
          <div className="w-10 h-10 rounded-xl bg-linear-to-br from-blue-600 to-indigo-600 flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-blue-500/30">
            A
          </div>
          <div>
            <h1 className="text-lg font-bold text-slate-900 tracking-tight">Akıllı Koç</h1>
            <p className="text-xs text-slate-500 font-medium">Öğrenci Asistanı</p>
          </div>
        </div>

        <nav className="space-y-2">
          {navItems.map((item) => (
            <SidebarItem
              key={item.path}
              {...item}
              active={location.pathname === item.path}
            />
          ))}
        </nav>

        <div className="absolute bottom-8 left-6 right-6 space-y-4">
          <button
            onClick={logout}
            className="flex items-center gap-3 px-4 py-3 rounded-xl text-red-500 hover:bg-red-50 hover:text-red-600 transition-all font-medium w-full"
          >
            <LogOut size={20} />
            <span>Çıkış Yap</span>
          </button>

          <div className="p-4 rounded-2xl bg-linear-to-br from-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-500/25">
            <p className="text-xs font-medium opacity-80 mb-1">Hedefine Kalan</p>
            <div className="flex items-end justify-between">
              <span className="text-2xl font-bold">
                {Math.ceil((new Date('2026-06-07') - new Date()) / (1000 * 60 * 60 * 24))} Gün
              </span>
              <span className="text-xs bg-white/20 px-2 py-1 rounded-lg">LGS 2026</span>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 min-w-0">
        <div className="lg:hidden p-4 flex items-center justify-between bg-white/80 backdrop-blur-md sticky top-0 z-40 border-b border-slate-100">
          <h1 className="font-bold text-slate-800">Akıllı Koç</h1>
          <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="p-2 text-slate-600">
            <Menu />
          </button>
        </div>

        <div className="p-4 sm:p-6 lg:p-8 max-w-6xl mx-auto">
          {children}
        </div>
      </main>

      {/* Overlay for mobile */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 lg:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}
    </div>
  );
}
