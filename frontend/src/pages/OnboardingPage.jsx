import { useState } from 'react';
import { api } from '../services/api';
import { useStudent } from '../context/StudentContext';
import { useNavigate } from 'react-router-dom';
import { Rocket, Target, User, BookOpen } from 'lucide-react';

export default function OnboardingPage() {
    const { login } = useStudent();
    const navigate = useNavigate();
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        full_name: '',
        grade: 8,
        target_score: 450,
        exam_group: 'LGS'
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const newStudent = await api.createStudent(formData);
            login(newStudent);
            // Generate initial plan
            await api.generatePlan(newStudent.id);
            navigate('/');
        } catch (err) {
            alert('Kayıt hatası: ' + err.message);
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
            <div className="max-w-md w-full glass-card p-8 animate-fade-in relative overflow-hidden">
                {/* Decorative background blob */}
                <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl -mr-10 -mt-10"></div>

                <div className="text-center mb-8 relative z-10">
                    <div className="w-16 h-16 bg-blue-600 rounded-2xl mx-auto flex items-center justify-center shadow-lg shadow-blue-500/30 mb-4 text-white">
                        <Rocket size={32} />
                    </div>
                    <h1 className="text-2xl font-bold text-slate-900">Hoş Geldin!</h1>
                    <p className="text-slate-500">Seni tanımamız için birkaç soru.</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6 relative z-10">
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">Adın Soyadın</label>
                        <div className="relative">
                            <User className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                            <input
                                required
                                className="input-modern pl-10"
                                placeholder="Örn: Ali Yılmaz"
                                value={formData.full_name}
                                onChange={e => setFormData({ ...formData, full_name: e.target.value })}
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">Kaçıncı Sınıfsın?</label>
                        <div className="relative">
                            <BookOpen className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                            <select
                                className="input-modern pl-10 appearance-none"
                                value={formData.grade}
                                onChange={e => {
                                    const g = parseInt(e.target.value);
                                    let group = 'LGS';
                                    if (g >= 9) group = 'YKS';
                                    setFormData({ ...formData, grade: g, exam_group: group });
                                }}
                            >
                                {[5, 6, 7, 8, 9, 10, 11, 12].map(g => (
                                    <option key={g} value={g}>{g}. Sınıf</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-2">Hedef Puanın</label>
                        <div className="relative">
                            <Target className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                            <input
                                type="number"
                                required
                                className="input-modern pl-10"
                                placeholder="Örn: 480"
                                value={formData.target_score}
                                onChange={e => setFormData({ ...formData, target_score: e.target.value })}
                            />
                        </div>
                    </div>

                    <button type="submit" className="btn-primary w-full py-3 text-lg mt-4">
                        Koçluğa Başla
                    </button>
                </form>
            </div>
        </div>
    );
}
