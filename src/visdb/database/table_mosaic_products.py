#!/usr/bin/env python
# coding: utf-8

""" Builds the Mosaic_Product table object using the 
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
from sqlalchemy import Integer, String, Text, Column, Boolean, Float, Identity, DateTime
from sqlalchemy import select, table, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import validates
import datetime
import yaml
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import as_declarative, declared_attr

Base = orm.declarative_base()

class Mosaic_Product(Base):
    __tablename__ = 'Mosaic_Products'

    id = Column(Integer, Identity(start=1), primary_key = True)
    """We need a list of rows from the rectified table.
    I couldn't figure out how to do it here, so instead I created a mapping
    table that has one reference to this table and then a list of source 
    references to the Rectified_Products table.
    The name of the mapping table is: table_mosaic_rectified_map.py
    """

    """The next question is what are we tracking for the mosaic? 
    Source images? Of course, that's the mapping mentioned above. 
    What else? 
    Geometry? Probably.
    Control points used to tie the images together? Probably.
    Settings for the software blending, etc? Probably. 
    Is the horizon visible? Maybe?
    A lot of all the the above are not yet obvious, so this is just a stub for now.
    """
    
    software_version = Column(String, nullable=False)

    def emit_pds_label():
        pass
