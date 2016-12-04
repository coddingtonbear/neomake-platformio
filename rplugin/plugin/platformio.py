import json
import subprocess

import neovim


@neovim.plugin
class Main(object):
    def __init__(self, nvim):
        self.nvim = nvim

    def get_idestate(self, path):
        found_start = False
        brace_count = 0

        lines = subprocess.check_output([
            'pio',
            'run',
            '-t',
            'idedata',
            '-d',
            path,
        ])
        json_lines = []

        for line in lines:
            if found_start and brace_count == 0:
                break
            if not found_start and line.startswith('{'):
                found_start = True
            if found_start:
                json_lines.append(line)
                brace_count = brace_count + line.count('{') - line.count('}')

        return json.loads(''.join(json_lines))

    @neovim.function('SetupPlatformioEnvironment', nargs=1)
    def setup_platformio_environment(self, args):
        path = args[0]
        idestate = self.get_idestate(path)

        with open('/tmp/output.txt') as out:
            out.write(json.dumps(idestate, indent=4, sort_keys=True))
