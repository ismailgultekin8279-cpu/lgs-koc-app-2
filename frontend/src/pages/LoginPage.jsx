import { useState } from 'react';
import { api } from '../services/api';
import { useStudent } from '../context/StudentContext';
import { useNavigate } from 'react-router-dom';
import { LogIn, User, Lock, UserPlus, GraduationCap, Target } from 'lucide-react';

export default function LoginPage() {
    const { login } = useStudent();
    const navigate = useNavigate();

    const [isLogin, setIsLogin] = useState(true);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Form States
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [grade, setGrade] = useState(8);
    const [targetScore, setTargetScore] = useState(400);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            let data;
            if (isLogin) {
                // Login
                data = await api.login(username, password);
            } else {
                // Register
                // First register, then it returns user, but we need tokens.
                // Our API register returns { refresh, access, student } directly!
                data = await api.register({
                    username,
                    password,
                    full_name: fullName,
                    grade,
                    target_score: targetScore
                });
            }

            login(data);
            navigate('/');

        } catch (err) {
            console.error(err);
            setError(isLogin
                ? 'Giriş başarısız. Kullanıcı adı veya şifre hatalı.'
                : 'Kayıt başarısız. Kullanıcı adı alınmış olabilir.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
            <div className="max-w-md w-full glass-card p-8 animate-fade-in relative overflow-hidden">
                <div className="text-center mb-8">
                    <div className="w-16 h-16 bg-indigo-600 rounded-2xl mx-auto flex items-center justify-center shadow-lg shadow-indigo-500/30 mb-4 text-white">
                        {isLogin ? <LogIn size={32} /> : <UserPlus size={32} />}
                    </div>
                    <h1 className="text-2xl font-bold text-slate-900">
                        {isLogin ? 'Tekrar Hoş Geldin!' : 'Aramıza Katıl'}
                    </h1>
                    <p className="text-slate-500">
                        {isLogin ? 'Hesabına giriş yap ve çalışmaya başla.' : 'Yapay zeka destekli koçun seni bekliyor.'}
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    {/* Common Fields */}
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">Kullanıcı Adı</label>
                        <div className="relative">
                            <User className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                            <input
                                required
                                type="text"
                                className="input-modern pl-10"
                                placeholder="kullanici_adi"
                                value={username}
                                onChange={e => setUsername(e.target.value)}
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">Şifre</label>
                        <div className="relative">
                            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                            <input
                                required
                                type="password"
                                className="input-modern pl-10"
                                placeholder="••••••••"
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                            />
                        </div>
                    </div>

                    {/* Register Only Fields */}
                    {!isLogin && (
                        <div className="space-y-4 animate-slide-up">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Ad Soyad</label>
                                <input
                                    required
                                    type="text"
                                    className="input-modern"
                                    placeholder="Ad Soyad"
                                    value={fullName}
                                    onChange={e => setFullName(e.target.value)}
                                />
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Sınıf</label>
                                    <div className="relative">
                                        <GraduationCap className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                                        <select
                                            className="input-modern pl-10"
                                            value={grade}
                                            onChange={e => setGrade(Number(e.target.value))}
                                        >
                                            <option value={5}>5. Sınıf</option>
                                            <option value={6}>6. Sınıf</option>
                                            <option value={7}>7. Sınıf</option>
                                            <option value={8}>8. Sınıf (LGS)</option>
                                            <option value={9}>9. Sınıf</option>
                                            <option value={10}>10. Sınıf</option>
                                            <option value={11}>11. Sınıf</option>
                                            <option value={12}>12. Sınıf (YKS)</option>
                                        </select>
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Hedef Puan</label>
                                    <div className="relative">
                                        <Target className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                                        <input
                                            required
                                            type="number"
                                            className="input-modern pl-10"
                                            value={targetScore}
                                            onChange={e => setTargetScore(Number(e.target.value))}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {error && (
                        <div className="p-3 bg-red-50 text-red-600 text-sm rounded-lg flex items-center gap-2">
                            ⚠️ {error}
                        </div>
                    )}

                    <button disabled={loading} type="submit" className="btn-primary w-full py-3 text-lg mt-4">
                        {loading ? 'İşleniyor...' : (isLogin ? 'Giriş Yap' : 'Kayıt Ol')}
                    </button>
                </form>

                <div className="text-center mt-6">
                    <button
                        onClick={() => setIsLogin(!isLogin)}
                        className="text-sm text-indigo-600 hover:text-indigo-800 font-medium transition-colors"
                    >
                        {isLogin ? 'Hesabın yok mu? Kayıt Ol' : 'Zaten hesabın var mı? Giriş Yap'}
                    </button>

                    {/* Old onboarding link fallback? Maybe redundant now */}
                </div>
            </div>
        </div>
    );
}
