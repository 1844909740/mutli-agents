from sqlalchemy import Column, String, BigInteger, Integer, Float, func, and_, PrimaryKeyConstraint
from typing import List, Dict
from app.servics.mysql_service import LocalSession, MysqlBase


class TbLiveConnectionStatisticsSpeed(MysqlBase):
    __tablename__ = "live_connection_statistics_speed_5m"
    __table_args__ = (
        PrimaryKeyConstraint(
            'os',
            'app_version',
            'device_model',
            'device_firmware_version',
            'record_time_window'
        ),
        {'extend_existing': True}
    )

    os = Column(String)
    app_version = Column(String)
    device_model = Column(String)
    device_firmware_version = Column(String)
    connect_protocol = Column(Integer)
    env = Column(String)  # GrepTime数据库可以有多个主键，但是mysql只能拥有一个主键
    total_connect = Column(Integer)
    avg_connect_retry_times = Column(Float)
    avg_connect_step1_time = Column(Float)
    avg_connect_step2_time = Column(Float)
    avg_first_frame_time = Column(Float)
    record_time_window = Column(BigInteger)

    @classmethod
    def list_connectionn_statistics_speeds(
            cls,
            device_model: str = None,
            env: str = None,
            start_time: int = None,
            end_time: int = None,
            group_by: str = None
   ) -> List[Dict]:
        """
        聚合每日连接统计信息
        :param device_model:
        :param env:
        :param start_time:
        :param end_time:
        :param group_time:
        :return:

        SQL:
        SELECT
            date_format(record_time_window, '%Y-%m-%d') AS day,
            os,
            app_version,
            device_firmware_version,
            connect_protocol,
            SUM(total_connect) AS total_connect_sum,
            AVG(avg_connect_retry_time) AS avg_connect_retry_time,
            AVG(avg_first_frame_time) AS avg_first_frame_time,
            MAX(max_first_frame_time) AS max_first_frame_time
        FROM live_connection_statistics_speed_5m
        WHERE device_model = "GW_GC1" and record_time_window >= "2025-05-25 00:00:00"
            and record_time_window <= "2025-05-30 00:00:00"
        GROUP BY
            day,
            os,
            app_version,
            device_firmware_version,
            connect_protocol
        ORDER BY
            day,
            os,
            app_version,
            device_firmware_version.
            connect_protocol
        """
        env = "prod" if not env else env

        if not group_by or group_by not in ["app_version", "device_firmware_version"]:
            group_by = "app_version"

        with LocalSession() as session:
            day = func.date_format(cls.record_time_window, "%Y-%m-%d").label("day")
            query = session.query(
                day,
                cls.os,
                cls.app_version if group_by == "app_version" else cls.device_firmware_version,
                cls.connect_protocol,
                func.sum(cls.total_connect).label("total_connect_sum"),
                func.avg(cls.avg_first_frame_time).label("avg_first_frame_time")
            )

            filters = []
            if device_model is not None:
                filters.append(cls.device_model == device_model)
            if env:
                filters.append(cls.env == env)
            if start_time is not None:
                filters.append(cls.record_time_window >= start_time)
            if end_time is  not None:
                filters.append(cls.record_time_window <= end_time)

            if filters:
                query = query.filter(and_(*filters))

            query = query.group_by(
                day,
                cls.os,
                cls.app_version if group_by == "app_version" else cls.device_firmware_version,
                cls.connect_protocol
            ).order_by(
                day,
                cls.os,
                cls.app_version if group_by == "app_version" else cls.device_firmware_version,
                cls.connect_protocol
            )

            results = query.all()

            if group_by == "app_version":
                data = [{
                    "day": day,
                    "os": os,
                    "app_version": app_version,
                    "connect_protocol": connect_protocol,
                    "total_connect_sum": total_connect_sum,
                    "avg_first_frame_time": avg_first_frame_time
                } for
                    day,
                    os,
                    app_version,
                    connect_protocol,
                    total_connect_sum,
                    avg_first_frame_time
                    in results
                ]
            else:
                data = [{
                    "day": day,
                    "os": os,
                    "app_version": app_version,
                    "connect_protocol": connect_protocol,
                    "total_connect_sum": total_connect_sum,
                    "avg_first_frame_time": avg_first_frame_time
                } for
                    day,
                    os,
                    app_version,
                    connect_protocol,
                    total_connect_sum,
                    avg_first_frame_time
                    in results
                ]

            return data


