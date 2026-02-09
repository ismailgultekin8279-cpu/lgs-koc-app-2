
import { CheckCircle2, Trophy, Target, ArrowUpRight } from 'lucide-react';
import { useStudent } from '../context/StudentContext';
import { api } from '../services/api';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import NetScoreChart from '../components/NetScoreChart';

const StatCard = ({ icon: Icon, label, value, trend, trendUp, color }) => (
    <div className="glass-card p-6 flex items-start justify-between relative overflow-hidden group">
        <div className={`absolute top-0 right-0 w-24 h-24 -mr-4 -mt-4 rounded-full opacity-10 transition-transform group-hover:scale-110 ${color}`}></div>
        <div>
            <p className="text-sm font-medium text-slate-500 mb-1">{label}</p>
            <h3 className="text-3xl font-bold text-slate-800">{value}</h3>
            {trend && (
                <div className={`flex items-center gap-1 mt-2 text-xs font-semibold ${trendUp ? 'text-green-600' : 'text-red-500'}`}>
                    {trendUp ? <ArrowUpRight size={14} /> : null}
                    {trend}
                </div>
            )}
        </div>
        <div className={`p-3 rounded-xl ${color} text-white shadow-lg`}>
            <Icon size={24} />
        </div>
    </div>
);

export default function Dashboard() {
    const { student } = useStudent();
    const [latestNet, setLatestNet] = useState('---');
    const [netTrend, setNetTrend] = useState(null);
    const [todaysTasks, setTodaysTasks] = useState([]);
    const [coachMessage, setCoachMessage] = useState(null);
    const [examHistory, setExamHistory] = useState([]);
    const [latestScore, setLatestScore] = useState(0);

    const [isUpdating, setIsUpdating] = useState(false);

    useEffect(() => {
        if (student?.id) {
            fetchStats();
        }
    }, [student?.id]);

    // Format data for chart
    const fetchStats = async () => {
        try {
            // 1. Latest Exams
            const exams = await api.getLatestExam(student.id);
            if (exams && exams.length > 0) {
                // Group by exam date to find the absolute latest set of results
                const latestDate = exams[0].exam_date;
                const latestExamSubjects = exams.filter(e => e.exam_date === latestDate);

                const totalNet = latestExamSubjects.reduce((sum, sub) => sum + (parseFloat(sub.net) || 0), 0);
                setLatestNet(totalNet.toFixed(2));

                // REALIST LGS SCORING ENGINE (Approximation based on coefficients)
                const mainSubjs = ["Matematik", "Fen Bilimleri", "Türkçe"];
                let weightedNet = 0;
                latestExamSubjects.forEach(s => {
                    const coef = mainSubjs.includes(s.subject) ? 4.3 : 1.3;
                    weightedNet += (parseFloat(s.net) || 0) * coef;
                });

                // LGS Base Score is approx 194. Let's use 200 as midpoint. Max weighted net approx 300.
                const estimatedScore = Math.min(500, Math.round(195 + (weightedNet * 0.95)));
                setLatestScore(estimatedScore);

                // Simple trend logic
                setNetTrend("Son deneme sonucu");

                // For chart: aggregate by date
                const history = {};
                exams.forEach(e => {
                    if (!history[e.exam_date]) history[e.exam_date] = 0;
                    history[e.exam_date] += parseFloat(e.net) || 0;
                });

                // Convert back to array
                const chartData = Object.keys(history).map(date => ({
                    exam_date: date,
                    net: history[date].toFixed(2)
                })).sort((a, b) => new Date(b.exam_date) - new Date(a.exam_date)); // DESC

                setExamHistory(chartData);
            }

            // 2. Tasks
            const tasks = await api.getStudentTasks(student.id, new Date().toISOString().split('T')[0]);
            setTodaysTasks(tasks);

            // 3. Coach Status
            const status = await api.getCoachStatus(student.id);
            if (status?.message) {
                setCoachMessage({
                    title: "Koç'un Tavsiyesi",
                    text: status.message,
                    action: "Programa Git"
                });
            } else if (status?.weaknesses && status.weaknesses.length > 0) {
                setCoachMessage({
                    title: "Gelişim Fırsatı",
                    text: `Son analizlerimde ${status.weaknesses[0]} dersinde zorlandığını görüyorum. Senin için bugünkü programa ekstra pratik ekledim.`,
                    action: "Programa Git"
                });
            } else {
                setCoachMessage({
                    title: "Harika Gidiyorsun!",
                    text: "Sonuçların gayet dengeli görünüyor. Mevcut çalışma planına sadık kalarak yükselişini sürdürebilirsin.",
                    action: "Planı İncele"
                });
            }

        } catch (err) {
            console.error(err);
        } finally {
            setIsUpdating(false);
        }
    };

    return (
        <div className="max-w-6xl mx-auto space-y-8">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-slate-900">Hoş geldin, {student?.full_name || 'Öğrenci'}! 👋</h1>
                <p className="text-slate-500 mt-2">Bugünün hedeflerini tamamla ve hedefine bir adım daha yaklaş.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <StatCard
                    icon={Target}
                    label="Hedef Puan"
                    value={student?.target_score || '---'}
                    // Higher realism: Progress is (Estimated Score / Target Score)
                    trend={`Hedefe %${student?.target_score > 0 ? Math.min(100, Math.round((latestScore / student.target_score) * 100)) : 0} Ulaşıldı`}
                    trendUp={true}
                    color="bg-purple-600"
                />
                <StatCard
                    icon={Trophy}
                    label="Son Deneme Neti"
                    value={latestNet}
                    trend={netTrend || "Henüz veri yok"}
                    trendUp={true}
                    color="bg-blue-600"
                />
                <StatCard
                    icon={CheckCircle2}
                    label="Tamamlanan Görev"
                    value={`${todaysTasks.filter(t => t.status === 'done').length}/${todaysTasks.length}`}
                    trend={`%${todaysTasks.length > 0 ? Math.round((todaysTasks.filter(t => t.status === 'done').length / todaysTasks.length) * 100) : 0} Günlük Başarı`}
                    trendUp={true}
                    color="bg-emerald-500"
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Today's Tasks */}
                <div className="glass-card p-6">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                        <div className="flex items-center gap-3">
                            <h3 className="text-lg font-bold text-slate-900">Bugünün Programı</h3>
                            <button
                                onClick={async (e) => {
                                    e.preventDefault();
                                    e.stopPropagation();
                                    if (isUpdating) return;
                                    setIsUpdating(true);
                                    try {
                                        await api.generatePlan(student.id);
                                        await fetchStats();
                                        alert("Program başarıyla güncellendi! 🚀");
                                    } catch (err) {
                                        alert("Güncellenemedi: " + err.message);
                                        setIsUpdating(false);
                                    }
                                }}
                                disabled={isUpdating}
                                className={`text-[11px] font-bold px-4 py-2 rounded-2xl transition-all shadow-md flex items-center gap-2 ${isUpdating
                                    ? 'bg-slate-200 text-slate-500 cursor-not-allowed scale-95'
                                    : 'bg-indigo-600 text-white hover:bg-indigo-700 active:scale-90 hover:shadow-indigo-500/20'
                                    }`}
                            >
                                {isUpdating ? (
                                    <>
                                        <div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                                        <span>Güncelleniyor...</span>
                                    </>
                                ) : (
                                    <>
                                        <span>🔄 Programı Güncelle</span>
                                    </>
                                )}
                            </button>
                        </div>
                    </div>

                    <div className="space-y-4">
                        {todaysTasks.length === 0 ? (
                            <div className="text-center py-8">
                                <p className="text-slate-500 text-sm italic mb-4">Bugün için henüz görev oluşturulmamış.</p>
                                <button
                                    onClick={async () => {
                                        try {
                                            await api.generatePlan(student.id);
                                            // Refresh stats to get the new tasks
                                            fetchStats();
                                        } catch (e) { console.error(e); alert("Plan oluşturulamadı"); }
                                    }}
                                    className="text-sm font-bold text-blue-600 hover:text-blue-700 bg-blue-50 px-4 py-2 rounded-lg"
                                >
                                    ⚡ Planı Oluştur
                                </button>
                            </div>
                        ) : (
                            todaysTasks.map((task) => (
                                <div
                                    key={task.id}
                                    className={`flex items-center gap-4 p-4 rounded-xl border transition-all cursor-pointer hover:shadow-md ${task.status === 'done'
                                        ? 'bg-emerald-50 border-emerald-200 opacity-75'
                                        : 'bg-slate-50 border-slate-100 hover:border-blue-200'
                                        }`}
                                    onClick={async () => {
                                        try {
                                            const updated = await api.toggleTaskStatus(task.id);
                                            setTodaysTasks(prev => prev.map(t => t.id === task.id ? updated : t));
                                        } catch (err) {
                                            console.error("Task update failed", err);
                                        }
                                    }}
                                >
                                    <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${task.status === 'done'
                                        ? 'bg-emerald-500 border-emerald-500 text-white'
                                        : 'border-slate-300 group-hover:border-blue-500'
                                        }`}>
                                        {task.status === 'done' && <CheckCircle2 size={16} />}
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <p className="text-[10px] font-bold uppercase tracking-wider text-blue-600 mb-0.5 opacity-80">
                                            {task.subject}
                                        </p>
                                        <p className={`font-semibold truncate ${task.status === 'done' ? 'text-slate-500 line-through' : 'text-slate-800'}`}>
                                            {task.topic_name || "Genel Çalışma"}
                                        </p>
                                        <p className="text-xs text-slate-500">{task.question_count} Soru • {Math.round(task.recommended_seconds / 60)} Dakika</p>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>

                {/* Coach Suggestion */}
                <div className="glass-card p-6 bg-linear-to-br from-indigo-900 to-slate-900 text-white relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500 rounded-full blur-3xl opacity-20 -mr-16 -mt-16"></div>

                    <div className="relative z-10">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">💡</div>
                            <h3 className="font-bold text-lg">Koç'un Tavsiyesi</h3>
                        </div>

                        <p className="text-indigo-100 leading-relaxed mb-6">
                            {coachMessage ? coachMessage.text : "Verilerini analiz ediyorum..."}
                        </p>

                        <Link to="/plan" className="block w-full">
                            <button className="w-full py-3 rounded-xl bg-white text-indigo-900 font-bold hover:bg-indigo-50 transition-colors">
                                {coachMessage ? coachMessage.action : "Bekleyiniz"}
                            </button>
                        </Link>
                    </div>
                </div>
            </div>

            {/* Charts Area */}
            <div className="md:col-span-2 glass-card p-6 mt-6">
                <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-bold text-slate-900">Net Gelişim Grafiği</h3>
                    <Link to="/exams" className="text-sm font-medium text-blue-600 hover:text-blue-700">Yeni Deneme Gir</Link>
                </div>
                <NetScoreChart data={examHistory} />
            </div>
        </div>
    );
}
