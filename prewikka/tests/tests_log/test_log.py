# Copyright (C) 2018-2020 CS GROUP - France. All Rights Reserved.
#
# This file is part of the Prewikka program.
#
# SPDX-License-Identifier: BSD-2-Clause
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIEDi
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Tests for `prewikka.log`.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import os
import sys

import pytest

from prewikka.config import ConfigSection
from prewikka.log import Log
from tests.utils.vars import TEST_DOWNLOAD_DIR


def test_log():
    """
    Test `prewikka.log.Log` class.
    """
    conf = ConfigSection("syslog")
    conf.level = "debug"

    log = Log([conf])
    log.log(10, 'foo bar')
    log.log(20, 'foo bar')
    log.log(30, 'foo bar')
    log.log(40, 'foo bar')
    log.log(50, 'foo bar')

    with pytest.raises(KeyError):
        log.log(60, 'foo bar')

    # with exception
    log.log(10, TypeError())

    # levels
    if env.config.log:
        for level in ('debug', 'all', 'warning', 'error', 'critical', 'invalid'):
            c = ConfigSection("syslog")
            c.level = level
            log = Log([c])
            log.log(10, 'foo bar')
            log.log(20, 'foo bar')
            log.log(30, 'foo bar')
            log.log(40, 'foo bar')
            log.log(50, 'foo bar')

    # request.web
    backup_web = copy.copy(env.request.web)
    env.request.web.is_xhr = True
    log = Log([conf])
    log.log(10, 'foo bar')
    env.request.web.is_xhr = False

    env.request.web.is_stream = True
    log = Log([conf])
    log.log(10, 'foo bar')
    env.request.web.is_stream = False

    env.request.web.port = 8080

    # clean
    env.request.web = backup_web


def test_log_syslog():
    """
    Test `prewikka.log.Log` class.

    With syslog option.
    """
    # syslog is by default
    # this test should be improved
    conf = ConfigSection("syslog")
    conf.level = "debug"

    log = Log([conf])
    log.log(10, 'foo bar')


def test_log_file():
    """
    Test `prewikka.log.Log` class.

    With file option.
    """
    conf = ConfigSection("file")
    conf.level = "debug"
    conf.file = os.path.join(TEST_DOWNLOAD_DIR, 'prewikka.logs')
    try:
        output_file_size = os.stat(conf.file).st_size
    except OSError:
        output_file_size = 0

    log = Log([conf])
    log.log(10, 'foo bar')

    assert output_file_size != os.stat(conf.file).st_size


@pytest.mark.xfail(reason='pytest upgrade required (3.0+)')
def test_log_stderr():
    """
    Test `prewikka.log.Log` class.

    With stderr option.

    FIXME: with pytest 3+, a solution exists to disable std* captured by pytest.
    https://docs.pytest.org/en/3.0.0/capture.html#accessing-captured-output-from-a-test-function
    """
    conf = ConfigSection("debug")
    conf.level = "debug"
    initial_stderr = sys.stderr

    log = Log([conf])
    log.log(10, 'foo bar')

    assert initial_stderr != sys.stderr


def test_log_smtp():
    """
    Test `prewikka.log.Log` class.

    With smtp option.
    """
    conf = ConfigSection("smtp")
    conf.level = "debug"
    conf.host = "localhost"
    conf["from"] = "user@localhost"
    conf.to = "root@localhost"
    conf.subject = "Prewikka Test !"

    log = Log([conf])
    log.log(10, 'foo bar')


def test_log_nteventlog():
    """
    Test `prewikka.log.Log` class.

    With nteventlog option.
    """
    conf = ConfigSection("nteventlog")
    conf.level = "debug"

    log = Log([conf])
    log.log(10, 'foo bar')


def test_log_invalid_format():
    """
    Test `prewikka.log.Log` class.

    With an invalid format.
    """
    conf = ConfigSection("somethinginvalid")
    conf.level = "debug"

    with pytest.raises(ValueError):
        Log([conf])
