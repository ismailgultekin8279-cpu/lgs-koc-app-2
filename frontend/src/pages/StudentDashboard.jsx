import React, { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
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

export default function StudentDashboard({ selectedStudentId }) {
  const qc = useQueryClient();
  const [pendingTaskId, setPendingTaskId] = useState(null);

  // Daily plan
  const {
    data: dailyPlanRaw,
    isLoading: dailyLoading,
    isError: dailyError,
    refetch: refetchDaily,
  } = useQuery({
    queryKey: ["dailyPlan", selectedStudentId],
    queryFn: () => getDailyPlan(selectedStudentId),
    enabled: Boolean(selectedStudentId),
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
    queryKey: ["coaching", selectedStudentId],
    queryFn: () => getCoaching(selectedStudentId),
    enabled: Boolean(selectedStudentId),
  });

  const coaching = useMemo(() => normalizeCoaching(coachingRaw), [coachingRaw]);

  // Complete task (optimistic + kalıcı)
  const completeTask = useMutation({
    mutationFn: (taskId) => patchTask(taskId, { status: "done" }),

    onMutate: async (taskId) => {
      setPendingTaskId(taskId);

      await qc.cancelQueries({ queryKey: ["dailyPlan", selectedStudentId] });
      const previous = qc.getQueryData(["dailyPlan", selectedStudentId]);

      qc.setQueryData(["dailyPlan", selectedStudentId], (old) => {
        const list = normalizeDailyPlan(old);
        return list.map((t) => (t.id === taskId ? { ...t, status: "done" } : t));
      });

      return { previous };
    },

    onError: (_err, _taskId, context) => {
      if (context?.previous) {
        qc.setQueryData(["dailyPlan", selectedStudentId], context.previous);
      }
    },

    onSettled: () => {
      setPendingTaskId(null);
      qc.invalidateQueries({ queryKey: ["dailyPlan", selectedStudentId] });
    },
  });

  if (!selectedStudentId) {
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
    <div className="grid gap-4 md:grid-cols-2">
      {/* Bugünün Planı */}
      <Card>
        <CardHeader title="Bugünün Planı" subtitle="Görevler ve ilerleme" />
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
            <div className="space-y-3">
              <div className="flex flex-wrap items-center gap-2 text-xs text-slate-600">
                <span className="rounded-xl border border-slate-100 bg-slate-50 px-2 py-1">
                  Toplam: <span className="font-medium text-slate-900">{totalCount}</span>
                </span>
                <span className="rounded-xl border border-emerald-100 bg-emerald-50 px-2 py-1 text-emerald-700">
                  Tamamlanan: <span className="font-medium">{doneCount}</span>
                </span>
                <span className="rounded-xl border border-indigo-100 bg-indigo-50 px-2 py-1 text-indigo-700">
                  Kalan: <span className="font-medium">{pendingCount}</span>
                </span>
              </div>

              <div className="space-y-2">
                {tasks.map((t) => {
                  const badge = statusBadge(t?.status);
                  const isDone = String(t?.status || "").toLowerCase() === "done";

                  const subject = t?.subject || t?.subject_name || "Görev";
                  const topic = t?.topic_name || "";

                  const recSec = t?.recommended_seconds ?? null;
                  const recMin =
                    recSec && Number(recSec) > 0 ? Math.round(Number(recSec) / 60) : null;

                  const meta = [
                    t?.task_type || null,
                    t?.question_count ? `${t.question_count} soru` : null,
                    recMin ? `önerilen ${recMin} dk` : null,
                  ]
                    .filter(Boolean)
                    .join(" • ");

                  const isPendingThis = pendingTaskId === t.id;

                  return (
                    <div
                      key={t.id}
                      className="rounded-2xl border border-slate-100 bg-white p-3 flex items-start justify-between gap-3"
                    >
                      <div className="min-w-0">
                        <div className="flex items-center gap-2">
                          <span className={`rounded-xl border px-2 py-0.5 text-xs ${badge.cls}`}>
                            {badge.text}
                          </span>
                          <div className="text-sm font-medium text-slate-900 truncate">
                            {subject}
                          </div>
                        </div>

                        {topic ? (
                          <div className="mt-1 text-xs text-slate-600 truncate">{topic}</div>
                        ) : null}

                        {meta ? <div className="mt-1 text-xs text-slate-500">{meta}</div> : null}
                      </div>

                      <button
                        className={isDone ? "btn-secondary" : "btn-primary"}
                        disabled={isDone || isPendingThis}
                        onClick={() => completeTask.mutate(t.id)}
                      >
                        {isDone ? "Tamamlandı" : isPendingThis ? "Kaydediliyor…" : "Tamamla"}
                      </button>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </CardBody>
      </Card>

      {/* Koç Mesajı */}
      <Card>
        <CardHeader title="Koç Mesajı" subtitle="Bugün için kısa öneri" />
        <CardBody>
          {coachingLoading ? (
            <div className="text-sm text-slate-600">Yükleniyor…</div>
          ) : coachingError ? (
            <div className="space-y-3">
              <div className="text-sm text-slate-700">Koç mesajı alınamadı.</div>
              <button
                type="button"
                className="btn-secondary"
                onClick={() => refetchCoaching()}
              >
                Yeniden Dene
              </button>
            </div>
          ) : coaching.lines.length === 0 ? (
            <div className="text-sm text-slate-600">Henüz mesaj yok.</div>
          ) : (
            <div className="space-y-2">
              {coaching.title ? (
                <div className="text-sm font-medium text-slate-900">{coaching.title}</div>
              ) : null}

              {coaching.lines.map((line, idx) => (
                <div
                  key={idx}
                  className="rounded-2xl border border-slate-100 bg-slate-50 p-3 text-sm text-slate-800"
                >
                  {line}
                </div>
              ))}
            </div>
          )}
        </CardBody>
      </Card>
    </div>
  );
}
