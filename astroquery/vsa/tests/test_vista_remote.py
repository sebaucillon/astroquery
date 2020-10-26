# Licensed under a 3-clause BSD style license - see LICENSE.rst


import pytest

from astropy.table import Table
from astropy.coordinates import SkyCoord
import astropy.units as units

from ... import vsa


vista = vsa.core.VsaClass()


@pytest.mark.remote_data
class TestVista:

    @pytest.mark.dependency(name='vsa_up')
    def test_is_vsa_up(self):
        try:
            vista._request("GET", "http://horus.roe.ac.uk:8080/vdfs/VgetImage_form.jsp")
        except Exception as ex:
            pytest.xfail("VISTA appears to be down.  Exception was: {0}".format(ex))

    @pytest.mark.dependency(depends=["vsa_up"])
    def test_get_images(self):

        crd = SkyCoord(l=336.489, b=-1.48, unit=(units.deg, units.deg), frame='galactic')
        images = vista.get_images(crd, frame_type='tilestack',
                                  image_width=5 * units.arcmin, waveband='H')
        assert images is not None

    @pytest.mark.dependency(depends=["vsa_up"])
    def test_get_images_async(self):
        crd = SkyCoord(l=336.489, b=-1.48, unit=(units.deg, units.deg), frame='galactic')
        images = vista.get_images_async(crd, frame_type='tilestack',
                                        image_width=5 * units.arcmin, waveband='H')
        assert images is not None

    @pytest.mark.dependency(depends=["vsa_up"])
    def test_get_image_list(self):
        crd = SkyCoord(l=350.488, b=0.949, unit=(units.deg, units.deg), frame='galactic')
        urls = vista.get_image_list(crd, frame_type='all', waveband='all')
        assert len(urls) > 0

    @pytest.mark.dependency(depends=["vsa_up"])
    def test_query_region_async(self):
        crd = SkyCoord(l=350.488, b=0.949, unit=(units.deg, units.deg), frame='galactic')
        response = vista.query_region_async(crd, radius=6 * units.arcsec, programme_id='VVV')
        assert response is not None

    @pytest.mark.dependency(depends=["vsa_up"])
    def test_query_region(self):
        crd = SkyCoord(l=350.488, b=0.949, unit=(units.deg, units.deg), frame='galactic')
        table = vista.query_region(crd, radius=6 * units.arcsec, programme_id='VVV')
        assert isinstance(table, Table)
        assert len(table) > 0

    @pytest.mark.dependency(depends=["vsa_up"])
    def test_query_region_constraints(self):
        crd = SkyCoord(l=350.488, b=0.949, unit=(units.deg, units.deg), frame='galactic')
        rad = 6 * units.arcsec
        constraints = '(priOrSec<=0 OR priOrSec=frameSetID)'
        table_noconstraint = vista.query_region(crd, radius=rad, programme_id='VVV')
        table_constraint = vista.query_region(crd, radius=rad, programme_id='VVV',
                                              constraints=constraints)
        assert isinstance(table_constraint, Table)
        assert len(table_noconstraint) >= len(table_constraint)
