from subprocess import run, PIPE


class OpenSSL:
    """openssl"""

    STDIN = '/dev/stdin'
    BIN = 'openssl'

    SERVER_KEY = 'server.key'
    SERVER_CSR = 'server.csr'
    SERVER_CRT = 'server.crt'

    def __call__(self, *args, input=None, encoding='utf-8'):
        cp = run([self.BIN, *args], input=input, stdout=PIPE,
                 encoding=encoding)

        if cp.returncode == 0:
            return cp.stdout.strip()
        else:
            return ''

    @staticmethod
    def cp(*args):
        return run(['cp', *args], stdout=PIPE).returncode == 0

    def version(self):
        return self('version')

    def gensra(self, passout, crypto='des3', bits='1024'):
        return self('genrsa', f'-{crypto}',
                    '-out', self.SERVER_KEY,
                    '-passout', f'pass:{passout}',
                    bits)

    def req(self, passin, C='CN', ST='ST', L='LOC', O='ON', OU='OUN',
            CN='COMM', emailAddress='email'):
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
        input_password     = {passin}

        [ req_distinguished_name ]
        C            = {C}
        ST           = {ST}
        L            = {L}
        O            = {O}
        OU           = {OU}
        CN           = {CN}
        emailAddress = {emailAddress}
        """

        # config_file = 'server.req.config'
        # with open(config_file, 'w') as f:
        #     f.write(CONFIG_TEMPLATE)

        return self('req', '-new',
                    '-key', self.SERVER_KEY,
                    '-out', self.SERVER_CSR,
                    '-config', self.STDIN,
                    input=CONFIG_TEMPLATE)

    def remove_passphrase(self, passin):
        SERVER_KEY_ORIGINAL = f'{self.SERVER_KEY}.original'
        self.cp(self.SERVER_KEY, SERVER_KEY_ORIGINAL)
        return self('rsa', '-in', SERVER_KEY_ORIGINAL,
                    '-out', self.SERVER_KEY,
                    '-passin', f'pass:{passin}')

    def x509(self, days='365'):
        return self('x509', '-req',
                    '-days', days,
                    '-in', self.SERVER_CSR,
                    '-signkey', self.SERVER_KEY,
                    '-out', self.SERVER_CRT)
