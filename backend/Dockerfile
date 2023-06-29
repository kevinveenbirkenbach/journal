FROM php:8.1-fpm
WORKDIR /var/www/
RUN apt-get update && apt-get install -y \
    zlib1g-dev \
    libxml2-dev \
    libzip-dev \
    libonig-dev \
    zip \
    curl \
    unzip
RUN docker-php-ext-install pdo_mysql mbstring zip exif pcntl
RUN pecl install xdebug \
    && docker-php-ext-enable xdebug
RUN curl -1sLf 'https://dl.cloudsmith.io/public/symfony/stable/setup.deb.sh' | bash 
RUN apt-get install -y symfony-cli
COPY --from=composer /usr/bin/composer /usr/bin/composer
COPY . /var/www/
CMD composer install ; php -S 0.0.0.0:8000 -t public
EXPOSE 8000
