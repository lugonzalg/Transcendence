listener "tcp" {
    address = "0.0.0.0:8200"
    tls_cert_file = "/cert/vault.crt"
    tls_key_file  = "/cert/vault.key"
}