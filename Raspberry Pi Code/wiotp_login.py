from sys import path
path.insert(0,"/home/pi")
path.insert(0,"/usr/local/lib/python3.7/dist-packages")

import auth_ibm_iam

try:
    from wiotp.sdk.device import DeviceClient #changed from import wiotp.sdk.device
except ImportError:
    # This part is only required to run the sample from within the samples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import wiotp.sdk"
    from inspect import getfile, currentframe

    cmd_subfolder = path.realpath(
        path.abspath(path.join(path.split(getfile(currentframe()))[0], "../../../src"))
    )
    if cmd_subfolder not in path:
        path.insert(0, cmd_subfolder)
    import wiotp.sdk.device

client = DeviceClient(auth_ibm_iam.query_wiotp_info()) # create a client using preset values
