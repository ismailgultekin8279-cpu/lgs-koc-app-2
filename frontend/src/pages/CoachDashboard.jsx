import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { Card, CardHeader, CardBody } from "../components/Card";
import { listStudents, getStudent, getDailyPlan } from "../lib/endpoints";

function studentLabel(s) {
  const name =
    s?.display_name ||
    s?.name ||
    s?.full_name ||
    s?.student_name ||
    s?.username ||
    `Öğrenci #${s?.id ?? ""}`;

  const grade =
    s?.grade ||
    s?.class_level ||
    s?.class ||
    s?.level ||
    s?.grade_level ||
    s?.grade_label;

  return grade ? `${name} — ${grade}. Sınıf` : name;
}

export default function CoachDashboard({ selectedStudentId, onSelectStudent }) {
  const { data: studentsRaw, isLoading: studentsLoading } = useQuery({
    queryKey: ["students"],
    queryFn: listStudents,
  });

  const students = useMemo(() => {
    if (!studentsRaw) return [];
    if (Array.isArray(studentsRaw)) return studentsRaw;
    if (Array.isArray(studentsRaw.results)) return studentsRaw.results;
    return [];
  }, [studentsRaw]);

  const { data: studentDetail } = useQuery({
    queryKey: ["student", selectedStudentId],
    queryFn: () => getStudent(selectedStudentId),
    enabled: Boolean(selectedStudentId),
  });

  const { data: dailyPlan, isLoading: planLoading } = useQuery({
    queryKey: ["dailyPlan", selectedStudentId],
    queryFn: () => getDailyPlan(selectedStudentId),
    enabled: Boolean(selectedStudentId),
  });

  return (
    <div className="grid gap-4 lg:grid-cols-12">
      <section className="lg:col-span-4">
        <Card>
          <CardHeader title="Öğrenci Seçimi" subtitle="Koç paneli" />
          <CardBody>
            <select
              className="input"
              value={selectedStudentId ?? ""}
              onChange={(e) => onSelectStudent?.(e.target.value ? Number(e.target.value) : null)}
            >
              <option value="">{studentsLoading ? "Yükleniyor..." : "Seçiniz"}</option>
              {students.map((s) => (
                <option key={s.id} value={s.id}>
                  {studentLabel(s)}
                </option>
              ))}
            </select>

            <div className="mt-3 text-xs text-slate-500">
              {students.length ? `Toplam: ${students.length}` : "Öğrenci yok."}
            </div>
          </CardBody>
        </Card>

        <Card className="mt-4">
          <CardHeader title="Hedef Puan" subtitle="Temel hedef ayarı" />
          <CardBody>
            {!selectedStudentId ? (
              <div className="text-sm text-slate-600">Öğrenci seçiniz.</div>
            ) : (
              <div className="text-sm text-slate-700">
                Seçili öğrenci: <span className="font-medium">{studentLabel(studentDetail || { id: selectedStudentId })}</span>
              </div>
            )}
          </CardBody>
        </Card>
      </section>

      <section className="lg:col-span-8">
        <Card>
          <CardHeader title="Günlük Plan" subtitle="Bugünün görevleri" />
          <CardBody>
            {!selectedStudentId ? (
              <div className="text-sm text-slate-600">Öğrenci seçiniz.</div>
            ) : planLoading ? (
              <div className="text-sm text-slate-600">Yükleniyor...</div>
            ) : !dailyPlan || (Array.isArray(dailyPlan.tasks) && dailyPlan.tasks.length === 0) ? (
              <div className="text-sm text-slate-600">Bugün için görev yok.</div>
            ) : (
              <pre className="text-xs bg-slate-50 border border-slate-100 rounded-xl p-3 overflow-auto">
                {JSON.stringify(dailyPlan, null, 2)}
              </pre>
            )}
          </CardBody>
        </Card>
      </section>
    </div>
  );
}
