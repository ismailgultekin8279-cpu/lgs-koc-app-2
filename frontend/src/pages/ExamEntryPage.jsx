import { useState } from 'react';
import Layout from '../components/layout/Layout';
import { Save, AlertCircle, CheckCircle2 } from 'lucide-react';
import clsx from 'clsx';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';
import { useStudent } from '../context/StudentContext';

const LGS_SUBJECTS = [
    { id: 'turkish', label: 'Türkçe', questions: 20, coeff: 4 },
    { id: 'math', label: 'Matematik', questions: 20, coeff: 4 },
    { id: 'science', label: 'Fen Bilimleri', questions: 20, coeff: 4 },
    { id: 'history', label: 'T.C. İnkılap Tarihi', questions: 10, coeff: 1 },
    { id: 'religion', label: 'Din Kültürü', questions: 10, coeff: 1 },
    { id: 'english', label: 'Yabancı Dil', questions: 10, coeff: 1 },
];

export default function ExamEntryPage() {
    const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
    const [results, setResults] = useState(
        LGS_SUBJECTS.reduce((acc, sub) => ({ ...acc, [sub.id]: { correct: '', wrong: '' } }), {})
    );
    const [status, setStatus] = useState('idle'); // idle, loading, success, error

    const handleInputChange = (subjectId, field, value) => {
        setResults(prev => ({
            ...prev,
            [subjectId]: { ...prev[subjectId], [field]: value }
        }));
    };

    const calculateNet = (correct, wrong) => {
        const c = parseInt(correct) || 0;
        const w = parseInt(wrong) || 0;
        return Math.max(0, c - (w / 3)).toFixed(2);
    };

    const calculateTotalNet = () => {
        return Object.values(results).reduce((acc, curr) => {
            const net = parseFloat(calculateNet(curr.correct, curr.wrong));
            return acc + net;
        }, 0).toFixed(2);
    };

    // Connect to backend API
    const { student } = useStudent();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus('loading');

        if (!student) {
            setStatus('error');
            alert('Öğrenci oturumu bulunamadı.');
            return;
        }

        try {
            const promises = LGS_SUBJECTS.map(sub => {
                const current = results[sub.id];
                const correct = parseInt(current.correct) || 0;
                const wrong = parseInt(current.wrong) || 0;

                return api.saveExamResult({
                    student_id: student.id,
                    exam_date: date,
                    subject: sub.label,
                    correct: correct,
                    wrong: wrong,
                    blank: sub.questions - correct - wrong,
                    net: parseFloat(calculateNet(correct, wrong))
                });
            });

            await Promise.all(promises);
            setStatus('success');

            // Trigger plan regeneration
            try {
                await api.generatePlan(student.id);
            } catch (planError) {
                console.warn("Plan generation failed but exam saved:", planError);
            }

        } catch (err) {
            console.error(err);
            setStatus('error');
            alert('Kaydetme hatası: ' + err.message);
        }
    };

    return (
        <Layout>
            <div className="max-w-4xl mx-auto">
                <div className="mb-8 flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-slate-900">Deneme Sınavı Girişi</h1>
                        <p className="text-slate-500 mt-2">LGS deneme sonuçlarını gir, yapay zeka analiz etsin.</p>
                    </div>
                    <div className="text-right">
                        <p className="text-sm font-medium text-slate-500">Toplam Net</p>
                        <p className="text-3xl font-bold text-indigo-600">{calculateTotalNet()}</p>
                    </div>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="glass-card p-6">
                        <label className="block text-sm font-medium text-slate-700 mb-2">Sınav Tarihi</label>
                        <input
                            type="date"
                            required
                            value={date}
                            onChange={(e) => setDate(e.target.value)}
                            className="input-modern max-w-xs"
                        />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {LGS_SUBJECTS.map((sub) => {
                            const current = results[sub.id];
                            const net = calculateNet(current.correct, current.wrong);
                            const empty = sub.questions - (parseInt(current.correct) || 0) - (parseInt(current.wrong) || 0);

                            return (
                                <div key={sub.id} className="glass-card p-5 border-l-4 border-l-blue-500">
                                    <div className="flex items-center justify-between mb-4">
                                        <h3 className="font-bold text-slate-800">{sub.label}</h3>
                                        <span className="text-xs font-mono bg-slate-100 px-2 py-1 rounded-md text-slate-500">
                                            {sub.questions} Soru
                                        </span>
                                    </div>

                                    <div className="grid grid-cols-3 gap-3">
                                        <div>
                                            <label className="text-xs font-semibold text-green-600 block mb-1">Doğru</label>
                                            <input
                                                type="number"
                                                min="0"
                                                max={sub.questions}
                                                value={current.correct}
                                                onChange={(e) => handleInputChange(sub.id, 'correct', e.target.value)}
                                                className="input-modern bg-green-50 focus:ring-green-500/20 text-center font-bold"
                                            />
                                        </div>
                                        <div>
                                            <label className="text-xs font-semibold text-red-600 block mb-1">Yanlış</label>
                                            <input
                                                type="number"
                                                min="0"
                                                max={sub.questions}
                                                value={current.wrong}
                                                onChange={(e) => handleInputChange(sub.id, 'wrong', e.target.value)}
                                                className="input-modern bg-red-50 focus:ring-red-500/20 text-center font-bold"
                                            />
                                        </div>
                                        <div className="text-center">
                                            <label className="text-xs font-semibold text-indigo-600 block mb-1">Net</label>
                                            <div className="h-[46px] flex items-center justify-center bg-indigo-50 rounded-xl font-bold text-indigo-700">
                                                {net}
                                            </div>
                                        </div>
                                    </div>
                                    {empty < 0 && (
                                        <p className="text-xs text-red-500 mt-2 flex items-center gap-1">
                                            <AlertCircle size={12} /> Soru sayısı aşıldı!
                                        </p>
                                    )}
                                </div>
                            );
                        })}
                    </div>

                    <div className="flex justify-end pt-4">
                        <button
                            type="submit"
                            disabled={status === 'loading'}
                            className="btn-primary flex items-center gap-2 text-lg px-8 py-3"
                        >
                            {status === 'loading' ? 'Kaydediliyor...' : <><Save size={20} /> Sonuçları Kaydet</>}
                        </button>
                    </div>
                </form>

                {status === 'success' && (
                    <div className="fixed bottom-8 right-8 glass bg-green-500/90 text-white p-4 rounded-xl flex items-center gap-3 shadow-2xl animate-slide-up">
                        <CheckCircle2 size={24} />
                        <div>
                            <h4 className="font-bold">Başarılı!</h4>
                            <p className="text-sm opacity-90">Deneme sonucu kaydedildi ve analiz edildi.</p>
                        </div>
                    </div>
                )}
            </div>
        </Layout>
    );
}
