#!/usr/bin/env python
# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import idl_schema
import json_parse
from js_interface_generator import JsInterfaceGenerator
from datetime import datetime
import model
import sys
import unittest

# The contents of a fake idl file.
fake_idl = """
// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// A totally fake API.
namespace fakeApi {
  enum Greek {
    ALPHA,
    BETA,
    GAMMA,
    DELTA
  };

  dictionary Bar {
    long num;
  };

  dictionary Baz {
    DOMString str;
    long num;
    boolean b;
    Greek letter;
    Greek? optionalLetter;
    long[] arr;
    Bar[]? optionalObjArr;
    Greek[] enumArr;
    any[] anythingGoes;
    Bar obj;
    long? maybe;
    (DOMString or Greek or long[]) choice;
    object plainObj;
  };

  callback VoidCallback = void();

  callback BazGreekCallback = void(Baz baz, Greek greek);

  interface Functions {
    // Does something exciting! And what's more, this is a multiline function
    // comment! It goes onto multiple lines!
    // |baz| : The baz to use.
    static void doSomething(Baz baz, VoidCallback callback);

    // |callback| : The callback which will most assuredly in all cases be
    // called; that is, of course, iff such a callback was provided and is
    // not at all null.
    static void bazGreek(optional BazGreekCallback callback);

    [deprecated="Use a new method."] static DOMString returnString();
  };

  interface Events {
    // Fired when we realize it's a trap!
    static void onTrapDetected(Baz baz);
  };
};
"""

# The output we expect from our fake idl file.
fake_idl_output = ("""// Copyright %s The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// This file was generated by:
//   %s.

/** @fileoverview Interface for fakeApi that can be overriden. */

assertNotReached('Interface file for Closure Compiler should not be executed.');

/** @interface */
function FakeApi() {}

FakeApi.prototype = {
  /**
   * Does something exciting! And what's more, this is a multiline function
   * comment! It goes onto multiple lines!
   * @param {!chrome.fakeApi.Baz} baz The baz to use.
   * @param {function():void} callback
   * @see https://developer.chrome.com/extensions/fakeApi#method-doSomething
   */
  doSomething: assertNotReached,

  /**
   * @param {function(!chrome.fakeApi.Baz, !chrome.fakeApi.Greek):void=}
   *     callback The callback which will most assuredly in all cases be called;
   *     that is, of course, iff such a callback was provided and is not at all
   *     null.
   * @see https://developer.chrome.com/extensions/fakeApi#method-bazGreek
   */
  bazGreek: assertNotReached,
};

/**
 * Fired when we realize it's a trap!
 * @type {!ChromeEvent}
 * @see https://developer.chrome.com/extensions/fakeApi#event-onTrapDetected
 */
FakeApi.prototype.onTrapDetected;""" % (datetime.now().year, sys.argv[0]))

class JsExternGeneratorTest(unittest.TestCase):
  def _GetNamespace(self, fake_content, filename):
    """Returns a namespace object for the given content"""
    api_def = idl_schema.Process(fake_content, filename)
    m = model.Model()
    return m.AddNamespace(api_def[0], filename)

  def setUp(self):
    self.maxDiff = None # Lets us see the full diff when inequal.

  def testBasic(self):
    namespace = self._GetNamespace(fake_idl, 'fake_api.idl')
    self.assertMultiLineEqual(
        fake_idl_output,
        JsInterfaceGenerator().Generate(namespace).Render())


if __name__ == '__main__':
  unittest.main()
