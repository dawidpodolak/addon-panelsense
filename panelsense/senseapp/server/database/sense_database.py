import base64
import os
from typing import Set

from loguru import logger
from server.client.sense_client import SenseClient, create_sense_client
from server.database.tables import *
from sqlalchemy import create_engine, exists, select
from sqlalchemy.orm import sessionmaker


class SenseDatabase:
    databasePath = os.getenv("PANEL_SENSE_DATABASE")
    engine = create_engine(f"sqlite:///{databasePath}")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    def create_or_update_sense_client(self, sense_client: SenseClient):
        result = self.session.query(
            exists().where(
                SenseClientDatabase.installation_id
                == sense_client.details.installation_id
            )
        ).scalar()
        logger.debug(f"database result: {result}")

        if result == False:
            logger.debug("Add sense client")
            base64_config = base64.b64encode(
                sense_client.configuration_str.encode("utf-8")
            ).decode("utf-8")
            sense_client_database = SenseClientDatabase(
                installation_id=sense_client.details.installation_id,
                name=sense_client.details.name,
                version_name=sense_client.details.version_name,
                version_code=sense_client.details.version_code,
                configuration=base64_config,
            )
            self.session.add(sense_client_database)

            try:
                self.session.commit()
            except Exception as e:
                logger.error(e)
                self.session.rollback()
        else:
            self.update_sense_client(sense_client)

    def update_sense_client(self, sense_client: SenseClient):
        statement = select(SenseClientDatabase).where(
            SenseClientDatabase.installation_id.in_(
                [sense_client.details.installation_id]
            )
        )

        sense_client_database = self.session.execute(statement).scalar_one()
        sense_client_database.name = sense_client.details.name
        sense_client_database.version_code = sense_client.details.version_code
        sense_client_database.version_name = sense_client.details.version_name

        try:
            self.session.commit()
        except Exception as e:
            logger.error(e)
            self.session.rollback()

    def update_sense_client_configuration(
        self, installation_id: str, configuration: str
    ):
        statement = select(SenseClientDatabase).where(
            SenseClientDatabase.installation_id.in_([installation_id])
        )
        base64_config = base64.b64encode(configuration.encode("utf-8")).decode("utf-8")
        sense_client_database = self.session.execute(statement).scalar_one()
        sense_client_database.configuration = base64_config

        try:
            self.session.commit()
        except Exception as e:
            logger.error(e)
            self.session.rollback()

    def get_sense_clients(self) -> Set[SenseClient]:
        statement = select(SenseClientDatabase)
        sense_client_set = set()

        for result in self.session.scalars(statement):
            config_str = base64.b64decode(result.configuration.encode("utf-8")).decode(
                "utf-8"
            )
            sense_client_set.add(
                create_sense_client(
                    name=result.name,
                    installation_id=result.installation_id,
                    version_code=result.version_code,
                    version_name=result.version_name,
                    configuration=config_str,
                )
            )
        return sense_client_set
