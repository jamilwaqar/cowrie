# -*- test-case-name: Cowrie Test Cases -*-

# Copyright (c) 2018 Michel Oosterhof
# See LICENSE for details.

"""
Tests for general shell interaction and echo command
"""


import os

from twisted.trial import unittest

from cowrie.shell import protocol
from cowrie.test import fake_server, fake_transport

os.environ["COWRIE_HONEYPOT_DATA_PATH"] = "../data"
os.environ["COWRIE_HONEYPOT_DOWNLOAD_PATH"] = "/tmp"
os.environ["COWRIE_SHELL_FILESYSTEM"] = "../share/cowrie/fs.pickle"

PROMPT = b"root@unitTest:~# "


class ShellEchoCommandTests(unittest.TestCase):
    def setUp(self):
        self.proto = protocol.HoneyPotInteractiveProtocol(
            fake_server.FakeAvatar(fake_server.FakeServer())
        )
        self.tr = fake_transport.FakeTransport("1.1.1.1", "1111")
        self.proto.makeConnection(self.tr)
        self.tr.clear()

    def test_awk_command_001(self):
        """
        Test $0, full input line contents
        """
        self.proto.lineReceived(b'echo "test test" | awk "{ print $0 }"\n')
        self.assertEqual(self.tr.value(), b"test test\n" + PROMPT)

    def test_awk_command_002(self):
        """
        Test $1, first agument
        """
        self.proto.lineReceived(b'echo "test" | awk "{ print $1 }"\n')
        self.assertEqual(self.tr.value(), b"test\n" + PROMPT)

    def test_awk_command_003(self):
        """
        Test $1 $2 space separated
        """
        self.proto.lineReceived(b'echo "test test" | awk "{ print $1 $2 }"\n')
        self.assertEqual(self.tr.value(), b"test test\n" + PROMPT)

    def test_awk_command_004(self):
        """
        Test $1,$2 comma separated
        """
        self.proto.lineReceived(b'echo "test test" | awk "{ print $1,$2 }"\n')
        self.assertEqual(self.tr.value(), b"test test\n" + PROMPT)

    def test_awk_command_005(self):
        """
        Test $1$2 not separated
        """
        self.proto.lineReceived(b'echo "test test" | awk "{ print $1$2 }"\n')
        self.assertEqual(self.tr.value(), b"testtest\n" + PROMPT)

    def tearDown(self):
        self.proto.connectionLost("tearDown From Unit Test")
