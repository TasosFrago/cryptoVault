
# CA

Reference:

- [create-ca](https://arminreiter.com/2022/01/create-your-own-certificate-authority-ca-using-openssl/)

- [use_ca](https://www.golinuxcloud.com/openssl-create-client-server-certificate/)

```bash
$ cd cryptoVault
cryptoVault $ mkdir ca
cryptoVault $ cd ca
ca $ openssl genrsa -aes256 -out ca.key 4096
Enter PEM pass phrase:
Verifying - Enter PEM pass phrase:

ca $ openssl req -config openss.cnf -key private/ca.key -new -x509  -days 7300 -sha256 -extensions v3_ca -out ./certs/ca.crt -subj "/C=GR/ST=Xanthi/L=Xanthi/O=cryptoVault/CN=ca"
Enter pass phrase for private/ca.key:

ca $ openssl x509 -noout -text -in certs/ca.crt
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            16:1d:dc:79:4e:32:b8:8d:a9:aa:fa:f9:cc:d5:0c:7c:64:6f:7a:8a
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=GR, ST=Xanthi, L=Xanthi, O=cryptoVault, CN=ca
        Validity
            Not Before: May 24 14:29:53 2025 GMT
            Not After : May 19 14:29:53 2045 GMT
        Subject: C=GR, ST=Xanthi, L=Xanthi, O=cryptoVault, CN=ca
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (4096 bit)
                Modulus:
                    00:9b:99:c1:3b:3d:b6:0f:0d:c8:90:d4:58:7b:db:
                    36:f6:a1:09:bc:1e:f7:22:4d:9c:fc:8f:67:04:2e:
                    a5:a7:09:87:63:a8:a7:07:80:fb:76:32:20:08:be:
                    2d:9a:82:6e:b8:69:29:03:e7:ea:9e:a9:4f:00:ae:
                    05:94:43:dc:a0:80:72:67:de:7a:7f:6f:59:3c:cc:
                    a4:46:10:6a:ce:de:86:e3:34:2b:f1:5d:46:71:8e:
                    5c:1b:e9:cd:e0:19:98:c7:a7:15:8e:81:08:03:fd:
                    cb:f0:04:91:02:77:1f:cd:ac:f5:ff:6f:73:06:b0:
                    85:eb:3b:12:a1:65:65:43:46:cb:a8:92:41:40:d7:
                    4e:e0:5d:56:53:a8:2f:1c:4b:05:5d:4e:d3:a3:69:
                    6e:f9:20:c3:58:c8:01:55:dd:31:73:ff:ff:d8:00:
                    8b:bf:0b:d5:77:67:a4:52:46:54:3a:30:1a:07:2b:
                    66:88:1c:36:89:8e:b9:5c:ac:37:64:36:e5:69:7b:
                    0e:a7:a1:d7:9c:f2:ec:45:41:06:e5:04:40:0d:40:
                    d0:f3:f5:0c:ff:07:b9:50:10:6e:c7:30:46:f7:87:
                    af:44:c9:cf:1a:f8:e0:f7:bd:15:9f:a0:ef:59:95:
                    32:d5:1f:91:6f:5c:4b:45:b0:1a:2f:b1:d1:57:b0:
                    63:2d:83:10:17:97:44:dd:02:7c:62:ad:7d:dd:70:
                    2f:46:72:2c:ad:f4:e2:dc:26:3d:6b:85:bb:90:71:
                    a6:9b:f8:91:03:70:9a:4a:ab:f4:5e:d8:ee:71:e5:
                    34:a8:55:77:af:eb:52:ce:a4:a4:de:02:11:14:d6:
                    b9:a3:f2:df:17:26:28:43:51:65:0f:0c:31:2f:cf:
                    01:37:3f:98:8e:45:9a:e1:27:d2:4c:84:9b:df:fd:
                    7b:18:9a:4d:6f:03:32:5e:c8:04:58:4a:cb:c7:7b:
                    9b:55:50:b6:09:57:4f:6e:c7:d7:73:f9:f5:84:5d:
                    68:cb:93:d6:04:41:99:a6:18:a8:93:8c:f0:74:2a:
                    79:aa:9f:33:74:34:64:12:b0:f7:2c:c3:f0:60:d6:
                    79:5a:3b:70:64:56:a5:63:e4:c4:c5:7f:f8:7a:ce:
                    8b:59:f6:24:59:44:0a:b5:fe:b5:fa:bc:0c:10:d6:
                    94:3b:0f:d8:ab:26:1f:95:0a:20:f6:7f:64:e4:5e:
                    24:79:74:35:af:29:3b:37:63:c0:c2:1c:68:88:80:
                    dc:ef:58:d6:95:c9:3e:9c:f6:00:cc:ea:d2:f0:fa:
                    5d:d3:dd:b4:71:6b:82:b8:e9:f8:6a:bc:d6:0c:fc:
                    14:bb:e3:ef:24:7e:3c:33:0c:e8:eb:1c:d6:cb:ca:
                    e8:a0:df
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Subject Key Identifier:
                E9:A7:29:07:B5:9F:01:99:CE:7E:40:57:DE:A9:1C:88:F3:31:BF:E9
            X509v3 Authority Key Identifier:
                E9:A7:29:07:B5:9F:01:99:CE:7E:40:57:DE:A9:1C:88:F3:31:BF:E9
            X509v3 Basic Constraints: critical
                CA:TRUE
            X509v3 Key Usage: critical
                Certificate Sign
    Signature Algorithm: sha256WithRSAEncryption
    Signature Value:
        73:92:08:74:bc:d7:05:63:6c:33:b3:1a:22:3b:9a:28:4e:31:
        7b:ba:5d:90:cc:4b:28:01:2c:68:b8:e1:35:10:65:89:ac:20:
        80:9d:08:44:dc:45:36:be:01:22:8e:f7:a9:d3:c2:a9:44:cc:
        d7:bc:27:2c:cb:1e:fb:1d:e9:c3:c0:af:32:9c:60:59:c2:d6:
        34:7f:13:a4:4c:df:40:bf:2c:f4:a5:88:da:3b:3f:c5:02:8c:
        5a:37:fc:2c:d7:0c:75:41:a0:7b:8b:9e:57:58:dc:1d:9f:ff:
        94:37:ac:e1:f7:15:ee:8c:78:43:96:5d:85:8d:a1:a5:84:36:
        1b:47:01:03:03:a2:d3:fe:15:5b:55:6f:0e:32:a2:0b:52:e3:
        f9:37:ff:76:8f:ba:aa:a5:c5:95:5d:ef:7c:22:46:80:86:30:
        a0:eb:5b:75:23:cd:23:97:1f:00:c7:c1:37:db:d6:95:f4:0b:
        9f:e7:77:e5:14:89:8d:06:98:74:2a:9b:91:b8:60:f3:cc:3f:
        f9:77:96:78:eb:f8:ec:f7:02:ce:31:8d:5c:8a:88:1f:83:c8:
        32:42:25:b4:1c:cb:2a:66:fc:f1:92:31:00:19:0f:91:8f:2f:
        82:a5:4e:23:c9:33:93:ea:46:40:34:1c:bf:23:18:f5:1e:c2:
        37:a2:a3:49:89:a7:d4:25:b3:a6:d8:84:7c:eb:a6:d4:9c:dc:
        66:28:11:5f:a8:8a:42:63:b0:71:4f:b7:3a:0e:87:5a:1c:1a:
        e8:2e:09:0d:58:39:71:01:1e:9f:3e:d6:e3:02:9a:cf:d7:21:
        6a:9e:24:51:14:fd:48:d9:58:f5:93:44:90:8c:2f:4f:7a:51:
        b4:97:54:f3:5b:17:a8:1a:01:0f:43:f1:4a:3b:1a:4b:5f:a2:
        31:0e:3d:d1:eb:25:48:24:13:2f:cf:dc:32:6f:11:ab:14:52:
        e6:f9:9a:19:c0:7c:64:ca:a8:19:50:45:63:4a:5b:01:ef:17:
        2d:21:a8:31:1d:b8:13:bf:29:ab:8a:89:e0:07:5a:25:dc:19:
        c9:e0:25:55:28:13:21:62:41:5a:73:fc:16:ee:1c:5d:51:17:
        30:e9:64:9a:7d:04:32:e3:3b:13:28:bd:0f:95:92:a6:d5:81:
        85:fa:a9:f6:d1:17:cf:2c:56:fa:6b:12:9f:85:15:1d:d3:7f:
        d7:67:c2:fd:d6:2c:fa:1b:30:4f:f5:d8:f9:3b:f2:fb:b2:10:
        6e:d8:a0:55:a0:9a:f2:b4:de:fe:56:68:b2:9a:5b:b0:2d:26:
        ae:13:f4:2b:0c:07:f5:07:2f:a2:6b:ae:4e:f7:7a:6f:5d:70:
        a7:8c:75:f5:9d:f8:6d:8f

ca $ openssl genpkey -algorithm RSA -out private/app.key -pkeyopt rsa_keygen_bits:2048
....+.+...........+.........+.......+..+++++++++++++++++++++++++++++++++++++++*......+........+.+......+........+....+.................+++++++++++++++++++++++++++++++++++++++*.+.+......+...+......+..+....+........+............+.+.....+...+......+.+..+.............+.....+.......+.....+...+............................+.........+...+..+.......+.....+.+...+.....+......+...+...++++++
.+.+.........+++++++++++++++++++++++++++++++++++++++*...+.+..+.............+++++++++++++++++++++++++++++++++++++++*...+......+.+.....+....+..+....+...+...+..+.............+..............+.+..+.+...............+......+...+......+.....+....+..+.+.........+........+.+.....+.......+.....+.............+.....+......+..........+...+..+....+..+............+...+....+.........+......+...........+.......+..+.............+..+....+..+.........+.+...+......+.....+...+......+.......+..+.+...........++++++
ca $ openssl genpkey -algorithm RSA -out private/user1.key -pkeyopt rsa_keygen_bits:2048
...+...+..+++++++++++++++++++++++++++++++++++++++*..+....+......+...+.........+...+++++++++++++++++++++++++++++++++++++++*...+..+..........+.....+......+.........+.+...............+......+.....+.+..+...............+...+.......+..+.+..............+.+.........++++++
...........+...+...+...+.+...+...+..+............+.............+..+.+...+..+++++++++++++++++++++++++++++++++++++++*........+.+.....+............+......+.+...+..+.............+............+...+..+......+...+++++++++++++++++++++++++++++++++++++++*...+........+.......+.....+.+...........................+........+....+..+...+.+......+.........+............+..+......+.......+...+.....+......+...+.+..............+.+.........+......+..+...+......+...++++++
ca $ openssl genpkey -algorithm RSA -out private/user2.key -pkeyopt rsa_keygen_bits:2048
...+.....+..........+...+.....+.+.....+.+...+..+.......+........+....+...+..+....+.........+...+...+.........+.....+.+..+...+.........+..........+..+++++++++++++++++++++++++++++++++++++++*.........+....+..+....+++++++++++++++++++++++++++++++++++++++*.............+.+........+......+.........+.+...+......+..+......................+..+....+.....+.......++++++
....+....+......+.....+...+.+.....+....+........+...+....+..+....+..+..........+.....+....+...........+...+++++++++++++++++++++++++++++++++++++++*...+.......+.....+.+......+......+.....+....+.........+......+++++++++++++++++++++++++++++++++++++++*.......+......+...+.+...+...+...+.....+......+..........+...............+.........+...........+...+......+...........................+...+.+...+..+.+.....+...+.........+..........+..+....+...............+.....+.+...+..+.........+..........+.........+...+..+...+....+.....+.+...+..+.......+..+...+...+.......+...........+....+........+..........+..................+.....+.+...+...+.........+...+...........+....+...+............+..+.........+.+...+...........+......+.+.........+........+.......+........+............+......+.......+............+..............+.+......+.........+...............+.....++++++
ca $ openssl genpkey -algorithm RSA -out private/user3.key -pkeyopt rsa_keygen_bits:2048
.....+++++++++++++++++++++++++++++++++++++++*....................+......+.........+....+...+........+....+......+++++++++++++++++++++++++++++++++++++++*.....+......+....+..+....+............+...+..+.........+......+....+......+...+..+............+.......+.....+......+...+....+..+.+.....+...+............+...+....+......+.........+...........+.........+...+.........+..........+........+......+.+..................+...+...+...........+..........+...+.....+...+.......+...........+.+......+..................+..++++++
.....+.....+......+++++++++++++++++++++++++++++++++++++++*........+........+.+.....+......+....+.....+...+...+...+.+...+++++++++++++++++++++++++++++++++++++++*....+..........+..............+......+...............+.......+...+............+..+.+........+......+...+...+...+....+..+...+.......+...+...+........+......+.+..+...+.......+.....+......+.........+.+..+....+...+.....+.+......+..............+.+......+..+...+.......+........+.........+....+.........+..+...+................+.....+......+.+...............+...............+..................+..+...+................+.....+.........+.......+.........+.....+.+...+.....+.+.....+.+.....+...+.......+.....+.........+....+.....+....+..+..........+........+...+............+................+......+.....+.+..+...+...+....+.....+.......+...+......+..+............+.+.....................+...+...+..+.+..+...+.......+..............+....+..+....+....................+.+........+......+...+...++++++
ca $ openssl genpkey -algorithm RSA -out private/user4.key -pkeyopt rsa_keygen_bits:2048
...+..+............+.........+.+.....+..........+.....+......+...+....+......+..+++++++++++++++++++++++++++++++++++++++*....+...+.....+.......+........+......+....+..+............+.+++++++++++++++++++++++++++++++++++++++*....+.........+......+.+.........+......+...+.................+.............+..+....+...+...+..+...+............+......+.+...............+...+...........+.+...+...+........+...................+......+......+........++++++
......+.....+...+......+.........+....+..+.+..+...+....+++++++++++++++++++++++++++++++++++++++*...+...+..+++++++++++++++++++++++++++++++++++++++*.+.......+.....+.+.....+.......+...............+..+.......+...........+...+.+.....+..............................+..................+.+..+...+.+.........+....................+.+...+........+....+...+...+...............+..+.......+...+.....+..........+...+........+....+..+.+...............+...+..+...+......+..........+.....+......+.........+...+............+...+...+....+.........+..+.........+...+.......+.....+.+.........+......+..+......+..................................+........+.............+......+...+.....+.......+......+..+...+............+...+.......+......+.....+......+.+.....+...............+...+.+...+...........+.+...+..+.+..+......+......+....+............+............+......+..............+...+....+.........++++++
ca $ openssl genpkey -algorithm RSA -out private/user5.key -pkeyopt rsa_keygen_bits:2048
...+++++++++++++++++++++++++++++++++++++++*.+.........+.....+....+...+..+...+....+...+.................+...+.......+.........+..+...+.+.........+..+.............+.....+......+.+..+.+..+..........+.....+.......+......+..+...+....+......+..+....+.........+++++++++++++++++++++++++++++++++++++++*...........+.........+....+.....+....+..+.............+...............+......+..+...+.......+...+......+.....+...+............+...+...+.............+.........+........++++++
..+.......+.....+...+....+++++++++++++++++++++++++++++++++++++++*......+........+......+....+...+............+......+..+...+++++++++++++++++++++++++++++++++++++++*..+...............+.....+......+...+......+....+...............+...............+......++++++

ca $ openssl req -new -key private/vault.key -out certs/vault.csr -subj "/C=GR/ST=Xanthi/L=Xanthi/O=cryptoVault/CN=vault"

ca $ for i in 1 2 3 4 5; do
        openssl req -new -key "private/user$i.key" -out "certs/user$i.csr" -subj "/C=GR/ST=Xanthi/O=cryptoVault/CN=user$i"
    done

ca $ ls certs
ca.crt  user1.csr  user2.csr  user3.csr  user4.csr  user5.csr  vault.csr

ca $ openssl ca -config openss.cnf -extensions usr_cert -days 365 -notext -md sha256 -in certs/vault.csr -out certs/vault.crt

Using configuration from openss.cnf
Enter pass phrase for /home/tasos/projects/cryptoVault/ca/private/ca.key:
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number: 4097 (0x1001)
        Validity
            Not Before: May 24 15:30:30 2025 GMT
            Not After : May 24 15:30:30 2026 GMT
        Subject:
            countryName               = GR
            stateOrProvinceName       = Xanthi
            organizationName          = cryptoVault
            commonName                = vault
        X509v3 extensions:
            X509v3 Basic Constraints:
                CA:FALSE
            Netscape Cert Type:
                SSL Client, S/MIME
            Netscape Comment:
                User Certificate
            X509v3 Subject Key Identifier:
                19:08:DA:63:EC:C1:D6:91:70:7E:A4:9B:41:51:BC:FE:23:83:DD:A0
            X509v3 Authority Key Identifier:
                E9:A7:29:07:B5:9F:01:99:CE:7E:40:57:DE:A9:1C:88:F3:31:BF:E9
            X509v3 Key Usage: critical
                Digital Signature, Non Repudiation, Key Encipherment
            X509v3 Extended Key Usage:
                TLS Web Client Authentication, E-mail Protection
Certificate is to be certified until May 24 15:30:30 2026 GMT (365 days)
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Database updated

ca $ for i in 1 2 3 4 5; do
        openssl ca -config openss.cnf -extensions usr_cert -days 365 -notext -md sha256 -in "certs/user$i.csr" -out "certs/user$i.crt"
    done

Using configuration from openss.cnf
Enter pass phrase for /home/tasos/projects/cryptoVault/ca/private/ca.key:
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number: 4098 (0x1002)
        Validity
            Not Before: May 24 15:34:43 2025 GMT
            Not After : May 24 15:34:43 2026 GMT
        Subject:
            countryName               = GR
            stateOrProvinceName       = Xanthi
            organizationName          = cryptoVault
            commonName                = user1
        X509v3 extensions:
            X509v3 Basic Constraints:
                CA:FALSE
            Netscape Cert Type:
                SSL Client, S/MIME
            Netscape Comment:
                User Certificate
            X509v3 Subject Key Identifier:
                85:A7:90:8E:F7:AC:A0:8D:DB:35:BB:C9:AA:EC:99:AD:5B:19:B4:16
            X509v3 Authority Key Identifier:
                E9:A7:29:07:B5:9F:01:99:CE:7E:40:57:DE:A9:1C:88:F3:31:BF:E9
            X509v3 Key Usage: critical
                Digital Signature, Non Repudiation, Key Encipherment
            X509v3 Extended Key Usage:
                TLS Web Client Authentication, E-mail Protection
Certificate is to be certified until May 24 15:34:43 2026 GMT (365 days)
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Database updated
Using configuration from openss.cnf
Enter pass phrase for /home/tasos/projects/cryptoVault/ca/private/ca.key:
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number: 4099 (0x1003)
        Validity
            Not Before: May 24 15:34:48 2025 GMT
            Not After : May 24 15:34:48 2026 GMT
        Subject:
            countryName               = GR
            stateOrProvinceName       = Xanthi
            organizationName          = cryptoVault
            commonName                = user2
        X509v3 extensions:
            X509v3 Basic Constraints:
                CA:FALSE
            Netscape Cert Type:
                SSL Client, S/MIME
            Netscape Comment:
                User Certificate
            X509v3 Subject Key Identifier:
                5A:E6:03:B4:84:9B:67:A0:13:4B:FB:7F:48:34:14:B9:58:BD:E7:60
            X509v3 Authority Key Identifier:
                E9:A7:29:07:B5:9F:01:99:CE:7E:40:57:DE:A9:1C:88:F3:31:BF:E9
            X509v3 Key Usage: critical
                Digital Signature, Non Repudiation, Key Encipherment
            X509v3 Extended Key Usage:
                TLS Web Client Authentication, E-mail Protection
Certificate is to be certified until May 24 15:34:48 2026 GMT (365 days)
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Database updated
Using configuration from openss.cnf
Enter pass phrase for /home/tasos/projects/cryptoVault/ca/private/ca.key:
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number: 4100 (0x1004)
        Validity
            Not Before: May 24 15:34:51 2025 GMT
            Not After : May 24 15:34:51 2026 GMT
        Subject:
            countryName               = GR
            stateOrProvinceName       = Xanthi
            organizationName          = cryptoVault
            commonName                = user3
        X509v3 extensions:
            X509v3 Basic Constraints:
                CA:FALSE
            Netscape Cert Type:
                SSL Client, S/MIME
            Netscape Comment:
                User Certificate
            X509v3 Subject Key Identifier:
                8B:18:BC:2A:DD:CC:E1:2E:3D:30:A6:36:05:C5:0D:D6:80:06:FD:6A
            X509v3 Authority Key Identifier:
                E9:A7:29:07:B5:9F:01:99:CE:7E:40:57:DE:A9:1C:88:F3:31:BF:E9
            X509v3 Key Usage: critical
                Digital Signature, Non Repudiation, Key Encipherment
            X509v3 Extended Key Usage:
                TLS Web Client Authentication, E-mail Protection
Certificate is to be certified until May 24 15:34:51 2026 GMT (365 days)
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Database updated
Using configuration from openss.cnf
Enter pass phrase for /home/tasos/projects/cryptoVault/ca/private/ca.key:
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number: 4101 (0x1005)
        Validity
            Not Before: May 24 15:34:57 2025 GMT
            Not After : May 24 15:34:57 2026 GMT
        Subject:
            countryName               = GR
            stateOrProvinceName       = Xanthi
            organizationName          = cryptoVault
            commonName                = user4
        X509v3 extensions:
            X509v3 Basic Constraints:
                CA:FALSE
            Netscape Cert Type:
                SSL Client, S/MIME
            Netscape Comment:
                User Certificate
            X509v3 Subject Key Identifier:
                54:3A:98:80:BB:D3:4F:9C:14:42:62:79:49:6E:D1:6E:83:8D:D8:66
            X509v3 Authority Key Identifier:
                E9:A7:29:07:B5:9F:01:99:CE:7E:40:57:DE:A9:1C:88:F3:31:BF:E9
            X509v3 Key Usage: critical
                Digital Signature, Non Repudiation, Key Encipherment
            X509v3 Extended Key Usage:
                TLS Web Client Authentication, E-mail Protection
Certificate is to be certified until May 24 15:34:57 2026 GMT (365 days)
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Database updated
Using configuration from openss.cnf
Enter pass phrase for /home/tasos/projects/cryptoVault/ca/private/ca.key:
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number: 4102 (0x1006)
        Validity
            Not Before: May 24 15:35:00 2025 GMT
            Not After : May 24 15:35:00 2026 GMT
        Subject:
            countryName               = GR
            stateOrProvinceName       = Xanthi
            organizationName          = cryptoVault
            commonName                = user5
        X509v3 extensions:
            X509v3 Basic Constraints:
                CA:FALSE
            Netscape Cert Type:
                SSL Client, S/MIME
            Netscape Comment:
                User Certificate
            X509v3 Subject Key Identifier:
                DA:EA:A2:2C:2E:02:E2:91:C6:D5:35:E9:4B:7C:CB:DB:CD:5C:A7:0B
            X509v3 Authority Key Identifier:
                E9:A7:29:07:B5:9F:01:99:CE:7E:40:57:DE:A9:1C:88:F3:31:BF:E9
            X509v3 Key Usage: critical
                Digital Signature, Non Repudiation, Key Encipherment
            X509v3 Extended Key Usage:
                TLS Web Client Authentication, E-mail Protection
Certificate is to be certified until May 24 15:35:00 2026 GMT (365 days)
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Database updated

ca $ openssl verify -CAfile certs/ca.crt  certs/vault.crt
certs/vault.crt: OK
```
