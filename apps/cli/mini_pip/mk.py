# Writes data/: the version, specifier, marker and requirement cases, the
# environments, the package index and the requirements files that mini_pip
# and oracle.py read.
import json, os
os.makedirs("data/reqs", exist_ok=True)

def w(name, text):
    open("data/" + name, "w").write(text)

w("versions.txt", """\
1.0
1.0.0
v1.0
 1.0\x20
V2
1!2.0
0001!1
01.02.003
1.0a-1
1.0a1
1.0alpha1
1.0b2
1.0Beta2
1.0c1
1.0rc1
1.0preview2
1.0rc
1.0.dev
1.0.DEV2
1.0a1.dev3
1.0-1
1.0-r1
1.0.post.
1.0a.
1.0post
1.0.r
1.0_rev3
1.0a1-1
1.0+ABC.def-1
1.0+local_1.2
1.0+5
1.0+abc
1.0+abc.5
2.0.post0.dev1
0.0
0
1.0.0.0.0
2024.8.30
1.0.
1.0+
1.0+abc..1
1.0--1
1.0-
1..0
.1
1.0 a1
1.0.a.b
abc
1.0'x
٣
""")

w("specifiers.txt", """\
>=1.0 | 0.9 1.0 1.0.post1 2.0a1 2.0 1.0+local foo
>=1.0, <2 | 1.0 1.5 2.0a1 2.0.dev0 1.9.post1 2.0
<2.0 | 1.9 2.0a1 2.0rc1 2.0.dev1 1.9.9+local
<2.0rc1 | 2.0b1 2.0rc1 1.9
>1.0 | 1.0 1.0.post1 1.0+local 1.0.1 1.1a1
>1.0.post1 | 1.0.post1 1.0.post2 1.0.post2.dev0 1.1
>1.0.dev1 | 1.0.dev1 1.0.dev2 1.0a1 1.0
>1.0rc1 | 1.0rc1 1.0rc1.post1 1.0rc2 1.0
<=1.0 | 1.0 1.0+local 1.0.post1 0.9 1.0.dev0
==1.0 | 1.0 1.0.0 1.0+abc 1.0.post1 1.0a1
==1.0+abc | 1.0+abc 1.0 1.0+abd
==1.* | 0.9 1.0 1.5a1 1.99 2.0 1.0.dev0
!=1.* | 0.9 1.5 2.0 2.0rc1
~=1.4.5 | 1.4.4 1.4.5 1.4.9 1.5 1.4.10a1
~=2.2 | 2.1 2.2 2.9 3.0 3.0a1
~=2.2.post3 | 2.2 2.2.post3 2.3 3.0
!=1.5, >=1.0 | 1.0 1.5 1.5.0 1.5+local 1.6
>=2.0a1 | 1.9 2.0a1 2.0b2 2.0 3.0.dev1
>=1,<1 | 1 0.9 1.0
==1.0, ==2.0 | 1.0 2.0
<0.dev0 | 0 0.dev0
>1.0, <1.0.post0 | 1.0.post0 1.0+local 1.0.0.post0
>2.0b1, <2.0b2 | 2.0b1 2.0b1.post1 2.0b2.dev0 2.0b2
 | 1.0 2.0a1 junk
===1.0+foo | 1.0+foo 1.0+FOO 1.0 foo
===foobar | foobar FooBar 1.0
>=1.0, ===1.0.0 | 1.0 1.0.0
===1.0, ===2.0 | 1.0
>=1.0,<2.0a.0 | 1.9 2.0a0 2.0.dev0
>= 1.0 ,  != 1.2.* | 1.1 1.2.3 1.3
<3, >=2, !=2.5, <2.5.0, >=2 | 2.0 2.4 2.5
=>1.0 | 1.0
~=1 | 1.0
>=1.0.* | 1.0
==1.0.post1.* | 1.0
<1.0+local | 1.0
""")

w("markers.txt", """\
python_version >= "3.10"
python_version<'3.9' or sys_platform=="win32"
(os_name == "nt" and platform_machine == "AMD64") or implementation_name == "pypy"
'linux' in sys_platform
"arm" not in platform_machine
platform_release >= "6"
python_full_version ~= "3.12.0"
implementation_version >= "7.3"
extra == "Socks_Proxy"
platform_system == "Linux" and python_version > "3.11" or platform_system == "Darwin"
platform_system == "Linux" and (python_version > "3.11" or platform_system == "Darwin")
sys.platform == "darwin"
os.name == 'posix'
python_implementation == "PyPy"
platform_version ~= "1.0"
extras == "socks"
python_version === "3.12"
python_version in "3.11 3.12"
"3.9" < python_version
python_version > "3.12.0rc1"
platform_machine >= "x86"
"a" == "b"
python_version >=
python_version = "3.8"
os_name == "nt" and
(python_version > "3.8"
platform_machine == x86_64
python_version >= "3.8" foo
not_a_var == "x"
os_name not "nt"
""")

