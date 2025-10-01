module.exports = {
  apps: [{
    name: 'avanti-django',
    script: '/var/www/avanti/venv/bin/python',
    args: '/var/www/avanti/venv/bin/gunicorn --config /var/www/avanti/gunicorn.conf.py avanti.wsgi:application',
    cwd: '/var/www/avanti',
    env: {
      DJANGO_SETTINGS_MODULE: 'avanti.settings_production'
    },
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    error_file: '/var/log/pm2/avanti-error.log',
    out_file: '/var/log/pm2/avanti-out.log',
    log_file: '/var/log/pm2/avanti.log',
    time: true
  }]
}