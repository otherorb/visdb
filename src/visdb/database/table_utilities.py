# coding: utf-8

import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import validates
import datetime
import yaml
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import MetaData
from table_raw_products import *

def get_engine(url):
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, echo=True)
    return(engine)

if __name__ == "__main__":

    """ Need to be able to read from: database, yamcs, and PDS label (xml)
        Read database configuration from 'local_settings.yml'
        Build the database URL using these settings. 
    """

    with open('local_db_settings.yml') as settings_f:
        db = yaml.load(settings_f, Loader=yaml.FullLoader)

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

    """ Set up some simple checks for now...
    These will be deleted when this code goes live.
    """
    
    start_time = datetime.datetime.now()
    stop_time = start_time + datetime.timedelta(minutes=10)
    file_creation_datetime = stop_time + datetime.timedelta(minutes=10)

    """Create a test table."""
    test_raw = Raw_Product(
        raw_product_id = 'def', 
        instrument_name = 'NavCam R', 
        start_time = start_time,
        stop_time = stop_time,
        mission_lid = "mission_lid",
        sc_lid = "sc_lid",
        bad_pixel_table_id = 7,
        exposure_time = 5,
        exposure_type = "Manual",
        NavLight_Left_On = False,
        NavLight_Right_On = False,
        HazLight_U_On = False,
        HazLight_V_On = False,
        HazLight_W_On = False,
        HazLight_X_On = False,
        HazLight_Y_On = False,
        HazLight_Z_On = False,
        compression_type = "Lossless",
        compression_ratio = 2.1,
        instrument_temperature = 27.2,
        mission_phase = "PSP",
        software_name = "visds",
        software_type = "python",
        software_version = "0.01",
        software_program_name = "python",
        file_creation_datetime = file_creation_datetime,
        file_checksum = "sum checked",
        lines = 1024,
        samples = 1024,
        pathname = "/path/to/file",
        source_file_name = "source_file.img",
        pixel_bits = 8)

    """ Build the session to connect to the database."""
    with orm.Session(engine) as session:
        session.begin()
        Raw_Product.__table__.create(bind=engine, checkfirst=True)
        try:
            print("Adding row...\n")
            session.add(test_raw)
            print("Added row...\n")
            session.commit()
            session.flush()
            print("Committed...\n")
        except:
            session.rollback()
            raise
    print("***********Committed the row.***********")

    """ Now, try to pull something from it."""
    with orm.Session(engine) as session:
        session.begin()
        try:
            statement = sql.select(Raw_Product).filter_by(instrument_name="NavCam R")
            results = session.execute(statement).scalars().all()
        except:
            raise
    print(results)

    print("id: ", results[0].id)
    print("mission phase: ", results[0].mission_phase)
    print("instrument name: ", results[0].instrument_name)

