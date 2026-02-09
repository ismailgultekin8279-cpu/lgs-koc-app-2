import React, { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Sparkles, Quote } from "lucide-react";
import { Card, CardHeader, CardBody, InfoBox } from "../components/Card";
import { getDailyPlan, getCoaching, patchTask, generatePlan } from "../lib/endpoints";

/* ---------- helpers ---------- */

function normalizeDailyPlan(data) {
  if (!data) return [];
  if (Array.isArray(data)) return data;
  if (Array.isArray(data.tasks)) return data.tasks;
  if (Array.isArray(data.results)) return data.results;
  return [];
}

function statusBadge(status) {
  const s = String(status || "").toLowerCase();
  if (s === "done") {
    return {
      text: "Tamamlandı",
      cls: "bg-emerald-50 text-emerald-700 border-emerald-100",
    };
  }
  return {
    text: "Bekliyor",
    cls: "bg-slate-50 text-slate-700 border-slate-100",
  };
}

function normalizeCoaching(data) {
  if (!data) return { title: null, lines: [] };

  if (typeof data === "string") return { title: null, lines: [data] };

  if (Array.isArray(data)) {
    const lines = data
      .map((x) => {
        if (typeof x === "string") return x;
        if (!x || typeof x !== "object") return null;
        return x.message || x.text || x.recommendation || x.tip || null;
      })
      .filter(Boolean);
    return { title: null, lines: lines.length ? lines : ["Öneri bulunamadı."] };
  }

  const title = data.title || data.header || null;
  const single =
    data.message || data.text || data.recommendation || data.tip || data.note || null;

  const list =
    data.messages || data.recommendations || data.tips || data.items || null;

  if (typeof single === "string" && single.trim()) return { title, lines: [single] };

  if (Array.isArray(list)) {
    const lines = list
      .map((x) => {
        if (typeof x === "string") return x;
        if (!x || typeof x !== "object") return null;
        return x.message || x.text || x.recommendation || x.tip || null;
      })
      .filter(Boolean);
    return { title, lines: lines.length ? lines : ["Öneri bulunamadı."] };
  }

  return { title, lines: ["Öneri bulunamadı."] };
}

/* ---------- page ---------- */

import { useStudent } from "../context/StudentContext";

