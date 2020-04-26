# Wild hook

A python import hook that rewrites source files to add one extra feature:

    import module*

That's all.

It only imports the first match. Might break zip imports. Likely also disables
`.pyc` caching. Doesn't work with `__main__` so use `python -m`.

## Installation

    $ cp wild_hook.py usercustomize.py $(python -m site --user-site)

## Demo

    $ cat example.py
    import test*
    $ cat testfoo.py
    print('foo')
    $ python -m example
    foo

Exciting, right?

## Why

A certain someone read the docs of openscad and thought that includes behaved
like this, allowing wildcards but only taking the first match. A couple of
hours later we realized it doesn't, but I already had 80% of this shitpost
written up.

## What name do I use to access that module in the code?

Does it look like I thought this through?
