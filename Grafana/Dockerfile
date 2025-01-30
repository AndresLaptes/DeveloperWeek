FROM grafana/grafana:latest

# Create necessary directories and copy everything
USER root

# Create grafana user and group if they don't exist
RUN addgroup --system grafana || true && \
    adduser --system --ingroup grafana grafana || true

# Copy your entire Grafana configuration directory
COPY ./etc/grafana /etc/grafana
COPY ./var/lib/grafana /var/lib/grafana

# Fix permissions
RUN chown -R grafana:grafana /etc/grafana /var/lib/grafana

USER grafana

EXPOSE 3000
