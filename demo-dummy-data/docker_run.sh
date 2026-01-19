#!/bin/bash
# Docker build and run script for Komplai Demo Pipeline
# Target runtime: Linux

set -e

IMAGE_NAME="komplai-demo-pipeline"
CONTAINER_NAME="komplai-pipeline-run"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "  Komplai Demo Pipeline - Docker Runner"
echo "=========================================="

# Parse arguments
BUILD_ONLY=false
RUN_ONLY=false
INTERACTIVE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --build-only)
            BUILD_ONLY=true
            shift
            ;;
        --run-only)
            RUN_ONLY=true
            shift
            ;;
        -it|--interactive)
            INTERACTIVE=true
            shift
            ;;
        -h|--help)
            echo ""
            echo "Usage: ./docker_run.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --build-only    Only build the image, don't run"
            echo "  --run-only      Only run (skip build, image must exist)"
            echo "  -it             Run in interactive mode (bash shell)"
            echo "  -h, --help      Show this help message"
            echo ""
            echo "Environment variables (set before running):"
            echo "  SMTP_EMAIL           Gmail address for sending emails"
            echo "  SMTP_PASSWORD        Gmail App Password (16 chars)"
            echo "  RECIPIENT_EMAIL      Email recipient (default: demo-komplai@gmail.com)"
            echo "  GOOGLE_SHEET_ID      Google Sheets ID"
            echo "  GOOGLE_CREDENTIALS_JSON  Base64-encoded service account JSON"
            echo ""
            echo "Example:"
            echo "  export SMTP_EMAIL='demo-komplai@gmail.com'"
            echo "  export SMTP_PASSWORD='xxxx-xxxx-xxxx-xxxx'"
            echo "  ./docker_run.sh"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Build the image
if [ "$RUN_ONLY" = false ]; then
    echo ""
    echo -e "${YELLOW}[Step 1] Building Docker image...${NC}"
    echo ""

    docker build \
        --platform linux/amd64 \
        -t "$IMAGE_NAME" \
        .

    echo ""
    echo -e "${GREEN}✓ Image built successfully: $IMAGE_NAME${NC}"
fi

if [ "$BUILD_ONLY" = true ]; then
    echo ""
    echo -e "${GREEN}Build complete. Use --run-only to run the container.${NC}"
    exit 0
fi

# Remove existing container if it exists
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo ""
    echo -e "${YELLOW}Removing existing container...${NC}"
    docker rm -f "$CONTAINER_NAME" > /dev/null 2>&1
fi

# Prepare environment variables
ENV_ARGS=""

if [ -n "$SMTP_EMAIL" ]; then
    ENV_ARGS="$ENV_ARGS -e SMTP_EMAIL=$SMTP_EMAIL"
fi

if [ -n "$SMTP_PASSWORD" ]; then
    ENV_ARGS="$ENV_ARGS -e SMTP_PASSWORD=$SMTP_PASSWORD"
fi

if [ -n "$RECIPIENT_EMAIL" ]; then
    ENV_ARGS="$ENV_ARGS -e RECIPIENT_EMAIL=$RECIPIENT_EMAIL"
else
    ENV_ARGS="$ENV_ARGS -e RECIPIENT_EMAIL=demo.komplai@gmail.com"
fi

if [ -n "$GOOGLE_SHEET_ID" ]; then
    ENV_ARGS="$ENV_ARGS -e GOOGLE_SHEET_ID=$GOOGLE_SHEET_ID"
fi

if [ -n "$GOOGLE_CREDENTIALS_JSON" ]; then
    ENV_ARGS="$ENV_ARGS -e GOOGLE_CREDENTIALS_JSON=$GOOGLE_CREDENTIALS_JSON"
fi

# Check for local credentials file and encode if env var not set
if [ -z "$GOOGLE_CREDENTIALS_JSON" ] && [ -f "dummy-data-483609-2b5f128b43ad.json" ]; then
    echo -e "${YELLOW}Using local credentials file...${NC}"
    GOOGLE_CREDENTIALS_JSON=$(base64 -w 0 dummy-data-483609-2b5f128b43ad.json 2>/dev/null || base64 -i dummy-data-483609-2b5f128b43ad.json)
    ENV_ARGS="$ENV_ARGS -e GOOGLE_CREDENTIALS_JSON=$GOOGLE_CREDENTIALS_JSON"
fi

# Set default Google Sheet ID if not provided
if [ -z "$GOOGLE_SHEET_ID" ]; then
    ENV_ARGS="$ENV_ARGS -e GOOGLE_SHEET_ID=1KXGIa1G8q7PMMC5FSbj7mzgIaszRMHsikevdVpw_0Aw"
fi

# Run the container
echo ""
echo -e "${YELLOW}[Step 2] Running container...${NC}"
echo ""

if [ "$INTERACTIVE" = true ]; then
    echo "Starting interactive shell..."
    docker run -it --rm \
        --name "$CONTAINER_NAME" \
        --platform linux/amd64 \
        $ENV_ARGS \
        -v "$(pwd)/output:/app/output" \
        -v "$(pwd)/Komplai_Demo_Master (Claude).xlsx:/app/Komplai_Demo_Master (Claude).xlsx" \
        "$IMAGE_NAME" \
        /bin/bash
else
    docker run --rm \
        --name "$CONTAINER_NAME" \
        --platform linux/amd64 \
        $ENV_ARGS \
        -v "$(pwd)/output:/app/output" \
        -v "$(pwd)/Komplai_Demo_Master (Claude).xlsx:/app/Komplai_Demo_Master (Claude).xlsx" \
        "$IMAGE_NAME"

    echo ""
    echo -e "${GREEN}=========================================="
    echo "  Pipeline Complete"
    echo "==========================================${NC}"
    echo ""
    echo "Output PDFs saved to: ./output/pdfs/"
fi
