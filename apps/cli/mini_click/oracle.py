# The oracle for mini_click: four command-line tools written with click
# 8.5.0 (BSD), run over data/runs.txt through click's own CliRunner. Each
# run prints its exit code and everything the tool wrote, stdout and
# stderr interleaved as a terminal shows them. Run from the app
# directory after mk.py: python3 -s -P oracle.py > expected.out
import configparser
import datetime
import os
import uuid

import click
from click.testing import CliRunner


def r(v):
    # The callbacks print their values in this one notation, so the
    # port does not need Python's repr of every type.
    if isinstance(v, bool) or v is None:
        return str(v)
    if isinstance(v, str):
        return repr(v)
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, tuple):
        inner = ", ".join(r(x) for x in v)
        return f"({inner},)" if len(v) == 1 else f"({inner})"
    if isinstance(v, list):
        return "[" + ", ".join(r(x) for x in v) + "]"
    if isinstance(v, datetime.datetime):
        return "datetime(" + v.isoformat(" ") + ")"
    if isinstance(v, uuid.UUID):
        return f"UUID({v})"
    raise TypeError(type(v))


def show(label, **kw):
    click.echo(label + ": " + ", ".join(f"{k}={r(v)}" for k, v in kw.items()))


def load_config(ctx, param, value):
    if value is None:
        return None
    cp = configparser.ConfigParser()
    if not cp.read(value):
        raise click.BadParameter(f"cannot read {value!r}", ctx=ctx, param=param)
    dm = {}
    for section in cp.sections():
        keys = dict(cp[section])
        if "tag" in keys:
            keys["tag"] = keys["tag"].split()
        parts = section.split(".")[1:]
        node = dm
        for p in parts:
            node = node.setdefault(p, {})
        node.update(keys)
    ctx.default_map = dm
    return value


@click.group(context_settings={"help_option_names": ["-h", "--help"], "auto_envvar_prefix": "DEPLOYCTL"})
@click.option("--config", type=click.Path(dir_okay=False), callback=load_config, is_eager=True, expose_value=False, help="Read option defaults from an INI file.")
@click.option("-v", "--verbose", count=True, help="Say more; repeat for even more.")
@click.option("--env", type=click.Choice(["dev", "staging", "prod"], case_sensitive=False), default="dev", show_default=True, show_envvar=True, help="Target environment.")
@click.version_option("2.7.0", prog_name="deployctl")
@click.pass_context
def deployctl(ctx, verbose, env):
    """Deploy services and manage their configuration.

    Every command talks to the deploy API of the chosen environment.
    """
    ctx.obj = {"verbose": verbose, "env": env}
    show("deployctl", verbose=verbose, env=env, invoked=ctx.invoked_subcommand)


@deployctl.command()
@click.argument("service")
@click.argument("version")
@click.option("-r", "--replicas", type=click.IntRange(1, 20), default=2, show_default=True, help="Pods to run.")
@click.option("--timeout", type=click.FloatRange(0, 600, min_open=True), default=30.0, help="Seconds to wait for health checks.")
@click.option("-t", "--tag", multiple=True, help="Image tag to add; can be repeated.")
@click.option("--strategy", type=click.Choice(["rolling", "blue-green", "canary"], case_sensitive=False), default="rolling", show_default=True)
@click.option("--at", type=click.DateTime(), help="Schedule the release.")
@click.option("--id", "release_id", type=click.UUID, help="Release id to reuse.")
@click.option("--notes", type=click.File("r"), help="Release notes file.")
@click.option("--manifest", type=click.Path(exists=True, dir_okay=False), help="Service manifest.")
@click.option("--dry-run/--no-dry-run", default=False, help="Plan without applying.")
@click.pass_context
def release(ctx, service, version, replicas, timeout, tag, strategy, at, release_id, notes, manifest, dry_run):
    """Release VERSION of SERVICE.

    The release waits for every pod to pass its health check before it
    moves on, and stops at the first failure.
    """
    show("release", service=service, version=version, replicas=replicas, timeout=timeout, tag=tag, strategy=strategy, at=at, id=release_id, dry_run=dry_run, env=ctx.obj["env"])
    if notes is not None:
        lines = notes.read().splitlines()
        click.echo(f"notes: {len(lines)} lines, first {lines[0]!r}")
    if manifest is not None:
        with open(manifest) as f:
            click.echo(f"manifest: {len(f.read().splitlines())} lines")
    src = ctx.get_parameter_source("replicas").name
    click.echo(f"replicas from {src}, tag from {ctx.get_parameter_source('tag').name}")


