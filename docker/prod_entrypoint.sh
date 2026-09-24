#!/bin/sh

# Disable Prisma telemetry and update checks to prevent hanging during bootstrap
export CHECKPOINT_DISABLE="${CHECKPOINT_DISABLE:-1}"
export PRISMA_TELEMETRY_INFORMATION="${PRISMA_TELEMETRY_INFORMATION:-0}"
export LITELLM_PRISMA_BOOTSTRAP_TIMEOUT="${LITELLM_PRISMA_BOOTSTRAP_TIMEOUT:-10}"
export NODE_OPTIONS="${NODE_OPTIONS:---max-old-space-size=256}"

case "$USE_DDTRACE" in
    [Tt][Rr][Uu][Ee])
        export DD_TRACE_OPENAI_ENABLED="False"
        exec ddtrace-run litellm --host 0.0.0.0 --port "${PORT:-4000}" "$@"
        ;;
esac

exec litellm --host 0.0.0.0 --port "${PORT:-4000}" "$@"
