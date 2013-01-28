#!/usr/bin/env python

from distutils.core import setup, Command
import sys
import os
from os.path import (
        basename,
        dirname,
        abspath,
        splitext,
        join as pjoin
)
from glob import glob
from unittest import TestLoader, TextTestRunner
import re
import datetime
from subprocess import call
import itertools

projectdir = dirname(abspath(__file__))
reportdir = pjoin(projectdir, 'reports')

srcdir = pjoin(projectdir, 'src')
moddir = pjoin(srcdir, 'modules')
testdir = pjoin(srcdir, 'test')

assert os.path.isdir(srcdir)
assert os.path.isdir(moddir)
#assert os.path.isdir(testdir)

class Report(object):

    def __init__(self):
        self.reportDateTime = datetime.datetime.utcnow()
        self.reportDir = os.path.join(reportdir, self.reportDateTime.strftime('%Y-%m-%d_%H_%M_%S'))
        
        # fails when dir already exists which is nice
        os.makedirs(self.reportDir)

    @property
    def coverageReportFileName(self):
        return os.path.join(self.reportDir, 'coverage.txt')

    @property
    def unitTestReportFileName(self):
        return os.path.join(self.reportDir, 'tests.txt')

def sourceFiles():
    sourceFilePattern = re.compile('^.*[.]py$')
    for root, dirs, files in os.walk(moddir):
        for f in files:
            if(not sourceFilePattern.match(f)):
                continue

            if(f.startswith('.#')):
                continue

            yield os.path.join(root, f)

def fullSplit(p):
    head, tail = os.path.split(p)
 
    if(len(head) > 0):
        for n in fullSplit(head):
            yield n
 
    yield tail
 
def findTestModules(rootPath):
    testFilePattern = re.compile('^(.*Test)[.]py$', re.IGNORECASE)
 
    for root, dirs, files in os.walk(rootPath):
        for f in files:
            m = testFilePattern.match(f)
 
            if(not m):
                continue
 
            relDir = os.path.relpath(root, rootPath)

            yield m.group(1)
    

def testModules():
    return findTestModules(testdir)
 
def printFile(fileName):
    if(not os.path.exists(fileName)):
        # TODO maybe we should not silently return?
        return

    with open(fileName, 'r') as f:
        for line in f:
            sys.stdout.write(line)

class TestFailException(Exception):
    '''Indicates that at least one of the unit tests has failed
    '''

    pass

def setUpPyDotPyPath():
    # insert project lookup paths at index 0 to make sure they are used
    # over global libraries
    sys.path.insert(0, moddir)
    sys.path.insert(0, testdir)

class test(Command):
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        self._cwd = os.getcwd()
        self._verbosity = 2

    def finalize_options(self): pass

    def run(self):
        report = Report()

        tests = [m for m in testModules()]

        print "..using:"
        print "  moddir:", moddir
        print "  testdir:", testdir
        print "  tests:", tests
        print "  sys.path:", sys.path
        print

        setUpPyDotPyPath()

        # TODO try to import all test cases here. the TestLoader is throwing
        # very confusing errors when imports can't be resolved.

        # configure logging
        if 'DEBUG' in os.environ:
            import logging
            logging.basicConfig(level = logging.DEBUG)

        try:
            with open(report.unitTestReportFileName, 'w') as testResultsFile:
                r = TextTestRunner(stream = testResultsFile, verbosity = self._verbosity)

                def runTests():
                    result = r.run(TestLoader().loadTestsFromNames(tests))

                    if(not result.wasSuccessful()):
                        raise TestFailException()

                try:
                    import coverage

                    c = coverage.coverage()
                    c.start()
                    runTests()
                    c.stop()
    
                    with open(report.coverageReportFileName, 'w') as reportFile:
                        c.report([f for f in sourceFiles()], file = reportFile)

                except ImportError:
                    # TODO ImportErrors from runTests() may look like coverage is missing

                    print ''
                    print 'coverage module not found.'
                    print 'To view source coverage stats install http://nedbatchelder.com/code/coverage/'
                    print ''

                    runTests()
        finally:
            # TODO use two streams instead of printing files after writing
            printFile(report.unitTestReportFileName)
            printFile(report.coverageReportFileName)

class PyLint(Command):
    description = 'show pylint results'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(sefl):
        import pylint.lint

        setUpPyDotPyPath()

        pylint.lint.Run(['--rcfile=etc/pylint.conf', '-iy', 'pydot', ])

setup(
    cmdclass = {
        'test': test,
        'pylint': PyLint,
    },

    name = 'pydot',
    description = 'pydot is a writer for the dog graph file format',
    version = '0.1',
    author = 'Markus Pielmeier',
    author_email = 'markus.pielmeier@gmail.com',
    license = 'GPLv3',

    requires = [],

    data_files = [
        (pjoin('share', 'doc', 'pydot'), ['README'])
    ],

    packages = ['pydot',],
    package_dir = {'': moddir},

    py_modules = ['pydot',],
)
