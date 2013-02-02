import unittest
import pydot

class OutMock(object):

    def __init__(self):
        self.written = ''

    def write(self, s):
        self.written += s

class WhenDotWriterExists(unittest.TestCase):

    def setUp(self):
        self.out = OutMock()
        self.writer = pydot.DotWriter(self.out)

    def assertWrittenRegexpMatches(self, regexp):
        self.assertRegexpMatches(self.out.written, regexp)

    def testThenAddVertexColorWritesColorLabel(self):
        self.writer.writeVertex('v', color = 'red')

        self.assertWrittenRegexpMatches('color=[\'"]?red[\'"]?')

    def testThenAddVertexDefaultColorIsNone(self):
        self.writer.writeVertex('v')

        self.assertTrue(not 'color' in self.out.written)

    def testThenAddVertexAddsVertexNameAsLabel(self):
        self.writer.writeVertex('Hello World!')

        self.assertWrittenRegexpMatches('label=[\'"]Hello World![\'"]')
