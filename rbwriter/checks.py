# system modules
import os
import shutil
import sys
import time

# internal modules
from .defines.configs import SECRET_KEY_SIZE
from .defines import paths
# available colors are BOLD, ERROR, SUCCESS, RESET, WARNING
from .defines.colors import BOLD, ERROR, SUCCESS, RESET


def checkup():
    """
    Global checkup for all files and directories.
    This also creates and/or copies missing files!
    If this doesn't succeed, the server will NOT start!
    """
    # TODO: make a proper checkup, not like this one here...
    # -> checklist = [] (append true/false everytime and check with if all())
    start_time = time.time()
    console = BOLD + "[CHECKUP] " + RESET
    print()
    print(console + "--- START ---", file=sys.stderr)

    if not os.path.isfile(paths.SECRET_KEY):
        print(console + f"Secret key doesn't exist, generating...", end="", file=sys.stderr)
        with open(paths.SECRET_KEY, "wb") as f:
            f.write(os.urandom(SECRET_KEY_SIZE))
        if not os.path.isfile(paths.SECRET_KEY):
            print(ERROR + "failed!" + RESET, sys.stderr)
            print(console + ERROR + f"Unable to write secret key to {paths.SECRET_KEY}!" + RESET, sys.stderr)
            print(console + ERROR + "Application is unusable without a secret key, check your read/write policies!",
                  file=sys.stderr)
            sys.exit(1)
    else:
        print(console + SUCCESS + "Secret key found at {paths.SECRET_KEY}!" + RESET, file=sys.stderr)

    if not os.path.isdir(paths.COOKIE_PATH):
        print(console + f"Cookie directory {paths.COOKIE_PATH} doesn't exist, creating...", end="", file=sys.stderr)
        os.mkdir(paths.COOKIE_PATH)
        print(SUCCESS + "done!" + RESET, file=sys.stderr)
    else:
        print(console + SUCCESS + "Cookie directory found!" + RESET, file=sys.stderr)

    if not os.path.isdir(paths.DB_PATH):
        print(console + f"DB directory {paths.DB_PATH} doesn't exist, creating...", end="", file=sys.stderr)
        os.mkdir(paths.DB_PATH)
        print(SUCCESS + "done!" + RESET, file=sys.stderr)
    else:
        print(console + SUCCESS + "DB directory found!" + RESET, file=sys.stderr)

    if not os.path.isdir(paths.TEMPLATE_PREFIX):
        print(console + f"Template directory {paths.TEMPLATE_PREFIX.absolute()} doesn't exist, creating...", end="",
              file=sys.stderr)
        paths.TEMPLATE_PREFIX.mkdir(parents=True, exist_ok=True)
        print(SUCCESS + "done!" + RESET, file=sys.stderr)
    else:
        print(console + SUCCESS + "Template directory found!" + RESET, file=sys.stderr)

    if not os.path.isdir(paths.USER_PATH):
        print(console + f"User directory {paths.USER_PATH} doesn't exist, creating...", end="", file=sys.stderr)
        os.mkdir(paths.USER_PATH)
        print(SUCCESS + "done!" + RESET, file=sys.stderr)
    else:
        print(console + SUCCESS + "User directory found!" + RESET, file=sys.stderr)

    if not os.path.exists(paths.PDF_TEMPLATE_PATH):
        print(console + "PDF template not found! Copying..." + RESET, end="", file=sys.stderr)
        shutil.copy2(paths.PDF_TEMPLATE_ORIGIN_PATH, paths.PDF_TEMPLATE_PATH)
        print(SUCCESS + "done!" + RESET, file=sys.stderr)

    else:
        print(console + SUCCESS + "PDF template found!" + RESET, file=sys.stderr)

    if not os.path.exists(paths.TODOLIST_TEMPLATE_PATH):
        print(console + "Todolist template not found! Copying..." + RESET, end="", file=sys.stderr)
        shutil.copy2(paths.TODOLIST_TEMPLATE_ORIGIN_PATH, paths.TODOLIST_TEMPLATE_PATH)
        print(SUCCESS + "done!" + RESET, file=sys.stderr)
    else:
        print(console + SUCCESS + "Todolist template found!" + RESET, file=sys.stderr)

    # Calculate time difference (just because we can)
    diff = time.time() - start_time

    print(console + "--- END ---\n", file=sys.stderr)
    print(console + BOLD + SUCCESS + f"Checkup finished successfully in {diff:.4f} seconds!\n" + RESET,
          file=sys.stderr)
