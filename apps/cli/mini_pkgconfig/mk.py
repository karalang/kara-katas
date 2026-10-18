# Writes data/ (the .pc files: the system's in pc/, a project's own in
# opt/acme/lib/pkgconfig/, a build tree's in build/, and broken ones in
# broken/) and jobs.tsv: one pkg-config command line per line, its
# arguments tab-separated. Leading NAME=value arguments are environment
# variables for that command.
import os
from system_pc import SYSTEM

FILES = {}
for name, text in SYSTEM.items():
    FILES["pc/" + name + ".pc"] = text

FILES["pc/acme-core.pc"] = """\
# Acme's core library, installed under /opt/acme.
prefix=/opt/acme
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
includedir=${prefix}/include
plugindir=${libdir}/acme/plugins
greeting="hello from acme"

Name: Acme Core
Description: Acme application core
URL: https://acme.example/core
Version: 2.4.1
Requires: zlib >= 1.2.11
Requires.private: libssl >= 3.0, libcrypto
Libs: -L${libdir} -lacme-core
Libs.private: -lm -ldl
Cflags: -I${includedir}/acme-2 -DACME_API=2 -DACME_GREETING=\\"${greeting}\\"
"""

FILES["pc/acme-net.pc"] = """\
prefix=/opt/acme
libdir=${prefix}/lib
includedir=${prefix}/include

Name: Acme Net
Description: Acme networking layer
Version: 2.4.1
Requires: acme-core = 2.4.1, glib-2.0 >= 2.70
Requires.private: gio-2.0
Libs: -L${libdir} -lacme-net -Wl,--as-needed
Libs.private: -lresolv -pthread
Cflags: -I${includedir}/acme-2 -pthread
"""

FILES["pc/acme-gui.pc"] = """\
prefix=/opt/acme
libdir=${prefix}/lib
includedir=${prefix}/include

Name: Acme GUI
Description: Acme widgets over pixman and fontconfig
Version: 2.5.0~beta1
Requires: acme-net, pixman-1 >= 0.40
Requires.private: fontconfig, libpng16
Conflicts: acme-legacy < 2
Libs: -L${libdir} -lacme-gui
Cflags: -I${includedir}/acme-2/gui -isystem ${includedir}/acme-2/compat
"""

FILES["pc/acme-legacy.pc"] = """\
prefix=/opt/acme-legacy

Name: Acme Legacy
Description: The old Acme API
Version: 1.9.3
Libs: -L${prefix}/lib -lacme
Cflags: -I${prefix}/include
"""

FILES["pc/acme-compat.pc"] = """\
prefix=/opt/acme

Name: Acme Compat
Description: Bridges the old API, but not to a version below 2
Version: 2.4.1
Requires: acme-legacy, acme-core
Conflicts: acme-legacy < 2
Libs: -L${prefix}/lib -lacme-compat
"""

FILES["pc/acme-cli.pc"] = """\
prefix=/opt/acme

Name: acme-cli
Description: Acme's command-line tool, as a dependency for plugins
Version: 2.4.1
Requires: acme-core > 2, acme-core < 3
Requires.internal: acme-net
"""

FILES["pc/acme-old.pc"] = """\
prefix=/opt/acme

Name: Acme Old Client
Description: Wants a GLib that does not exist yet
Version: 0.9
Requires: glib-2.0 >= 3.0
Libs: -lacme-old
"""

FILES["pc/jpeg-turbo.pc"] = """\
prefix=/usr
libdir=${prefix}/lib/x86_64-linux-gnu
includedir=${prefix}/include

Name: libjpeg-turbo
Description: A SIMD-accelerated JPEG codec that provides the libjpeg API
Version: 2.1.5
Provides: libjpeg = 8.2.2
Libs: -L${libdir} -ljpeg
Cflags: -I${includedir}
"""

FILES["pc/acme-image.pc"] = """\
prefix=/opt/acme

Name: Acme Image
Description: Image loading for Acme
Version: 2.4.1
Requires: libjpeg >= 8, libpng16
Libs: -L${prefix}/lib -lacme-image
Cflags: -I${prefix}/include/acme-2
"""

FILES["pc/acme-tools.pc"] = """\
prefix=/opt/acme

Name: Acme Tools
Description: Missing a dependency
Version: 2.4.1
Requires: acme-core, libfrobnicate >= 1.0
Libs: -lacme-tools
"""

FILES["pc/quirks.pc"] = """\
# A file written by hand, with the shapes pkgconf has to cope with.
prefix = /opt/quirks
libdir=${prefix}/lib
long_flags=-DONE=1 \\
    -DTWO=2
quoted='single quoted value'
literal=$prefix and ${undefined} and ${prefix}

Name: Quirks
Description: Odd but legal syntax
Version: 1.0.0-rc.2
libs: -L${libdir} -lquirks -lquirks -L${libdir}
CFLAGS: ${long_flags} "-DPATH=\\"/opt/quirks dir\\"" -I${prefix}/include -I/usr/include
"""

