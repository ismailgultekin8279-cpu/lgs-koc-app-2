from datetime import datetime, time

from django.db.models import Sum, Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_GET

from .models import Student, Session, BehaviorLog, ExamResult, StudyTask
from .serializers import StudentSerializer, StudyTaskSerializer, ExamResultSerializer
from .serializers import StudentSerializer, StudyTaskSerializer, ExamResultSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = Student.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            student = user.student_profile
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "student": {
                    "id": student.id,
                    "full_name": student.full_name,
                    "grade": student.grade,
                    "target_score": student.target_score
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            from django.contrib.auth.models import User
            user = User.objects.get(username=request.data['username'])
            try:
                student = user.student_profile
                response.data['student'] = {
                    "id": student.id,
                    "full_name": student.full_name,
                    "grade": student.grade,
                    "target_score": student.target_score
                }
            except:
                pass
        return response

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudyTaskViewSet(viewsets.ModelViewSet):
    queryset = StudyTask.objects.all()
    serializer_class = StudyTaskSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        student_id = self.request.query_params.get('student')
        date_param = self.request.query_params.get('date')
        
        if student_id:
            qs = qs.filter(student_id=student_id)
        if date_param:
            qs = qs.filter(date=date_param)
            
        return qs

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        task = self.get_object()
        if task.status == 'done':
            task.status = 'pending'
            task.completed_at = None
        else:
            task.status = 'done'
            task.completed_at = timezone.now()
        
        task.save()
        return Response(self.get_serializer(task).data)

class ExamResultViewSet(viewsets.ModelViewSet):
    queryset = ExamResult.objects.all()
    serializer_class = ExamResultSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        student_id = self.request.query_params.get('student_id')
        if student_id:
            qs = qs.filter(student_id=student_id)
        
        # Simple manual ordering since we didn't install django-filter
        ordering = self.request.query_params.get('ordering')
        if ordering == '-exam_date':
            qs = qs.order_by('-exam_date')
            
        return qs
    
    @action(detail=False, methods=["post"], url_path="bulk-upsert")
    def bulk_upsert(self, request):
        from django.db import transaction
        from .serializers import ExamResultsBulkUpsertSerializer

        serializer = ExamResultsBulkUpsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        student_id = data["student"]
        exam_date = data["exam_date"]
        results = data["results"]

        with transaction.atomic():
            for item in results:
                ExamResult.objects.update_or_create(
                    student_id=student_id,
                    exam_date=exam_date,
                    subject=item["subject"],
                    defaults={
                        "correct": item["correct"],
                        "wrong": item["wrong"],
                        "blank": item["blank"],
                        # net field computes itself on save if not provided, or we can compute it here.
                        # model save() method doesn't compute net automatically if inputs are provided?
                        # Model doesn't have compute method in save. Let's compute it quickly or let frontend send it.
                        # Wait, model definition has net field. Let's compute it.
                        "net": max(0, item["correct"] - (item["wrong"] / 3.0)) 
                    },
                )

        qs = ExamResult.objects.filter(student_id=student_id, exam_date=exam_date).order_by("subject")
        return Response(ExamResultSerializer(qs, many=True).data, status=status.HTTP_200_OK)

def start_session(request):
    student_id = request.GET.get("student_id")
    if not student_id:
        return JsonResponse({"error": "student_id zorunludur"}, status=400)

    student = get_object_or_404(Student, id=student_id)

    active = Session.objects.filter(student=student, end_time__isnull=True).first()

    # Otomatik kapanış eşiği (3 saat)
    AUTO_CLOSE_SECONDS = 3 * 60 * 60

    if active:
        now = timezone.now()

        # start_time boşsa güvenliğe al
        if not active.start_time:
            active.start_time = now
            active.save(update_fields=["start_time"])

        age_seconds = (now - active.start_time).total_seconds()

        # Çok eski aktif oturum varsa otomatik kapat
        if age_seconds >= AUTO_CLOSE_SECONDS:
            active.end_time = now
            duration = (active.end_time - active.start_time).total_seconds()
            active.duration_seconds = int(max(0, duration))
            active.save(update_fields=["end_time", "duration_seconds"])

            # Bu otomatik kapatma için log
            BehaviorLog.objects.update_or_create(
                session=active,
                defaults={
                    "risk_level": 1,
                    "note": "Otomatik kapatma: oturum çok uzun süre açık kaldı (>=3 saat)"
                }
            )
        else:
            # Gerçekten aktif ve yeni: yeni session açılmasın
            return JsonResponse(
                {"error": "Bu öğrenci için zaten aktif bir oturum var."},
                status=400
            )

    # Yeni session başlat
    session = Session.objects.create(student=student, start_time=timezone.now())

    return JsonResponse({
        "message": "Oturum başlatıldı",
        "session_id": session.id
    })


def end_session(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    session = Session.objects.filter(student=student, end_time__isnull=True).first()
    if not session:
        return JsonResponse({"error": "Aktif oturum bulunamadı."}, status=400)

    session.end_time = timezone.now()

    # start_time boş kalmışsa (normalde kalmamalı) yine de patlamasın
    if not session.start_time:
        session.start_time = session.end_time

    duration = (session.end_time - session.start_time).total_seconds()
    session.duration_seconds = int(duration)
    session.save()

    # Risk analizi
    if duration < 30:
        risk = 2
        note = "30 sn altı: hızlı çıkış"
    elif duration < 120:
        risk = 2
        note = "Kaçış başladı"
    elif duration < 600:
        risk = 1
        note = "Kaçma eğilimi (10 dk altı)"
    else:
        risk = 0
        note = "Normal kullanım"

    # Aynı session için 2 kere log yazmayı engelle (idempotent)
    BehaviorLog.objects.update_or_create(
        session=session,
        defaults={"risk_level": risk, "note": note}
    )

    return JsonResponse({
        "message": "Oturum kapatıldı",
        "duration_seconds": session.duration_seconds,
        "risk_level": risk,
        "note": note
    })


def student_report(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    sessions = Session.objects.filter(student=student)
    logs = BehaviorLog.objects.filter(session__student=student)

    total_duration = sessions.aggregate(total=Sum("duration_seconds"))["total"] or 0
    avg_risk = logs.aggregate(avg=Avg("risk_level"))["avg"] or 0

    return JsonResponse({
        "student": student.name,
        "total_sessions": sessions.count(),
        "total_duration_seconds": total_duration,
        "average_risk_level": round(avg_risk, 2),
    })


def coach_message(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return JsonResponse({"error": "session_id zorunludur"}, status=400)

    session = get_object_or_404(Session, id=session_id)
    log = BehaviorLog.objects.filter(session=session).order_by("created_at").last()

    if not log:
        return JsonResponse({"error": "Bu oturum için BehaviorLog yok"}, status=404)

    if log.risk_level == 2:
        msg = "Buradayım. Hiçbir şey yapmak zorunda değilsin."
    elif log.risk_level == 1:
        msg = "Bugün sadece burada olman yeterli."
    else:
        msg = "Harika gidiyorsun. İstersen kısa bir ipucu paylaşabilirim."

    return JsonResponse({
        "student": session.student.name,
        "session_id": session.id,
        "risk_level": log.risk_level,
        "note": log.note,
        "message": msg
    })


def _parse_date_yyyy_mm_dd(date_str: str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()


@require_GET
def daily_report(request):
    from datetime import datetime, time
    from django.utils import timezone

    date_str = request.GET.get("date")
    if date_str:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse({"error": "date format YYYY-MM-DD olmalı"}, status=400)
    else:
        target_date = timezone.localdate()

    tz = timezone.get_current_timezone()
    day_start = timezone.make_aware(datetime.combine(target_date, time.min), tz)
    day_end = timezone.make_aware(datetime.combine(target_date, time.max), tz)

    sessions = (
        Session.objects
        .select_related("student")
        .filter(start_time__gte=day_start, start_time__lte=day_end)
        .order_by("student_id", "start_time")
    )

    if not sessions.exists():
        return JsonResponse({"date": target_date.isoformat(), "students": []})

    logs = (
        BehaviorLog.objects
        .select_related("session")
        .filter(session__in=sessions)
        .order_by("created_at")
    )

    students_payload = {}

    for s in sessions:
        sid = s.student_id
        if sid not in students_payload:
            students_payload[sid] = {
                "student_id": sid,
                "student_name": s.student.name,
                "sessions": [],
                "logs": []
            }
        students_payload[sid]["sessions"].append(s)

    for log in logs:
        sid = log.session.student_id
        students_payload[sid]["logs"].append(log)

    result = []

    for data in students_payload.values():
        student_sessions = data["sessions"]
        student_logs = data["logs"]

        total_seconds = sum(
            s.duration_seconds or 0
            for s in student_sessions
        )

        risk_counts = {"0": 0, "1": 0, "2": 0, "unknown": 0}
        last_risk = None

        session_has_log = {s.id: False for s in student_sessions}

        for log in student_logs:
            rl = str(log.risk_level)
            if rl in risk_counts:
                risk_counts[rl] += 1
            last_risk = log.risk_level
            session_has_log[log.session_id] = True

        for has_log in session_has_log.values():
            if not has_log:
                risk_counts["unknown"] += 1

        notes_sample = []
        seen = set()
        for log in reversed(student_logs):
            note = (log.note or "").strip()
            if note and note not in seen:
                notes_sample.append(note)
                seen.add(note)
            if len(notes_sample) == 3:
                break
        notes_sample.reverse()

        if last_risk == 2:
            coach_message = "Buradayım. Hiçbir şey yapmak zorunda değilsin."
        elif last_risk == 1:
            coach_message = "Bugün sadece burada olman yeterli."
        else:
            coach_message = "Harika gidiyorsun. İstersen kısa bir ipucu paylaşabilirim."

        result.append({
            "student_id": data["student_id"],
            "student_name": data["student_name"],
            "sessions_count": len(student_sessions),
            "total_minutes": total_seconds // 60,
            "risk": {
                "last": last_risk,
                "counts": risk_counts
            },
            "notes_sample": notes_sample,
            "coach_message": coach_message
        })

        # --- SUMMARY (dashboard üst kartlar) ---
    total_students = len(result)
    total_sessions = sum(item["sessions_count"] for item in result)
    total_minutes = sum(item["total_minutes"] for item in result)

    summary_risk_counts = {"0": 0, "1": 0, "2": 0, "unknown": 0}
    for item in result:
        counts = item["risk"]["counts"]
        for k in summary_risk_counts.keys():
            summary_risk_counts[k] += int(counts.get(k, 0))

    def _pct(n, d):
        return round((n * 100.0 / d), 1) if d else 0.0

    summary_risk_percent = {
        "0": _pct(summary_risk_counts["0"], total_sessions),
        "1": _pct(summary_risk_counts["1"], total_sessions),
        "2": _pct(summary_risk_counts["2"], total_sessions),
        "unknown": _pct(summary_risk_counts["unknown"], total_sessions),
    }
    # Dashboard sıralaması: risk=2 en üst, sonra risk=1, sonra risk=0; eşitlikte dakika çok olan üstte
    result.sort(key=lambda x: (x["risk"]["last"] is None, -(x["risk"]["last"] or 0), -x["total_minutes"]))

    return JsonResponse({
        "date": target_date.isoformat(),
        "summary": {
            "total_students": total_students,
            "total_sessions": total_sessions,
            "total_minutes": total_minutes,
            "risk_counts": summary_risk_counts,
            "risk_percent": summary_risk_percent,
        },
        "students": result
    })

@require_GET
def weekly_report(request):
    """
    GET /api/weekly-report?start=YYYY-MM-DD
    - start verilmezse: bugün dahil geriye doğru 6 gün (son 7 gün)
    - Risk: session başına son log; yoksa unknown
    - Süre: açık unutulan/çok uzun oturumlar clamp edilir (3 saat)
    """
    from datetime import datetime, time, timedelta
    from django.utils import timezone

    start_str = request.GET.get("start")

    if start_str:
        try:
            start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse({"error": "start format YYYY-MM-DD olmalı"}, status=400)
    else:
        start_date = timezone.localdate() - timedelta(days=6)

    end_date = start_date + timedelta(days=6)

    tz = timezone.get_current_timezone()
    range_start = timezone.make_aware(datetime.combine(start_date, time.min), tz)
    range_end = timezone.make_aware(datetime.combine(end_date, time.max), tz)

    sessions_qs = (
        Session.objects
        .filter(start_time__gte=range_start, start_time__lte=range_end)
        .only("id", "start_time", "end_time", "duration_seconds")
    )

    session_ids = list(sessions_qs.values_list("id", flat=True))

    # session_id -> last risk_level
    last_risk_by_session = {}
    if session_ids:
        for row in (
            BehaviorLog.objects
            .filter(session_id__in=session_ids)
            .order_by("session_id", "created_at")
            .values("session_id", "risk_level")
        ):
            last_risk_by_session[row["session_id"]] = row["risk_level"]

    def empty_counts():
        return {"0": 0, "1": 0, "2": 0, "unknown": 0}

    # 7 günlük iskelet (clamped_sessions burada garanti 0 olarak başlar)
    days_map = {}
    for i in range(7):
        d = start_date + timedelta(days=i)
        days_map[d.isoformat()] = {
            "date": d.isoformat(),
            "sessions": 0,
            "minutes": 0,
            "clamped_sessions": 0,
            "risk_counts": empty_counts(),
        }

    MAX_SESSION_SECONDS = 3 * 60 * 60  # 3 saat

    for s in sessions_qs:
        day_key = timezone.localdate(s.start_time).isoformat()
        if day_key not in days_map:
            continue

        days_map[day_key]["sessions"] += 1

        # süre hesabı
        if s.duration_seconds is not None:
            sec = max(0, int(s.duration_seconds))
        elif s.end_time and s.start_time:
            sec = max(0, int((s.end_time - s.start_time).total_seconds()))
        else:
            sec = 0

        # clamp
        if sec > MAX_SESSION_SECONDS:
            sec = MAX_SESSION_SECONDS
            days_map[day_key]["clamped_sessions"] += 1

        days_map[day_key]["minutes"] += (sec // 60)

        # risk
        rl = last_risk_by_session.get(s.id)
        if rl in (0, 1, 2):
            days_map[day_key]["risk_counts"][str(rl)] += 1
        else:
            days_map[day_key]["risk_counts"]["unknown"] += 1

    days_list = [days_map[(start_date + timedelta(days=i)).isoformat()] for i in range(7)]
    series = {
        "labels": [d["date"] for d in days_list],
        "minutes": [d["minutes"] for d in days_list],
        "sessions": [d["sessions"] for d in days_list],
        "risk0": [d["risk_counts"]["0"] for d in days_list],
        "risk1": [d["risk_counts"]["1"] for d in days_list],
        "risk2": [d["risk_counts"]["2"] for d in days_list],
        "unknown": [d["risk_counts"]["unknown"] for d in days_list],
        "clamped_sessions": [d["clamped_sessions"] for d in days_list],
    }

    total_sessions = sum(d["sessions"] for d in days_list)
    total_minutes = sum(d["minutes"] for d in days_list)
    total_clamped = sum(d["clamped_sessions"] for d in days_list)

    total_risk_counts = {"0": 0, "1": 0, "2": 0, "unknown": 0}
    for d in days_list:
        for k in total_risk_counts:
            total_risk_counts[k] += int(d["risk_counts"].get(k, 0))

    return JsonResponse({
        "start": start_date.isoformat(),
        "end": end_date.isoformat(),
        "totals": {
            "sessions": total_sessions,
            "minutes": total_minutes,
            "clamped_sessions": total_clamped,
            "risk_counts": total_risk_counts,
        },        
            "series": series,
            "days": days_list,
    })
@require_GET
def open_sessions(request):
    qs = (
        Session.objects
        .select_related("student")
        .filter(end_time__isnull=True)
        .order_by("start_time")
    )

    now = timezone.now()
    items = []
    for s in qs:
        start = s.start_time or now
        open_seconds = max(0, int((now - start).total_seconds()))
        items.append({
            "session_id": s.id,
            "student_id": s.student_id,
            "student_name": s.student.name,
            "start_time": start.isoformat(),
            "open_minutes": open_seconds // 60,
        })

    return JsonResponse({
        "count": len(items),
        "sessions": items
    })
