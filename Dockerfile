# Multi-stage build for Python web scraper
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

# Create non-root user for security
RUN useradd -m -u 1000 scraper && \
    mkdir -p /app && \
    chown -R scraper:scraper /app

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/scraper/.local

# Copy application code
COPY scraper/ ./scraper/

# Set PATH to include user local bin
ENV PATH=/home/scraper/.local/bin:$PATH

# Switch to non-root user
USER scraper

# Default command
CMD ["python", "-c", "from scraper.main import int_extractor; print('Container is ready')"]
