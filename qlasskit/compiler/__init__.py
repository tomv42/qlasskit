# Copyright 2023 Davide Gessa

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# isort:skip_file

from typing import Literal, get_args

from .expqmap import ExpQMap  # noqa: F401
from .compiler import Compiler, CompilerException, optimizer  # noqa: F401

from .internalcompiler import InternalCompiler
from .poccompiler3 import POCCompiler3
from .tweedledumcompiler import TweedledumCompiler


SupportedCompiler = Literal["internal", "poc3", "tweedledum"]
SupportedCompilers = list(get_args(SupportedCompiler))


def to_quantum(name, args, returns, exprs, compiler: SupportedCompiler = "internal"):
    sel_compiler: Compiler

    if compiler == "internal":
        sel_compiler = InternalCompiler()
    elif compiler == "poc3":
        sel_compiler = POCCompiler3()
    elif compiler == "tweedledum":
        sel_compiler = TweedledumCompiler()
    else:
        raise Exception(
            f"Compiler {compiler} not supported. Choose one between {SupportedCompilers}"
        )

    circ = sel_compiler.compile(name, args, returns, exprs)
    return circ
