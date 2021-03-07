#!/bin/bash

# Start the run once job.
echo "Docker container has been started"

# Setup a cron schedule
echo "*/30 * * * * /app/submit.sh  > /dev/stdout" >> /etc/cron.d/scheduler
# This extra line makes it a valid cron" > scheduler.txt

crontab /etc/cron.d/scheduler

./submit.sh
cron -f