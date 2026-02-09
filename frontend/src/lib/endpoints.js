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
export function getDailyPlan(studentId, { includeUpcoming = true } = {}) {
  const today = new Date().toISOString().split('T')[0];
  if (includeUpcoming) {
    // Return all upcoming tasks for the student (usually the 7-day plan)
    // Sorted by date on backend or frontend
    return apiGet(`/students/tasks/?student=${studentId}`);
  }
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

export function generatePlan(studentId) {
  return apiPost(`/coaching/coach/${studentId}/generate_plan/`, {});
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
