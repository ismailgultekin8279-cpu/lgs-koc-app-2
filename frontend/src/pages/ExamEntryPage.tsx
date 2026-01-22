import { useEffect, useMemo, useState } from "react";

type Student = {
  id: number;
  display_name?: string;
  full_name?: string;
  name?: string;
};

type ResultItem = {
  subject: string;
  correct: number;
  wrong: number;
  blank: number;
  net: number;
};

const API_BASE = "/api";

const SUBJECTS = ["Matematik", "Türkçe", "Fen", "İnkılap", "Din", "İngilizce"];

function calcNet(correct: number, wrong: number) {
  return Number((correct - wrong / 4).toFixed(2));
}

export default function ExamEntryPage() {
  const [students, setStudents] = useState<Student[]>([]);
  const [studentId, setStudentId] = useState<number | "">("");
  const [examDate, setExamDate] = useState<string>(() => {
    const d = new Date();
    const yyyy = d.getFullYear();
    const mm = String(d.getMonth() + 1).padStart(2, "0");
    const dd = String(d.getDate()).padStart(2, "0");
    return `${yyyy}-${mm}-${dd}`;
  });

  const [rows, setRows] = useState<Record<string, { correct: number; wrong: number; blank: number }>>(() => {
    const init: Record<string, { correct: number; wrong: number; blank: number }> = {};
    for (const s of SUBJECTS) init[s] = { correct: 0, wrong: 0, blank: 0 };
    return init;
  });

  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState<string>("");

  useEffect(() => {
    let cancelled = false;

    async function loadStudents() {
      try {
        const res = await fetch(`${API_BASE}/students/`);
        if (!res.ok) throw new Error();
        const data = await res.json();
        if (cancelled) return;

        const list: Student[] = Array.isArray(data) ? data : data?.results ?? [];
        setStudents(list);

        if (list.length && studentId === "") {
          setStudentId(list[0].id);
        }
      } catch {
        setStudents([]);
      }
    }

    loadStudents();
    return () => {
      cancelled = true;
    };
  }, []);

  const payloadResults: ResultItem[] = useMemo(() => {
    return SUBJECTS.map((subject) => {
      const r = rows[subject];
      const net = calcNet(r.correct, r.wrong);
      return { subject, ...r, net };
    }).filter((x) => x.correct + x.wrong + x.blank > 0);
  }, [rows]);

  async function handleSave() {
    setMsg("");
    if (studentId === "") return setMsg("Öğrenci seçmelisin.");
    if (!payloadResults.length) return setMsg("En az 1 derse D/Y/B gir.");

    setSaving(true);
    try {
      const res = await fetch(`${API_BASE}/exam-results/bulk-upsert/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          student: Number(studentId),
          exam_date: examDate,
          results: payloadResults,
        }),
      });

      if (!res.ok) throw new Error();
      setMsg("Kaydedildi");
    } catch {
      setMsg("Kaydetme hatası");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div style={{ padding: 16, maxWidth: 900 }}>
      <h2>Deneme Girişi</h2>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        <select value={studentId} onChange={(e) => setStudentId(Number(e.target.value))}>
          {students.map((s) => (
            <option key={s.id} value={s.id}>
              {s.display_name || s.full_name || s.name || `Öğrenci #${s.id}`}
            </option>
          ))}
        </select>

        <input type="date" value={examDate} onChange={(e) => setExamDate(e.target.value)} />
      </div>

      <table>
        <thead>
          <tr>
            <th>Ders</th>
            <th>Doğru</th>
            <th>Yanlış</th>
            <th>Boş</th>
            <th>Net</th>
          </tr>
        </thead>
        <tbody>
          {SUBJECTS.map((s) => (
            <tr key={s}>
              <td>{s}</td>
              <td><input type="number" value={rows[s].correct} onChange={(e) => setRows({ ...rows, [s]: { ...rows[s], correct: Number(e.target.value) } })} /></td>
              <td><input type="number" value={rows[s].wrong} onChange={(e) => setRows({ ...rows, [s]: { ...rows[s], wrong: Number(e.target.value) } })} /></td>
              <td><input type="number" value={rows[s].blank} onChange={(e) => setRows({ ...rows, [s]: { ...rows[s], blank: Number(e.target.value) } })} /></td>
              <td>{calcNet(rows[s].correct, rows[s].wrong)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <button onClick={handleSave} disabled={saving}>
        {saving ? "Kaydediliyor..." : "Kaydet"}
      </button>

      {msg && <div>{msg}</div>}
    </div>
  );
}
