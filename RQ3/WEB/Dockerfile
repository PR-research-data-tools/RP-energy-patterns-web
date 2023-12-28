# Use the official PHP image with Apache
FROM php:7.4-apache

# Install any required PHP extensions
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Suppress the FQDN warning by setting a ServerName
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Copy your PHP source code into the image
COPY . /var/www/html/

# Expose port 80 to access the Apache server
EXPOSE 80
