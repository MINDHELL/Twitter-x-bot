# Use the official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the required files
COPY requirements.txt .
COPY bot.py .
COPY scraper.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its dependencies
RUN pip install playwright && playwright install && playwright install-deps

# Start the bot
CMD ["python", "bot.py"]
