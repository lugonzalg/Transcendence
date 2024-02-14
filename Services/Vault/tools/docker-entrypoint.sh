#!/bin/sh

vault server \
	-config /tmp/vault-main.hcl \
	-config /tmp/vault-storage.hcl \
	-config /tmp/vault-listener.hcl
