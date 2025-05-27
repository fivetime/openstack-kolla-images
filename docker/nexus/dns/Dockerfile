FROM alpine:latest

LABEL org.opencontainers.image.source="https://github.com/openstack"
LABEL org.opencontainers.image.description="Nexus DNS"
LABEL org.opencontainers.image.licenses="Apache-2.0"

# Install dnsmasq and tools
RUN apk add --no-cache \
    dnsmasq \
    curl \
    jq \
    bind-tools \
    iproute2 \
    procps \
    bash

# Install kubectl
ARG KUBECTL_VERSION=v1.33.0
RUN curl -L -o /usr/local/bin/kubectl \
    "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl" \
    && chmod +x /usr/local/bin/kubectl

# Create nexus user
RUN addgroup -g 42424 nexus \
    && adduser -D -u 42424 -G nexus nexus

# Create directories
RUN mkdir -p /var/log/nexus/dnsmasq \
    && mkdir -p /etc/nexus \
    && mkdir -p /var/lib/nexus \
    && mkdir -p /shared/config \
    && mkdir -p /etc/dnsmasq.d \
    && chown -R nexus:nexus /var/log/nexus \
    && chown -R nexus:nexus /etc/nexus \
    && chown -R nexus:nexus /var/lib/nexus \
    && chown -R nexus:nexus /shared/config \
    && chown -R nexus:nexus /etc/dnsmasq.d

# Health check using dig
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD dig @127.0.0.1 kubernetes.default.svc.cluster.local +short +time=3 >/dev/null || exit 1

EXPOSE 53/udp 53/tcp

USER nexus