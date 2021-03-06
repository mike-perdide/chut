# -*- coding: utf-8 -*-
import os


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        dest = self.buildout['buildout']['directory']
        dest = os.path.join(dest, 'bin')
        dest = os.path.expanduser(self.options.get('destination', dest))
        self.options['destination'] = dest

    def scripts(self):
        import chut.scripts
        args = ['--destination', self.options.get('destination')]
        for line in self.options.get('locations', '.').split():
            chut.scripts.chutify(args + [line])

    def run(self, update=False):
        import chut as sh
        if update:
            sh.env.buildout_update = '1'
        sh.env.path += os.pathsep + self.options.get('destination')
        run = self.options.get('run', '')
        for line in run.split('\n'):
            line = line.strip()
            if not line:
                continue
            print('$ %s' % line)
            if ' ' in line:
                binary, args = line.split(' ', 1)
                sh[binary](args) > 2
            else:
                binary = line
                sh[line]() > 2
        return ()

    def install(self):
        """Installer"""
        self.scripts()
        self.run(update=False)
        return ()

    def update(self):
        """Update"""
        self.scripts()
        self.run(update=True)
        return ()
