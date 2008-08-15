# -*- coding: utf-8 -*-
"""Recipe release"""

import re
egg_name_re = re.compile(r'(\S+?)([=<>!].+)')

from getpaid.recipe.release.getpaidcorepackages import GETPAID_CORE_PACKAGES

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        # These are passed onto zc.recipe.egg.
        options['eggs'] = self.getpaid_eggs()

    def install(self):
        """Installer"""
        # XXX Implement recipe functionality here
        
        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return tuple()

    def update(self):
        """Updater"""
        pass

    def getpaid_eggs(self):
        """Read the eggs from dist_plone
        """
        egg_spec = self.options.get('eggs', '')
        explicit_eggs = {}
        for spec in egg_spec.split():
            name = spec
            version = ''
            match = egg_name_re.match(spec)
            if match:
                name = match.groups(1)
                version = match.groups(2)
            explicit_eggs[name] = version
        
        eggs = []
        for pkg in GETPAID_CORE_PACKAGES:
            name = pkg.name
            if name in explicit_eggs:
                eggs.append(name + explicit_eggs[name])
                del explicit_eggs[name]
            else:
                if pkg.version is not None:
                    name += "==%s" % pkg.version
                eggs.append(name)
        
        for name, version in explicit_eggs.items():
            eggs.append(name + version)
        
        return '\n'.join(eggs)
