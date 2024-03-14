#!/bin/sh

set -e

certbot certonly \
	--webroot -w "/var/www/certbot" \
	--email "$EMAIL" \
	--force-renewal \
	--agree-tos \
	--domains "$DOMAIN"
