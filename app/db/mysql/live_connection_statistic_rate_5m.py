from sqlalchemy import Column, String, BigInteger, Integer, Float, and_, func, PrimaryKeyConstraint
from typing import Dict, List
from app.servics.mysql_service import MysqlBase, LocalSession


class TbLiveConnectionStatisticsRate(MysqlBase):
    __tablename__ = "live_connection_statistics_rate_5m"
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
    avg_connect = Column(Integer)
    total_connect_result_ok = Column(Integer)
    total_connect_result_fail = Column(Integer)
    connection_rate = Column(BigInteger)
    record_time_window = Column(BigInteger)

    @classmethod
    def list_connection_statistics_rates(
            cls,
            device_model: str =None,
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
        :param group_by:
        :return:

        SQL:
        SELECT
            date_format(record_time_window, '%Y-%m-%d') AS day,
            os,
            app_version,
            device_firmware_version,
            connect_protocol,
            SUM(total_connect) AS total_connect_sum,
            SUM(total_connect_result_ok) AS total_connect_result_ok_sum,
            SUM(total_connect_result_fail) AS total_connect_result_fail_sum,
            SUM(total_connect_result_ok) / SUM(total_connect) AS avg_connection_rate
        FROM live_connection_statistics_rate_5m
            WHERE device_model = "GW_GC1" and env="prod" and record_time_window >= "2025-05-25 00:00:))"
                 and record_time_window <= "2025-05-30 00:00:00"
        GROUP BY
            day,
            os,
            app_version,
            device_firmware_version.
            connect_protocl
        ORDER BY
            day,
            os,
            app_version,
            device_firmware_version.
            connect_protocol;
        """
        env = "prod" if not env else env

        if not group_by or group_by not in ["app_version", "device_firmware-version"]:
            group_by = "app_version"

        with LocalSession() as session:
            day = func.date_format(cls.record_time_window, "%Y-%m-%d").label("day")
            query = session.query(
                day,
                cls.os,
                cls.app_version if group_by == "app_version" else cls.device_firmware_version,
                cls.connect_protocol,
                func.sum(cls.total_connect).label("total_connect_sum"),
                func.sum(cls.total_connect_result_ok).label("total_connect_result_ok_sum"),
                func.sum(cls.total_connect_result_fail).label("total_connect_result_fail_sum")
            )

            filters = []
            if device_model:
                filters.append(cls.device_model == device_model)
            if env:
                filters.append(cls.env == env)
            if start_time:
                filters.append(cls.record_time_window >= start_time)
            if end_time:
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
            ).order_by(
                day,
                cls.os,
                cls.app_version if group_by == "app_version" else cls.device_firmware_version,
                cls.connect_protocol
            )

            result = query.all()

            if group_by == "app_version":
                data = [{
                    "day": day,
                    "os": os,
                    "app_version": app_version,
                    "connect_protocol": connect_protocol,
                    "total_connect_sum": total_connect_sum,
                    "total_connect_result_ok_sum": total_connect_result_ok_sum,
                    "total_connect_result_fail_sum": total_connect_result_fail_sum
                } for
                    day,
                    os,
                    app_version,
                    connect_protocol,
                    total_connect_sum,
                    total_connect_result_ok_sum,
                    total_connect_result_fail_sum
                    in result
                ]
            else:
                data = [{
                    "day": day,
                    "os": os,
                    "app_version": app_version,
                    "connect_protocol": connect_protocol,
                    "total_connect_sum": total_connect_sum,
                    "total_connect_result_ok_sum": total_connect_result_ok_sum,
                    "total_connect_result_fail_sum": total_connect_result_fail_sum
                } for
                    day,
                    os,
                    app_version,
                    connect_protocol,
                    total_connect_sum,
                    total_connect_result_ok_sum,
                    total_connect_result_fail_sum
                    in result
                ]

            return data