FILES["pc/frameworks.pc"] = """\
Name: Frameworks
Description: macOS-style framework flags
Version: 3
Libs: -framework CoreFoundation -lobjc -framework Security -framework CoreFoundation -Wl,-rpath,/opt/fw/lib
Cflags: -F/opt/fw -fobjc-arc -std=c11
"""

FILES["opt/acme/lib/pkgconfig/acme-plugins.pc"] = """\
prefix=/opt/acme
libdir=${prefix}/lib
plugindir=${libdir}/acme/plugins
here=${pcfiledir}

Name: Acme Plugins
Description: The plugin SDK, relocatable with its prefix
Version: 2.4.1
Requires: acme-core
Libs: -L${libdir} -lacme-plugins
Cflags: -I${prefix}/include/acme-2/plugins -DPLUGIN_DIR=\\"${plugindir}\\"
"""

FILES["build/acme-core-uninstalled.pc"] = """\
prefix=/home/dev/acme/build
libdir=${prefix}/src
includedir=/home/dev/acme/include

Name: Acme Core
Description: Acme application core, from the build tree
Version: 2.5.0-dev
Requires: zlib >= 1.2.11
Libs: -L${libdir} -lacme-core
Cflags: -I${includedir} -I${prefix}/generated
"""

FILES["build/acme-core.pc"] = """\
prefix=/srv/acme-staging

Name: Acme Core
Description: A staged install that the uninstalled file shadows
Version: 2.4.9
Libs: -L${prefix}/lib -lacme-core
"""

FILES["broken/noversion.pc"] = """\
Name: No Version
Description: Forgot its Version field
Libs: -lnoversion
"""

FILES["broken/spaced.pc"] = """\
prefix=/opt/spaced\x20\x20
 Name: Spaced
Description: Whitespace in odd places
Libs.private: -lm\t
Version: 1.2 beta
Libs: -L${prefix}/lib -lspaced
"""

FILES["broken/cycle-a.pc"] = """\
Name: cycle-a
Description: Half of a dependency cycle
Version: 1
Requires: cycle-b
Libs: -lcycle-a
"""

FILES["broken/cycle-b.pc"] = """\
Name: cycle-b
Description: The other half
Version: 1
Requires: cycle-a
Libs: -lcycle-b
"""

FILES["broken/badquote.pc"] = """\
Name: Bad Quote
Description: An unterminated quote in Cflags
Version: 1
Cflags: -DNAME="unterminated -I/opt/bq
Libs: -lbq
"""

jobs = []
def j(*args):
    jobs.append("\t".join(args))

