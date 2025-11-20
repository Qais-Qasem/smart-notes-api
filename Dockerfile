# 1. Choose a lightweight Python base image (Linux-based)
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file first
# (We do this before copying the code to use Docker's cache efficiently)
COPY requirements.txt .

# 4. Install dependencies
# --no-cache-dir: Keeps the image small by not saving temporary cache files
# We explicitly point to the CPU version of PyTorch to save massive space (GBs)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container
COPY . .

# 6. Expose the port the app runs on
EXPOSE 8000

# 7. The command to run the application
# host 0.0.0.0 is crucial for Docker (it makes the app accessible from outside the container)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]