export default function StudentDashboard({ selectedStudentId }) {
  const qc = useQueryClient();
  const [pendingTaskId, setPendingTaskId] = useState(null);
  const { student } = useStudent();

  // If provided prop is null, try to use the logged-in student's ID
  // This allows the component to work for both Coaches (selecting a student) and Students (viewing themselves)
  const studentId = selectedStudentId || student?.id;

  // Daily plan
  const {
    data: dailyPlanRaw,
    isLoading: dailyLoading,
    isError: dailyError,
    refetch: refetchDaily,
  } = useQuery({
    queryKey: ["dailyPlan", studentId],
    queryFn: () => getDailyPlan(studentId),
    enabled: Boolean(studentId),
  });

  const tasks = useMemo(() => normalizeDailyPlan(dailyPlanRaw), [dailyPlanRaw]);

  const { totalCount, doneCount, pendingCount } = useMemo(() => {
    const total = tasks.length;
    const done = tasks.filter(
      (t) => String(t?.status || "").toLowerCase() === "done"
    ).length;
    return { totalCount: total, doneCount: done, pendingCount: total - done };
  }, [tasks]);

  // Coaching
  const {
    data: coachingRaw,
    isLoading: coachingLoading,
    isError: coachingError,
    refetch: refetchCoaching,
  } = useQuery({
    queryKey: ["coaching", studentId],
    queryFn: () => getCoaching(studentId),
    enabled: Boolean(studentId),
  });

  const coaching = useMemo(() => normalizeCoaching(coachingRaw), [coachingRaw]);

  // Generate Plan Mutation
  const generatePlanMutation = useMutation({
    mutationFn: () => generatePlan(studentId),
    onSuccess: () => {
      qc.invalidateQueries(["dailyPlan", studentId]);
      qc.invalidateQueries(["coaching", studentId]);
    },
    onError: (err) => {
      console.error("Plan generation failed:", err);
      alert("Plan oluşturulurken bir hata oluştu: " + err.message);
    }
  });

  // Toggle task (optimistic + kalıcı)
  const toggleTask = useMutation({
    mutationFn: ({ taskId, newStatus }) => patchTask(taskId, { status: newStatus }),

    onMutate: async ({ taskId, newStatus }) => {
      setPendingTaskId(taskId);

      await qc.cancelQueries({ queryKey: ["dailyPlan", studentId] });
      const previous = qc.getQueryData(["dailyPlan", studentId]);

      qc.setQueryData(["dailyPlan", studentId], (old) => {
        const list = normalizeDailyPlan(old);
        return list.map((t) => (t.id === taskId ? { ...t, status: newStatus } : t));
      });

      return { previous };
    },

    onError: (_err, _vars, context) => {
      if (context?.previous) {
        qc.setQueryData(["dailyPlan", studentId], context.previous);
      }
    },

    onSettled: () => {
      setPendingTaskId(null);
      qc.invalidateQueries({ queryKey: ["dailyPlan", studentId] });
    },
  });

  // Grouping tasks by date
  const groupedTasks = useMemo(() => {
    const groups = {};
    tasks.forEach((t) => {
      const d = t.date || "Bugün";
      if (!groups[d]) groups[d] = [];
      groups[d].push(t);
    });
    // Sort by date key
    const sortedDates = Object.keys(groups).sort();
    const result = {};
    sortedDates.forEach(date => {
      result[date] = groups[date];
    });
    return result;
  }, [tasks]);

  const getDayLabel = (dateStr) => {
    if (!dateStr || dateStr === "Bugün") return "Bugün";
    try {
      const taskDate = new Date(dateStr);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      taskDate.setHours(0, 0, 0, 0);

      const diffTime = taskDate.getTime() - today.getTime();
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

      const dayName = taskDate.toLocaleDateString('tr-TR', { weekday: 'long' });

      if (diffDays === 0) return `Bugün (${dayName})`;
      if (diffDays === 1) return `Yarın (${dayName})`;

      return dayName;
    } catch (e) {
      return dateStr;
    }
  };

  if (!studentId) {
    return (
      <Card>
        <CardHeader title="Öğrenci Paneli" subtitle="Haftalık plan + koç mesajı" />
        <CardBody>
          <InfoBox
            title="Öğrenci seçiniz"
            description="Öğrenci seçildiğinde haftalık plan ve koç mesajı burada görünecek."
          />
        </CardBody>
      </Card>
    );
  }

  // Extract focus from coaching response
  const currentFocus = coachingRaw?.current_focus || "LGS Hazırlık";

  return (
    <div className="space-y-6">
      {/* Koç Mesajı - Banner Style */}
      <div className="relative overflow-hidden rounded-3xl bg-linear-to-br from-violet-600 to-indigo-600 p-1 shadow-xl shadow-indigo-500/20">
        <div className="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-white/10 blur-xl"></div>
        <div className="absolute bottom-0 left-0 -mb-4 -ml-4 h-24 w-24 rounded-full bg-black/10 blur-xl"></div>

        <div className="relative h-full rounded-[20px] bg-slate-900/40 backdrop-blur-sm p-6 text-white flex flex-col md:flex-row items-center gap-6">
          <div className="flex shrink-0 h-16 w-16 items-center justify-center rounded-2xl bg-white/20 shadow-inner">
            <Sparkles className="h-8 w-8 text-yellow-300" />
          </div>

          <div className="flex-1 text-center md:text-left">
            <div className="flex items-center justify-center md:justify-start gap-3 mb-2">
              <h3 className="font-bold text-xl leading-tight">Yapay Zeka Koçun</h3>
              {currentFocus && (
                <span className="text-[10px] font-bold uppercase tracking-wider bg-white/20 px-2 py-0.5 rounded-full border border-white/10">
                  {currentFocus}
                </span>
              )}
            </div>

            {coachingLoading ? (
              <div className="flex items-center justify-center md:justify-start gap-2 text-sm text-indigo-200 animate-pulse">
                <div className="h-2 w-2 rounded-full bg-indigo-400 animate-bounce"></div>
                <div className="h-2 w-2 rounded-full bg-indigo-400 animate-bounce delay-75"></div>
                <div className="h-2 w-2 rounded-full bg-indigo-400 animate-bounce delay-150"></div>
                Analiz ediliyor...
              </div>
            ) : coachingError ? (
              <div className="flex items-center gap-3">
                <span className="text-red-200 text-sm">Mesaj alınamadı.</span>
                <button onClick={() => refetchCoaching()} className="underline text-xs">Tekrar Dene</button>
              </div>
            ) : (
              <div className="relative">
                <Quote className="absolute -top-3 -left-4 h-6 w-6 text-white/10 rotate-180 hidden md:block" />
                {coaching.lines.length === 0 ? (
                  <p className="text-indigo-100 italic">Henüz bir mesajın yok.</p>
                ) : (
                  <div className="space-y-1">
                    {coaching.title && <h4 className="font-semibold text-indigo-50">{coaching.title}</h4>}
                    {coaching.lines.map((line, idx) => (
                      <p key={idx} className="text-lg md:text-xl font-medium leading-relaxed text-indigo-50">
                        "{line}"
                      </p>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Çalışma Planı - Grouped by Day */}
      <Card>
        <CardHeader
          title="Haftalık Çalışma Planı"
          subtitle="Öğrenciye özel 7 günlük gelişim rotası"
          right={
            <button
              onClick={() => generatePlanMutation.mutate()}
              disabled={generatePlanMutation.isPending}
              className="text-sm bg-blue-600 text-white px-4 py-2 rounded-xl hover:bg-blue-700 shadow-lg shadow-blue-500/30 transition-all active:scale-95 disabled:opacity-50 flex items-center gap-2 font-bold"
            >
              <Sparkles size={16} />
              {generatePlanMutation.isPending ? "Oluşturuluyor..." : "Planı Yenile"}
            </button>
          }
        />
        <CardBody>
          {dailyLoading ? (
            <div className="text-sm text-slate-600 px-4 py-8 text-center">Plan yükleniyor...</div>
          ) : dailyError ? (
            <div className="text-center py-8">
              <p className="text-red-500 mb-4">Plan alınamadı.</p>
              <button className="btn-secondary" onClick={() => refetchDaily()}>Tekrar Dene</button>
            </div>
          ) : tasks.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-slate-500 mb-6 font-medium">Şu an aktif bir çalışma planın yok.</p>
              <button
                onClick={() => generatePlanMutation.mutate()}
                disabled={generatePlanMutation.isPending}
                className="bg-blue-600 text-white px-8 py-3 rounded-2xl hover:bg-blue-700 shadow-xl shadow-blue-600/30 font-bold transition-all hover:scale-105 active:scale-95"
              >
                {generatePlanMutation.isPending ? "Analiz Ediliyor..." : "✨ Planımı Hemen Oluştur"}
              </button>
            </div>
          ) : (
            <div className="space-y-10">
              {/* Stats Bar */}
              <div className="flex flex-wrap items-center gap-3 text-sm text-slate-600 pb-4 border-b border-slate-100">
                <span className="rounded-full border border-slate-200 px-3 py-1 bg-white">
                  Toplam Görev: <span className="font-bold text-slate-900">{totalCount}</span>
                </span>
                <span className="rounded-full border border-emerald-200 px-3 py-1 bg-emerald-50 text-emerald-700">
                  Tamamlanan: <span className="font-bold">{doneCount}</span>
                </span>
                <div className="ml-auto flex items-center gap-2">
                  <div className="w-32 h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500 transition-all duration-500" style={{ width: `${(doneCount / totalCount) * 100}%` }}></div>
                  </div>
                  <span className="font-bold text-slate-700">{Math.round((doneCount / totalCount) * 100)}%</span>
                </div>
              </div>

              {/* Day Groups */}
              {Object.entries(groupedTasks).map(([date, dayTasks]) => (
                <div key={date} className="space-y-4">
                  <div className="flex items-center gap-3">
                    <h4 className="text-sm font-black uppercase tracking-widest text-slate-400 bg-slate-50 px-3 py-1 rounded-lg border border-slate-100">
                      {getDayLabel(date)}
                    </h4>
                    <div className="h-px flex-1 bg-slate-100"></div>
                  </div>

                  <div className="grid gap-3 sm:grid-cols-1 lg:grid-cols-2">
                    {dayTasks.map((t) => {
                      const isDone = String(t?.status || "").toLowerCase() === "done";
                      const subject = t?.subject || t?.subject_name || "Görev";
                      const topic = t?.topic_name || "";
                      const recSec = t?.recommended_seconds ?? null;
                      const recMin = recSec && Number(recSec) > 0 ? Math.round(Number(recSec) / 60) : null;

                      const meta = [
                        t?.task_type === 'remediation' ? 'Eksik Tamamlama' : t?.task_type === 'review' ? 'Tekrar' : 'Pratik',
                        t?.question_count ? `${t.question_count} soru` : null,
                        recMin ? `~${recMin} dk` : null
                      ].filter(Boolean).join(" • ");

                      const isPendingThis = pendingTaskId === t.id;
                      const isCritical = (t?.topic_name || "").includes("Kritik") || (t?.task_type === 'remediation');
                      const isTest = t?.task_type === 'test';
                      const isReview = t?.task_type === 'review' && t?.subject === 'Genel Tekrar';

                      let cardCls = "bg-white border-slate-200 shadow-sm hover:shadow-md hover:border-blue-300";
                      if (isDone) {
                        cardCls = "bg-slate-50/50 border-slate-100 grayscale-[0.5] opacity-60";
                      } else if (isCritical) {
                        cardCls = "bg-red-50/30 border-red-200 shadow-sm hover:shadow-md hover:border-red-300";
                      } else if (isTest) {
                        cardCls = "bg-amber-50/50 border-amber-200 shadow-md border-2 hover:border-amber-400";
                      } else if (isReview) {
                        cardCls = "bg-indigo-50/50 border-indigo-200 shadow-md border-2 hover:border-indigo-400";
                      }

                      return (
                        <div key={t.id} className={`relative group transition-all duration-300 p-4 rounded-2xl border flex items-center gap-4 ${cardCls}`}>
                          <div className="shrink-0">
                            {isDone ? (
                              <div className="w-10 h-10 rounded-full bg-slate-400 text-white flex items-center justify-center">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                              </div>
                            ) : isTest ? (
                              <div className="w-10 h-10 rounded-full bg-amber-500 text-white flex items-center justify-center shadow-lg shadow-amber-200">
                                <Sparkles className="h-5 w-5" />
                              </div>
                            ) : isReview ? (
                              <div className="w-10 h-10 rounded-full bg-indigo-500 text-white flex items-center justify-center shadow-lg shadow-indigo-200">
                                <Quote className="h-5 w-5" />
                              </div>
                            ) : (
                              <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-xs border shadow-sm ${isCritical ? "bg-red-100 text-red-700 border-red-200" : "bg-indigo-50 text-indigo-700 border-indigo-100"}`}>
                                {subject.substring(0, 2).toUpperCase()}
                              </div>
                            )}
                          </div>

                          <div className="min-w-0 flex-1">
                            <div className="flex items-center gap-2 mb-0.5">
                              <h4 className={`text-sm font-bold truncate ${isDone ? "text-slate-500" : "text-slate-900"}`}>{subject}</h4>
                              {isCritical && !isDone && <span className="text-[10px] font-bold uppercase tracking-wider text-red-600 bg-red-100 px-1.5 py-0.5 rounded leading-none">ACİL</span>}
                            </div>
                            {topic && <p className={`text-xs truncate mb-1 ${isDone ? "text-slate-400 font-normal" : "text-slate-600 font-medium"}`}>{topic.replace(`${subject} - `, '').split('(')[0].trim()}</p>}
                            <div className={`text-[11px] font-medium ${isDone ? "text-slate-400" : "text-slate-500"}`}>{meta}</div>
                          </div>

                          <div className="shrink-0 ml-auto">
                            <button
                              className={`h-9 px-4 rounded-xl text-xs font-bold transition-all duration-200 ${isDone ? "bg-slate-200 text-slate-600 hover:bg-slate-300" : "bg-blue-600 text-white hover:bg-blue-700 shadow-lg shadow-blue-600/20 active:scale-95"}`}
                              disabled={isPendingThis}
                              onClick={() => toggleTask.mutate({ taskId: t.id, newStatus: isDone ? "pending" : "done" })}
                            >
                              {isPendingThis ? "..." : isDone ? "Geri Al" : "Yap"}
                            </button>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardBody>
      </Card>
    </div>
  );
}
