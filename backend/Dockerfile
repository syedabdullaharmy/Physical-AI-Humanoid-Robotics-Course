FROM python:3.11-slim

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Install system dependencies (as root before switching, or sudo if needed, but for slim image we need to do this before switching user or use root to install)
# Re-ordering to install as root first
USER root
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application with ownership
COPY --chown=user app/ ./app/
COPY --chown=user scripts/ ./scripts/

# Switch back to non-root user
USER user

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
