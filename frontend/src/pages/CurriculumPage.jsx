import React, { useState, useEffect } from 'react';
import { BookOpen, CheckCircle, Circle, ChevronRight, Calculator, Calendar } from 'lucide-react';
import { Card } from '../components/Card';
import { api } from '../services/api';

export default function CurriculumPage() {
    const [curriculum, setCurriculum] = useState(null);

    // Initialize state from localStorage if available
    const [selectedMonth, setSelectedMonth] = useState(() => {
        return localStorage.getItem('lgs_curriculum_month') || null;
    });
    const [selectedSubject, setSelectedSubject] = useState(() => {
        return localStorage.getItem('lgs_curriculum_subject') || 'matematik';
    });

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [toggling, setToggling] = useState({}); // { topicId: boolean }

    const SUBJECTS = [
        { slug: 'matematik', name: 'Matematik', icon: Calculator },
        { slug: 'fen-bilimleri', name: 'Fen Bilimleri', icon: Circle },
        { slug: 'turkce', name: 'Türkçe', icon: BookOpen },
        { slug: 'tc-inkilap-tarihi', name: 'İnkılap Tarihi', icon: Calendar },
        { slug: 'din-kulturu', name: 'Din Kültürü', icon: BookOpen },
        { slug: 'yabanci-dil', name: 'Yabancı Dil', icon: BookOpen },
    ];

    // Persist Subject Selection
    useEffect(() => {
        if (selectedSubject) {
            localStorage.setItem('lgs_curriculum_subject', selectedSubject);
        }
    }, [selectedSubject]);

    // Persist Month Selection
    useEffect(() => {
        if (selectedMonth) {
            localStorage.setItem('lgs_curriculum_month', selectedMonth);
        }
    }, [selectedMonth]);

    useEffect(() => {
        fetchCurriculum(selectedSubject);
    }, [selectedSubject]);

    const fetchCurriculum = async (subjectSlug) => {
        try {
            setLoading(true);
            const data = await api.getCurriculum(subjectSlug);
            setCurriculum(data);

            // Ensure IDs are integers
            // SIMPLIFIED LOGIC: Always default to the first available month (September/9)
            // unless we have a persistent choice. This disables the "Auto-Select January" feature
            // that was causing confusion.

            let monthToSelect = null;

            // 1. Try to keep existing selection if valid
            if (selectedMonth) {
                const stillExists = data.months.find(m => Number(m.id) === Number(selectedMonth));
                if (stillExists) {
                    monthToSelect = stillExists.id;
                }
            }

            // 2. Fallback to "Smart" Active Month
            // Search for the first month that has incomplete topics
            if (!monthToSelect && data.months.length > 0) {
                let firstIncompleteMonth = null;

                for (const m of data.months) {
                    // Check all weeks in this month
                    const hasPending = m.weeks.some(w =>
                        w.topics.some(t => t.status !== 'completed')
                    );

                    if (hasPending) {
                        firstIncompleteMonth = m.id;
                        break; // Found the first month with work to do!
                    }
                }

                if (firstIncompleteMonth) {
                    console.log("Smart Select: Found pending work in Month", firstIncompleteMonth);
                    monthToSelect = firstIncompleteMonth;
                } else {
                    // If everything is completed, maybe show the last month? or the first?
                    // Let's show the last one (June) as victory!
                    // Or default to first if somehow empty.
                    monthToSelect = data.months[0].id;
                }
            }

            console.log("Setting Selected Month to:", monthToSelect);
            setSelectedMonth(monthToSelect);

        } catch (err) {
            console.error(err);
            setError("Müfredat yüklenirken bir hata oluştu.");
        } finally {
            setLoading(false);
        }
    };

    const handleToggle = async (topicId) => {
        if (toggling[topicId]) return;

        setToggling(prev => ({ ...prev, [topicId]: true }));
        try {
            const res = await api.toggleTopic(topicId);

            // Update local state with response (Wait-For-Response Logic)
            setCurriculum(prev => {
                if (!prev) return prev;
                const newMonths = prev.months.map(m => ({
                    ...m,
                    weeks: m.weeks.map(w => ({
                        ...w,
                        topics: w.topics.map(t => {
                            if (t.id === topicId) {
                                return { ...t, status: res.status };
                            }
                            return t;
                        })
                    }))
                }));
                return { ...prev, months: newMonths };
            });

        } catch (err) {
            console.error(err);
            alert("Hata: Değişiklik kaydedilemedi. Lütfen tekrar giriş yapmayı deneyin.");
            // Since we wait for response, the UI never changes to green if API fails.
            // But we should ensure the Spinner goes away.
        } finally {
            setToggling(prev => ({ ...prev, [topicId]: false }));
        }
    };

    // We keep the structure to allow Tabs to be visible even during loading? 
    // Actually, easy fix: if loading, show tabs + skeleton. 
    // For now, let's just stick to simple loading but maybe move tabs outside?
    // Let's keep the early return for now but maybe just make it less invasive.

    if (loading && !curriculum) return <div className="p-8 text-center text-slate-500">Müfredat yükleniyor...</div>;
    if (error) return <div className="p-8 text-center text-red-500">{error}</div>;
    if (!curriculum || !curriculum.months || curriculum.months.length === 0) return (
        <div className="p-8 text-center text-slate-500">
            Henüz müfredat verisi girilmemiş.
        </div>
    );

    // Filter current month data
    const currentMonthData = curriculum.months.find(m => Number(m.id) === Number(selectedMonth)) || curriculum.months[0];

    // Calculate progress
    const allTopics = currentMonthData ? currentMonthData.weeks.flatMap(w => w.topics) : [];
    const completedCount = allTopics.filter(t => t.status === 'completed').length;
    const progressPercent = allTopics.length > 0 ? Math.round((completedCount / allTopics.length) * 100) : 0;

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
                        <BookOpen className="text-blue-600" />
                        Müfredat Takibi
                    </h1>
                    <p className="text-slate-600">8. Sınıf {SUBJECTS.find(s => s.slug === selectedSubject)?.name} Konu Haritası</p>
                </div>

                {/* Ders Seçici Tabs */}
                <div className="flex bg-slate-100/50 p-1.5 rounded-2xl overflow-x-auto gap-2 mb-4 md:mb-0">
                    {SUBJECTS.map((sub) => {
                        const Icon = sub.icon;
                        const isActive = selectedSubject === sub.slug;
                        return (
                            <button
                                key={sub.slug}
                                onClick={() => setSelectedSubject(sub.slug)}
                                type="button"
                                className={`
                                    flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition-all whitespace-nowrap
                                    ${isActive
                                        ? 'bg-white text-blue-600 shadow-sm ring-1 ring-black/5'
                                        : 'text-slate-600 hover:bg-white/50 hover:text-slate-900'
                                    }
                                `}
                            >
                                <Icon size={16} className={isActive ? "text-blue-500" : "text-slate-400"} />
                                {sub.name}
                            </button>
                        );
                    })}
                </div>

                {/* Ay Seçici - Only show if curriculum loads */}
                {curriculum && (
                    <div className="flex bg-white p-1 rounded-xl border border-slate-200 shadow-sm overflow-x-auto">
                        {curriculum.months.map(month => (
                            <button
                                key={month.id}
                                onClick={(e) => {
                                    e.preventDefault(); // Extra safety
                                    console.log("Clicked Month Explicitly:", month.id);
                                    setSelectedMonth(Number(month.id));
                                }}
                                type="button"
                                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${Number(selectedMonth) === Number(month.id)
                                    ? 'bg-blue-600 text-white shadow-md'
                                    : 'text-slate-600 hover:bg-slate-50'
                                    }`}
                            >
                                {month.name}
                            </button>
                        ))}
                    </div>
                )}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Sol Taraf: Zaman Çizelgesi */}
                <div className="lg:col-span-2 space-y-6">
                    {currentMonthData.weeks.map((week, index) => (
                        <div key={week.week_number} className="relative pl-8 pb-8 last:pb-0">
                            {/* Dikey Çizgi */}
                            {index !== currentMonthData.weeks.length - 1 && (
                                <div className="absolute left-[15px] top-8 bottom-0 w-0.5 bg-slate-200"></div>
                            )}

                            {/* Hafta Başlığı */}
                            <div className="absolute left-0 top-1 w-8 h-8 rounded-full bg-blue-100 border-4 border-white shadow-sm flex items-center justify-center font-bold text-blue-600 text-sm z-10">
                                {week.week_number}
                            </div>

                            <Card>
                                <div className="p-5">
                                    <div className="flex items-center justify-between mb-4 pb-4 border-b border-slate-100">
                                        <div>
                                            <span className="text-xs font-bold text-blue-600 uppercase tracking-wider mb-1 block">
                                                {week.week_number}. Hafta
                                            </span>
                                            <h3 className="font-bold text-lg text-slate-800 flex items-center gap-2">
                                                {week.focus}
                                            </h3>
                                        </div>
                                        <div className="p-2 bg-slate-50 rounded-lg text-slate-400">
                                            <Calculator size={20} />
                                        </div>
                                    </div>

                                    <div className="space-y-3">
                                        {week.topics.map(topic => (
                                            <div
                                                key={topic.id}
                                                className={`flex items-center gap-3 p-3 rounded-xl border transition-all cursor-pointer ${topic.status === 'completed'
                                                    ? 'bg-emerald-50 border-emerald-100'
                                                    : 'bg-white border-slate-100 hover:border-blue-200 hover:shadow-sm'
                                                    }`}
                                                onClick={() => handleToggle(topic.id)}
                                            >
                                                <button
                                                    className="shrink-0 transition-colors"
                                                    disabled={toggling[topic.id]}
                                                >
                                                    {toggling[topic.id] ? (
                                                        <div className="w-[22px] h-[22px] rounded-full border-2 border-slate-200 border-t-blue-500 animate-spin"></div>
                                                    ) : topic.status === 'completed' ? (
                                                        <CheckCircle className="text-emerald-500" size={22} />
                                                    ) : (
                                                        <Circle className="text-slate-300 hover:text-blue-500" size={22} />
                                                    )}
                                                </button>
                                                <div className="flex-1 select-none">
                                                    <p className={`text-sm font-medium ${topic.status === 'completed' ? 'text-emerald-900 line-through decoration-emerald-500/30' : 'text-slate-700'
                                                        }`}>
                                                        {topic.title}
                                                    </p>
                                                </div>
                                                {topic.status !== 'completed' && (
                                                    <ChevronRight size={16} className="text-slate-300" />
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </Card>
                        </div>
                    ))}
                </div>

                {/* Sağ Taraf: Özet ve İstatistik */}
                <div className="space-y-6">
                    <Card>
                        <div className="p-5 bg-linear-to-br from-slate-900 to-slate-800 text-white rounded-t-2xl">
                            <h3 className="font-bold text-lg mb-1">Aylık Durum</h3>
                            <p className="text-slate-300 text-sm">{currentMonthData.name} Ayı İlerlemesi</p>
                        </div>
                        <div className="p-6">
                            <div className="mb-6">
                                <div className="flex justify-between text-sm font-medium mb-2">
                                    <span className="text-slate-700">Tamamlanan</span>
                                    <span className="text-blue-600">%{progressPercent}</span>
                                </div>
                                <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-blue-600 rounded-full transition-all duration-500"
                                        style={{ width: `${progressPercent}%` }}
                                    ></div>
                                </div>
                            </div>

                            <div className="space-y-4">
                                <div className="flex items-start gap-3">
                                    <div className="p-2 bg-blue-50 text-blue-600 rounded-lg">
                                        <Calendar size={20} />
                                    </div>
                                    <div>
                                        <p className="text-xs text-slate-500 font-medium">ŞU ANKİ ODAK</p>
                                        <p className="font-semibold text-slate-800">{currentMonthData.weeks[0]?.focus || "Genel Tekrar"}</p>
                                    </div>
                                </div>
                            </div>

                            <button
                                onClick={() => fetchCurriculum(selectedSubject)}
                                className="w-full mt-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-medium transition-colors shadow-lg shadow-blue-600/20 active:scale-95"
                            >
                                Çalışma Planımı Güncelle
                            </button>
                        </div>
                    </Card>

                    <div className="bg-amber-50 border border-amber-100 rounded-2xl p-4">
                        <h4 className="font-bold text-amber-800 text-sm mb-2">💡 Koç Tavsiyesi</h4>
                        <p className="text-sm text-amber-700/80 leading-relaxed">
                            {progressPercent < 50
                                ? "Ayın başındayız. Tempolu bir giriş yaparak ilk konuları erkenden bitirmeni öneririm."
                                : "Harika gidiyorsun! Konuların yarısını tamamladın. Soru çözümleriyle pekiştirmeyi unutma."}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
