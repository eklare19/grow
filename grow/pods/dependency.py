"""Dependency graph for content references."""

import os

class Error(Exception):
    pass


class BadFieldsError(Error, ValueError):
    pass


class DependencyGraph(object):
    def __init__(self):
        self.reset()

    def add_all(self, data):
        """Add all from a data source."""

        for key, value in data.iteritems():
            self.add_references(key, value)

    def add_references(self, source, references):
        """Add references made in a source file to the graph."""
        if not references:
            return

        self._dependencies[source] = set(references)

        # Bi-directional dependency references for easier lookup.
        for reference in references:
            if reference not in self._dependents:
                self._dependents[reference] = set()
            self._dependents[reference].add(source)

    def export(self):
        result = {}

        for key, value in self._dependencies.iteritems():
            result[key] = list(value)

        return result

    def get_dependents(self, reference):
        """
        Gets dependents that rely upon the reference or a collection that
        contains the reference.
        """
        return (self._dependents.get(reference, set())
            | self._dependents.get(os.path.dirname(reference), set())
            | set([reference]))

    def get_dependencies(self, source):
        return self._dependencies.get(source, set())

    def reset(self):
        self._dependents = {}
        self._dependencies = {}


class DependencyLog(object):
    """Log of all dependencies that occure as the template is rendered."""
    def __init__(self):
        self.log = set()

    def add(self, item):
        self.log.add(item)

    def read_all(self):
        return self.log
