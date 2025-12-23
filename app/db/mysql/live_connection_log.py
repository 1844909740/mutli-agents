from sqlalchemy import BigInteger, Column, String, Integer, Float, and_, desc
from typing import Dict, List
from app.servics.mysql_service import LocalSession, MysqlBase, model_to_dict


class TbLiveConnectionLog(MysqlBase):
    __tablename__ = "live_connection_log"

    os = Column(String)
    app_version = Column(String)
    iot_online = Column(Integer)
    first_frame_time = Column(Float)
    device_model = Column(String, primary_key=True)
    device_mac = Column(String)
    device_firmware_version = Column(String)
    env = Column(String)
    connect_result = Column(Integer)
    connect_error = Column(String)
    connect_protocol = Column(Integer)
    record_time = Column(BigInteger, primary_key=True)

    @classmethod
    def list_live_connection_log(
            cls,
            device_model: str = None,
            device_id: str = None,
            env: str = None,
            start_time: int = None,
            end_time: int = None
    ) -> List[Dict]:
        """
        :param device_model:
        :param device_id:
        :param env:
        :param start_time:
        :param end_time:
        :return:
        """
        env = "prod" if not env else env

        with LocalSession() as session:
            query = session.query(TbLiveConnectionLog)

            filters = []
            if device_model:
                filters.append(cls.device_model == device_model)
            if device_id:
                filters.append(cls.device_mac == device_id)
            if env:
                filters.append(cls.env == env)
            if start_time:
                filters.append(cls.record_time >= start_time)
            if end_time:
                filters.append(cls.record_time <= end_time)

            filters.append(cls.iot_online != 0)

            filters.append(cls.connect_result != -1)

            if filters:
                query = query.filter(and_(*filters))

            # 降序
            query = query.order_by(desc(cls.record_time))

            return [model_to_dict(item) for item in query.all()]
















