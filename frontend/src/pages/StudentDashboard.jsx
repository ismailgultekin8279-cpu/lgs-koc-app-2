import React, { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Sparkles, Quote } from "lucide-react";
import { Card, CardHeader, CardBody, InfoBox } from "../components/Card";
import { getDailyPlan, getCoaching, patchTask } from "../lib/endpoints";

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

  // Complete task (optimistic + kalıcı)
  const completeTask = useMutation({
    mutationFn: (taskId) => patchTask(taskId, { status: "done" }),

    onMutate: async (taskId) => {
      setPendingTaskId(taskId);

      await qc.cancelQueries({ queryKey: ["dailyPlan", studentId] });
      const previous = qc.getQueryData(["dailyPlan", studentId]);

      qc.setQueryData(["dailyPlan", studentId], (old) => {
        const list = normalizeDailyPlan(old);
        return list.map((t) => (t.id === taskId ? { ...t, status: "done" } : t));
      });

      return { previous };
    },

    onError: (_err, _taskId, context) => {
      if (context?.previous) {
        qc.setQueryData(["dailyPlan", studentId], context.previous);
      }
    },

    onSettled: () => {
      setPendingTaskId(null);
      qc.invalidateQueries({ queryKey: ["dailyPlan", studentId] });
    },
  });

  if (!studentId) {
    return (
      <Card>
        <CardHeader title="Öğrenci Paneli" subtitle="Bugünün planı + koç mesajı" />
        <CardBody>
          <InfoBox
            title="Öğrenci seçiniz"
            description="Öğrenci seçildiğinde günlük plan ve koç mesajı burada görünecek."
          />
        </CardBody>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Koç Mesajı - Banner Style - Moved to TOP */}
      <div className="relative overflow-hidden rounded-3xl bg-linear-to-br from-violet-600 to-indigo-600 p-1 shadow-xl shadow-indigo-500/20">
        <div className="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-white/10 blur-xl"></div>
        <div className="absolute bottom-0 left-0 -mb-4 -ml-4 h-24 w-24 rounded-full bg-black/10 blur-xl"></div>

        <div className="relative h-full rounded-[20px] bg-slate-900/40 backdrop-blur-sm p-6 text-white flex flex-col md:flex-row items-center gap-6">
          {/* Left Icon Area */}
          <div className="flex shrink-0 h-16 w-16 items-center justify-center rounded-2xl bg-white/20 shadow-inner">
            <Sparkles className="h-8 w-8 text-yellow-300" />
          </div>

          {/* Content Area */}
          <div className="flex-1 text-center md:text-left">
            <h3 className="font-bold text-xl leading-tight mb-2">Yapay Zeka Koçun</h3>

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

      {/* Bugünün Planı - Full Width List */}
      <Card>
        <CardHeader title="Bugünün Planı" subtitle="Hedeflerine ulaşmak için bugünkü görevlerin" />
        <CardBody>
          {dailyLoading ? (
            <div className="text-sm text-slate-600">Yükleniyor…</div>
          ) : dailyError ? (
            <div className="space-y-3">
              <div className="text-sm text-slate-700">Günlük plan alınamadı.</div>
              <button type="button" className="btn-secondary" onClick={() => refetchDaily()}>
                Yeniden Dene
              </button>
            </div>
          ) : tasks.length === 0 ? (
            <div className="text-sm text-slate-600">Bugün için görev yok.</div>
          ) : (
            <div className="space-y-4">
              {/* Stats Bar */}
              <div className="flex flex-wrap items-center gap-3 text-sm text-slate-600 pb-4 border-b border-slate-100">
                <span className="rounded-full border border-slate-200 px-3 py-1 bg-white">
                  Toplam: <span className="font-bold text-slate-900">{totalCount}</span>
                </span>
                <span className="rounded-full border border-emerald-200 px-3 py-1 bg-emerald-50 text-emerald-700">
                  Tamamlanan: <span className="font-bold">{doneCount}</span>
                </span>
                <span className="rounded-full border border-indigo-200 px-3 py-1 bg-indigo-50 text-indigo-700">
                  Kalan: <span className="font-bold">{pendingCount}</span>
                </span>
              </div>

              {/* Task List - Grid for larger screens? No, list is fine but maybe 2 cols for tasks if many? Let's stick to list but nicer. */}
              <div className="grid gap-3 sm:grid-cols-1 lg:grid-cols-2">
                {tasks.map((t) => {
                  const badge = statusBadge(t?.status);
                  const isDone = String(t?.status || "").toLowerCase() === "done";

                  const subject = t?.subject || t?.subject_name || "Görev";
                  const topic = t?.topic_name || "";

                  const recSec = t?.recommended_seconds ?? null;
                  const recMin =
                    recSec && Number(recSec) > 0 ? Math.round(Number(recSec) / 60) : null;

                  const meta = [
                    t?.task_type === 'remediation' ? 'Eksik Tamamlama' :
                      t?.task_type === 'review' ? 'Tekrar' : 'Pratik',
                    t?.question_count ? `${t.question_count} soru` : null,
                    recMin ? `~${recMin} dk` : null,
                  ]
                    .filter(Boolean)
                    .join(" • ");

                  const isPendingThis = pendingTaskId === t.id;

                  const isCritical = (t?.topic_name || "").includes("Kritik");

                  // Card Styles
                  const containerClass = `
                    relative group transition-all duration-200 p-4 rounded-2xl border flex items-center gap-4
                    ${isDone
                      ? "bg-slate-50 border-slate-200 opacity-60 grayscale-[0.5]"
                      : isCritical
                        ? "bg-red-50/30 border-red-200 shadow-sm hover:shadow-md hover:border-red-300"
                        : "bg-white border-slate-200 shadow-sm hover:shadow-md hover:border-blue-300"
                    }
                  `;

                  return (
                    <div
                      key={t.id}
                      className={containerClass}
                    >
                      {/* Left: Status Icon/Badge */}
                      <div className="shrink-0">
                        {isDone ? (
                          <div className="w-10 h-10 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                          </div>
                        ) : (
                          <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm border ${isCritical ? "bg-red-100 text-red-700 border-red-200" : "bg-blue-50 text-blue-700 border-blue-100"}`}>
                            {subject.substring(0, 2).toUpperCase()}
                          </div>
                        )}
                      </div>

                      {/* Middle: Info */}
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center gap-2 mb-0.5">
                          <h4 className={`text-sm font-bold truncate ${isDone ? "text-slate-500 line-through" : "text-slate-900"}`}>
                            {subject}
                          </h4>
                          {isCritical && !isDone && (
                            <span className="text-[10px] font-bold uppercase tracking-wider text-red-600 bg-red-100 px-1.5 py-0.5 rounded">KRİTİK</span>
                          )}
                        </div>

                        {topic && (
                          <p className="text-xs text-slate-600 truncate mb-1" title={topic}>{topic.replace(`${subject} - `, '')}</p>
                        )}

                        <div className="text-xs text-slate-500 font-medium">
                          {meta}
                        </div>
                      </div>

                      {/* Right: Button */}
                      <div className="shrink-0">
                        <button
                          className={`
                                h-9 px-4 rounded-lg text-sm font-semibold transition-colors
                                ${isDone
                              ? "bg-transparent text-slate-400 cursor-default"
                              : "bg-blue-600 text-white hover:bg-blue-700 shadow-lg shadow-blue-600/20 active:translate-y-0.5"
                            }
                            `}
                          disabled={isDone || isPendingThis}
                          onClick={() => completeTask.mutate(t.id)}
                        >
                          {isDone ? "Bitti" : isPendingThis ? "..." : "Yap"}
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </CardBody>
      </Card>
    </div>
  );
}
