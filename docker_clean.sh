#!/bin/bash
DOCKER_USERNAME="$1"
DOCKER_PASSWORD="$2"
REPO_NAME="flaskaws"

# Fetch all image tags from Docker Hub and sort them numerically
TAGS=$(curl -s -H "Authorization: Bearer $DOCKER_PASSWORD" \
"https://hub.docker.com/v2/repositories/$DOCKER_USERNAME/$REPO_NAME/tags/?page_size=1000" | jq -r ".results[].name" | sort -V)

# Store tags in an array (correct way to handle multiline output)
mapfile -t TAG_ARRAY <<< "$TAGS"

KEEP_COUNT=20
TOTAL_TAGS=${#TAG_ARRAY[@]}

if (( TOTAL_TAGS > KEEP_COUNT )); then
  DELETE_TAGS=("${TAG_ARRAY[@]:0:TOTAL_TAGS-KEEP_COUNT}")

  for TAG in "${DELETE_TAGS[@]}"; do
      echo "Deleting image: $TAG"
      curl -X DELETE -H "Authorization: Bearer $DOCKER_PASSWORD" \
      "https://hub.docker.com/v2/repositories/$DOCKER_USERNAME/$REPO_NAME/tags/$TAG"
  done
else
  echo "No old images to delete. Less than or equal to $KEEP_COUNT images exist."
fi  
