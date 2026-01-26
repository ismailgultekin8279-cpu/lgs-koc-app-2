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

/* ---------------- Daily Plan ---------------- */
export function getDailyPlan(studentId) {
  // Use the standard task filtering endpoint
  // Takes query params: student (ID) and optional date
  const today = new Date().toISOString().split('T')[0];
  // Adding /v1 prefix as per api.js pattern
  return apiGet(`/students/tasks/?student=${studentId}&date=${today}`);
}

/* ---------------- Tasks ---------------- */
export function patchTask(taskId, payload) {
  return apiPatch(`/students/tasks/${taskId}/`, payload);
}

/* ---------------- Coaching ---------------- */
export function getCoaching(studentId) {
  // Use the working endpoint from api.js logic
  return apiGet(`/coaching/coach/${studentId}/status/`);
}

/* ---------------- Exam Results ---------------- */
export function bulkUpsertExamResults(payload) {
  return apiPost(`/students/exam-results/bulk-upsert/`, payload);
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
