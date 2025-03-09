#!/bin/bash

# Define paths
GIT_PATH="/Users/basar/Documents/Manual Library/GitHub/RHT_RFID"
DRIVE_PATH="/Users/basar/Documents/Manual Library/Drive/RHT_RFID"

# Ensure drive directories exist
mkdir -p "$DRIVE_PATH/main"
mkdir -p "$DRIVE_PATH/simple_membership"

# Function to sync a branch
sync_branch() {
    local branch=$1
    local target_dir=$2
    
    echo "Syncing $branch branch to $target_dir..."
    
    # Switch to branch
    git -C "$GIT_PATH" checkout "$branch"
    
    # Sync files
    rsync -av --exclude='.git' \
              --exclude='venv' \
              --exclude='__pycache__' \
              --exclude='*.pyc' \
              --exclude='.DS_Store' \
              "$GIT_PATH/" "$target_dir/"
              
    echo "Sync complete for $branch"
}

# Update README with sync time
update_readme() {
    local date=$(date '+%Y-%m-%d %H:%M:%S')
    sed -i '' "s/^- Date:.*$/- Date: $date/" "$DRIVE_PATH/README.md"
}

# Main sync process
echo "Starting sync process..."

# Sync main branch
sync_branch "main" "$DRIVE_PATH/main"

# Sync simple_membership branch
sync_branch "simple_membership" "$DRIVE_PATH/simple_membership"

# Update README
update_readme

echo "Sync completed successfully!"
