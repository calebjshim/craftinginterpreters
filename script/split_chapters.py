#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import codecs
import glob
import os

CHAPTERS = [
  "Framework",
  "Scanning",
  "Syntax Trees",
  "Parsing Expressions",
  "Interpreting ASTs",
  "Variables",
  "Functions",
  "Closures",
  "Control Flow",
  "Classes",
  "Inheritance",
  # TODO: Figure out what to do with this stuff.
  "Uhh"
]


def chapter_to_package(index):
  name = CHAPTERS[index].split()[0].lower()
  return "chap{0:02d}_{1}".format(index + 1, name)


def split_file(path, chapter_index):
  relative = os.path.relpath(path, "java")
  directory = os.path.dirname(relative)

  # Don't split the generated files.
  if relative == "com/craftinginterpreters/vox/Expr.java": return
  if relative == "com/craftinginterpreters/vox/Stmt.java": return

  package = chapter_to_package(chapter_index)
  ensure_dir(os.path.join("gen", package, directory))
  print "  ", relative

  min_chapter = 0
  max_chapter = 999

  # Some chunks of code are replaced in later chapters, so they are commented
  # out in the canonical source. This tracks when we are in one of those.
  in_block_comment = False

  # Read the source file and preprocess it.
  output = ""
  with open(path, 'r') as input:
    # Read each line, preprocessing the special codes.
    for line in input:
      if line.startswith("//>= "):
        chapter_name = line[4:].strip()
        min_chapter = CHAPTERS.index(chapter_name)
        max_chapter = 999
      elif line.startswith("/*== "):
        chapter_name = line[4:].strip()
        min_chapter = CHAPTERS.index(chapter_name)
        max_chapter = min_chapter
        in_block_comment = True
      elif in_block_comment and line.strip() == "*/":
        in_block_comment = False
      elif chapter_index >= min_chapter and chapter_index <= max_chapter:
        output += line

  # Write the output.
  if output:
    output_path = os.path.join("gen", package, relative)
    with codecs.open(output_path, "w", encoding="utf-8") as out:
      out.write(output)


def ensure_dir(path):
  if not os.path.exists(path):
      os.makedirs(path)


def walk(dir, extension, callback):
  """
  Walks [dir], and executes [callback] on each file.
  """

  dir = os.path.abspath(dir)
  for path in os.listdir(dir):
    nfile = os.path.join(dir, path)
    if os.path.isdir(nfile):
      walk(nfile, extension, callback)
    elif os.path.splitext(path)[1] == extension:
      callback(nfile)


for i, chapter in enumerate(CHAPTERS):
  print i, chapter

  walk("java", ".java", lambda path: split_file(path, i))