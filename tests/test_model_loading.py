# Copyright 2021 DB Netz AG
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pathlib

import pytest

import capellambse


@pytest.fixture
def aird_model():
    return capellambse.MelodyModel(
        pathlib.Path(__file__).parent
        / "data"
        / "melodymodel"
        / "5_0"
        / "MelodyModelTest.aird"
    )


def test_loading_aird_model(aird_model):
    assert list(aird_model.la.all_functions.by_owner)