@deployctl.command()
@click.argument("services", nargs=-1, required=True)
@click.option("-n", "--lines", type=click.IntRange(min=0), default=100, help="Lines to show.")
@click.option("-f", "--follow", is_flag=True, help="Keep streaming.")
@click.option("--level", type=click.Choice(["debug", "info", "warn", "error"]), multiple=True)
@click.option("--since", type=click.DateTime(["%Y-%m-%d"]))
@click.option("--grep", multiple=True, metavar="PATTERN", help="Only lines matching PATTERN.")
def logs(services, lines, follow, level, since, grep):
    """Show recent log lines of SERVICES."""
    show("logs", services=services, lines=lines, follow=follow, level=level, since=since, grep=grep)


@deployctl.command()
@click.argument("service")
@click.option("--to", "target", metavar="VERSION", help="Version to go back to (default: the previous one).")
@click.confirmation_option(prompt="Roll back the service?")
@click.pass_obj
def rollback(obj, service, target):
    """Roll SERVICE back to an earlier release."""
    show("rollback", service=service, target=target, env=obj["env"])


@deployctl.command()
@click.argument("service")
@click.option("--set", "settings", type=(str, int), multiple=True, metavar="KEY N", help="Set a resource limit.")
@click.option("--window", nargs=2, type=int, help="Autoscale window in minutes.")
@click.option("--min", "min_", type=click.IntRange(0, clamp=True), default=1, show_default=True)
@click.option("--max", "max_", type=click.IntRange(1, 100, clamp=True), default=10, show_default=True)
@click.option("--ratio", type=click.FloatRange(0, 1, min_open=True, max_open=True), default=0.8, show_default=True)
def scale(service, settings, window, min_, max_, ratio):
    """Change how SERVICE scales."""
    show("scale", service=service, settings=settings, window=window, min=min_, max=max_, ratio=ratio)


@deployctl.group(invoke_without_command=True)
@click.option("--json", "as_json", is_flag=True, help="Print JSON.")
@click.pass_context
def config(ctx, as_json):
    """Read and change remote configuration."""
    if ctx.invoked_subcommand is None:
        click.echo("config: listing all keys")
    show("config", as_json=as_json, invoked=ctx.invoked_subcommand)


@config.command("get")
@click.argument("key")
def config_get(key):
    """Print the value of KEY."""
    show("config get", key=key)


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """Set KEY to VALUE."""
    show("config set", key=key, value=value)


@config.command("unset")
@click.argument("keys", nargs=-1)
def config_unset(keys):
    """Remove KEYS."""
    show("config unset", keys=keys)


@config.command("list", hidden=True)
def config_list():
    show("config list")


@deployctl.group()
def user():
    """Manage deploy users."""


@user.command()
@click.argument("name")
@click.option("--role", type=click.Choice(["viewer", "deployer", "admin"]), default="viewer", show_default=True)
@click.password_option()
def create(name, role, password):
    """Create user NAME."""
    show("user create", name=name, role=role, password_len=len(password))


@user.command()
@click.option("--email", prompt="Email address", help="Who to invite.")
@click.option("--days", prompt=True, type=click.IntRange(1, 30), default=7, help="Days the invite stays valid.")
def invite(email, days):
    """Send an invitation."""
    show("user invite", email=email, days=days)


@deployctl.command()
@click.argument("dirs", nargs=-1, required=True, type=click.Path(exists=True, file_okay=False))
@click.option("--dest", type=click.Path(file_okay=False), default="data/out", show_default=True)
def sync(dirs, dest):
    """Copy service DIRS to the deploy host."""
    show("sync", dirs=dirs, dest=dest)
    for d in dirs:
        with open(os.path.join(d, "VERSION")) as f:
            click.echo(f"{d}: version {f.read().strip()}")


@deployctl.command("debug-dump", hidden=True)
@click.pass_obj
def debug_dump(obj):
    show("debug-dump", verbose=obj["verbose"])


@deployctl.command(deprecated="Use 'release' instead.")
@click.argument("service")
def promote(service):
    """Promote SERVICE from staging to prod."""
    show("promote", service=service)


@deployctl.command()
@click.option("--format", "fmt", type=click.Choice(["table", "json"]), default="table", help="Output format.")
@click.option("--wide", is_flag=True, hidden=True)
@click.option("--legacy-color", is_flag=True, deprecated=True, help="Old colour scheme.")
@click.pass_context
def status(ctx, fmt, wide, legacy_color):
    """Show what runs where."""
    show("status", fmt=fmt, wide=wide, legacy_color=legacy_color, env=ctx.obj["env"], env_source=ctx.parent.get_parameter_source("env").name)


# ------------------------------------------------------------ pipeline

@click.group(chain=True, invoke_without_command=True)
@click.option("-j", "--jobs", type=int, default=1, help="Parallel jobs.")
@click.pass_context
def pipeline(ctx, jobs):
    """Run build steps in order."""
    show("pipeline", jobs=jobs, invoked=ctx.invoked_subcommand)


