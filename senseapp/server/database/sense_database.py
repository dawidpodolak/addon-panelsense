from typing import Set

from loging.logger import _LOGGER
from server.client.sense_client import SenseClient, create_sense_client
from server.database.tables import *
from sqlalchemy import create_engine, exists, select
from sqlalchemy.orm import sessionmaker


class SenseDatabase:
    engine = create_engine("sqlite:///sense_database.db", echo=True)
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
        _LOGGER.debug(f"database result: {result}")

        if result == False:
            _LOGGER.debug("Add sense client")
            sense_client_database = SenseClientDatabase(
                installation_id=sense_client.details.installation_id,
                name=sense_client.details.name,
                version_name=sense_client.details.version_name,
                version_code=sense_client.details.version_code,
                configuration=sense_client.configuration_str,
            )
            self.session.add(sense_client_database)

            try:
                self.session.commit()
            except Exception as e:
                _LOGGER.error(e)
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
        _LOGGER.debug(f"update sense client result: {sense_client_database}")

        try:
            self.session.commit()
        except Exception as e:
            _LOGGER.error(e)
            self.session.rollback()

    def get_sense_clients(self) -> Set[SenseClient]:
        statement = select(SenseClientDatabase)
        # results = self.session.execute(statement)
        sense_client_set = set()

        for result in self.session.scalars(statement):
            _LOGGER.info(f"Result ---> {result.name}")
            sense_client_set.add(
                create_sense_client(
                    name=result.name,
                    installation_id=result.installation_id,
                    version_code=result.version_code,
                    version_name=result.version_name,
                    configuration=result.configuration,
                )
            )
        return sense_client_set
