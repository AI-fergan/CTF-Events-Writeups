FROM ruby:3.1

# Install dependencies
RUN apt-get update -qq && apt-get install -y \
    build-essential \
    libmariadb-dev-compat \
    libmariadb-dev \
    netcat-openbsd

# Set working directory
WORKDIR /app

# Copy Gemfile and install gems
COPY Gemfile ./
RUN bundle install

# Copy wait-for-it script
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Copy application code
COPY . .

# Expose port
EXPOSE 4567

# Start the application
CMD ["wait-for-it.sh", "db", "3306", "--", "rackup", "--host", "0.0.0.0", "--port", "4567"]
