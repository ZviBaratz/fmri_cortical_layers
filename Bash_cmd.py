import platform
import os


def bash_get(cmd):
    is32bit = platform.architecture()[0] == "32bit"
    system32 = os.path.join(
        os.environ["SystemRoot"], "SysNative" if is32bit else "System32"
    )
    bash = os.path.join(system32, "bash.exe")
    cmd = cmd.replace("C:", "/mnt/c")
    cmd = cmd.replace(os.sep, "/")
    cmd = r'{0} {1}'.format(bash,cmd)
    return cmd
