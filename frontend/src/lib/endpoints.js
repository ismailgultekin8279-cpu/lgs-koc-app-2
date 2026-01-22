import { apiGet, apiPatch, apiPost } from "./apiClient";

/**
 * BACKEND API ROUTES (Django)
 * Base: /api  (apiClient içinde API_BASE="/api")
 *
 * ✅ Bu dosyada export edilen isimler,
 * sayfalardaki import isimleriyle %100 aynı olmalı.
 */

/* ---------------- Students ---------------- */
export function listStudents() {
  return apiGet("/students/");
}

export function getStudent(studentId) {
  return apiGet(`/students/${studentId}/`);
}

export function patchStudent(studentId, payload) {
  return apiPatch(`/students/${studentId}/`, payload);
}

/* ---------------- Daily Plan ----------------
   CoachDashboard şu fonksiyonu çağırıyor: getDailyPlan(studentId)
   Backend’de endpointin hangisi olduğuna göre aşağıdaki path’i gerekirse değiştiririz.
*/
export function getDailyPlan(studentId) {
  // Eğer sende endpoint farklıysa burayı 1 satır değiştiririz.
  // Sık kullanılan örnekler:
  // return apiGet(`/students/${studentId}/daily-plan/`);
  // return apiGet(`/daily-plans/?student=${studentId}`);
  return apiGet(`/students/${studentId}/daily-plan/`);
}

/* ---------------- Tasks ---------------- */
export function patchTask(taskId, payload) {
  return apiPatch(`/tasks/${taskId}/`, payload);
}

/* ---------------- Coaching ----------------
   StudentDashboard konsolda bunu istiyor: getCoaching
*/
export function getCoaching(studentId) {
  // Backend’de varsa çalışır; yoksa 404 döner ama artık "export yok" hatası biter.
  return apiGet(`/students/${studentId}/coaching/`);
}

/* ---------------- Exam Results ----------------
   Senin backend’de çalışan endpoint:
   POST /api/exam-results/bulk-upsert/
*/
export function bulkUpsertExamResults(payload) {
  return apiPost(`/exam-results/bulk-upsert/`, payload);
}

/**
 * Sonuç listeleme:
 * Senin backend get_queryset parametreleri:
 * ?student=...&exam_date=...
 * (sen bazen student_id yazmışsın; backend "student" bekliyor)
 */
export function listExamResults({ studentId, examDate } = {}) {
  const params = new URLSearchParams();
  if (studentId) params.set("student", String(studentId));
  if (examDate) params.set("exam_date", String(examDate));
  const qs = params.toString();
  return apiGet(`/exam-results/${qs ? `?${qs}` : ""}`);
}
