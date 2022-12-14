# Copyright 2014 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""This module detects whether third-party libraries, utilized by third-party
drivers, are present on the system. If they are not, it mocks them and tinkers
with sys.modules so that the drivers can be loaded by unit tests, and the unit
tests can continue to test the functionality of those drivers without the
respective external libraries' actually being present.

Any external library required by a third-party driver should be mocked here.
Current list of mocked libraries:

- iboot
"""

import importlib
import sys
from unittest import mock

from oslo_utils import importutils

from ironic_staging_drivers.tests.unit import third_party_driver_mock_specs \
    as mock_specs


# attempt to load the external 'iboot' library, which is required by
# the optional drivers.modules.iboot module
iboot = importutils.try_import('iboot')
if not iboot:
    ib = mock.MagicMock(spec_set=mock_specs.IBOOT_SPEC)
    ib.iBootInterface = mock.MagicMock(spec_set=[])
    sys.modules['iboot'] = ib

# if anything has loaded the iboot driver yet, reload it now that the
# external library has been mocked
if 'ironic_staging_drivers.iboot.power' in sys.modules:
    importlib.reload(sys.modules['ironic_staging_drivers.iboot.power'])

# attempt to load the external 'libvirt' library, which is required by
# the optional drivers.modules.libvirt module
libvirt = importutils.try_import('libvirt')
if not libvirt:
    lv = mock.MagicMock(spec_set=mock_specs.LIBVIRT_SPEC)
    lv.libvirtError = Exception
    sys.modules['libvirt'] = lv

# if anything has loaded the libvirt driver yet, reload it now that the
# external library has been mocked
if 'ironic_staging_drivers.libvirt.power' in sys.modules:
    importlib.reload(sys.modules['ironic_staging_drivers.libvirt.power'])

# attempt to load the external 'ovirtsdk4' library, which is required by
# the optional drivers.modules.ovirt module
ovirtsdk4 = importutils.try_import('ovirtsdk4')
if not ovirtsdk4:
    ov = mock.MagicMock(spec_set=mock_specs.OVIRT4_SPEC)
    sys.modules['ovirtsdk4'] = ov
    sys.modules['ovirtsdk4.types'] = ov.types
