#!/bin/bash
set -e

printenv | grep -E '^(LEGO_|PUSHOVER_)' | sed 's/^/export /' > /etc/environment.cron

chmod 600 /etc/environment.cron
tr -d '\r' < /etc/environment.cron > /tmp/environment.cron && mv /tmp/environment.cron /etc/environment.cron

exec cron -f