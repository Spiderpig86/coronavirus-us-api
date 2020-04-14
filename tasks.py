"""Tooling for coronavirus-us-api.
"""

import invoke

INPUT_DESCRIPTION = 'List of directories to act on. [default = "."]'


@invoke.task(help={"targets": INPUT_DESCRIPTION})
def black(ctx, targets="."):
    """Formats code with black.
    
    Arguments:
        ctx {context} -- program context execution.
    
    Keyword Arguments:
        targets {str} -- space separated list of directories (default: {'.'})
    """
    print(f"Formatting code under directories: [{targets}]")
    args = ["black", targets]
    ctx.run(" ".join(args))


@invoke.task(help={"targets": INPUT_DESCRIPTION})
def sort(ctx, targets="."):
    """Sort imports of files listed under given directories.
    
    Arguments:
        ctx {context} -- program context execution.
    
    Keyword Arguments:
        targets {str} -- space separated list of directories (default: {'.'})
    """
    print(f"Sorting imports under directories: [{targets}]")
    args = ["black", targets]
    ctx.run(" ".join(args))

@invoke.task
def check(ctx, format=False, sort=False, diff=False):
    """Master function for code cleaning.
    
    Arguments:
        ctx {context} -- program context execution.
    
    Keyword Arguments:
        format {bool} -- whether to format (default: {False})
        sort {bool} -- whether to sort (default: {False})
        diff {bool} -- display diff for commands (default: {False})
    """
    if not any([format, sort]):
        format = True
        sort = True

    fmt_args = ["black", "--check", "."]
    sort_args = ["isort", "-rc", "--check", "."]

    if diff:
        fmt_args.append("--diff")
        sort_args.append("--diff")

    cmd_args = []
    if format:
        cmd_args.extend(fmt_args)
    if sort:
        if cmd_args:
            cmd_args.append("&")
        cmd_args.extend(sort_args)
    ctx.run(" ".join(cmd_args))