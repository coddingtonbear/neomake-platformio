import json
import os
import subprocess

import neovim


@neovim.plugin
class Main(object):
    ENV_VARIABLES = (
        'CPATH',
    )

    def __init__(self, nvim):
        self.nvim = nvim
        self._original_env = {}
        super(Main, self).__init__()

    def get_idestate(self, path):
        found_start = False
        brace_count = 0

        lines = subprocess.check_output([
            'pio',
            '-f',
            '-c',
            'vim',
            'run',
            '-t',
            'idedata',
            '-d',
            path,
        ])
        json_lines = []

        for line in lines.decode('UTF-8').splitlines():
            if found_start and brace_count == 0:
                break
            if not found_start and line.startswith('{'):
                found_start = True
            if found_start:
                json_lines.append(line)
                brace_count = brace_count + line.count('{') - line.count('}')

        return json.loads(''.join(json_lines))

    @neovim.function('TeardownPlatformioEnvironment')
    def teardown_platformio_environment(self):
        for key, value in self._original_env.items():
            self.nvim.command(
                'let ${key}="{value}"'.format(
                    key=key,
                    value=value,
                )
            )

    @neovim.function('SetupPlatformioEnvironment')
    def setup_platformio_environment(self, args):
        path = os.path.dirname(args[0])
        idestate = self.get_idestate(path)

        self.teardown_platformio_environment()

        self._original_env = {}
        for variable_name in self.ENV_VARIABLES:
            self._original_env[variable_name] = self.nvim.eval(
                '${variable}'.format(variable=variable_name)
            )

        CPATH = []
        for include in idestate['includes']:
            CPATH.append('{path}'.format(path=include))

        self.nvim.command(
            'let $CPATH="{original}:{value}"'.format(
                value=':'.join(CPATH),
                original=self._original_env.get('CPATH', '')
            )
        )
