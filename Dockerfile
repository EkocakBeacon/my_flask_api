# Use official Python 3.11 image
FROM python:3.11-slim

# Install system dependencies for pyodbc and ODBC drivers
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        curl \
        gnupg2 \
        unixodbc \
        unixodbc-dev \
        libgssapi-krb5-2 \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 10000

# Run with Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
