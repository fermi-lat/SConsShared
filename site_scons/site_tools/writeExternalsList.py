import os, os.path
import SCons.Action
import SCons.Builder

def generate(env):
    # Write a file in $INST_DIR/data directory listing externals
    # with versions used by this super-package
    def createExternalsList(target = None, source = None, env = None):
        fp = open(str(target[0]), 'w')
        fp.write("# externals required for this super-package \n\n")
        for ext in env['configuredExternals']:
            #print("writeExternalsList: Processing external " + str(ext["name"]))
            fp.write("%s-%s" %(ext["name"], ext["version"]))
            fp.write("\n")
        fp.close()
        return 0


    def createExternalsListGenerator(source, target, env, for_signature):
        actions = [env.Action(createExternalsList, "Creating externals list")]

        return actions

    suf = 'extList'

    env.Append(BUILDERS={'GenerateExternalsList' : env.Builder(generator=createExternalsListGenerator,
                                                         suffix=suf)})

def exists(env):
    return 1;

