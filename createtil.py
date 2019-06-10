#!/usr/bin/env python
''' Simple script to auto-generate the README.md file for a til project.
    Apply as a git hook by running the following command in linux:
        cd .git/hooks/ && ln -s ../../createtil.py pre-commit && cd -
'''
from __future__ import print_function
import os

HEADER = '''# TIL

> Today I Learned

A collection of concise write-ups on small things I learn day to day across a
variety of languages and technologies.

'''

FOOTER = '''## Usage

Steps to follow : 

1. Create directories for specific topics for example if you solve a problem on *HackerRank* create 
   a directory named `Competitive Programming` or if you learned something new in JavaScript , create a 
   directory for the same .
   Some recommended categories :
    - Data Structures & Algo
    - Meetups
    - C++/JavaScript/Python
    - HTML/CSS
    - Git/Version Control
    - Machine Learning

2. Inside those directories create a [`Markdown`](https://www.markdownguide.org/basic-syntax/) file with your title for example 
    `Variables_in_JavaScript.md`, `Create_React_App.md` etc.
3. Run `python createtil.py > README.md` to auto-generate the New README file for you 
    OR
   If you are using git, you can install this script as a pre-commit git hook so
    that it is autogenerated on each commit.  Use the following command:
    `cd .git/hooks/ && ln -s ../../createtil.py pre-commit && cd -`
 
4. Once satisfied push your changes.


## About

Original Idea/Work [thoughtbot/til](https://github.com/thoughtbot/til).

## Other TIL Collections

* [Today I Learned by Hashrocket](https://til.hashrocket.com)
* [jwworth/til](https://github.com/jwworth/til)
* [thoughtbot/til](https://github.com/thoughtbot/til)
'''

def get_list_of_categories():
    ''' Walk the current directory and get a list of all subdirectories at that
    level.  These are the "categories" in which there are TILs.'''
    dirs = [x for x in os.listdir('.') if os.path.isdir(x) and
            '.git' not in x]
    return dirs

def get_title(til_file):
    ''' Read the file until we hit the first line that starts with a #
    indicating a title in markdown.  We'll use that as the title for this
    entry. '''
    with open(til_file) as _file:
        for line in _file:
            line = line.strip()
            if line.startswith('#'):
                return line[1:].lstrip()  # text after # and whitespace

def get_tils(category):
    ''' For a given category, get the list of TIL titles. '''
    til_files = [x for x in os.listdir(category)]
    titles = []
    for filename in til_files:
        fullname = os.path.join(category, filename)
        if (os.path.isfile(fullname)) and fullname.endswith('.md'):
            title = get_title(fullname)
            titles.append((title, fullname))
    return titles

def get_category_dict(category_names):
    categories = {}
    count = 0
    for category in category_names:
        titles = get_tils(category)
        categories[category] = titles
        count += len(titles)
    return count, categories

def print_file(category_names, count, categories):
    ''' Now we have all the information, print it out in markdown format. '''
    with open('README.md', 'w') as file_:
        file_.write(HEADER)
        file_.write('\n')
        file_.write('_{0} TILs and counting..._'.format(count))
        file_.write('\n')
        file_.write('''
---

### Categories

''')
        # print the list of categories with links
        for category in sorted(category_names):
            file_.write('* [{0}](#{1})\n'.format(category.capitalize(),
                                                 category))

        # print the section for each category
        file_.write('''
---

''')
        for category in sorted(category_names):
            file_.write('### {0}\n'.format(category.capitalize()))
            file_.write('\n')
            tils = categories[category]
            for (title, filename) in sorted(tils):
                file_.write('- [{0}]({1})\n'.format(title, filename))
            file_.write('\n')

        file_.write(FOOTER)

def create_readme():
    ''' Create a TIL README.md file with a nice index for using it directly
        from github. '''
    category_names = get_list_of_categories()
    count, categories = get_category_dict(category_names)
    print_file(category_names, count, categories)

if __name__ == '__main__':
    create_readme()
    os.system('git add README.md')