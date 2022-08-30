#!/usr/bin/env python
# coding: utf-8

""" Builds the Hazard_Rectified_Map table object using the 
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
from sqlalchemy import Integer, String, Text, Column, Boolean, Float, 
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

class Hazard_Rectified_Map(Base):
    __tablename__ = 'Hazard_Rectified_Maps'

    id = Column(Integer, Identity(start=1), primary_key = True)
    hazard_product_table_id = Column(Integer, ForeignKey("Hazard_Product.id"))

    """Note that the following column is not stored in the database as a python list
    object, but rather as a pickled MutableList object from sqlalchemy, so more 
    care probably needs to be taken when reading/writing this, but it's especially
    important to know that it's not necessarily accessible outside of sqlalchemy."""
    rectified_product_table_ids = Column(MutableList.as_mutable(PickleType), 
                                         default=[])
    
    software_version = Column(String, nullable=False)
