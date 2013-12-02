#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unipath import Path


class NormalizedList(list):

    def normalize_element(self, element):
        return element

    def append(self, value):
        return super(NormalizedList,
                     self).append(self.normalize_element(value))


class Paths(NormalizedList):

    def __init__(self, root="."):
        self.root = Path(root).expand()
        super(NormalizedList, self).__init__()


    def normalize_element(self, path_val):
        path = Path(path_val)
        # /foo
        if path.isabsolute():
            return path.expand()
        # foo
        else:
            return Path(self.root, path_val)


class Extensions(NormalizedList):

    def normalize_element(self, extension):
        if "." in extension:
            return extension
        else:
            return ".%s" % extension

class ExtensionsDict(Extensions):

    def __setitem__(self, key, value):
        return super(ExtensionsDict,
                     self).__setitem__(Extensions())


class Index(object):

    def __init__(self, root=".", paths=None, extensions=None, alias=None):
        self.root = root
        self.paths = paths
        self.extensions = extensions
        self.alias = alias

        self.entries = {}
        super(Index, self).__init__()

    def find(self, *logical_paths):
        base_path = self.root
        for path_val in logical_paths:
            path = Path(path_val.lstrip("/"))
            #self.find_in_base_path(path_val, base_path)
            return self.find_in_paths(path_val)

    def find_in_paths(self, path_val):
        logical_path = Path(path_val)
        dirname, basename = logical_path.parent, logical_path.name
        for base_path in self.paths:
            result = self.match(Path(base_path, dirname), basename)
            if not result:
                continue
            print result
            return result

    def find_in_base_path(self, path_val, base_path):
        logical_path = Path(base_path, path_val)
        dirname, basename = logical_path.parent, logical_path.name
        for base_path in self.paths:
            if self.paths_contains(dirname):
                return self.match(dirname, basename)

    def match(self, dirname, basename):
        matches = self.get_entries(dirname)
        for match in matches:
            if basename == match.name:
                return match

    def paths_contains(self, dirname):
        return any(path.startswith(dirname) for path in self.paths)

    def get_entries(self, dirname):
        return Path(dirname).listdir()


class Pack(object):

    def __init__(self, root="."):
        self.root = Path(root).expand()
        self.paths = Paths(root)
        self.extensions = Extensions()
        self.alias = ExtensionsDict()
        super(Pack, self).__init__()

    def append_path(self, path):
        self.paths.append(path)

    def append_extension(self, extension):
        self.extensions.append(extension)

    def find(self, *args, **kwargs):
        return self.index.find(*args, **kwargs)

    @property
    def index(self):
        return Index(self.root, self.paths,
                     self.extensions,
                     self.alias)


