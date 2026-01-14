from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta
from .models import Visitor, PageView
from django.db.models import Count, Sum
import json


@staff_member_required
def analytics_dashboard(request):
    """Analytics dashboard view"""
    # Get selected period (default: 7 days)
    period = request.GET.get('period', '7')
    try:
        days = int(period)
    except:
        days = 7
    
    # Get stats for different periods
    stats_7days = Visitor.get_stats(7)
    stats_30days = Visitor.get_stats(30)
    stats_all = Visitor.get_stats(365)  # Last year
    
    # Current period stats
    current_stats = Visitor.get_stats(days)
    
    # Top pages
    start_date = timezone.now() - timedelta(days=days)
    top_pages = PageView.objects.filter(
        timestamp__gte=start_date
    ).values('url', 'title').annotate(
        views=Count('id')
    ).order_by('-views')[:10]
    
    # Recent visitors
    recent_visitors = Visitor.objects.all()[:20]
    
    # Hourly distribution (last 24 hours)
    last_24h = timezone.now() - timedelta(hours=24)
    hourly_data = {}
    for hour in range(24):
        hour_start = timezone.now().replace(minute=0, second=0, microsecond=0) - timedelta(hours=23-hour)
        hour_end = hour_start + timedelta(hours=1)
        count = Visitor.objects.filter(
            first_visit__gte=hour_start,
            first_visit__lt=hour_end
        ).count()
        hourly_data[hour_start.strftime('%H:00')] = count
    
    context = {
        'stats_7days': stats_7days,
        'stats_30days': stats_30days,
        'stats_all': stats_all,
        'current_stats': current_stats,
        'current_period': days,
        'top_pages': top_pages,
        'recent_visitors': recent_visitors,
        'hourly_data_json': json.dumps(hourly_data),
        'by_date_json': json.dumps(current_stats['by_date']),
        'by_country_json': json.dumps(current_stats['by_country']),
    }
    
    return render(request, 'analytics/dashboard.html', context)