# Versions and existence
j("--modversion", "zlib")
j("--modversion", "glib-2.0", "gio-2.0", "acme-core")
j("--exists", "acme-net")
j("--exists", "glib-2.0", ">=", "2.70")
j("--exists", "glib-2.0 > 2.80.0")
j("--exists", "--print-errors", "glib-2.0", ">", "2.80.0")
j("--exists", "--print-errors", "no-such-lib")
j("--exists", "--short-errors", "--print-errors", "no-such-lib")
j("--atleast-version=2.4", "acme-core")
j("--atleast-version=3", "acme-core")
j("--exact-version=2.4.1", "acme-core")
j("--max-version=2.4.0", "acme-core")
j("--atleast-version=1", "no-such-lib")
j("--modversion", "acme-gui")
j("--exists", "acme-gui > 2.5.0")
j("--exists", "acme-gui >= 2.5.0~alpha")
j("--exists", "libpng16 >= 1.6.43", "sqlite3 < 3.45.1.1", "openssl != 1.1.1")
j("--exists", "--print-errors", "acme-old")
j("--modversion", "--print-errors", "acme-tools")
j("--atleast-pkgconfig-version=1.6")
j("--version")
# Flags
j("--cflags", "zlib")
j("--libs", "zlib")
j("--cflags", "--libs", "acme-core")
j("--libs", "glib-2.0")
j("--libs", "--static", "glib-2.0")
j("--libs", "gio-2.0")
j("--libs", "--static", "gio-2.0")
j("--cflags", "gio-2.0")
j("--cflags", "--static", "expat")
j("--cflags", "acme-net")
j("--libs", "acme-net")
j("--libs", "--static", "acme-net")
j("--libs", "--static", "--pure", "acme-net")
j("--cflags", "--libs", "acme-gui")
j("--libs", "--static", "acme-gui")
j("--libs", "acme-gui", "acme-net", "acme-core")
j("--libs", "acme-core", "zlib", "acme-core")
j("--cflags", "--keep-system-cflags", "zlib", "libpng16")
j("--libs", "--keep-system-libs", "libpng16")
j("PKG_CONFIG_ALLOW_SYSTEM_LIBS=1", "--libs", "libxml-2.0")
j("--libs", "--static", "libxml-2.0")
j("--libs", "--static", "freetype2")
j("--cflags", "freetype2")
j("--libs-only-l", "--static", "acme-net")
j("--libs-only-L", "acme-gui")
j("--libs-only-other", "--static", "acme-net")
j("--cflags-only-I", "acme-gui")
j("--cflags-only-other", "acme-net", "acme-core")
j("--libs", "--cflags", "quirks")
j("--libs", "frameworks")
j("--cflags", "frameworks")
j("--libs", "openssl")
j("--libs", "--static", "openssl")
j("--libs", "--maximum-traverse-depth=1", "acme-net")
j("--cflags", "--fragment-filter=I", "acme-gui")
j("--libs", "acme-cli")
j("--cflags", "acme-cli")
j("--cflags", "--internal-cflags", "acme-cli")
j("--libs", "acme-image")
j("--cflags", "--libs", "fontconfig")
j("--env=ACME", "acme-core")
j("--env=ACME", "--cflags", "--libs", "acme-core")
# Variables and listings
j("--variable=prefix", "acme-core")
j("--variable=libdir", "acme-core", "zlib", "glib-2.0")
j("--variable=greeting", "acme-core")
j("--variable=plugindir", "acme-core")
j("--variable=pcfiledir", "zlib")
j("--variable=nothere", "zlib")
j("--define-variable=prefix=/srv/acme", "--variable=plugindir", "acme-core")
j("--define-variable=prefix=/srv/acme", "--cflags", "--libs", "acme-core")
j("--variable=literal", "quirks")
j("--variable=long_flags", "quirks")
j("--variable=quoted", "quirks")
j("--print-variables", "acme-core")
j("--print-variables", "zlib")
j("--variable=pc_path", "pkg-config")
j("--modversion", "pkg-config")
j("--print-requires", "acme-gui")
j("--print-requires-private", "acme-gui")
j("--print-requires", "acme-cli")
j("--print-requires-private", "gio-2.0")
j("--print-provides", "jpeg-turbo")
j("--print-provides", "acme-core")
j("--path", "acme-core", "zlib")
j("--digraph", "acme-net")
j("--list-all")
j("PKG_CONFIG_PATH=broken", "--list-package-names")
# Search paths, the build tree and relocation
j("--with-path=opt/acme/lib/pkgconfig", "--modversion", "acme-plugins")
j("PKG_CONFIG_PATH=opt/acme/lib/pkgconfig", "--cflags", "--libs", "acme-plugins")
j("PKG_CONFIG_PATH=opt/acme/lib/pkgconfig", "--define-prefix", "--cflags", "--libs", "acme-plugins")
j("PKG_CONFIG_PATH=opt/acme/lib/pkgconfig", "--define-prefix", "--variable=plugindir", "acme-plugins")
j("PKG_CONFIG_PATH=opt/acme/lib/pkgconfig", "--variable=here", "acme-plugins")
j("PKG_CONFIG_PATH=opt/acme/lib/pkgconfig", "--path", "acme-plugins")
j("PKG_CONFIG_PATH=build", "--modversion", "acme-core")
j("PKG_CONFIG_PATH=build", "--cflags", "--libs", "acme-core")
j("PKG_CONFIG_PATH=build", "--uninstalled", "acme-core")
j("PKG_CONFIG_PATH=build", "--uninstalled", "zlib")
j("PKG_CONFIG_PATH=build", "--no-uninstalled", "--modversion", "acme-core")
j("PKG_CONFIG_PATH=build:opt/acme/lib/pkgconfig", "--libs", "acme-plugins")
j("PKG_CONFIG_LIBDIR=", "--modversion", "zlib")
j("pc/zlib.pc", "--libs")
# Errors and broken files
j("--cflags", "acme-tools")
j("--libs", "acme-old")
j("--libs", "--errors-to-stdout", "acme-old")
j("--cflags", "--short-errors", "acme-tools")
j("--libs", "--silence-errors", "acme-tools")
j("--exists", "--print-errors", "acme-gui", "acme-legacy")
j("--libs", "acme-legacy", "acme-gui")
j("--libs", "--ignore-conflicts", "acme-legacy", "acme-gui")
j("--exists", "--print-errors", "acme-compat")
j("--libs", "--ignore-conflicts", "acme-compat")
j("PKG_CONFIG_PATH=broken", "--modversion", "noversion")
j("PKG_CONFIG_PATH=broken", "--validate", "spaced")
j("PKG_CONFIG_PATH=broken", "--modversion", "--libs", "spaced")
j("PKG_CONFIG_PATH=broken", "--libs", "cycle-a")
j("PKG_CONFIG_PATH=broken", "--print-requires", "cycle-b")
j("PKG_CONFIG_PATH=broken", "--cflags", "--libs", "badquote")
j("PKG_CONFIG_PATH=broken", "--validate", "badquote")
j("--libs")
j("--cflags", "--libs", "")
j("--frobnicate", "zlib")
j("--modv", "zlib")
j("--variable")

def write_all():
    for name, text in FILES.items():
        path = os.path.join("data", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").write(text)
    open("jobs.tsv", "w").write("\n".join(jobs) + "\n")

if __name__ == "__main__":
    write_all()
