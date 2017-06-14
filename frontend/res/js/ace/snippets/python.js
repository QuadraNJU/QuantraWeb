ace.define("ace/snippets/python",["require","exports","module"], function(require, exports, module) {
"use strict";

exports.snippetText = "snippet #!\n\
\t#!/usr/bin/env python\n\
snippet account.params\n\
\taccount.params['${1:name}']\n\
snippet account.cash\n\
\taccount.cash\n\
snippet account.portfolio\n\
\taccount.portfolio\n\
snippet account.sec_pos\n\
\taccount.sec_pos[${1:stock}]\n\
snippet account.price\n\
\taccount.price[${1:stock}]\n\
snippet account.universe_data\n\
\taccount.universe_data\n\
snippet account.today_data\n\
\taccount.today_data\n\
snippet account.get_stocks\n\
\taccount.get_stocks()\n\
snippet account.get_history\n\
\taccount.get_history('${1:attr}', ${2:days})\n\
snippet account.trade\n\
\taccount.trade(${1:stock}, ${2:target})\n\
snippet imp\n\
\timport ${1:module}\n\
snippet from\n\
\tfrom ${1:package} import ${2:module}\n\
# Module Docstring\n\
snippet docs\n\
\t'''\n\
\tFile: ${1:FILENAME:file_name}\n\
\tAuthor: ${2:author}\n\
\tDescription: ${3}\n\
\t'''\n\
snippet wh\n\
\twhile ${1:condition}:\n\
\t\t${2:# TODO: write code...}\n\
# dowh - does the same as do...while in other languages\n\
snippet dowh\n\
\twhile True:\n\
\t\t${1:# TODO: write code...}\n\
\t\tif ${2:condition}:\n\
\t\t\tbreak\n\
snippet with\n\
\twith ${1:expr} as ${2:var}:\n\
\t\t${3:# TODO: write code...}\n\
# New Class\n\
snippet cl\n\
\tclass ${1:ClassName}(${2:object}):\n\
\t\t\"\"\"${3:docstring for $1}\"\"\"\n\
\t\tdef __init__(self, ${4:arg}):\n\
\t\t\t${5:super($1, self).__init__()}\n\
\t\t\tself.$4 = $4\n\
\t\t\t${6}\n\
# New Function\n\
snippet def\n\
\tdef ${1:fname}(${2:`indent('.') ? 'self' : ''`}):\n\
\t\t\"\"\"${3:docstring for $1}\"\"\"\n\
\t\t${4:# TODO: write code...}\n\
snippet deff\n\
\tdef ${1:fname}(${2:`indent('.') ? 'self' : ''`}):\n\
\t\t${3:# TODO: write code...}\n\
# New Method\n\
snippet defs\n\
\tdef ${1:mname}(self, ${2:arg}):\n\
\t\t${3:# TODO: write code...}\n\
# New Property\n\
snippet property\n\
\tdef ${1:foo}():\n\
\t\tdoc = \"${2:The $1 property.}\"\n\
\t\tdef fget(self):\n\
\t\t\t${3:return self._$1}\n\
\t\tdef fset(self, value):\n\
\t\t\t${4:self._$1 = value}\n\
# Ifs\n\
snippet if\n\
\tif ${1:condition}:\n\
\t\t${2:# TODO: write code...}\n\
snippet el\n\
\telse:\n\
\t\t${1:# TODO: write code...}\n\
snippet ei\n\
\telif ${1:condition}:\n\
\t\t${2:# TODO: write code...}\n\
# For\n\
snippet for\n\
\tfor ${1:item} in ${2:items}:\n\
\t\t${3:# TODO: write code...}\n\
# Encodes\n\
snippet cutf8\n\
\t# -*- coding: utf-8 -*-\n\
snippet clatin1\n\
\t# -*- coding: latin-1 -*-\n\
snippet cascii\n\
\t# -*- coding: ascii -*-\n\
# Lambda\n\
snippet ld\n\
\t${1:var} = lambda ${2:vars} : ${3:action}\n\
snippet .\n\
\tself.\n\
snippet try Try/Except\n\
\ttry:\n\
\t\t${1:# TODO: write code...}\n\
\texcept ${2:Exception}, ${3:e}:\n\
\t\t${4:raise $3}\n\
snippet try Try/Except/Else\n\
\ttry:\n\
\t\t${1:# TODO: write code...}\n\
\texcept ${2:Exception}, ${3:e}:\n\
\t\t${4:raise $3}\n\
\telse:\n\
\t\t${5:# TODO: write code...}\n\
snippet try Try/Except/Finally\n\
\ttry:\n\
\t\t${1:# TODO: write code...}\n\
\texcept ${2:Exception}, ${3:e}:\n\
\t\t${4:raise $3}\n\
\tfinally:\n\
\t\t${5:# TODO: write code...}\n\
snippet try Try/Except/Else/Finally\n\
\ttry:\n\
\t\t${1:# TODO: write code...}\n\
\texcept ${2:Exception}, ${3:e}:\n\
\t\t${4:raise $3}\n\
\telse:\n\
\t\t${5:# TODO: write code...}\n\
\tfinally:\n\
\t\t${6:# TODO: write code...}\n\
# if __name__ == '__main__':\n\
snippet ifmain\n\
\tif __name__ == '__main__':\n\
\t\t${1:main()}\n\
# __magic__\n\
snippet _\n\
\t__${1:init}__${2}\n\
# python debugger (pdb)\n\
snippet pdb\n\
\timport pdb; pdb.set_trace()\n\
# ipython debugger (ipdb)\n\
snippet ipdb\n\
\timport ipdb; ipdb.set_trace()\n\
# ipython debugger (pdbbb)\n\
snippet pdbbb\n\
\timport pdbpp; pdbpp.set_trace()\n\
snippet pprint\n\
\timport pprint; pprint.pprint(${1})${2}\n\
snippet \"\n\
\t\"\"\"\n\
\t${1:doc}\n\
\t\"\"\"\n\
# test function/method\n\
snippet test\n\
\tdef test_${1:description}(${2:self}):\n\
\t\t${3:# TODO: write code...}\n\
# test case\n\
snippet testcase\n\
\tclass ${1:ExampleCase}(unittest.TestCase):\n\
\t\t\n\
\t\tdef test_${2:description}(self):\n\
\t\t\t${3:# TODO: write code...}\n\
snippet fut\n\
\tfrom __future__ import ${1}\n\
#getopt\n\
snippet getopt\n\
\ttry:\n\
\t\t# Short option syntax: \"hv:\"\n\
\t\t# Long option syntax: \"help\" or \"verbose=\"\n\
\t\topts, args = getopt.getopt(sys.argv[1:], \"${1:short_options}\", [${2:long_options}])\n\
\t\n\
\texcept getopt.GetoptError, err:\n\
\t\t# Print debug info\n\
\t\tprint str(err)\n\
\t\t${3:error_action}\n\
\n\
\tfor option, argument in opts:\n\
\t\tif option in (\"-h\", \"--help\"):\n\
\t\t\t${4}\n\
\t\telif option in (\"-v\", \"--verbose\"):\n\
\t\t\tverbose = argument\n\
";
exports.scope = "python";

});