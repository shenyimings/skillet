#!/bin/bash
# Execute a PHP script on the Moodle server
# Usage: ./exec_php.sh <local_php_file>

set -e

if [ -z "$MOODLE_LIGHTSAIL_IP" ]; then
    echo "Error: MOODLE_LIGHTSAIL_IP environment variable is not set"
    exit 1
fi

SSH_USER=${MOODLE_SSH_USER:-ubuntu}

if [ $# -lt 1 ]; then
    echo "Usage: $0 <local_php_file>"
    exit 1
fi

PHP_FILE=$1

if [ ! -f "$PHP_FILE" ]; then
    echo "Error: File not found: $PHP_FILE"
    exit 1
fi

# Upload and execute
REMOTE_TMP="/tmp/$(basename $PHP_FILE)"
scp "$PHP_FILE" "${SSH_USER}@${MOODLE_LIGHTSAIL_IP}:${REMOTE_TMP}"
ssh "${SSH_USER}@${MOODLE_LIGHTSAIL_IP}" "sudo php ${REMOTE_TMP}"
