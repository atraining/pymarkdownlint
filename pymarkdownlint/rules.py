from abc import abstractmethod, ABCMeta
from pymarkdownlint.options import IntOption

import re


class Rule(object):
    """ Class representing markdown rules. """
    options_spec = []
    id = []
    name = ""
    __metaclass__ = ABCMeta

    def __init__(self, opts={}):
        self.options = {}
        for op_spec in self.options_spec:
            self.options[op_spec.name] = op_spec
            actual_option = opts.get(op_spec.name)
            if actual_option:
                self.options[op_spec.name].set(actual_option)

    @abstractmethod
    def validate(self):
        pass


class FileRule(Rule):
    """ Class representing rules that act on an entire file """
    pass


class LineRule(Rule):
    """ Class representing rules that act on a line by line basis """
    pass


class RuleViolation(object):
    def __init__(self, rule_id, message, line_nr=None):
        self.rule_id = rule_id
        self.line_nr = line_nr
        self.message = message

    def __eq__(self, other):
        return self.rule_id == other.rule_id and self.message == other.message and self.line_nr == other.line_nr

    def __str__(self):
        return "{0}: {1} {2}".format(self.line_nr, self.rule_id, self.message)

    def __repr__(self):
        return self.__str__()


class MaxLineLengthRule(LineRule):
    name = "Max line length"
    id = "R1"
    options_spec = [IntOption('line-length', 80, "Max line length")]

    def validate(self, line):
        max_length = self.options['line-length'].value
        if len(line) > max_length:
            return RuleViolation(self.id, "Line exceeds max length ({0}>{1})".format(len(line), max_length))


class TrailingWhiteSpace(LineRule):
    name = "Trailing whitespace"
    id = "R2"

    def validate(self, line):
        pattern = re.compile(r"\s$")
        if pattern.search(line):
            return RuleViolation(self.id, "Line has trailing whitespace")