w("requirement-tests.txt", """\
requests
requests[security,socks] >= 2.8.1, == 2.8.*
Django>=4.2,<5.0 ; python_version >= "3.8"
name @ https://example.com/pkgs/name-1.0-py3-none-any.whl
name @ file:///tmp/x.tar.gz ; os_name == "nt"
pip (>=24.0)
Foo.Bar_baz-qux==1.0+local.7
numpy~=1.26.0
pkg[ b , a ]
pkg===1.0-custom
pkg!=1.0.*,!=1.1.*
typing_extensions>=4.6.1; python_version < "3.13"
urllib3[brotli]>=1.21.1; extra == "Use_Chardet"
>=1.0
pkg[a b]
pkg[a,]
pkg >= 1.0 extra
pkg (>=1.0
pkg>=1.0.*
pkg==1.0rc1.*
pkg<=1.0+local
pkg @ 
pkg @ https://x.whl; python_version>"3"
pkg ;\x20
pkg ==1.0 ; python_version >= "3.8" and
pkg~=1
pkg[extra]extra2
""")

w("envs.txt", """\
[linux-py312]
implementation_name = cpython
implementation_version = 3.12.7
os_name = posix
platform_machine = x86_64
platform_release = 6.8.0-45-generic
platform_system = Linux
platform_version = #45-Ubuntu SMP PREEMPT_DYNAMIC
python_full_version = 3.12.7
platform_python_implementation = CPython
python_version = 3.12
sys_platform = linux

[win-py39]
implementation_name = cpython
implementation_version = 3.9.13
os_name = nt
platform_machine = AMD64
platform_release = 10
platform_system = Windows
platform_version = 10.0.19045
python_full_version = 3.9.13
platform_python_implementation = CPython
python_version = 3.9
sys_platform = win32

[mac-pypy310]
implementation_name = pypy
implementation_version = 7.3.17
os_name = posix
platform_machine = arm64
platform_release = 23.6.0
platform_system = Darwin
platform_version = Darwin Kernel Version 23.6.0
python_full_version = 3.10.14
platform_python_implementation = PyPy
python_version = 3.10
sys_platform = darwin
""")

def rel(v, deps=(), py=None, yanked=False):
    r = {"version": v, "requires_dist": list(deps)}
    if py is not None:
        r["requires_python"] = py
    if yanked:
        r["yanked"] = True
    return r

