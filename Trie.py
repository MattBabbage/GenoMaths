#!/usr/bin/env python
#
# Copyright Stephen Doyle 2008 stephendoyle75@gmail.com
#
#http://softwareramblings.com/wp-content/uploads/2008/11/visitor.py
#######################################################################    
# Simple representation of a node used to build a trie
class Node:
    nextName = 0

    def __init__(self):
        self.name = Node.nextName
        Node.nextName += 1
        self.children = {}
        self.isOutputNode = False

    def insert(self, edge):
        if edge in self.children.keys():
            return self.children[edge]
        else:
            newNode = Node()
            self.children[edge] = newNode
            return newNode

    def walk(self, visitor):
        visitor.visitNode(self)
        for nextNode in self.children.values():
            nextNode.walk(visitor)

    def walkandreturn(self, visitor):
        visitor.visitNode(self)
        for nextNode in self.children.values():
            nextNode.walk(visitor)
#######################################################################

# A Trie
class Trie:
    def __init__(self):
        self.root = Node()

    def addPattern(self, pattern):
        node = self.root
        for char in pattern:
            node = node.insert(char)
        node.isOutputNode = True

    def walk(self, visitor):
        self.root.walk(visitor)

    def getDigraph(self):
        strDigraph = 'digraph trie { \n\trankdir="TB"; \n\tnode [shape = "circle"];'
        return

#######################################################################
# Visitor interface
class Visitor:
    def visitNode(self, node):
        pass


#######################################################################
# Visitor subclass that generates Graphviz dot file contents.
class GraphvizVisitor:
    def __init__(self, dotGen):
        self.dotGen = dotGen

    def visitNode(self, node):
        if node.isOutputNode:
            dotGen.setNodeProperty(node.name, 'shape', 'doublecircle')
        for edge, nextNode in node.children.items():
            dotGen.addLink(node.name, nextNode.name, edge)


#######################################################################
# Generates a rudimentary Graphviz dot file 
class DotFileGenerator:

    def __init__(self, name):
        self.name = name
        self.outf = open(name + '.dot', 'w')
        self.strDigraph = 'digraph trie { \n\trankdir="TB"; \n\tnode [shape = "circle"];'

    def setNodeProperty(self, nodeName, property, value):
        self.strDigraph = self.strDigraph + '\n\t%s [%s = %s];' % (nodeName, property, value)

    def addLink(self, lhs, rhs, label):
        self.strDigraph = self.strDigraph + '\n\t%s -> %s [label = %s];' % (lhs, rhs, label)

    def close(self):
        self.strDigraph = self.strDigraph + '\n}';
        self.outf.write(self.strDigraph)
        self.outf.close()

#######################################################################

if __name__ == "__main__":
    # Build a trie
    trie = Trie()
    trie.addPattern("abc")
    trie.addPattern("abcdef")
    trie.addPattern("abcxyz")
    trie.addPattern("abdef")

    # Generate the dot file contents by walking the trie
    dotGen = DotFileGenerator('trie')
    visitor = GraphvizVisitor(dotGen)

    trie.walk(visitor)

    dotGen.close()

    print(dotGen.strDigraph)


