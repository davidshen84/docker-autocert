#!/usr/bin/env python3

from subprocess import run, PIPE


STDIN = '/dev/stdin'
OPENSSL_BIN = '/usr/local/opt/openssl/bin/openssl'

INSECURE_PASS = '1234'

SERVER_KEY = 'server.key'
SERVER_CSR = 'server.csr'
SERVER_CRT = 'server.crt'


def openssl(*args, input=None, encoding='utf-8'):
    cp = run([OPENSSL_BIN, *args], input=input, stdout=PIPE, encoding=encoding)

    if cp.returncode == 0:
        return cp.stdout.strip()
    # .decode('utf-8').strip()
    else:
        return ''


def cp(*args):
    return run(['cp', *args], stdout=PIPE).returncode == 0


def get_openssl_version():
    return openssl('version')


def gensra(crypto='des3', passout=INSECURE_PASS, bits='1024'):
    return openssl('genrsa', f'-{crypto}',
                   '-out', SERVER_KEY,
                   '-passout', f'pass:{passout}',
                   bits)


def req(C='CN', ST='ST', L='LOC', O='ON', OU='OUN', CN='COMM',
        emailAddress='email', passin=INSECURE_PASS):
    """Generate request

    @param C Country
    @param ST State
    @param L Local
    @param O Organization
    @param OU Organizatio Unit
    @param CN Common Name
    @param emailAddress Email address
    """

    CONFIG_TEMPLATE = f"""
[ req ]
prompt             = no
default_bits       = 1024
distinguished_name = req_distinguished_name
input_password     = {INSECURE_PASS}

[ req_distinguished_name ]
C            = {C}
ST           = {ST}
L            = {L}
O            = {O}
OU           = {OU}
CN           = {CN}
emailAddress = {emailAddress}
"""

    config_file = 'server.req.config'
    with open(config_file, 'w') as f:
        f.write(CONFIG_TEMPLATE)

    return openssl('req', '-new',
                   '-key', SERVER_KEY,
                   '-out', SERVER_CSR,
                   '-config', STDIN,
                   input=CONFIG_TEMPLATE)


def remove_passphrase():
    SERVER_KEY_ORIGINAL = f'{SERVER_KEY}.original'
    cp(SERVER_KEY, SERVER_KEY_ORIGINAL)
    return openssl('rsa', '-in', SERVER_KEY_ORIGINAL,
                   '-out', SERVER_KEY,
                   '-passin', f'pass:{INSECURE_PASS}')


def x509(days='365'):
    return openssl('x509', '-req',
                   '-days', days,
                   '-in', SERVER_CSR,
                   '-signkey', SERVER_KEY,
                   '-out', SERVER_CRT)


if __name__ == '__main__':
    print(get_openssl_version())
    print(gensra())
    print(req())
    print(remove_passphrase())
    print(x509())
