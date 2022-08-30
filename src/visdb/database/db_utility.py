"""
Various vipersci database utilities.
"""


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
from datetime import datetime, date
import hashlib
from importlib import resources
import logging
from pathlib import Path
import yaml
from sqlalchemy import create_engine, MetaData, select
from sqlalchemy import orm, schema, inspect

import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'../..'))
from vipersci.pds import pid as pds
from vipersci import util

logger = logging.getLogger(__name__)


"""Add arguments here for the utility program."""
def arg_parser():
    parser = argparse.ArgumentParser(
            description=__doc__,
            parents=[util.parent_parser()]
    )
    parser.add_argument(
            "-d", "--drop",
            type=str,
            help="Table name to drop. Or 'All' to drop all tables."
    )
    parser.add_argument(
            "-c", "--config",
            type=Path,
            help="Path to database configuration file."
    )
    parser.add_argument(
            "-l", "--list",
            action='store_true',
            help="List tables in database."
    )
    parser.add_argument(
            "-q", "--query",
            action='store_true',
            help='run special query.'
    )
    return parser

def get_engine(url):
    engine = create_engine(url, echo=True)
    return(engine)

""" Read database configuration file."""
def read_db_settings(fname):
    with open(fname, 'r') as f:
        conf_text = f.read()
        
    db = yaml.load(conf_text, Loader=yaml.FullLoader)
    print(db)

    db_host = db['db_host']
    db_host = db['db_host']
    db_port = db['db_port']
    db_name = db['db_name']
    db_user = db['db_user']
    db_pass = db['db_pass']
    db_type = db['db_type']
    url = f'{db_type}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

    engine = get_engine(url)
    Base = orm.declarative_base()
    Base.metadata.create_all(engine)
    return(Base, engine, db)

""" Drop database tables."""
def drop_db_table(table_name, engine, Base):
    metadata = MetaData(engine)
    print(table_name)
    table_to_drop = metadata.tables.get(table_name)
    print(table_to_drop)
    if table_to_drop is not None:
        if table_name == "all":
            logging.info('Deleting all tables')
            Base.metadata.drop_all(engine)
        else: 
            try:
                Base.metadata.drop_all(engine, [table_to_drop], checkfirst=True)
                logging.info(f'Attempting to delete {table_to_drop} table')
                print("*****************************************")
                print(f"DELETED table {table_to_drop}!!!!")
                print("*****************************************")
            except Exception as e:
                logging.error(e)
    tables = list_db_tables(Base, engine)
    print("*****************************************")
    print(f"These tables still exist: {tables}!!!!")
    print(type(tables))
    print("*****************************************")

def list_db_tables(Base, engine):
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    return(table_names)

"""This is not a generic query function, it's just for testing."""
def query(Base, engine):
    from sqlalchemy.orm import sessionmaker
    import table_raw_products as tb
    Session = sessionmaker(bind=engine)
    with orm.Session(engine, future=True) as session:
        session.begin()
        try:
            for instance in session.query(tb.Raw_Product).order_by(tb.Raw_Product.id):
                print(instance.id, instance.mission_lid, instance.instrument_name)
        except:
            raise



if __name__ == "__main__":
    args = arg_parser().parse_args()
    util.set_logger(args.verbose)

    print(args)

    db_config = args.config

    Base, engine, db = read_db_settings(db_config)

    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    print("*****************************************")
    print("*****************************************")
    print("*****************************************")
    print(table_names)
    print("*****************************************")
    print("*****************************************")
    print("*****************************************")

    if args.list:
        db_tables = list_db_tables(Base, engine)
        print(db_tables)

    if args.drop:
        print("*****************************************")
        print("*****************************************")
        print(f"Dropping table, {args.drop}!!!")
        drop_db_table(args.drop, engine, Base)

    if args.query:
        query(Base, engine)

