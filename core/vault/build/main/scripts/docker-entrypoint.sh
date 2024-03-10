#!/bin/ash

vault server \
	-config /conf/vault-main.hcl \
	-config /conf/vault-storage.hcl \
	-config /conf/vault-listener.hcl > /dev/null 2>&1