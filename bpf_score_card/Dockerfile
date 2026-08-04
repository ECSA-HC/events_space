FROM php:8.3-apache

RUN docker-php-ext-install pdo pdo_mysql

# Apache serves from /var/www/html by default; the app's own relative asset
# paths (assets/css/..., email.php, etc.) work unchanged whether this is
# reached directly or proxied under /scorecard/ by the main app's nginx.
COPY . /var/www/html/

EXPOSE 80
