FROM python:3.12-slim
# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install packages first (changes rarely)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Set Playwright browser location to a shared path
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Install Playwright browsers as root
RUN playwright install chromium
RUN playwright install-deps chromium

# Create a non-root user and switch to non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Give appuser access to browsers
RUN chown -R appuser:appuser /ms-playwright

COPY src/ ./src/

USER appuser