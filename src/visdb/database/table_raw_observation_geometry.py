#!/usr/bin/env python
# coding: utf-8

""" Builds the Observation_Geometry table object using the 
sqlAlchemy ORM as much as possible."""

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
import sqlalchemy as sql
from sqlalchemy.sql import func
from sqlalchemy import orm
from sqlalchemy import Integer, String, Text, Column, Boolean, Float
from sqlalchemy import Identity, DateTime, PickleType
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import select, table, create_engine 
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import validates
import datetime
import yaml
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import as_declarative, declared_attr

Base = orm.declarative_base()

class Observation_Geometry(Base):
    __tablename__ = 'Observation_Geometries'

    id = Column(Integer, Identity(start=1), primary_key = True)
    raw_product_table_id = Column(Integer, ForeignKey("Raw_Product.id"))
    software_version = Column(String, nullable=False)
    emission_angle = Column(Float, nullable=False)
    incidence_angle = Column(Float, nullable=False)
    phase_angle = Column(Float, nullable=False)
    image_center_latitude = Column(Float, nullable=False)
    image_center_longitude = Column(Float, nullable=False)
    north_azimuth = Column(Float, nullable=False)
    sub_solar_azimuth = Column(Float, nullable=False)
    sub_solar_latitude = Column(Float, nullable=False)
    sub_solar_longitude = Column(Float, nullable=False)
    solar_distance = Column(Float, nullable=False)
    solar_longitude = Column(Float, nullable=False)
    local_time = Column(DateTime, nullable=False)

    """
    What other geometries are valid?
    For this table, it's a map to the Raw_Products table, so it should not include
    mosaic geometries.
    However, the geometry of the front cameras might require more or fewer parameters
    compared with the geometry for the HazCams or AftCams. What are those differences? 
    Is there some sort of declination or elevation angle for the navcams?
    Is there some any chance we'll be looking high enough to see the horizon? 
        Do we have to keep track of that kind of information here?
    """

    """
    When using SQL functions with the func construct, we “call” the named function, 
    e.g. with parenthesis as in func.now(). This differs from when we specify a 
    Python callable as a default such as datetime.datetime, where we pass the 
    function itself, but we don’t invoke it ourselves. In the case of a SQL 
    function, invoking func.now() returns the SQL expression object that will 
    render the “NOW” function into the SQL being emitted."""
    last_update = Column(DateTime, onupdate=func.utc_timestamp(), nullable=False)

