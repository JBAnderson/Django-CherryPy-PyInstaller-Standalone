#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tango_project.settings")

    from django.core.management import execute_from_command_line
    import django.test
    import HTMLParser
    import Cookie
    import django.contrib.sessions.serializers

    execute_from_command_line(sys.argv)
