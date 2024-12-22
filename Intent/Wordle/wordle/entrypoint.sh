#!/usr/bin/env bash

set -e

# Start gotty as the $USERNAME user
echo "Starting gotty"
gotty --address 0.0.0.0 --port 3000 --permit-write --reconnect /bin/bash