# misc tests

import re
import sys
import unittest

import roundup.anypy.cmp_

from roundup.anypy.strings import StringIO  # define StringIO
from roundup.cgi import cgitb
from roundup.cgi.accept_language import parse


class AcceptLanguageTest(unittest.TestCase):
    def testParse(self):
        self.assertEqual(parse("da, en-gb;q=0.8, en;q=0.7"),
                         ['da', 'en_gb', 'en'])
        self.assertEqual(parse("da, en-gb;q=0.7, en;q=0.8"),
                         ['da', 'en', 'en_gb'])
        self.assertEqual(parse("en;q=0.2, fr;q=1"), ['fr', 'en'])
        self.assertEqual(parse("zn; q = 0.2 ,pt-br;q =1"), ['pt_br', 'zn'])
        self.assertEqual(parse("pt-br;q =1, zn; q = 0.2"), ['pt_br', 'zn'])
        self.assertEqual(parse("pt-br,zn;q= 0.1, en-US;q=0.5"),
                         ['pt_br', 'en_US', 'zn'])
        # verify that items with q=1.0 are in same output order as input
        self.assertEqual(parse("pt-br,en-US; q=0.5, zn;q= 1.0" ),
                         ['pt_br', 'zn', 'en_US'])
        self.assertEqual(parse("zn;q=1.0;q= 1.0,pt-br,en-US; q=0.5" ),
                         ['zn', 'pt_br', 'en_US'])
        self.assertEqual(parse("es-AR"), ['es_AR'])
        self.assertEqual(parse("es-es-cat"), ['es_es_cat'])
        self.assertEqual(parse(""), [])
        self.assertEqual(parse(None),[])
        self.assertEqual(parse("   "), [])
        self.assertEqual(parse("en,"), ['en'])

class CmpTest(unittest.TestCase):
    def testCmp(self):
        roundup.anypy.cmp_._test()

class VersionCheck(unittest.TestCase):
    def test_Version_Check(self):

        # test for valid versions
        from roundup.version_check import VERSION_NEEDED
        self.assertEqual((2, 7), VERSION_NEEDED)
        del(sys.modules['roundup.version_check'])


        # fake an invalid version
        real_ver =  sys.version_info
        sys.version_info = (2, 1)

        # exit is called on failure, but that breaks testing so
        # just return and discard the exit code.
        real_exit = sys.exit 
        sys.exit =  lambda code: code

        # error case uses print(), capture and check
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        from roundup.version_check import VERSION_NEEDED
        sys.stdout = sys.__stdout__
        self.assertIn("Roundup requires Python 2.7", capturedOutput.getvalue())

        # reset to valid values for future tests
        sys.exit = real_exit
        sys.version_info = real_ver


