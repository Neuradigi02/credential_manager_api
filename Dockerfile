#  base image
FROM python:3.13.2

WORKDIR /app

# Install Dependencies
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && apt-get clean

# for neccessry files
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


#  to whole file copy 
COPY . .

# Set Environment Variable for PDFKit
ENV PATH="/usr/bin:$PATH"
ENV WKHTMLTOPDF_PATH="/usr/bin/wkhtmltopdf"


#  port 
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
