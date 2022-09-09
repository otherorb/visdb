#!/usr/bin/env python
# coding: utf-8

""" Builds the Panorama_Product table object using the 
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
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Text, Column, Boolean, Float
from sqlalchemy import select, table, create_engine, Identity, DateTime
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import validates
import datetime
import yaml
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import as_declarative, declared_attr

Base = orm.declarative_base()

class Panorama_Product(Base):
    __tablename__ = 'Panorama_Products'

    id = Column(Integer, Identity(start=1), primary_key = True)
    """We need a list of rows from the rectified table.
    I couldn't figure out how to do it here, so instead I created a mapping
    table that has one reference to this table and then a list of source 
    references to the Rectified_Products table.
    The name of the mapping table is: table_panorama_rectified_map.py
    """
    
    software_version = Column(String, nullable=False)

    """ What sorts of things do we need to track about for a panorama?
    Is there a point cloud that's used to generate the ties between images, or
    are we just doing this assuming pointing is correct? 

    * Scale
    * Radial distance from source camera(s)?
    * Time period of contributing data
    * Geographic information
        * Lat/lon extent
        * right ascenscion and declanation?
        * others?
    * Vertical height? 
    * Vertical angle subtended?
    * Horizontal angle subtended
    * Others?
    """

    def emit_pds_label():
        pass
