# coding: utf-8

""" Builds the terrain_model_products table object using the 
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

import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Integer, String, Text, Column, Boolean, Float, 
from sqlalchemy import Identity, DateTime
from sqlalchemy import select, table, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import validates
import datetime
from sqlalchemy.ext.declarative import as_declarative, declared_attr

Base = orm.declarative_base()

class Terrain_Model_Product(Base):
    __tablename__ = 'Terrain_Model_Products'

    id = Column(Integer, Identity(start=1), primary_key = True)
    """We need a mapping from the source stereo pairs to this product.
    That's in the table_terrain_rectified_map.py file."""

    """What sorts of things do we need to track about the terrain model?
    * Time Period of contributing data?
    * Geographic information?
    * Vertical Accuracy?
    * Positional Accuracy?
    * Resolution or scale (lat, lon, height)
    * Coordinate System definition
    * Other FGDC metadata requirements?
    """

    software_version = Column(String, nullable=False)

    def emit_pds_label():
        pass
