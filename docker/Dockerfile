FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx supervisor curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Baked into the image so it doesn't depend on the host's own venv (which is
# tied to a specific system Python install/ABI). App code, the frontend
# build, and uploads/ are bind-mounted at runtime (see docker-compose.yml)
# so a normal `git pull` + `npm run build` on the host takes effect with
# just a container restart — no image rebuild needed for routine deploys.
COPY api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY docker/nginx.conf /etc/nginx/sites-enabled/default
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
