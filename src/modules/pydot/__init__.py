import re

class DotWriter(object):

    def __init__(self, out, indention = '\t'):
        self.out = out
        self.indention = indention
        self.vertexIdReplacePattern = re.compile('[^a-zA-Z0-9_]')

    def writeGraphBegin(self, name):
        self.out.write('digraph %s {\n' % (name,))

    def vertexId(self, vertex):
        return 'v' + self.vertexIdReplacePattern.sub('_', unicode(vertex))

    def writeVertex(self, vertex, color = None):
        self.out.write(self.indention)
        self.out.write(self.vertexId(vertex))

        self.out.write(' [label="')
        self.out.write(vertex)
        self.out.write('"')

        if(not color is None):
            self.out.write(' color=')
            self.out.write(color)

        self.out.write(']\n')

    def writeEdge(self, fromVertex, toVertex, label = None, color = None):
        self.out.write(self.indention)
        self.out.write(self.vertexId(fromVertex))
        self.out.write(' -> ')
        self.out.write(self.vertexId(toVertex))

        self.out.write(' [')

        if(not label is None):
            self.out.write(' label=%s' % (label,))

        if(not color is None):
            self.out.write(' color=%s' % (color,))

        self.out.write(']\n')

    def writeGraphEnd(self):
        self.out.write('}\n')
