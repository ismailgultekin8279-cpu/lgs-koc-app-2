import React, { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';
import { Card } from '../components/Card';
import { Trash2, Plus, BookOpen } from 'lucide-react';

export default function CurriculumAdminPage() {
    const queryClient = useQueryClient();
    const [newItem, setNewItem] = useState({
        subject: 1, // Default ID, todo: fetch subjects
        title: '',
        month: 9,
        week: 1,
        order: 0
    });

    // Fetch topics (flat list)
    const { data: topics, isLoading } = useQuery({
        queryKey: ['admin-topics'],
        queryFn: api.getTopics,
    });

    const createMutation = useMutation({
        mutationFn: api.createTopic,
        onSuccess: () => {
            queryClient.invalidateQueries(['admin-topics']);
            setNewItem(prev => ({ ...prev, title: '' })); // reset title
        }
    });

    const deleteMutation = useMutation({
        mutationFn: api.deleteTopic,
        onSuccess: () => {
            queryClient.invalidateQueries(['admin-topics']);
        }
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        createMutation.mutate(newItem);
    };

    if (isLoading) return <div className="p-8">Yükleniyor...</div>;

    const subjects = [{ id: 1, name: 'Matematik' }]; // Hardcoded for now till we add Subject CRUD

    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold flex items-center gap-2">
                <BookOpen className="text-blue-600" />
                Müfredat Yönetimi
            </h1>

            {/* Add Form */}
            <Card>
                <div className="p-5">
                    <h3 className="font-bold text-lg mb-4">Yeni Konu Ekle</h3>
                    <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-5 gap-4 items-end">
                        <div>
                            <label className="block text-xs font-medium text-slate-500 mb-1">Ders</label>
                            <select
                                className="w-full p-2 rounded-lg border border-slate-200"
                                value={newItem.subject}
                                onChange={e => setNewItem({ ...newItem, subject: parseInt(e.target.value) })}
                            >
                                {subjects.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                            </select>
                        </div>
                        <div>
                            <label className="block text-xs font-medium text-slate-500 mb-1">Ay (1-12)</label>
                            <input
                                type="number"
                                className="w-full p-2 rounded-lg border border-slate-200"
                                value={newItem.month}
                                onChange={e => setNewItem({ ...newItem, month: parseInt(e.target.value) })}
                            />
                        </div>
                        <div>
                            <label className="block text-xs font-medium text-slate-500 mb-1">Hafta (1-5)</label>
                            <input
                                type="number"
                                className="w-full p-2 rounded-lg border border-slate-200"
                                value={newItem.week}
                                onChange={e => setNewItem({ ...newItem, week: parseInt(e.target.value) })}
                            />
                        </div>
                        <div className="md:col-span-2">
                            <label className="block text-xs font-medium text-slate-500 mb-1">Konu Başlığı</label>
                            <div className="flex gap-2">
                                <input
                                    type="text"
                                    className="w-full p-2 rounded-lg border border-slate-200"
                                    placeholder="Örn: Kareköklü Sayılar"
                                    value={newItem.title}
                                    onChange={e => setNewItem({ ...newItem, title: e.target.value })}
                                    required
                                />
                                <button
                                    type="submit"
                                    disabled={createMutation.isPending}
                                    className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700"
                                >
                                    <Plus />
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </Card>

            {/* List */}
            <Card>
                <div className="p-5">
                    <h3 className="font-bold text-lg mb-4">Konu Listesi</h3>
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead className="text-slate-500 bg-slate-50 font-medium">
                                <tr>
                                    <th className="p-3">ID</th>
                                    <th className="p-3">Ders</th>
                                    <th className="p-3">Ay</th>
                                    <th className="p-3">Hafta</th>
                                    <th className="p-3">Başlık</th>
                                    <th className="p-3 text-right">İşlem</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {topics?.results ? topics.results.map(topic => (
                                    <tr key={topic.id} className="hover:bg-slate-50">
                                        <td className="p-3 text-slate-400">#{topic.id}</td>
                                        <td className="p-3">Matematik</td>
                                        <td className="p-3">{topic.month}. Ay</td>
                                        <td className="p-3">{topic.week}</td>
                                        <td className="p-3 font-medium">{topic.title}</td>
                                        <td className="p-3 text-right">
                                            <button
                                                onClick={() => deleteMutation.mutate(topic.id)}
                                                className="text-red-400 hover:text-red-600 p-1"
                                            >
                                                <Trash2 size={18} />
                                            </button>
                                        </td>
                                    </tr>
                                )) : (
                                    <tr><td colSpan="6" className="p-4 text-center">Veri yok.</td></tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </Card>
        </div>
    );
}
