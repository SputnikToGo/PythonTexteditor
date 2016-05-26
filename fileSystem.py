# -*- coding: utf-8 -*-
__author__ = 'Jani Anttonen'
import os
import json
import hashlib


# File system
class File:

    """
    Specifies the file to be worked with
    Works with both new and old files (creates a new one if nonexistent)
    """
    def __init__(self, path):

        # Original file (flat text)
        self.original = path

        # Make data directory, if not present
        os.makedirs("data/",exist_ok=True)

        # Initialize tag file (JSON)
        self.path = "data/" + hashlib.md5(path.encode('utf-8')).hexdigest() + ".json"
        if not os.path.isfile(self.path):
            # Write to the file
            with open(self.path, 'w') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    """
    Tagging functionality.
    Gets the tag and its indeces,
    and then appends them to the tag file.
    """
    def tag(self,description,index):
        """
        :rtype: object
        :param description:
        :param index:
        """

        # Form the tag
        tag = {'index':index,'tag':[description]}

        # Load existing tags
        with open(self.path) as tagsjson:
            tags = json.load(tagsjson)

        # Add the new tag to the end of tags
        if len(tags)>0:
            for existing_tags in tags:
                if index == existing_tags['index']:
                    for existing_tag in existing_tags['tag']:
                        for new_tag in tag.get('tag'):
                            if new_tag==existing_tag:
                                print("No duplicate tags allowed.")
                                return False
                    for new_tag in tag.get('tag'):
                        existing_tags['tag'].append(new_tag)
        else:
            tags.append(tag)

        # Save to file
        with open(self.path, 'w') as f:
            json.dump(tags, f, ensure_ascii=False, indent=2, sort_keys=True)


    """
    GET + SET
    """
    # GETTER
    def read(self):
        with open(self.original) as f:
            return f.read()

    # SETTER
    def write(self,content):
        with open(self.original, 'a+', encoding=('utf-8')) as f:
            f.write(content)

    # READ TAGS
    def readtags(self):
        with open(self.path) as tagsjson:
            return json.load(tagsjson)

    # READ TAGS BY INDEX
    def get_tags_by_index(self, index):
        for tag in self.readtags():
            if index == tag['index']:
                return tag['tag']
