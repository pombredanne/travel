#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_travel
----------------------------------

Tests for `travel` module.
"""

from travel import travel

class UppercaseList(travel.NormalizedList):

    def normalize_element(self, element):
        return element.upper()


class TestNormalizedList:

    def test_brackets_with_start_and_length(self):
        array = UppercaseList()
        array.append("a")
        array.append("b")
        array.append("c")
        assert array[0] == "A"

class TestPaths:

    def test_absolute_path_stay_the_same(self):
        paths = travel.Paths("/foo")
        paths.append("/tmp")
        assert paths == ["/tmp"]

    def test_relative_path_gets_expanded(self):
        paths = travel.Paths("/foo")
        paths.append("bar")
        paths.append("tmp")
        assert paths == ["/foo/bar", "/foo/tmp"]

    def test_relative_path_expand_vars(self):
        paths = travel.Paths("~/foo")
        paths.append("bar")
        assert "home" in paths[0].split("/")


class TestExtensions:

    def test_extension_with_dot_stay_the_same(self):
        extensions = travel.Extensions()
        extensions.append(".js")
        assert extensions == [".js"]


    def test_extension_without_dot_get_added_automatic(self):
        extensions = travel.Extensions()
        extensions.append("css")
        assert extensions == [".css"]

# Todo: Add fixture
"""
class TestPack:

    def test_find_in_absolute_path(self):
        pack = travel.Pack("/home/krazy/framework/travel")
        pack.append_extension("py")
        pack.append_path("travel")
        pack.append_path("tests")

        result = pack.find("test_travel.py")
        assert result == "/home/krazy/framework/travel/tests/test_travel.py"

"""
