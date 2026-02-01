# Build stage
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy source code into 'backend' directory to preserve package structure
# assuming 'backend' is the build context, copying '.' copies contents of backend.
# We want /app/backend/app/...
COPY . ./backend

# Add /app to PYTHONPATH so 'backend.app...' imports work
ENV PYTHONPATH=/app

EXPOSE 8000

# Run uvicorn pointing to the correct module
CMD ["uvicorn", "backend.app.server:app", "--host", "0.0.0.0", "--port", "8000"]
