#!/bin/bash

# Ubuntu Server Deployment Script for Avanti Django Application
# Run this script as root or with sudo

echo "🚀 Starting Avanti Django Deployment..."

# Update system
apt update && apt upgrade -y

# Install required packages
apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib git

# Create application user
if ! id "www-data" &>/dev/null; then
    useradd --system --group --home /var/www --shell /bin/bash www-data
fi

# Create application directory
mkdir -p /var/www/avanti
cd /var/www/avanti

# Clone the repository
git clone https://github.com/nsimsek979/avanti-last.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install -r requirements_production.txt

# Create environment file
cp .env.example .env
echo "⚠️  Please edit /var/www/avanti/.env with your production values"

# Create log directories
mkdir -p /var/log/django
mkdir -p /var/log/gunicorn
mkdir -p /var/run/gunicorn
chown -R www-data:www-data /var/log/django
chown -R www-data:www-data /var/log/gunicorn
chown -R www-data:www-data /var/run/gunicorn

# Set permissions
chown -R www-data:www-data /var/www/avanti

# Setup PostgreSQL (optional)
echo "Setting up PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE avanti_db;"
sudo -u postgres psql -c "CREATE USER avanti_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE avanti_db TO avanti_user;"

echo "📝 Database created. Please update your .env file with the correct credentials."

# Django setup
echo "Setting up Django..."
export DJANGO_SETTINGS_MODULE=avanti.settings_production
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py compilemessages

# Create superuser (optional)
echo "Creating Django superuser..."
python manage.py createsuperuser

# Install systemd service
cp avanti.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable avanti
systemctl start avanti

# Configure Nginx
cp nginx.conf /etc/nginx/sites-available/avanti
ln -sf /etc/nginx/sites-available/avanti /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

# Enable firewall
ufw allow 'Nginx Full'
ufw allow OpenSSH
ufw --force enable

echo "✅ Deployment completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit /var/www/avanti/.env with your production values"
echo "2. Update ALLOWED_HOSTS in settings_production.py"
echo "3. Configure SSL certificates (Let's Encrypt recommended)"
echo "4. Update nginx.conf with your domain name"
echo "5. Restart services: systemctl restart avanti nginx"
echo ""
echo "🌐 Your site should be available at http://your-server-ip"
