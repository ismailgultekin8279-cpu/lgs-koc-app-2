import Layout from '../components/layout/Layout';
import NetScoreChart from '../components/NetScoreChart';
import { useStudent } from '../context/StudentContext';
import { api } from '../services/api';
import { useState, useEffect } from 'react';

export default function ExamResultsPage() {
  const { student } = useStudent();
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (student?.id) {
      api.getLatestExam(student.id).then(exams => {
        if (exams) {
          const h = {};
          exams.forEach(e => {
            if (!h[e.exam_date]) h[e.exam_date] = 0;
            h[e.exam_date] += parseFloat(e.net) || 0;
          });
          const chartData = Object.keys(h).map(date => ({
            exam_date: date,
            net: h[date].toFixed(2)
          })).sort((a, b) => new Date(b.exam_date) - new Date(a.exam_date));
          setHistory(chartData);
        }
      });
    }
  }, [student]);

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-slate-900 mb-6">Gelişim Analizi</h1>
      <div className="glass-card p-6">
        <NetScoreChart data={history} />
      </div>
    </div>
  );
}
