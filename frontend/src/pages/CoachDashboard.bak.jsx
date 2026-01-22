import { useEffect, useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Card, CardHeader, CardBody } from "../components/Card";
import {
  getDailyPlan,
  getStudent,
  listStudents,
  patchStudent,
  patchTask,
} from "../lib/endpoints";

/* ---------- helpers ---------- */

function getStudentLabel(s) {
  const name =
    s?.label ||
    s?.display_name ||
    s?.name ||
    s?.full_name ||
    s?.student_name ||
    s?.username ||
    s?.title ||
    "Ã–ÄŸrenci";

  const grade = s?.grade ?? s?.class_grade ?? s?.level ?? null;
  return grade ? `${name} â€” ${grade}. SÄ±nÄ±f` : name;
}

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
      text: "TamamlandÄ±",
      cls: "bg-emerald-50 text-emerald-700 border-emerald-100",
    };
  }
  return {
    text: "Bekliyor",
    cls: "bg-slate-50 text-slate-700 border-slate-100",
  };
}

/* ---------- page ---------- */

export default function CoachDashboard({ selectedStudentId, onSelectStudent }) {
  const qc = useQueryClient();

  /* students */
  const { data: studentsRaw } = useQuery({
    queryKey: ["students"],
    queryFn: listStudents,
  });

  const students = useMemo(() => {
    if (!studentsRaw) return [];
    if (Array.isArray(studentsRaw)) return studentsRaw;
    if (Array.isArray(studentsRaw.results)) return studentsRaw.results;
    return [];
  }, [studentsRaw]);

  /* student detail */
  const { data: studentDetail } = useQuery({
    queryKey: ["student", selectedStudentId],
    queryFn: () => getStudent(selectedStudentId),
    enabled: Boolean(selectedStudentId),
  });

  /* daily plan */
  const { data: dailyPlanRaw, isLoading: dailyLoading } = useQuery({
    queryKey: ["dailyPlan", selectedStudentId],
    queryFn: () => getDailyPlan(selectedStudentId),
    enabled: Boolean(selectedStudentId),
  });

  const tasks = useMemo(() => normalizeDailyPlan(dailyPlanRaw), [dailyPlanRaw]);

  /* target score */
  const [targetScore, setTargetScore] = useState("");

  useEffect(() => {
    if (!studentDetail) return;
    setTargetScore(
      studentDetail.target_score == null ? "" : String(studentDetail.target_score)
    );
  }, [studentDetail]);

  const updateStudent = useMutation({
    mutationFn: ({ id, payload }) => patchStudent(id, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["student", selectedStudentId] });
      qc.invalidateQueries({ queryKey: ["students"] });
    },
  });

  const completeTask = useMutation({
    mutationFn: (taskId) => patchTask(taskId, { status: "done" }),

    // optimistic update
    onMutate: async (taskId) => {
      await qc.cancelQueries({ queryKey: ["dailyPlan", selectedStudentId] });

      const previous = qc.getQueryData(["dailyPlan", selectedStudentId]);

      qc.setQueryData(["dailyPlan", selectedStudentId], (old) => {
        const list = normalizeDailyPlan(old);
        // old yapÄ±sÄ± {tasks: []} ise aynÄ± formatÄ± korumak iÃ§in:
        if (old && !Array.isArray(old) && Array.isArray(old.tasks)) {
          return {
            ...old,
            tasks: list.map((t) => (t.id === taskId ? { ...t, status: "done" } : t)),
          };
        }
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
      qc.invalidateQueries({ queryKey: ["dailyPlan", selectedStudentId] });
    },
  });

  return (
    <div className="grid gap-4 lg:grid-cols-12">
      {/* LEFT */}
      <section className="lg:col-span-4">
        <Card>
          <CardHeader title="Ã–ÄŸrenci SeÃ§imi" />
          <CardBody>
            <select
              className="input"
              value={selectedStudentId ?? ""}
              onChange={(e) =>
                onSelectStudent?.(e.target.value ? Number(e.target.value) : null)
              }
            >
              <option value="">SeÃ§inizâ€¦</option>
              {students.map((s) => (
                <option key={s.id} value={s.id}>
                  {getStudentLabel(s)}
                </option>
              ))}
            </select>
          </CardBody>
        </Card>

        <Card className="mt-4">
          <CardHeader title="Hedef Puan" />
          <CardBody>
            {!selectedStudentId ? (
              <div className="text-sm text-slate-600">Ã–ÄŸrenci seÃ§iniz.</div>
            ) : (
              <>
                <input
                  className="input"
                  type="number"
                  value={targetScore}
                  onChange={(e) => setTargetScore(e.target.value)}
                  placeholder="Ã–rn: 450"
                />

                <button
                  className="btn-primary mt-2"
                  disabled={updateStudent.isPending}
                  onClick={() =>
                    updateStudent.mutate({
                      id: selectedStudentId,
                      payload: {
                        target_score: targetScore === "" ? null : Number(targetScore),
                      },
                    })
                  }
                >
                  {updateStudent.isPending ? "Kaydediliyorâ€¦" : "Kaydet"}
                </button>
              </>
            )}
          </CardBody>
        </Card>
      </section>

      {/* RIGHT */}
      <section className="lg:col-span-8">
        <Card>
          <CardHeader title="GÃ¼nlÃ¼k Plan" />
          <CardBody>
            {!selectedStudentId ? (
              <div className="text-sm text-slate-600">Ã–ÄŸrenci seÃ§iniz.</div>
            ) : dailyLoading ? (
              <div className="text-sm text-slate-600">YÃ¼kleniyorâ€¦</div>
            ) : tasks.length === 0 ? (
              <div className="text-sm text-slate-600">BugÃ¼n iÃ§in gÃ¶rev yok.</div>
            ) : (
              <div className="space-y-3">
                {tasks.map((t) => {
                  const badge = statusBadge(t.status);
                  const isDone = String(t.status || "").toLowerCase() === "done";

                  const subject = t.subject || t.subject_name || "GÃ¶rev";
                  const topic = t.topic_name || "";
                  const meta = [
                    t.task_type || null,
                    t.question_count ? `${t.question_count} soru` : null,
                  ]
                    .filter(Boolean)
                    .join(" â€¢ ");

                  return (
                    <div
                      key={t.id}
                      className="rounded-2xl border border-slate-100 bg-white p-3 flex justify-between gap-3"
                    >
                      <div>
                        <div className="flex items-center gap-2">
                          <span
                            className={`rounded-xl border px-2 py-0.5 text-xs ${badge.cls}`}
                          >
                            {badge.text}
                          </span>
                          <span className="font-medium">{subject}</span>
                        </div>

                        {topic && <div className="text-xs text-slate-600 mt-1">{topic}</div>}
                        {meta && <div className="text-xs text-slate-500 mt-1">{meta}</div>}
                      </div>

                      <button
                        className={isDone ? "btn-secondary" : "btn-primary"}
                        disabled={isDone || completeTask.isPending}
                        onClick={() => completeTask.mutate(t.id)}
                      >
                        {isDone
                          ? "TamamlandÄ±"
                          : completeTask.isPending
                          ? "Kaydediliyorâ€¦"
                          : "Tamamla"}
                      </button>
                    </div>
                  );
                })}
              </div>
            )}
          </CardBody>
        </Card>
      </section>
    </div>
  );
}