index = {
    "certifi": [rel("2024.8.30", py=">=3.6"), rel("2025.1.31", py=">=3.6"), rel("2025.6.15", py=">=3.7")],
    "charset-normalizer": [rel("3.3.2", py=">=3.7.0"), rel("3.4.0", py=">=3.7.0"), rel("3.4.2", py=">=3.7")],
    "idna": [rel("3.7", py=">=3.5"), rel("3.8", py=">=3.6"), rel("3.10", py=">=3.6"), rel("4.0rc1", py=">=3.8")],
    "urllib3": [
        rel("1.26.20", ["brotli==1.0.9; (os_name != \"nt\" or python_version >= \"3\") and platform_python_implementation == \"CPython\" and extra == \"brotli\"",
                        "PySocks!=1.5.7,<2.0,>=1.5.6; extra == \"socks\""],
            py=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*"),
        rel("2.0.0", py=">=3.7", yanked=True),
        rel("2.2.3", ["brotli>=1.0.9; platform_python_implementation == \"CPython\" and extra == \"brotli\"",
                      "brotlicffi>=0.8.0; platform_python_implementation != \"CPython\" and extra == \"brotli\"",
                      "pysocks!=1.5.7,<2.0,>=1.5.6; extra == \"socks\""], py=">=3.8"),
        rel("2.3.0", ["brotli>=1.0.9; platform_python_implementation == \"CPython\" and extra == \"brotli\"",
                      "brotlicffi>=0.8.0; platform_python_implementation != \"CPython\" and extra == \"brotli\"",
                      "pysocks!=1.5.7,<2.0,>=1.5.6; extra == \"socks\""], py=">=3.9"),
        rel("2.5.0", ["brotli>=1.0.9; platform_python_implementation == \"CPython\" and extra == \"brotli\"",
                      "brotlicffi>=1.0.9; platform_python_implementation != \"CPython\" and extra == \"brotli\"",
                      "pysocks!=1.5.7,<2.0,>=1.5.6; extra == \"socks\""], py=">=3.9"),
    ],
    "requests": [
        rel("2.31.0", ["charset-normalizer<4,>=2", "idna<4,>=2.5", "urllib3<3,>=1.21.1", "certifi>=2017.4.17",
                       "PySocks!=1.5.7,>=1.5.6; extra == \"socks\"", "chardet<6,>=3.0.2; extra == \"use_chardet_on_py3\""], py=">=3.7"),
        rel("2.32.3", ["charset-normalizer<4,>=2", "idna<4,>=2.5", "urllib3<3,>=1.21.1", "certifi>=2017.4.17",
                       "PySocks!=1.5.7,>=1.5.6; extra == \"socks\"", "chardet<6,>=3.0.2; extra == \"use-chardet-on-py3\""], py=">=3.8"),
        rel("2.32.4", ["charset_normalizer<4,>=2", "idna<4,>=2.5", "urllib3<3,>=1.21.1", "certifi>=2017.4.17",
                       "PySocks!=1.5.7,>=1.5.6; extra == \"socks\"", "chardet<6,>=3.0.2; extra == \"use-chardet-on-py3\""], py=">=3.8"),
    ],
    "pysocks": [rel("1.5.6"), rel("1.5.7"), rel("1.7.1", py=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*")],
    "brotli": [rel("1.0.9"), rel("1.1.0")],
    "brotlicffi": [rel("1.1.0.0", ["cffi>=1.0.0"], py=">=3.7")],
    "cffi": [rel("1.17.1", ["pycparser"], py=">=3.8")],
    "pycparser": [rel("2.22", py=">=3.8")],
    "flask": [
        rel("2.3.3", ["Werkzeug>=2.3.7", "Jinja2>=3.1.2", "itsdangerous>=2.1.2", "click>=8.1.3", "blinker>=1.6.2",
                      "importlib-metadata>=3.6.0; python_version < \"3.10\"",
                      "asgiref>=3.2; extra == \"async\"", "python-dotenv; extra == \"dotenv\""], py=">=3.8"),
        rel("3.0.3", ["Werkzeug>=3.0.0", "Jinja2>=3.1.2", "itsdangerous>=2.1.2", "click>=8.1.3", "blinker>=1.6.2",
                      "importlib-metadata>=3.6.0; python_version < \"3.10\"",
                      "asgiref>=3.2; extra == \"async\"", "python-dotenv; extra == \"dotenv\""], py=">=3.8"),
        rel("3.1.1", ["blinker>=1.9.0", "click>=8.1.3", "importlib-metadata>=3.6.0; python_version < \"3.10\"",
                      "itsdangerous>=2.2.0", "jinja2>=3.1.2", "markupsafe>=2.1.1", "werkzeug>=3.1.0",
                      "asgiref>=3.2; extra == \"async\"", "python-dotenv; extra == \"dotenv\""], py=">=3.9"),
    ],
    "werkzeug": [rel("2.3.8", ["MarkupSafe>=2.1.1"], py=">=3.8"), rel("3.0.6", ["MarkupSafe>=2.1.1"], py=">=3.8"),
                 rel("3.1.3", ["MarkupSafe>=2.1.1", "watchdog>=2.3; extra == \"watchdog\""], py=">=3.9")],
    "jinja2": [rel("3.1.4", ["MarkupSafe>=2.0", "Babel>=2.7; extra == \"i18n\""], py=">=3.7"),
               rel("3.1.6", ["MarkupSafe>=2.0", "Babel>=2.7; extra == \"i18n\""], py=">=3.7")],
    "markupsafe": [rel("2.1.5", py=">=3.7"), rel("3.0.2", py=">=3.9")],
    "itsdangerous": [rel("2.1.2", py=">=3.7"), rel("2.2.0", py=">=3.8")],
    "click": [rel("8.1.7", ["colorama; platform_system == \"Windows\"", "importlib-metadata; python_version < \"3.8\""], py=">=3.7"),
              rel("8.1.8", ["colorama; platform_system == \"Windows\"", "importlib-metadata; python_version < \"3.8\""], py=">=3.7"),
              rel("8.2.0", ["colorama; platform_system == \"Windows\""], py=">=3.10")],
    "colorama": [rel("0.4.6", py=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*")],
    "blinker": [rel("1.8.2", py=">=3.8"), rel("1.9.0", py=">=3.9")],
    "importlib-metadata": [rel("8.5.0", ["zipp>=3.20", "typing-extensions>=3.6.4; python_version < \"3.8\""], py=">=3.8")],
    "zipp": [rel("3.20.2", py=">=3.8"), rel("3.21.0", py=">=3.9")],
    "asgiref": [rel("3.8.1", ["typing_extensions>=4; python_version < \"3.11\""], py=">=3.8")],
    "typing-extensions": [rel("4.12.2", py=">=3.8"), rel("4.13.0rc1", py=">=3.8"), rel("4.13.2", py=">=3.8")],
    "python-dotenv": [rel("1.0.1", py=">=3.8"), rel("1.1.0", py=">=3.9")],
    "waitress": [rel("3.0.1", py=">=3.8"), rel("3.0.2", py=">=3.9")],
    "gunicorn": [rel("22.0.0", ["packaging"], py=">=3.7"), rel("23.0.0", ["packaging"], py=">=3.7")],
    "packaging": [rel("24.2", py=">=3.8"), rel("25.0", py=">=3.8")],
    "django": [
        rel("4.2.16", ["asgiref<4,>=3.6.0", "backports.zoneinfo; python_version < \"3.9\"", "sqlparse>=0.3.1",
                       "tzdata; sys_platform == \"win32\""], py=">=3.8"),
        rel("5.1.4", ["asgiref<4,>=3.8.1", "sqlparse>=0.3.1", "tzdata; sys_platform == \"win32\""], py=">=3.10"),
        rel("5.2rc1", ["asgiref>=3.8.1", "sqlparse>=0.3.1", "tzdata; sys_platform == \"win32\""], py=">=3.10"),
        rel("5.2.1", ["asgiref>=3.8.1", "sqlparse>=0.3.1", "tzdata; sys_platform == \"win32\""], py=">=3.10"),
    ],
    "sqlparse": [rel("0.5.1", py=">=3.8"), rel("0.5.3", py=">=3.8")],
    "tzdata": [rel("2024.2", py=">=2"), rel("2025.2", py=">=2")],
    "backports-zoneinfo": [rel("0.2.1", py=">=3.6")],
    "numpy": [rel("1.24.4", py=">=3.8"), rel("1.26.4", py=">=3.9"), rel("2.0.2", py=">=3.9"),
              rel("2.2.6", py=">=3.10"), rel("2.3.0", py=">=3.11")],
    "pandas": [
        rel("2.0.3", ["python-dateutil>=2.8.2", "pytz>=2020.1", "tzdata>=2022.1",
                      "numpy>=1.20.3; python_version < \"3.10\"", "numpy>=1.21.0; python_version >= \"3.10\"",
                      "numpy>=1.23.2; python_version >= \"3.11\""], py=">=3.8"),
        rel("2.2.3", ["numpy>=1.22.4; python_version < \"3.11\"", "numpy>=1.23.2; python_version == \"3.11\"",
                      "numpy>=1.26.0; python_version >= \"3.12\"", "python-dateutil>=2.8.2", "pytz>=2020.1",
                      "tzdata>=2022.7"], py=">=3.9"),
    ],
    "python-dateutil": [rel("2.8.2", ["six>=1.5"], py="!=3.0.*,!=3.1.*,!=3.2.*,>=2.7"),
                        rel("2.9.0.post0", ["six>=1.5"], py="!=3.0.*,!=3.1.*,!=3.2.*,>=2.7")],
    "six": [rel("1.16.0"), rel("1.17.0", py="!=3.0.*,!=3.1.*,!=3.2.*,>=2.7")],
    "pytz": [rel("2024.2"), rel("2025.2")],
    "pydantic": [
        rel("2.9.2", ["annotated-types>=0.6.0", "pydantic-core==2.23.4", "typing-extensions>=4.6.1; python_version < \"3.13\"",
                      "typing-extensions>=4.12.2; python_version >= \"3.13\""], py=">=3.8"),
        rel("2.10.6", ["annotated-types>=0.6.0", "pydantic-core==2.27.2", "typing-extensions>=4.12.2"], py=">=3.8"),
        rel("2.11.0b1", ["annotated-types>=0.6.0", "pydantic-core==2.30.0", "typing-extensions>=4.12.2"], py=">=3.9"),
    ],
    "pydantic-core": [rel("2.23.4", ["typing-extensions!=4.7.0,>=4.6.0"], py=">=3.8"),
                      rel("2.27.2", ["typing-extensions!=4.7.0,>=4.6.0"], py=">=3.8"),
                      rel("2.30.0", ["typing-extensions>=4.6.0,!=4.7.0"], py=">=3.9")],
    "annotated-types": [rel("0.7.0", ["typing-extensions>=4.0.0; python_version < \"3.9\""], py=">=3.8")],
    "boto3": [rel("1.35.90", ["botocore<1.36.0,>=1.35.90", "jmespath<2.0.0,>=0.7.1", "s3transfer<0.11.0,>=0.10.0"], py=">=3.8"),
              rel("1.35.99", ["botocore<1.36.0,>=1.35.99", "jmespath<2.0.0,>=0.7.1", "s3transfer<0.11.0,>=0.10.0"], py=">=3.8"),
              rel("1.36.0", ["botocore<1.37.0,>=1.36.0", "jmespath<2.0.0,>=0.7.1", "s3transfer<0.12.0,>=0.11.0"], py=">=3.8"),
              rel("1.36.2", ["botocore<1.37.0,>=1.36.2", "jmespath<2.0.0,>=0.7.1", "s3transfer<0.12.0,>=0.11.0"], py=">=3.8")],
    "botocore": [rel("1.35.90", ["jmespath<2.0.0,>=0.7.1", "python-dateutil<3.0.0,>=2.1", "urllib3<1.27,>=1.25.4; python_version < \"3.10\"",
                                 "urllib3!=2.2.0,<3,>=1.25.4; python_version >= \"3.10\""], py=">=3.8"),
                 rel("1.35.99", ["jmespath<2.0.0,>=0.7.1", "python-dateutil<3.0.0,>=2.1", "urllib3<1.27,>=1.25.4; python_version < \"3.10\"",
                                 "urllib3!=2.2.0,<3,>=1.25.4; python_version >= \"3.10\""], py=">=3.8"),
                 rel("1.36.0", ["jmespath<2.0.0,>=0.7.1", "python-dateutil<3.0.0,>=2.1", "urllib3<1.27,>=1.25.4; python_version < \"3.10\"",
                                "urllib3!=2.2.0,<3,>=1.25.4; python_version >= \"3.10\""], py=">=3.8"),
                 rel("1.36.2", ["jmespath<2.0.0,>=0.7.1", "python-dateutil<3.0.0,>=2.1", "urllib3<1.27,>=1.25.4; python_version < \"3.10\"",
                                "urllib3!=2.2.0,<3,>=1.25.4; python_version >= \"3.10\""], py=">=3.8")],
    "s3transfer": [rel("0.10.4", ["botocore<2.0a.0,>=1.33.2"], py=">=3.8"), rel("0.11.0", ["botocore<2.0a.0,>=1.36.0"], py=">=3.8")],
    "jmespath": [rel("1.0.1", py=">=3.7")],
}
open("data/index.json", "w").write(json.dumps({"meta": {"api-version": "1.1"}, "projects": index}, indent=2) + "\n")

w("reqs/web.txt", """\
# The web service.
Flask[async,dotenv]>=2.3  # the app
requests[socks] ~= 2.32
gunicorn>=22 ; sys_platform != "win32"
waitress ; sys_platform == "win32"   # Windows has no gunicorn
-c constraints.txt
""")
w("reqs/constraints.txt", """\
urllib3<2.3
werkzeug != 3.1.3
""")
w("reqs/data.txt", """\
-r base.txt
pandas
numpy<2 ; python_version < "3.10"
pytz==2024.2 \\
    ; python_version >= "3.9"
""")
w("reqs/base.txt", """\
six
typing_extensions>=4.12
""")
w("reqs/aws.txt", """\
boto3
botocore<1.36
""")
w("reqs/api.txt", """\
pydantic>=2.10
django>=4.2,<5.2
idna>=3.9
""")
w("reqs/pre.txt", """\
django>=5.2rc1
pydantic>=2.11.0b1
""")
w("reqs/conflict.txt", """\
pydantic==2.9.2
pydantic-core>=2.27
""")
w("reqs/yanked.txt", """\
urllib3==2.0.0
idna>=4.0.dev0
""")
w("reqs/yanked2.txt", """\
urllib3>=2.0,<2.1
""")
w("reqs/missing.txt", """\
requests
left-pad>=1.0
""")
w("reqs/bad.txt", """\
requests
flask >= 2.0 async
""")
w("jobs.txt", """\
web.txt linux-py312
web.txt win-py39
web.txt mac-pypy310
data.txt linux-py312
data.txt win-py39
aws.txt linux-py312
api.txt linux-py312
api.txt win-py39
pre.txt linux-py312
conflict.txt linux-py312
yanked.txt linux-py312
yanked2.txt linux-py312
missing.txt linux-py312
bad.txt linux-py312
""")
