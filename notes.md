
# CA

Reference:

- [create-ca](https://arminreiter.com/2022/01/create-your-own-certificate-authority-ca-using-openssl/)

```sh
➜  projects cd cryptoVault
➜  cryptoVault mkdir ca
➜  cryptoVault cd ca
➜  ca openssl genrsa -aes256 -out ca.key 4096
Enter PEM pass phrase:
Verifying - Enter PEM pass phrase:

➜  ca openssl req -x509 -new -nodes -key ca.key -sha256 -days 1826 -out ca.crt
Enter pass phrase for ca.key:
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:GR
State or Province Name (full name) [Some-State]:Xanthi
Locality Name (eg, city) []:Xanthi
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Crypto Vault Ltd
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:cryptoVault
Email Address []:

```
