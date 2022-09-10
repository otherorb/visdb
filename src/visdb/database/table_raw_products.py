#!/usr/bin/env python
# coding: utf-8

""" Builds the Raw_Product table using the sqlAlchemy ORM as much as possible."""

# Copyright 2022, United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import sys
import os
from sqlalchemy import orm
from sqlalchemy import Integer, String, Text, Column, Boolean, Float, Identity, DateTime
from sqlalchemy.ext.hybrid import hybrid_property

sys.path.insert(1, os.path.join(sys.path[0], '../..'))
from vipersci.pds.pid import VISID, vis_instruments, vis_compression


Base = orm.declarative_base()


class Raw_Product(Base):
    """ Note that SQLAlchemy will default the table name to the name of the
    class. We want the class to provide a single instance (object) whereas
    the table is the full table of all of these objects. To that end, we
    use the plural for the table name and the singular for the class name.
    """
    __tablename__ = 'Raw_Products'

    id = Column(Integer, Identity(start=1), primary_key=True)
    _pid = Column("product_id", String, nullable=False)
    instrument_name = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    stop_time = Column(DateTime, nullable=False)
    observation_lid = Column(String, nullable=False)
    mission_lid = Column(String, nullable=False)
    sc_lid = Column(String, nullable=False)
    bad_pixel_table_id = Column(Integer, nullable=False)
    exposure_time = Column(Integer, nullable=False)
    exposure_type = Column(String, nullable=False)
    NavLight_Left_On = Column(Boolean, nullable=False)
    NavLight_Right_On = Column(Boolean, nullable=False)
    HazLight_U_On = Column(Boolean, nullable=False)
    HazLight_V_On = Column(Boolean, nullable=False)
    HazLight_W_On = Column(Boolean, nullable=False)
    HazLight_X_On = Column(Boolean, nullable=False)
    HazLight_Y_On = Column(Boolean, nullable=False)
    HazLight_Z_On = Column(Boolean, nullable=False)
    purpose = Column(String, nullable=False)
    compression_type = Column(String, nullable=False)
    compression_ratio = Column(Float, nullable=False)
    instrument_temperature = Column(Float, nullable=False)
    purpose = Column(String, nullable=False)
    mission_phase = Column(String, nullable=False)
    software_name = Column(String, nullable=False)
    software_version = Column(String, nullable=False)
    software_type = Column(String, nullable=False)
    software_program_name = Column(String, nullable=False)
    file_creation_datetime = Column(DateTime, nullable=False)
    file_checksum = Column(String, nullable=False)
    lines = Column(Integer, nullable=False)
    samples = Column(Integer, nullable=False)
    pathname = Column(String, nullable=False)
    source_file_name = Column(String, nullable=False)
    pixel_bits = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        print("in init")
        if "product_id" in kwargs:
            pid = VISID(kwargs["product_id"])

            if "start_time" in kwargs and pid.datetime() != kwargs["start_time"]:
                raise ValueError(
                    f"The product_id datetime ({pid.datetime()}) and the "
                    f"provided start_time ({kwargs['start_time']}) disagree."
                )

            if (
                "instrument_name" in kwargs and not (
                    vis_instruments[pid.instrument] == kwargs["instrument_name"] or
                    pid.instrument == kwargs["instrument_name"]
                )
            ):
                raise ValueError(
                    f"The product_id instrument code ({pid.instrument}) and "
                    f"the provided instrument_name "
                    f"({kwargs['instrument_name']}) disagree."
                )

            if (
                "compression_ratio" in kwargs and not (
                    vis_compression[pid.compression] == kwargs["compression_ratio"] or
                    pid.compression == kwargs["compression_ratio"]
                )
            ):
                raise ValueError(
                    f"The product_id compression code ({pid.compression}) and "
                    f"the provided compression_ratio "
                    f"({kwargs['compression_ratio']}) disagree."
                )

            # Need another one of these if-statements for compression_type, but
            # need to modify pid.py first.

            # Final cleanup so that super() works later.
            del kwargs["product_id"]
        elif (
            kwargs.keys() >= {
                "start_time", "instrument_name", "compression_ratio"
            }
        ):
            pid = VISID(
                kwargs["start_time"].date(),
                kwargs["start_time"].time(),
                # Need to update pid.py to take long-form of these two params.
                kwargs["instrument_name"],
                kwargs["compression_ratio"]
            )
        else:
            raise ValueError(
                "Either product_id must be given, or each of start_time, "
                "instrument_name, and compression_ratio."
            )

        super().__init__(**kwargs)
        self.product_id = pid

        return

    @hybrid_property
    def product_id(self):
        return VISID(self._pid)

    @product_id.setter
    def product_id(self, pid):
        vid = VISID(pid)
        self._pid = str(vid)
        self.start_time = vid.datetime()
        self.instrument_name = vis_instruments[vid.instrument]
        self.compression_ratio = vis_compression[vid.compression]

    def emit_pds_label():
        """This should pull from Ross's code when it's been updated."""
        # As discussed, this functionality belongs elsewhere, remove.
        pass

    def __repr__(self):
        # This is not what a __repr__() should do.  Let's remove for now.
        print(f"<VISDS Raw Product with raw_product_ID: {self.raw_product_id}>")
        return(f"<VISDS Raw Product with raw_product_ID: {self.raw_product_id}>")
