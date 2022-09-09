#!/usr/bin/env python
# coding: utf-8

""" Builds the Anaglyph_Product table object using the 
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
from sqlalchemy import Integer, String, Text, Column, Boolean, Float, Identity, DateTime
from sqlalchemy import select, table, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import validates
import datetime
import yaml
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import as_declarative, declared_attr

Base = orm.declarative_base()

class Anaglyph_Product(Base):
    __tablename__ = 'Anaglyph_Products'

    id = Column(Integer, Identity(start=1), primary_key = True)

    """We need two rows from the undistorted table. The left and right looks.
    This doesn't require a separate mapping table, I don't think."""
    
    left_undistored_table_id = Column(Integer, ForeignKey("Undistorted_Product.id"))
    right_undistored_table_id = Column(Integer, ForeignKey("Undistorted_Product.id"))

    """What other data are required to be stored in this table?
    * Obviously the left and right undistored (or is it rectified) images.
    * geometry information?
    * parallax angle?
    * vertical exaggeration?
    * control point information (left and right)?
    * image processing information (contrast stretch, noise reduction, etc?)
    * Others?

    """
    
    software_version = Column(String, nullable=False)

    def emit_pds_label():
        pass
