from django.db import models
from django.utils import timezone
from datetime import timedelta
import requests

class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    session_key = models.CharField(max_length=40, db_index=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    user_agent = models.TextField(blank=True)
    first_visit = models.DateTimeField(auto_now_add=True, db_index=True)
    last_visit = models.DateTimeField(auto_now=True)
    page_views = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['-first_visit']
        verbose_name = 'Visitor'
        verbose_name_plural = 'Visitors'
        indexes = [
            models.Index(fields=['-first_visit']),
            models.Index(fields=['session_key']),
        ]
    
    def __str__(self):
        return f"{self.ip_address} - {self.country or 'Unknown'} ({self.first_visit.strftime('%Y-%m-%d %H:%M')})"
    
    def get_location_from_ip(self):
        """Get location data from IP address using ipapi.co"""
        if not self.country:
            try:
                response = requests.get(f'https://ipapi.co/{self.ip_address}/json/', timeout=2)
                if response.status_code == 200:
                    data = response.json()
                    self.country = data.get('country_name', '')
                    self.country_code = data.get('country_code', '')
                    self.city = data.get('city', '')
                    self.save(update_fields=['country', 'country_code', 'city'])
            except:
                pass
    
    @classmethod
    def get_stats(cls, days=7):
        """Get visitor statistics for the last N days"""
        start_date = timezone.now() - timedelta(days=days)
        visitors = cls.objects.filter(first_visit__gte=start_date)
        
        total_visitors = visitors.count()
        total_page_views = visitors.aggregate(total=models.Sum('page_views'))['total'] or 0
        
        # Group by country
        by_country = visitors.values('country', 'country_code').annotate(
            count=models.Count('id')
        ).order_by('-count')[:10]
        
        # Group by date
        by_date = {}
        for visitor in visitors:
            date_key = visitor.first_visit.date()
            if date_key not in by_date:
                by_date[date_key] = {'visitors': 0, 'page_views': 0}
            by_date[date_key]['visitors'] += 1
            by_date[date_key]['page_views'] += visitor.page_views
        
        # Format by_date for JSON
        by_date_list = [
            {'date': str(date), 'count': stats['visitors'], 'page_views': stats['page_views']}
            for date, stats in sorted(by_date.items(), key=lambda x: x[0])
        ]
        
        return {
            'total_visitors': total_visitors,
            'total_page_views': total_page_views,
            'by_country': list(by_country),
            'by_date': by_date_list,
            'start_date': start_date,
            'end_date': timezone.now(),
        }


class PageView(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='views')
    url = models.CharField(max_length=500)
    title = models.CharField(max_length=200, blank=True)
    referrer = models.CharField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Page View'
        verbose_name_plural = 'Page Views'
    
    def __str__(self):
        return f"{self.url} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
