import argparse
import calendar
import logging
import os
import re

from colorlog import ColoredFormatter
from dateutil.parser import parse as date_parse
from lxml import etree
import html2text
import xattr
import biplist

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red',
    }
)
stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
stream.setFormatter(formatter)
logger = logging.getLogger('evernote2markdown')
logger.setLevel(logging.DEBUG)
logger.addHandler(stream)


class EvernoteToMarkdown(object):

    def __init__(self, enex_path, dest_dir, extra_tags):
        self.enex_path = enex_path
        self.extra_tags = extra_tags
        self.h2t = html2text.HTML2Text()
        self.h2t.body_width = 0
        self.h2t.ignore_links = True
        self.h2t.single_line_break = True
        if not os.path.isdir(dest_dir):
            os.mkdir(dest_dir)
        self.dest_dir = dest_dir

    def create_file(self, title, text, ct):
        chk_path = os.path.join(self.dest_dir, '%s.md' % title)
        if os.path.isfile(chk_path):
            title = '%s (%s).md' % (title, str(ct))
        else:
            title = '%s.md' % title
        path = os.path.join(self.dest_dir, title)
        with open(path, 'w') as md_file:
            md_file.write(self._process_text(text))
        return path

    def add_file_metadata(self, path, updated_timestamp, tags):
        if self.extra_tags:
            if tags:
                tags += self.extra_tags
            else:
                tags = self.extra_tags
        # set file modified/accessed date
        os.utime(path, (updated_timestamp, updated_timestamp))

        # add file tag xattr's
        plist_str = biplist.writePlistToString(tags)
        # use both OpenMeta tags and Apple Mavericks tags
        xattr_domains = [
            'com.apple.metadata:_kMDItemUserTags',
            'com.apple.metadata:kMDItemOMUserTags'
        ]
        for domain in xattr_domains:
            xattr.setxattr(path, domain, plist_str)

    def _process_text(self, raw_text):
        pre_converted_text = self.h2t.handle(raw_text)
        converted_text = unicode(
            pre_converted_text.replace('\n\\- ', '\n* ')
        ).encode('utf-8').strip()
        return converted_text

    def convert(self):
        with open(self.enex_path, 'r') as enex_file:
            xml_tree = etree.parse(enex_file)
        raw_notes = xml_tree.xpath('//note')
        ct = 0
        for note in raw_notes:
            raw_title = note.xpath('title')[0].text
            title = re.sub(r'[^a-zA-Z0-9\?\-]+', " ", raw_title).strip()
            updated = date_parse(note.xpath('updated')[0].text)
            updated_timestamp = calendar.timegm(updated.timetuple())
            tags = [tag.text for tag in note.xpath('tag')]
            content = note.xpath('content')
            if content:
                raw_text = content[0].text
                if 'en-crypt' in content[0].text:
                    # TODO: logging
                    logger.warning('Encrypted content in: %s', title)
            else:
                raw_text = ''

            ct += 1
            markdown_file_path = self.create_file(title, raw_text, ct)
            self.add_file_metadata(markdown_file_path, updated_timestamp, tags)
        return ct


def main():
    parser = argparse.ArgumentParser(
        description='Convert Evernote .enex export to Markdown files.')
    parser.add_argument('src')
    parser.add_argument('dest')
    parser.add_argument('tags', nargs='?', default='')
    args = parser.parse_args()
    # TODO: validate input
    extra_tags = args.tags.split(',') if args.tags else None
    en2md = EvernoteToMarkdown(args.src, args.dest, extra_tags)
    total = en2md.convert()
    logger.info('%d documents processed', total)

if __name__ == '__main__':
    main()