class CgiTbCheck(unittest.TestCase):

    def test_NiceDict(self):
        d = cgitb.niceDict("    ", { "two": "three", "four": "five" })

        expected = (
            "<tr><td><strong>four</strong></td><td>'five'</td></tr>\n"
            "<tr><td><strong>two</strong></td><td>'three'</td></tr>"
            )

        self.assertEqual(expected, d)

    def test_breaker(self):
        b = cgitb.breaker()

        expected = ('<body bgcolor="white"><font color="white" size="-5">'
                    ' > </font> </table></table></table></table></table>')

        self.assertEqual(expected, b)

    def test_pt_html(self):
        """ templating error """
        try:
            f = 5
            d = a + 4
        except Exception:
            p = cgitb.pt_html(context=2)

        expected2 = """<h1>Templating Error</h1>
<p><b>&lt;type 'exceptions.NameError'&gt;</b>: global name 'a' is not defined</p>
<p class="help">Debugging information follows</p>
<ol>

</ol>
<table style="font-size: 80%; color: gray">
 <tr><th class="header" align="left">Full traceback:</th></tr>
 <tr><td><pre>Traceback (most recent call last):
  File "XX/test/test_misc.py", line XX, in test_pt_html
    d = a + 4
NameError: global name 'a' is not defined
</pre></td></tr>
</table>
<p>&nbsp;</p>"""

        expected3 = """<h1>Templating Error</h1>
<p><b>&lt;class 'NameError'&gt;</b>: name 'a' is not defined</p>
<p class="help">Debugging information follows</p>
<ol>

</ol>
<table style="font-size: 80%; color: gray">
 <tr><th class="header" align="left">Full traceback:</th></tr>
 <tr><td><pre>Traceback (most recent call last):
  File "XX/test/test_misc.py", line XX, in test_pt_html
    d = a + 4
NameError: name 'a' is not defined
</pre></td></tr>
</table>
<p>&nbsp;</p>"""

        # allow file directory prefix and line number to change
        p = re.sub(r'(File ")/.*/(test/test_misc.py",)', r'\1XX/\2', p)
        p = re.sub(r'(", line )\d*,', r'\1XX,', p)

        print(p)

        if sys.version_info > (3, 0, 0):
            self.assertEqual(expected3, p)
        else:
            self.assertEqual(expected2, p)

    def notest_html(self):
        """ templating error """
        # enabiling this will cause the test to fail as the variable
        # is included in the live outpu but not in expected.
        # self.maxDiff = None

        try:
            f = 5
            d = a + 4
        except Exception:
            h = cgitb.html(context=2)

            expected2 = """
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="heading">
<tr bgcolor="#777777">
<td valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial">&nbsp;<br><font size=+1><strong>NameError</strong>: global name 'a' is not defined</font></font></td
><td align=right valign=bottom
><font color="#ffffff" face="helvetica, arial">Python XX</font></td></tr></table>
    <p>A problem occurred while running a Python script. Here is the sequence of function calls leading up to the error, with the most recent (innermost) call first. The exception attributes are:<br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__class__&nbsp;= &lt;type 'exceptions.NameError'&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__delattr__&nbsp;= &lt;method-wrapper '__delattr__' of exceptions.NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__dict__&nbsp;= {} <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__doc__&nbsp;= 'Name not found globally.' <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__format__&nbsp;= &lt;built-in method __format__ of exceptions.NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__getattribute__&nbsp;= &lt;method-wrapper '__getattribute__' of exceptions.NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__getitem__&nbsp;= &lt;method-wrapper '__getitem__' of exceptions.NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__getslice__&nbsp;= &lt;method-wrapper '__getslice__' of exceptions.NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__hash__&nbsp;= &lt;method-wrapper '__hash__' of exceptions.NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__init__&nbsp;= &lt;method-wrapper '__init__' of exceptions.NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__new__&nbsp;= &lt;built-in method __new__ of type object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__reduce__&nbsp;= &lt;built-in method __reduce__ of exceptions.NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__reduce_ex__&nbsp;= &lt;built-in method __reduce_ex__ of exceptions.NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__repr__&nbsp;= &lt;method-wrapper '__repr__' of exceptions.NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__setattr__&nbsp;= &lt;method-wrapper '__setattr__' of exceptions.NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__setstate__&nbsp;= &lt;built-in method __setstate__ of exceptions.NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__sizeof__&nbsp;= &lt;built-in method __sizeof__ of exceptions.NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__str__&nbsp;= &lt;method-wrapper '__str__' of exceptions.NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__subclasshook__&nbsp;= &lt;built-in method __subclasshook__ of type object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__unicode__&nbsp;= &lt;built-in method __unicode__ of exceptions.NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>args&nbsp;= ("global name 'a' is not defined",) <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>message&nbsp;= "global name 'a' is not defined"<p>
<table width="100%" bgcolor="#dddddd" cellspacing=0 cellpadding=2 border=0>
<tr><td><a href="file:XX/test/test_misc.py">XX/test/test_misc.py</a> in <strong>test_html</strong>(self=&lt;test.test_misc.CgiTbCheck testMethod=test_html&gt;)</td></tr></table>
<tt><small><font color="#909090">&nbsp;&nbsp;XX</font></small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;f&nbsp;=&nbsp;5<br>
</tt>


<table width="100%" bgcolor="white" cellspacing=0 cellpadding=0 border=0>
<tr><td><tt><small><font color="#909090">&nbsp;&nbsp;XX</font></small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;d&nbsp;=&nbsp;a&nbsp;+&nbsp;4<br>
</tt></td></tr></table>
<tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt><small><font color="#909090"><strong>d</strong>&nbsp;= <em>undefined</em>, <em>global</em> <strong>a</strong>&nbsp;= <em>undefined</em></font></small><br><p>&nbsp;</p>"""

            expected3 = """\n<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="heading">\n<tr bgcolor="#777777">\n<td valign=bottom>&nbsp;<br>\n<font color="#ffffff" face="helvetica, arial">&nbsp;<br><font size=+1><strong>NameError</strong>: name \'a\' is not defined</font></font></td\n><td align=right valign=bottom\n><font color="#ffffff" face="helvetica, arial">Python XX</font></td></tr></table>\n    <p>A problem occurred while running a Python script. Here is the sequence of function calls leading up to the error, with the most recent (innermost) call first. The exception attributes are:<br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__cause__&nbsp;= None <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__class__&nbsp;= &lt;class \'NameError\'&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__context__&nbsp;= None <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__delattr__&nbsp;= &lt;method-wrapper \'__delattr__\' of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__dict__&nbsp;= {} <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__dir__&nbsp;= &lt;built-in method __dir__ of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__doc__&nbsp;= \'Name not found globally.\' <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__eq__&nbsp;= &lt;method-wrapper \'__eq__\' of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__format__&nbsp;= &lt;built-in method __format__ of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__ge__&nbsp;= &lt;method-wrapper \'__ge__\' of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__getattribute__&nbsp;= &lt;method-wrapper \'__getattribute__\' of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__gt__&nbsp;= &lt;method-wrapper \'__gt__\' of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__hash__&nbsp;= &lt;method-wrapper \'__hash__\' of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__init__&nbsp;= &lt;method-wrapper \'__init__\' of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__init_subclass__&nbsp;= &lt;built-in method __init_subclass__ of type object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__le__&nbsp;= &lt;method-wrapper \'__le__\' of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__lt__&nbsp;= &lt;method-wrapper \'__lt__\' of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__ne__&nbsp;= &lt;method-wrapper \'__ne__\' of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__new__&nbsp;= &lt;built-in method __new__ of type object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__reduce__&nbsp;= &lt;built-in method __reduce__ of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__reduce_ex__&nbsp;= &lt;built-in method __reduce_ex__ of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__repr__&nbsp;= &lt;method-wrapper \'__repr__\' of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__setattr__&nbsp;= &lt;method-wrapper \'__setattr__\' of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__setstate__&nbsp;= &lt;built-in method __setstate__ of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__sizeof__&nbsp;= &lt;built-in method __sizeof__ of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__str__&nbsp;= &lt;method-wrapper \'__str__\' of NameError object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__subclasshook__&nbsp;= &lt;built-in method __subclasshook__ of type object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__suppress_context__&nbsp;= False <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>__traceback__&nbsp;= &lt;traceback object&gt; <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>args&nbsp;= ("name \'a\' is not defined",) <br><tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt>with_traceback&nbsp;= &lt;built-in method with_traceback of NameError object&gt;<p>\n<table width="100%" bgcolor="#dddddd" cellspacing=0 cellpadding=2 border=0>\n<tr><td><a href="file:XX/test/test_misc.py">XX/test/test_misc.py</a> in <strong>test_html</strong>(self=&lt;test.test_misc.CgiTbCheck testMethod=test_html&gt;)</td></tr></table>\n<tt><small><font color="#909090">&nbsp;&nbsp;XX</font></small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;f&nbsp;=&nbsp;5<br>\n</tt>\n\n\n<table width="100%" bgcolor="white" cellspacing=0 cellpadding=0 border=0>\n<tr><td><tt><small><font color="#909090">&nbsp;&nbsp;XX</font></small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;d&nbsp;=&nbsp;a&nbsp;+&nbsp;4<br>\n</tt></td></tr></table>\n<tt><small>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small>&nbsp;</tt><small><font color="#909090"><strong>d</strong>&nbsp;= <em>undefined</em>, <em>global</em> <strong>a</strong>&nbsp;= <em>undefined</em></font></small><br><p>&nbsp;</p>"""

        # strip file path prefix from href and text
        # /home/user/develop/roundup/test/test_misc.py in test_html
        h = re.sub(r'(file:)/.*/(test/test_misc.py")', r'\1XX/\2', h)
        h = re.sub(r'(/test_misc.py">)/.*/(test/test_misc.py</a>)',
                   r'\1XX/\2', h)
        # replace code line numbers with XX
        h = re.sub(r'(&nbsp;)\d*(</font>)', r'\1XX\2', h)
        # normalize out python version/path
        h = re.sub(r'(Python )[\d.]*<br>[^<]*(</font><)', r'\1XX\2', h)

        print(h)

        if sys.version_info > (3, 0, 0):
            self.assertEqual(expected3, h)
        else:
            self.assertEqual(expected2, h)
