import os
import shutil
import shlex
import subprocess
import sys

from utils import ParaLogger, configtransport


def cleanup(mountpoint, tc_mountpoint, tempdir, value_from_argparser):
    try:
        cleanupLogger = ParaLogger('cleanup')
        parser = configtransport()

        #
        # Unmounting Truecrypt
        #
        try:
            if os.path.exists(tc_mountpoint) and os.path.ismount(tc_mountpoint):
                cleanupLogger.info("Unmounting Truecrypt Container")
                cleanupLogger.debug('UNMOUNT COMMAND: ' + parser.get('truecrypting', 'unmount'))
                subprocess.check_call(shlex.split(parser.get('truecrypting', 'unmount')))

        except OSError:
            cleanupLogger.error("Could not unmount tc container on {}").format(tc_mountpoint)
            cleanupLogger.exception("Could not unmount tc container on {}").format(tc_mountpoint)

        #
        # Unmounting USB-Stick
        #

        try:
            if value_from_argparser and os.path.exists(mountpoint) and os.path.ismount(mountpoint) is True:
                cleanupLogger.info("Unmounting USB-Stick")
                if (sys.platform == "darwin"):
                    subprocess.check_call(['diskutil', 'eject', mountpoint])
                else:
                    subprocess.check_call(["umount", mountpoint])
        except OSError:
            cleanupLogger.error("Could not umount {}").format(mountpoint)
            cleanupLogger.exception("Could not umount {}").format(mountpoint)

        #
        # Removing Temporary Directories
        #

        cleanupLogger.info("Cleaning up Temporary Directories")

        try:
            if value_from_argparser and os.path.exists(mountpoint) and os.path.ismount(mountpoint) is False:
                shutil.rmtree(mountpoint)
            if os.path.exists(tc_mountpoint) and os.path.ismount(tc_mountpoint) is False:
                shutil.rmtree(tc_mountpoint)
            if (sys.platform == "darwin") and os.path.exists(tempdir+"/dmg") and os.path.ismount(tempdir+"/dmg"):
                subprocess.check_call(['diskutil', 'eject', os.path.join(tempdir+"/dmg/")])
            elif os.path.exists(tempdir+"/dmg") and os.path.ismount(tempdir+"/dmg"):
                subprocess.check_call(['umount', os.path.join(tempdir+"/dmg/")])
            if os.path.exists(tempdir):
                shutil.rmtree(tempdir)
        except OSError:
            cleanupLogger.error("Some temporary Directories could not be removed")
            cleanupLogger.exception("Some temporary Directories could not be removed")

    except KeyboardInterrupt:
        cleanupLogger.error("You've hit Strg+C for interrupting Parabird. Now clean up your own mess. Exiting...")
        sys.exit()


def cleanup_failed(mountpoint, tc_mountpoint, tempdir, value_from_argparser, container_name):
    try:
        cleanupLogger = ParaLogger('cleanup')
        parser = configtransport()

        #
        # Unmounting Truecrypt
        #
        try:
            if os.path.exists(tc_mountpoint) and os.path.ismount(tc_mountpoint) is True:
                cleanupLogger.info("Unmounting Truecrypt Container")
                cleanupLogger.debug('UNMOUNT COMMAND: ' + parser.get('truecrypting', 'unmount'))
                subprocess.check_call(shlex.split(parser.get('truecrypting', 'unmount')))

        except OSError:
            cleanupLogger.error("Could not unmount tc container on {}").format(tc_mountpoint)
            cleanupLogger.exception("Could not unmount tc container on {}").format(tc_mountpoint)
        #
        # Delete incomplete TC-Container
        #

        try:
            if os.path.exists(tc_mountpoint+"/"+container_name) and os.path.ismount(tc_mountpoint) is False:
                cleanupLogger.info("Deleting incomplete TC-Container")
                cleanupLogger.debug("Deleting incomplete TC-Container")
                shutil.rmtree(tc_mountpoint+"/"+container_name)

        except OSError:
            cleanupLogger.error("Could not delete TC-Container: {}").format(tc_mountpoint+"/"+container_name)
            cleanupLogger.exception("Could not delete TC-Container on {}").format(tc_mountpoint+"/"+container_name)

        #
        # Unmounting USB-Stick
        #

        try:
            if value_from_argparser and os.path.exists(mountpoint) and os.path.ismount(mountpoint) is True:
                cleanupLogger.info("Unmounting USB-Stick")
                if (sys.platform == "darwin"):
                    subprocess.check_call(['diskutil', 'eject', mountpoint])
                else:
                    subprocess.check_call(["umount", mountpoint])
        except OSError:
            cleanupLogger.error("Could not umount {}").format(mountpoint)
            cleanupLogger.exception("Could not umount {}").format(mountpoint)

        #
        # Removing Temporary Directories
        #

        cleanupLogger.info("Cleaning up Temporary Directories")

        try:
            if value_from_argparser and os.path.exists(mountpoint) and os.path.ismount(mountpoint) is False:
                shutil.rmtree(mountpoint)
            if os.path.exists(tc_mountpoint) and os.path.ismount(tc_mountpoint) is False:
                shutil.rmtree(tc_mountpoint)
            if (sys.platform == "darwin") and os.path.exists(tempdir+"/dmg") and os.path.ismount(tempdir+"/dmg"):
                subprocess.check_call(['diskutil', 'eject', os.path.join(tempdir+"/dmg/")])
            elif os.path.exists(tempdir+"/dmg") and os.path.ismount(tempdir+"/dmg"):
                subprocess.check_call(['umount', os.path.join(tempdir+"/dmg/")])
            if os.path.exists(tempdir):
                shutil.rmtree(tempdir)
        except OSError:
            cleanupLogger.error("Some temporary Directories could not be removed")
            cleanupLogger.exception("Some temporary Directories could not be removed")

    except KeyboardInterrupt:
        cleanupLogger.error("You've hit Strg+C for interrupting Parabird. Now clean up your own mess. Exiting...")
        sys.exit()
