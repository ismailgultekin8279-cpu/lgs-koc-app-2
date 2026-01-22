import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

export default function NetScoreChart({ data }) {
    if (!data || data.length === 0) return (
        <div className="h-64 flex items-center justify-center text-slate-400 italic bg-slate-50/50 rounded-xl">
            Henüz veri yok.
        </div>
    );

    // Format data for chart
    // Expecting data: [{ exam_date, net }]
    const chartData = data.map(d => ({
        date: new Date(d.exam_date).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' }),
        net: parseFloat(d.net)
    })).reverse(); // API sends DESC, chart wants ASC usually

    return (
        <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                    <defs>
                        <linearGradient id="colorNet" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#4F46E5" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#4F46E5" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                    <XAxis
                        dataKey="date"
                        axisLine={false}
                        tickLine={false}
                        tick={{ fill: '#64748B', fontSize: 12 }}
                        dy={10}
                    />
                    <YAxis
                        axisLine={false}
                        tickLine={false}
                        tick={{ fill: '#64748B', fontSize: 12 }}
                    />
                    <Tooltip
                        contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                        cursor={{ stroke: '#6366f1', strokeWidth: 2 }}
                    />
                    <Area
                        type="monotone"
                        dataKey="net"
                        stroke="#4F46E5"
                        strokeWidth={3}
                        fillOpacity={1}
                        fill="url(#colorNet)"
                    />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
}
