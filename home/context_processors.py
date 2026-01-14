from home.models import HeroSection

def hero_image(request):
    """Make hero image available in all templates"""
    hero = HeroSection.objects.filter(is_active=True).first()
    return {
        'hero_image': hero.image if hero and hero.image else None
    }
