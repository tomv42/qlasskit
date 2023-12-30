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

import unittest
from typing import Dict

from parameterized import parameterized, parameterized_class
from sympy import Symbol
from sympy.logic.boolalg import Boolean

from qlasskit import qlassf
from qlasskit.ast2logic.typing import BoolExpList
from qlasskit.boolopt.bool_optimizer import custom_simplify_logic
from qlasskit.decompiler import Decompiler

from .utils import ENABLED_COMPILERS, compute_and_compare_results


def _merge_expressions(
    exps: BoolExpList, emap: Dict[Symbol, Boolean] = {}
) -> BoolExpList:
    n_exps = []

    for s, e in exps:
        e = e.xreplace(emap)
        e = custom_simplify_logic(e)

        if s.name[0:4] != "_ret":
            emap[s] = e
        else:
            n_exps.append((s, e))

    return n_exps


@parameterized_class(("compiler"), ENABLED_COMPILERS)
class TestDecompiler(unittest.TestCase):
    @parameterized.expand(
        [
            ("def test(a: bool) -> bool:\n\treturn not a"),
            ("def test(a: bool) -> bool:\n\treturn True if a else False"),
            ("def test(a: bool, b: bool) -> bool:\n\tc = a and b\n\treturn c"),
            ("def test(a: bool, b: bool) -> bool:\n\treturn a | b"),
        ]
    )
    def test_exact_decompilation(self, f):
        qf = qlassf(f, to_compile=True)  # , compiler=self.compiler)

        dc = Decompiler().decompile(qf.circuit())

        self.assertEqual(len(dc), 1)
        self.assertEqual(len(dc[0].expressions), len(qf.expressions))

        # Set False values for initialization
        _rets = {}
        for s in qf.returns.bitvec:
            _rets[Symbol(s)] = False
        for s in ["anc_0", "anc_1"]:
            _rets[Symbol(s)] = False

        dc0_exps = _merge_expressions(dc[0].expressions, _rets)

        for orig, decomp in zip(qf.expressions, dc0_exps):
            self.assertEqual(orig, decomp)
