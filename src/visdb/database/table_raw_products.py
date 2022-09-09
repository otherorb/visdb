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

import argparse
import sys
import os
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Integer, String, Text, Column, Boolean, Float, Identity, DateTime
from sqlalchemy import select, table, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import validates
import datetime
import yaml
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import as_declarative, declared_attr

Base = orm.declarative_base()

class Raw_Product(Base):
    """ Note that SQLAlchemy will default the table name to the name of the 
    class. We want the class to provide a single instance (object) whereas
    the table is the full table of all of these objects. To that end, we
    use the plural for the table name and the singular for the class name.
    """
    __tablename__ = 'Raw_Products'

    """ It's not clear whether I should use CheckConstraint or a validator.
    Personally I feel a validation method or methods would be nicer, but 
    that doesn't seem to work when 'automagically' after the object is 
    constructed, which might mean the need for another pile of methods to
    check constratins whenever we need them. However, CheckConstraint is 
    not database agnostic, so if we decided to use some other database, then 
    we could end up with problematic columns if the CheckConstraint calls 
    aren't also updated."""
    #__table_args__ = (
            #CheckConstraint("file_creation_datetime > stop_time", 
            #    name="file creation younger than stop_time"),
            #CheckConstraint("stop_time > start_time", name="stop_time after start_time"),
            #CheckConstraint(instrument_name.in_(["NavCam Left","NavCam Right","AftCam Left", 
            #             "AftCam Right","HazCam Port Front","HazCam Port Back", 
            #             "HazCam Starboard Front","HazCam Starboard Back"]), 
            #             name="instrument name check"),
            #)

    id = Column(Integer, Identity(start=1), primary_key = True)
    raw_product_id = Column(String, nullable=False)
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

    """ Removing the validators from the class for now. Trying to decide if 
    they're the best way to go; maybe not. According to some, the database 
    should be doing the validating, not sqlAlchemy.
    
    @validates(raw_product_id,
                mission_lid,
                sc_lid,
                bad_pixel_table_id,
                exposure,
                compression_ratio,
                instrument_temperature,
                mission_phase,
                software_name,
                software_version,
                software_program_name,
                file_checksum,
                lines,
                samples,
                pathname,
                source_file_name,
                pixel_bits)
    def _is_valid(self, key, value):
        assert value != None
        assert value != ''
        print(value)
        return(value)
    
    @validates(NavLight_Left_On,
               NavLight_Right_On,
               HazLight_U_On,
               HazLight_V_On,
               HazLight_W_On,
               HazLight_X_On,
               HazLight_Y_On,
               HazLight_Z_On)
    def _is_valid_boolean(self, key, value):
        assert value != None
        assert isinstance(value, bool)
        return(value)
    
    @validates(instrument_name)
    def _is_valid_instrument_name(self, key, inst_name):
        assert inst_name != None
        assert inst_name != ''
        print(inst_name)
        assert inst_name in ["NavCam Left", "NavCam Right", "AftCam Left", 
                         "AftCam Right", "HazCam Port Front", "HazCam Port Back", 
                         "HazCam Starboard Front", "HazCam Starboard Back"]
        return(inst_name)

    #@validates('start_time')
    #def _is_valid_start_time(self, key, start_time):
    #    assert start_time != None
    #    assert isinstance(start_time, datetime.datetime)
    #    assert start_time > datetime.datetime(2022,1,1)
    #    return(start_time)
    
    @validates(start_time, stop_time)
    def _is_valid_start_stop_time(self, start_time, stop_time):
        assert stop_time != None
        assert start_time != None
        print("In validation step, ", start_time)
        print("Here start_time is a ", type(start_time))
        assert isinstance(start_time, datetime.datetime)
        assert isinstance(stop_time, datetime.datetime)
        assert stop_time > start_time
        return(start_time, stop_time)
    
    @validates(file_creation_datetime)
    def _is_valid_file_creation_datetime(self, key, file_creation_time, stop_time):
        assert file_creation_time != Null
        assert isinstance(file_creation_time, datetime.datetime)
        assert file_creation_time > stop_time
        return(file_creation_time)
    
    @validates(compression_type)
    def _is_valid_compression_type(self, key, compression_type):
        assert compression_type != None
        assert compression_type in ["Lossless", "ICER"]
        return(compression_type)
    """



    def emit_pds_label():
        """This should pull from Ross's code when it's been updated."""
        pass

    def product_id(self):
        """Use the pid.py module to add methods and classes to 
        this object.
        """
        sys.path.insert(1, os.path.join(sys.path[0],'../..'))
        from vipersci.pds import pid

        """ Try to create an observation id using the start_time (datetime object)
        and the instrument name"""
        start_date = self.start_time.date()
        start_hhmmss = self.start_time.time()
        inst_name = self.instrument_name.lower()

        self.raw_product_id = pid.VISID(start_date, start_hhmmss, 
                                inst_name, self.compression_type).__str__()
        print(self.raw_product_id)
        return(self.raw_product_id)

        """
        This is opied from the pid.py module imported above, mostly for 
        documentation purposes here.
        :ivar date: a six digit string denoting YYMMDD (or strftime %y%m%d) where
        the two digit year can be prefixed with "20" to get the four-digit year.
        :ivar time: a six or nine digit string denoting hhmmss (or strftime
        %H%M%S%f) or hhmmssuuu, similar to the first, but where the trailing
        three digits are miliseconds.
        :ivar instrument: A three character sequence denoting the instrument.
        """
        

    def __repr__(self):
        print(f"<VISDS Raw Product with raw_product_ID: {self.raw_product_id}>")
        return(f"<VISDS Raw Product with raw_product_ID: {self.raw_product_id}>")

