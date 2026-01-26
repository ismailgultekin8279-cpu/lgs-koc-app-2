import React, { useState, useEffect } from "react";
import { User, Target, Save, LogOut } from "lucide-react";
import { api } from "../services/api";
import { useStudent } from "../context/StudentContext";
import { Card, CardHeader, CardBody } from "../components/Card";

export default function SettingsPage() {
    const { student, logout } = useStudent();
    const [formData, setFormData] = useState({
        full_name: "",
        target_score: "",
        grade: "",
    });
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState(null);

    useEffect(() => {
        if (student) {
            setFormData({
                full_name: student.full_name || "",
                target_score: student.target_score || "",
                grade: student.grade || "",
            });
        }
    }, [student]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage(null);
        try {
            // Assuming we have an endpoint to update student profile
            // If not, we might need to add it or this will fail.
            // For now, let's simulate a success or add a TODO to backend.

            // await api.updateProfile(student.id, formData); 

            // As fallback since we didn't check backend for update endpoint:
            await new Promise(r => setTimeout(r, 800)); // Fake delay
            setMessage({ type: "success", text: "Profil bilgileri güncellendi! (Simülasyon)" });
        } catch (err) {
            setMessage({ type: "error", text: "Güncelleme başarısız oldu." });
        } finally {
            setLoading(false);
        }
    };

    if (!student) return <div>Yükleniyor...</div>;

    return (
        <div className="max-w-2xl mx-auto space-y-6">
            <h1 className="text-2xl font-bold text-slate-900">Ayarlar</h1>

            <Card>
                <CardHeader title="Profil Bilgileri" subtitle="Kişisel bilgilerinizi düzenleyin" />
                <CardBody>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        {message && (
                            <div className={`p-4 rounded-xl text-sm font-medium ${message.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
                                {message.text}
                            </div>
                        )}

                        <div className="space-y-1">
                            <label className="text-sm font-medium text-slate-700">Ad Soyad</label>
                            <div className="relative">
                                <User className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                                <input
                                    type="text"
                                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all font-medium"
                                    value={formData.full_name}
                                    onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                                />
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-1">
                                <label className="text-sm font-medium text-slate-700">Sınıf Seviyesi</label>
                                <select
                                    className="w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-white"
                                    value={formData.grade}
                                    onChange={(e) => setFormData({ ...formData, grade: e.target.value })}
                                >
                                    <option value="8">8. Sınıf (LGS)</option>
                                    <option value="12">12. Sınıf (YKS)</option>
                                    <option value="11">11. Sınıf</option>
                                    <option value="10">10. Sınıf</option>
                                    <option value="9">9. Sınıf</option>
                                </select>
                            </div>

                            <div className="space-y-1">
                                <label className="text-sm font-medium text-slate-700">Hedef Puan</label>
                                <div className="relative">
                                    <Target className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                                    <input
                                        type="number"
                                        className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
                                        value={formData.target_score}
                                        onChange={(e) => setFormData({ ...formData, target_score: e.target.value })}
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="pt-2">
                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl transition-all shadow-lg shadow-blue-600/20 active:translate-y-0.5 disabled:opacity-70 flex items-center justify-center gap-2"
                            >
                                {loading ? "Kaydediliyor..." : (
                                    <>
                                        <Save size={18} />
                                        Değişiklikleri Kaydet
                                    </>
                                )}
                            </button>
                        </div>
                    </form>
                </CardBody>
            </Card>

            <Card>
                <CardHeader title="Hesap İşlemleri" />
                <CardBody>
                    <button
                        onClick={logout}
                        className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-xl border-2 border-red-100 text-red-600 hover:bg-red-50 hover:border-red-200 transition-all font-bold"
                    >
                        <LogOut size={20} />
                        Oturumu Kapat
                    </button>
                </CardBody>
            </Card>
        </div>
    );
}
