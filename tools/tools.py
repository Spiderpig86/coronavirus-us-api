"""Tooling for coronavirus-us-api.
"""

import invoke

INPUT_DESCRIPTION = 'List of directories to act on. [default = "."]'

@invoke.task(help={ 'targets': INPUT_DESCRIPTION })
def black(ctx, targets='.'):
    """Formats code with black.
    
    Arguments:
        ctx {context} -- program context execution.
    
    Keyword Arguments:
        targets {str} -- space separated list of directories (default: {'.'})
    """
    

@invoke.task(help={ 'targets': INPUT_DESCRIPTION })
def sort_imports(ctx, targets='.'):
    """Sort imports of files listed under given directories.
    
    Arguments:
        ctx {context} -- program context execution.
    
    Keyword Arguments:
        targets {str} -- space separated list of directories (default: {'.'})
    """
    print(f'Sorting imports under directories: [{targets}]')
    args = ['black', targets]
    ctx.run(' '.join(args))