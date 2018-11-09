#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from grr_response_core.lib.util import csv
import unittest


class CsvWriterTest(unittest.TestCase):

  def testEmpty(self):
    writer = csv.Writer()

    self.assertEqual(writer.Content(), "")

  def testSingleRow(self):
    writer = csv.Writer()
    writer.WriteRow(["foo", "bar", "baz"])

    self.assertEqual(writer.Content(), "foo,bar,baz\n")

  def testMultipleRows(self):
    writer = csv.Writer()
    writer.WriteRow(["foo", "quux"])
    writer.WriteRow(["bar", "norf"])
    writer.WriteRow(["baz", "thud"])

    self.assertEqual(writer.Content(), "foo,quux\nbar,norf\nbaz,thud\n")

  def testUnicode(self):
    writer = csv.Writer()
    writer.WriteRow(["jodła", "świerk", "dąb"])
    writer.WriteRow(["żyto", "jęczmień", "ryż"])

    self.assertEqual(writer.Content(), "jodła,świerk,dąb\nżyto,jęczmień,ryż\n")

  def testCustomDelimiter(self):
    writer = csv.Writer(delimiter="|")
    writer.WriteRow(["foo", "bar", "baz"])

    self.assertEqual(writer.Content(), "foo|bar|baz\n")


class CsvDictWriter(unittest.TestCase):

  def testEmpty(self):
    writer = csv.DictWriter(["foo", "bar", "baz"])

    self.assertEqual(writer.Content(), "")

  def testSingleRow(self):
    writer = csv.DictWriter(["foo", "bar", "baz"])
    writer.WriteRow({"foo": "quux", "bar": "norf", "baz": "blargh"})

    self.assertEqual(writer.Content(), "quux,norf,blargh\n")

  def testMultipleRows(self):
    writer = csv.DictWriter(["x", "y", "z"])
    writer.WriteRow({"x": "foo", "y": "bar", "z": "baz"})
    writer.WriteRow({"x": "quux", "y": "norf", "z": "blargh"})

    self.assertEqual(writer.Content(), "foo,bar,baz\nquux,norf,blargh\n")

  def testCustomDelimiter(self):
    writer = csv.DictWriter(["1", "2", "3"], delimiter=" ")
    writer.WriteRow({"1": "a", "2": "b", "3": "c"})

    self.assertEqual(writer.Content(), "a b c\n")

  def testIrrelevantOrder(self):
    writer = csv.DictWriter(["1", "2", "3"])
    writer.WriteRow({"1": "a", "2": "b", "3": "c"})
    writer.WriteRow({"3": "d", "2": "e", "1": "f"})

    self.assertEqual(writer.Content(), "a,b,c\nf,e,d\n")

  def testWriteHeader(self):
    writer = csv.DictWriter(["A", "B", "C"])
    writer.WriteHeader()
    writer.WriteRow({"A": "foo", "B": "bar", "C": "baz"})

    self.assertEqual(writer.Content(), "A,B,C\nfoo,bar,baz\n")

  def testRaisesOnMissingColumn(self):
    writer = csv.DictWriter(["foo", "bar", "baz"])

    with self.assertRaises(ValueError):
      writer.WriteRow({"foo": "quux", "bar": "norf"})


if __name__ == "__main__":
  unittest.main()
