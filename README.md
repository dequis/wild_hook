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

## References

These pages were useful while writing this:

* https://docs.python.org/3/library/importlib.html#setting-up-an-importer
    * A bare but useful example on how to set up an importer that just uses the
      same class as the default one.
* https://stackoverflow.com/questions/43571737/how-to-implement-an-import-hook-that-can-modify-the-source-code-on-the-fly-using
    * Has a concrete example of subclassing those classes, although not in the
      most convenient way.
* https://stackoverflow.com/questions/214881/can-you-add-new-statements-to-pythons-syntax
    * Several neat ideas, like rewriting the token stream with the tokenizer
      module (used in this project), or using sys.settrace (not used)
* https://github.com/ajalt/fuckitpy
    * Didn't use any ideas from here, but worth looking at for AST manipulation
      inspiration
