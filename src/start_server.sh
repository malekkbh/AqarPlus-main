#! /usr/bin/env sh
set -e

export GRANIAN_HOST="0.0.0.0"
export GRANIAN_PORT="8080"
export GRANIAN_WORKERS=$(nproc) # Number of CPU cores
export GRANIAN_LOG_LEVEL="info"

flask db upgrade # Apply database migrations

# start granian
exec granian --no-access-log --interface wsgi 'wsgi:app'

# Wait for any process to exit
echo "Waiting for processes to exit..."
wait -n

# Exit with status of process that exited first
exit $?
