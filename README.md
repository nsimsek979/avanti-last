# Avanti Global - Multi-language Django Website

A professional multi-language website for Avanti Global aviation catering services, built with Django and Bootstrap.

## Features

- 🌍 **Multi-language support** (English, Turkish, Romanian)
- 🏗️ **Hierarchical product categories**
- 📱 **Responsive Bootstrap design**
- 🔐 **Django Admin panel for content management**
- 🔧 **i18n/l10n internationalization**
- 📊 **Analytics dashboard**
- 🚀 **Production-ready deployment configuration**

## Local Development

### Prerequisites

- Python 3.8+
- pip
- virtualenv

### Installation

1. Clone the repository:
```bash
git clone https://github.com/nsimsek979/avanti-last.git
cd avanti-last
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Compile translations:
```bash
python manage.py compilemessages
```

7. Run development server:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to see the website.

## Production Deployment (Ubuntu Server)

### Quick Deployment

1. Copy the deployment script to your Ubuntu server:
```bash
scp deploy.sh user@your-server:/tmp/
```

2. Run the deployment script:
```bash
ssh user@your-server
sudo chmod +x /tmp/deploy.sh
sudo /tmp/deploy.sh
```

3. Configure your environment:
```bash
sudo nano /var/www/avanti/.env
```

4. Update settings with your domain:
```bash
sudo nano /var/www/avanti/avanti/settings_production.py
sudo nano /var/www/avanti/nginx.conf
```

5. Restart services:
```bash
sudo systemctl restart avanti nginx
```

### Manual Deployment

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib git

# Create application directory
sudo mkdir -p /var/www/avanti
cd /var/www/avanti

# Clone repository
sudo git clone https://github.com/nsimsek979/avanti-last.git .
```

#### 2. Python Environment

```bash
# Create virtual environment
sudo python3 -m venv venv
sudo chown -R www-data:www-data /var/www/avanti

# Activate and install packages
sudo -u www-data /var/www/avanti/venv/bin/pip install -r requirements.txt
sudo -u www-data /var/www/avanti/venv/bin/pip install -r requirements_production.txt
```

#### 3. Database Setup (PostgreSQL)

```bash
# Create database and user
sudo -u postgres psql -c "CREATE DATABASE avanti_db;"
sudo -u postgres psql -c "CREATE USER avanti_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE avanti_db TO avanti_user;"
```

#### 4. Django Configuration

```bash
# Copy environment template
sudo cp .env.example .env
sudo nano .env  # Edit with your values

# Django setup
export DJANGO_SETTINGS_MODULE=avanti.settings_production
sudo -u www-data /var/www/avanti/venv/bin/python manage.py collectstatic --noinput
sudo -u www-data /var/www/avanti/venv/bin/python manage.py migrate
sudo -u www-data /var/www/avanti/venv/bin/python manage.py compilemessages
sudo -u www-data /var/www/avanti/venv/bin/python manage.py createsuperuser
```

#### 5. Systemd Service

```bash
# Install service
sudo cp avanti.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable avanti
sudo systemctl start avanti
```

#### 6. Nginx Configuration

```bash
# Configure Nginx
sudo cp nginx.conf /etc/nginx/sites-available/avanti
sudo ln -sf /etc/nginx/sites-available/avanti /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

## Configuration Files

- `avanti/settings_production.py` - Production Django settings
- `gunicorn.conf.py` - Gunicorn WSGI server configuration
- `nginx.conf` - Nginx web server configuration
- `avanti.service` - Systemd service configuration
- `.env.example` - Environment variables template

## SSL/HTTPS Setup

For production, it's recommended to use Let's Encrypt for free SSL certificates:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Uncomment the HTTPS section in `nginx.conf` and update Django settings for SSL.

## Languages

To add new translations:

1. Add language code to `LANGUAGES` in settings.py
2. Create translation files:
```bash
python manage.py makemessages -l es  # for Spanish
```
3. Translate strings in locale/es/LC_MESSAGES/django.po
4. Compile translations:
```bash
python manage.py compilemessages
```

## Admin Panel

Access the admin panel at `/admin/` with your superuser credentials to manage:
- Content translations
- Product categories
- Services
- Client information
- Site analytics

## Support

For support and questions, please contact the development team.

## License

This project is proprietary software for Avanti Global.
