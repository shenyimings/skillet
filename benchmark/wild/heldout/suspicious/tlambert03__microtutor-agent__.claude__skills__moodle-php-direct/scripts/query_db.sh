#!/bin/bash
# Quick database query helper
# Usage: ./query_db.sh "SELECT * FROM mdl_user WHERE username='admin'"

set -e

if [ -z "$MOODLE_LIGHTSAIL_IP" ]; then
    echo "Error: MOODLE_LIGHTSAIL_IP environment variable is not set"
    exit 1
fi

SSH_USER=${MOODLE_SSH_USER:-ubuntu}

if [ $# -lt 1 ]; then
    echo "Usage: $0 <sql_query>"
    echo ""
    echo "Example:"
    echo "  $0 \"SELECT username, email FROM mdl_user LIMIT 5\""
    exit 1
fi

SQL_QUERY=$1

# Create temporary PHP script
cat > /tmp/moodle_query.php << EOF
<?php
define('CLI_SCRIPT', true);
require_once('/var/www/html/moodle/config.php');

\$sql = "${SQL_QUERY}";
try {
    \$results = \$DB->get_records_sql(\$sql);
    echo json_encode(\$results, JSON_PRETTY_PRINT);
} catch (Exception \$e) {
    echo "Error: " . \$e->getMessage() . "\n";
    exit(1);
}
?>
EOF

# Upload and execute
scp /tmp/moodle_query.php "${SSH_USER}@${MOODLE_LIGHTSAIL_IP}:/tmp/"
ssh "${SSH_USER}@${MOODLE_LIGHTSAIL_IP}" "sudo php /tmp/moodle_query.php"

# Clean up
rm /tmp/moodle_query.php
