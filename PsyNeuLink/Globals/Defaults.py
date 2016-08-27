# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
#
#
# ********************************************  System Defaults ********************************************************
#

from enum import Enum

from PsyNeuLink.Globals.TimeScale import TimeScale

MPI_IMPLEMENTATION = False

# State values:
inputValueSystemDefault = [0]
outputValueSystemDefault = [0]

# TimeScale:
timeScaleSystemDefault = TimeScale.TRIAL

# Default input:
SystemDefaultInputValue = 0.0

# Default control allocation mode values:
class DefaultControlAllocationMode(Enum):
    GUMBY_MODE = 0.0
    BADGER_MODE = 1.0
    TEST_MODE = 240
defaultControlAllocation = DefaultControlAllocationMode.BADGER_MODE.value
