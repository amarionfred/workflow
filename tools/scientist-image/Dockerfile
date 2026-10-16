# Keep the upstream checkout and its built image intact. This local layer
# updates only two vulnerable transitive dependencies in Headless.
ARG BASE_IMAGE
FROM ${BASE_IMAGE}
USER root
WORKDIR /opt/headless
COPY patch-dependencies.py /tmp/patch-headless-dependencies.py
RUN python /tmp/patch-headless-dependencies.py
USER agent
WORKDIR /workspace
