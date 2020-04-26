import io
import os
import sys
import glob
import tokenize
import importlib.abc
import importlib.machinery

MAGIC = "WILDCARD_EXPANSION_GOES_HERE"

def translate_tokens(readline):
    in_import = False
    buffered_token = None

    for token in tokenize.tokenize(readline):
        token_type, token_string, *_ = token
        if token_type == tokenize.NL:
            in_import = False
        elif token_type == tokenize.NAME:
            if token_string == 'import':
                in_import = True
        elif token_type == tokenize.OP:
            if token_string == '*' and in_import and buffered_token:
                token_type, token_string = buffered_token
                token_string += MAGIC
                buffered_token = None

        if buffered_token is not None:
            yield buffered_token

        buffered_token = (token_type, token_string)

    if buffered_token is not None:
        yield buffered_token


class WildcardSourceLoader(importlib.abc.SourceLoader):
    def __init__(self, fullname, path):
        self.fullname = fullname
        self.path = path

    def get_filename(self, fullname):
        return self.path

    def get_data(self, path):
        with io.open_code(str(path)) as fd:
            return tokenize.untokenize(translate_tokens(fd.readline))


class WildcardPathFinder(importlib.machinery.PathFinder):
    @classmethod
    def find_spec(cls, modulename, path=None, target=None):
        if modulename.find(MAGIC) != -1:
            pattern = modulename.replace(MAGIC, '*')
            for entry in (path or sys.path):
                matches = glob.glob(os.path.join(entry, pattern))
                if matches:
                    filename = os.path.basename(matches[0])
                    modulename = os.path.splitext(filename)[0]
                    break

        return super().find_spec(modulename, path, target)


def install():
    path_hook = importlib.machinery.FileFinder.path_hook((
        WildcardSourceLoader,
        importlib.machinery.SOURCE_SUFFIXES
    ))
    sys.path_hooks.insert(0, path_hook)
    sys.meta_path.insert(0, WildcardPathFinder)
    sys.path_importer_cache.clear()