@pipeline.result_callback()
def pipeline_done(results, jobs):
    click.echo(f"pipeline done: {r(results)} with {jobs} job(s)")


@pipeline.command()
@click.option("--target", default="x86", show_default=True)
def build(target):
    """Compile the project."""
    show("build", target=target)
    return f"build:{target}"


@pipeline.command()
@click.option("--shard", type=click.IntRange(1, 8), default=1)
def test(shard):
    """Run the test suite."""
    show("test", shard=shard)
    return f"test:{shard}"


@pipeline.command()
@click.option("--channel", type=click.Choice(["stable", "beta"]), default="stable")
def publish(channel):
    """Upload the artifacts."""
    show("publish", channel=channel)
    return f"publish:{channel}"


# --------------------------------------------------------------- greet

@click.command(context_settings={"token_normalize_func": lambda s: s.lower(), "show_default": True, "auto_envvar_prefix": "GREET"})
@click.argument("names", nargs=-1)
@click.option("--greeting", default="Hello", help="Word to greet with.")
@click.option("--shout/--no-shout", default=False, help="Shout it.")
@click.option("--upper", "case", flag_value="upper", help="Upper-case the names.")
@click.option("--lower", "case", flag_value="lower", help="Lower-case the names.")
@click.option("--plain", "case", flag_value="plain", default=True, help="Leave the names alone.")
@click.option("--times", type=click.IntRange(0, 10), default=1, show_envvar=True, help="Repeat count.")
@click.option("--pos", type=(float, float), default=(0.0, 0.0), help="Where to stand.")
@click.option("--lang", type=click.Choice(["en", "fr", "de"]), default="en", show_envvar=True, envvar="GREET_LANG")
@click.option("--sep", default=", ", help="Between names.")
@click.version_option("0.3", "-V", "--version", message="%(prog)s %(version)s")
def greet(names, greeting, shout, case, times, pos, lang, sep):
    """Greet NAMES."""
    show("greet", names=names, greeting=greeting, shout=shout, case=case, times=times, pos=pos, lang=lang, sep=sep)
    words = {"en": greeting, "fr": "Bonjour", "de": "Hallo"}
    for _ in range(times):
        shown = [n.upper() if case == "upper" else n.lower() if case == "lower" else n for n in names]
        line = f"{words[lang]} {sep.join(shown) or 'nobody'}"
        click.echo(line.upper() + "!" if shout else line)


# ---------------------------------------------------------------- wrap

@click.command(context_settings={"max_content_width": 60})
@click.option("--size", type=click.Choice(["S", "M", "L", "XL"]), required=True, help="The size of the shirt to print the long design on, chosen from the four sizes the printer can handle without rotating the design.")
@click.option("--old-name", hidden=True)
@click.option("--colour", "--color", "-c", default="black", show_default="black, or the brand colour", help="Ink.")
@click.option("--really-long-option-name-for-testing", is_flag=True, help="An option whose name is wider than the column.")
@click.option("--count", "-n", count=True, help="Copies.")
@click.argument("design", required=False, default="logo", help="The design file; defaults to the logo.")
def wrap(size, old_name, colour, really_long_option_name_for_testing, count, design):
    """Print a design on a shirt.

    This paragraph is long enough that the help formatter has to wrap it
    over several lines when the content width is limited to sixty columns.

    \b
    Sizes:
      S   small
      XL  extra large

    Only the first paragraph of this text is used for the short help.
    """
    show("wrap", size=size, old_name=old_name, colour=colour, count=count, design=design)


TOOLS = {"deployctl": deployctl, "pipeline": pipeline, "greet": greet, "wrap": wrap}


def main():
    os.environ["COLUMNS"] = "80"
    runner = CliRunner()
    with open("data/runs.txt") as f:
        lines = f.read().splitlines()
    for n, line in enumerate(lines, 1):
        tool, env, inp, *args = line.split("\t")
        envmap = {}
        if env != "-":
            for kv in env.split(";"):
                k, v = kv.split("=", 1)
                envmap[k] = v
        text = None if inp == "-" else ("" if inp == "" else "\n".join(inp.split("|")) + "\n")
        shown = " ".join(args)
        print(f"== run {n}: {tool} {shown}".rstrip())
        res = runner.invoke(TOOLS[tool], args, prog_name=tool, env=envmap, input=text)
        if res.exception is not None and not isinstance(res.exception, SystemExit):
            raise res.exception
        print(f"exit: {res.exit_code}")
        out = res.output
        print(out, end="" if out.endswith("\n") or not out else "\n<no newline>\n")


main()
