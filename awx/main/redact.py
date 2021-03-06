import re
import urllib.parse as urlparse

from django.conf import settings

REPLACE_STR = '$encrypted$'


class UriCleaner(object):
    REPLACE_STR = REPLACE_STR
    SENSITIVE_URI_PATTERN = re.compile(r'(\w+:(\/?\/?)[^\s]+)', re.MULTILINE)  # NOQA

    @staticmethod
    def remove_sensitive(cleartext):
        # exclude_list contains the items that will _not_ be redacted
        exclude_list = [settings.PUBLIC_GALAXY_SERVER['url']]
        if settings.PRIMARY_GALAXY_URL:
            exclude_list += [settings.PRIMARY_GALAXY_URL]
        if settings.FALLBACK_GALAXY_SERVERS:
            exclude_list += [server['url'] for server in settings.FALLBACK_GALAXY_SERVERS]
        redactedtext = cleartext
        text_index = 0
        while True:
            match = UriCleaner.SENSITIVE_URI_PATTERN.search(redactedtext, text_index)
            if not match:
                break
            uri_str = match.group(1)
            # Do not redact items from the exclude list
            if any(uri_str.startswith(exclude_uri) for exclude_uri in exclude_list):
                text_index = match.start() + len(uri_str)
                continue
            try:
                # May raise a ValueError if invalid URI for one reason or another
                o = urlparse.urlsplit(uri_str)

                if not o.username and not o.password:
                    if o.netloc and ":" in o.netloc:
                        # Handle the special case url http://username:password that can appear in SCM url
                        # on account of a bug? in ansible redaction
                        (username, password) = o.netloc.split(':')
                    else:
                        text_index += len(match.group(1))
                        continue
                else:
                    username = o.username
                    password = o.password

                # Given a python MatchObject, with respect to redactedtext, find and
                # replace the first occurance of username and the first and second
                # occurance of password

                uri_str = redactedtext[match.start():match.end()]
                if username:
                    uri_str = uri_str.replace(username, UriCleaner.REPLACE_STR, 1)
                # 2, just in case the password is $encrypted$
                if password:
                    uri_str = uri_str.replace(password, UriCleaner.REPLACE_STR, 2)

                t = redactedtext[:match.start()] + uri_str
                text_index = len(t)
                if (match.end() < len(redactedtext)):
                    t += redactedtext[match.end():]

                redactedtext = t
                if text_index >= len(redactedtext):
                    text_index = len(redactedtext) - 1
            except ValueError:
                # Invalid URI, redact the whole URI to be safe
                redactedtext = redactedtext[:match.start()] + UriCleaner.REPLACE_STR + redactedtext[match.end():]
                text_index = match.start() + len(UriCleaner.REPLACE_STR)

        return redactedtext


class PlainTextCleaner(object):
    REPLACE_STR = REPLACE_STR

    @staticmethod
    def remove_sensitive(cleartext, sensitive):
        if sensitive == '':
            return cleartext
        return re.sub(r'%s' % re.escape(sensitive), '$encrypted$', cleartext)
