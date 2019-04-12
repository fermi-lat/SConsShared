import os, os.path
import SCons.Action
import SCons.Builder
from subprocess import call
from glob import glob

def generate(env):
    # Make user, source or developer tarball
    def createTarball(target = None, source = None, env = None):
        # Form tar command which outputs to target; execute with popen
        # from root dir of the installation.
        # Determine release type by looking for value of env variable
        # RELEASE_TYPE - one of 'user', 'source', 'devel'

        # We need the following for all release types
        args = ['tar', '-czf', str(target[0]), '--exclude', 'build', '--exclude', env['PLATBRIEF'], '--exclude', 'config.log', '--exclude', '"*.tar.gz"', '--exclude-vcs', '--exclude-backups' ]
        rtp = env['RELEASE_TYPE']

        # Build products should be excluded for source, included for dev & user
        products = env['products']
        
        contents = glob('../*')
        for i,v in enumerate(contents):
            contents[i] = v[3:]

        # --exclude of *.tar.gz isn't working properly, so exclude by hand here
        for v in contents:
            if v[len(v) - 6:] == 'tar.gz': contents.remove(v)
        # Remove from products anything not in contents
        for v in products:
            if v not in contents: products.remove(v)

        if rtp == 'source':
            # exclude products, explicitly ask for everything else
            for e in products:
                contents.remove(e)
            args.extend(contents)
        elif rtp == 'user':
            args.extend(products)

        elif rtp == 'devel':
            args.extend(contents)

        #print 'Args are: ', args
        r = call(args, cwd='../')
        if r != 0: print("subprocess.call returned ", r)

    def createTarballGenerator(source, target, env, for_signature):
        actions = [env.Action(createTarball, "Creating release tarball")]

        return actions

    env.Append(BUILDERS={'GenerateReleaseTarball' : env.Builder(generator=createTarballGenerator)})

def exists(env):
    return 1;

