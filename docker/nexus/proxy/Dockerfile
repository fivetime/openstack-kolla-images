FROM nginx:1.25-alpine

LABEL org.opencontainers.image.source="https://github.com/fivetime/nexus"
LABEL org.opencontainers.image.description="Nexus Proxy - Dynamic OpenStack API proxy"
LABEL org.opencontainers.image.licenses="Apache-2.0"

# Install required tools
RUN apk add --no-cache \
    curl \
    jq \
    bind-tools \
    iproute2 \
    procps \
    bash

# Install kubectl
ARG KUBECTL_VERSION=v1.28.0
RUN curl -L -o /usr/local/bin/kubectl \
    "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl" \
    && chmod +x /usr/local/bin/kubectl

# Create directories
RUN mkdir -p /var/log/nexus \
    && mkdir -p /shared/config \
    && chown -R nginx:nginx /var/log/nexus \
    && chown -R nginx:nginx /shared/config

# Remove default config
RUN rm -f /etc/nginx/conf.d/default.conf

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/nginx-health || exit 1

EXPOSE 80 443 8080

USER nginx