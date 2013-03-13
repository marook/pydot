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

    def writeAttribute(self, key, value):
        self.out.write(' ')
        self.out.write(key)
        self.out.write('="')
        # TODO escape value
        self.out.write(value)
        self.out.write('"')

    def writeAttributes(self, **kwargs):
        for key, value in kwargs.iteritems():
            if(value is None):
                continue

            self.writeAttribute(key, value)

    def writeVertex(self, vertex, **kwargs):
        self.out.write(self.indention)
        self.out.write(self.vertexId(vertex))

        self.out.write(' [label="')
        self.out.write(vertex)
        self.out.write('"')

        self.writeAttributes(**kwargs)

        self.out.write(']\n')

    def writeEdge(self, fromVertex, toVertex, **kwargs):
        self.out.write(self.indention)
        self.out.write(self.vertexId(fromVertex))
        self.out.write(' -> ')
        self.out.write(self.vertexId(toVertex))

        self.out.write(' [')

        self.writeAttributes(**kwargs)

        self.out.write(']\n')

    def writeGraphEnd(self):
        self.out.write('}\n')
