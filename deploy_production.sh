#!/bin/bash

# Avanti Django Production Deployment Script
# Bu script'i sunucuda çalıştırın

echo "🚀 Avanti Django Production Deployment başlatılıyor..."

# 1. Gerekli dizinleri oluştur
echo "📁 Gerekli dizinler oluşturuluyor..."
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/log/django
sudo mkdir -p /var/run/gunicorn
sudo mkdir -p /var/www/avanti/staticfiles
sudo mkdir -p /var/www/avanti/media

# 2. İzinleri ayarla
echo "🔐 İzinler ayarlanıyor..."
sudo chown -R www-data:www-data /var/www/avanti
sudo chown -R www-data:www-data /var/log/gunicorn
sudo chown -R www-data:www-data /var/log/django
sudo chown -R www-data:www-data /var/run/gunicorn
sudo chmod -R 755 /var/www/avanti

# 3. Virtual environment'ı aktifleştir ve bağımlılıkları yükle
echo "📦 Bağımlılıklar yükleniyor..."
cd /var/www/avanti
source venv/bin/activate
pip install -r requirements_production.txt

# 4. Django migrations ve static files
echo "🗄️ Django migrations çalıştırılıyor..."
export DJANGO_SETTINGS_MODULE=avanti.settings_production
python manage.py migrate
python manage.py collectstatic --noinput

# 5. Systemd service dosyasını kopyala ve etkinleştir
echo "⚙️ Systemd service kuruluyor..."
sudo cp avanti.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable avanti.service

# 6. Nginx konfigürasyonunu kopyala
echo "🌐 Nginx konfigürasyonu ayarlanıyor..."
sudo cp nginx.conf /etc/nginx/sites-available/avanti
sudo ln -sf /etc/nginx/sites-available/avanti /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 7. Nginx konfigürasyonunu test et
echo "🔍 Nginx konfigürasyonu test ediliyor..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Nginx konfigürasyonu başarılı!"

    # 8. Servisleri başlat
    echo "🚀 Servisler başlatılıyor..."
    sudo systemctl restart avanti.service
    sudo systemctl restart nginx

    # 9. Servis durumlarını kontrol et
    echo "📊 Servis durumları kontrol ediliyor..."
    echo "Avanti Service Status:"
    sudo systemctl status avanti.service --no-pager -l

    echo "Nginx Service Status:"
    sudo systemctl status nginx --no-pager -l

    echo "🎉 Deployment tamamlandı!"
    echo "🌐 Site adresi: http://avanti.konnektomdev.com"
    echo "📝 Log dosyaları:"
    echo "   - Gunicorn: /var/log/gunicorn/"
    echo "   - Django: /var/log/django/"

else
    echo "❌ Nginx konfigürasyonu hatası! Lütfen nginx.conf dosyasını kontrol edin."
    exit 1
fi
