import logging
import smtplib
import ssl
import certifi
import base64
import os
import json
import zipfile
from io import BytesIO
from strands import tool
from app.servics.get_date import get_current_date
from app.servics.get_device_model import get_device_model
from typing import Dict
from app.db.mysql.live_connection_statistic_rate_5m import TbLiveConnectionStatisticsRate
from app.db.mysql.live_connection_statistics_speed_5m import TbLiveConnectionStatisticsSpeed
from email.message import EmailMessage
from email.utils import formatdate
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# 配置本地存储设置
LOCAL_STORAGE_BASE_DIR = os.getenv("LOCAL_STORAGE_DIR", "")
_REPORT_DIR = os.path.join(LOCAL_STORAGE_BASE_DIR, "")

# 确保基础目录存在
os.makedirs(LOCAL_STORAGE_BASE_DIR, exist_ok=True)
os.makedirs(_REPORT_DIR, exist_ok=True)



# 工具定义



@tool
def get_and_upload_app_rates(date: str, device_model: str, env: str, start_time: int, end_time: int) -> str:
    """
    获取App版本连接率数据并写入本地文件
    """
    logging.info(f"app rates params: {device_model}, {env}, {start_time}, {end_time}")

    start_dt = datetime.fromtimestamp(start_time / 1e9)
    end_dt = datetime.fromtimestamp(end_time / 1e9)
    logging.info(f"时间范围: {start_dt} 到 {end_dt}")

    app_rates = TbLiveConnectionStatisticsRate.list_connection_statistics_rates(
        device_model=device_model,
        env=env,
        start_time=start_time,
        end_time=end_time,
        group_by="app_version"
    )

    file_key = f"/{date}/{device_model}/device_connection_app_rates.json"
    write_local_file(
        file_key=file_key,
        file_content=json.dumps(app_rates)
    )
    return f"成功获取App版本连接率数据并写入本地文件: {file_key}, data: {app_rates}"


@tool
def get_and_upload_firmware_rates(date: str, device_model: str, env: str, start_time: int, end_time: int) -> str:
    """
    获取firmware版本连接率数据并写入本地文件
    """
    logging.info(f"firmware rates params: {device_model}, {env}, {start_time}, {end_time}")


    start_dt = datetime.fromtimestamp(start_time / 1e9)
    end_dt = datetime.fromtimestamp(end_time / 1e9)
    logging.info(f"时间范围: {start_dt} 到 {end_dt}")

    firmware_rates = TbLiveConnectionStatisticsRate.list_connection_statistics_rates(
        device_model=device_model,
        env=env,
        start_time=start_time,
        end_time=end_time,
        group_by="device_firmware_version"
    )

    file_key = f"/{date}/{device_model}/device_connection_firmware_rates.json"
    write_local_file(
        file_key=file_key,
        file_content=json.dumps(firmware_rates)
    )
    return f"成功获取firmware版本连接率数据并写入本地文件: {file_key}, data: {firmware_rates}"


@tool
def get_and_upload_app_speeds(date: str, device_model: str, env: str, start_time: int, end_time: int) -> str:
    """
    获取App版本连接速度数据并写入本地文件
    """
    logging.info(f"app speeds params: {device_model}, {env}, {start_time}, {end_time}")

    start_dt = datetime.fromtimestamp(start_time / 1e9)
    end_dt = datetime.fromtimestamp(end_time / 1e9)
    logging.info(f"时间范围: {start_dt} 到 {end_dt}")

    app_speed = TbLiveConnectionStatisticsSpeed.list_connectionn_statistics_speeds(
        device_model=device_model,
        env=env,
        start_time=start_time,
        end_time=end_time,
        group_by="app_version"
    )

    file_key = f"/{date}/{device_model}/device_connection_app_speeds.json"
    write_local_file(
        file_key=file_key,
        file_content=json.dumps(app_speed)
    )
    return f"成功获取App版本连接速度数据并写入本地文件: {file_key}, data: {app_speed}"


@tool
def get_and_upload_firmware_speeds(date: str, device_model: str, env: str, start_time: int, end_time: int) -> str:
    """
    获取firmware版本连接速度数据并写入本地文件
    """
    logging.info(f"firmware speeds params: {device_model}, {env}, {start_time}, {end_time}")

    start_dt = datetime.fromtimestamp(start_time / 1e9)
    end_dt = datetime.fromtimestamp(end_time / 1e9)
    logging.info(f"时间范围: {start_dt} 到 {end_dt}")

    firmware_speed = TbLiveConnectionStatisticsSpeed.list_connectionn_statistics_speeds(
        device_model=device_model,
        env=env,
        start_time=start_time,
        end_time=end_time,
        group_by="device_firmware_version"
    )

    file_key = f"/{date}/{device_model}/device_connection_firmware_speeds.json"
    write_local_file(
        file_key=file_key,
        file_content=json.dumps(firmware_speed)
    )
    return f"成功获取firmware版本连接速度数据并写入本地文件: {file_key}, data: {firmware_speed}"



@tool
def write_local_file(file_key: str, file_content: str) -> str:
    f"""
    将指定内容写入到本地文件中，适用于存储分析结果，日志或其他文本数据，提供file_content时请注意多文本进行转义.

    参数:
    - file_key: 本地中的文件路径/键，如"data.txt" 
        - P2P JSON报告: file_key="/{get_current_date()}/{get_device_model()}/p2p_analysis_report.json"
        - 注意：file_key必须包含完整的设备型号路径，例如：/2025-09-14//p2p_analysis_report.json
        - 如果file_key不包含设备型号路径，函数将返回错误信息
    - file_content: 要写入的文件内容，可以是纯文本、JSON等格式

    返回:
    写入操作的结果信息, 包含成功写入的文件完整路径或错误信息

    示例调用:
    1. 写入P2P JSON报告: write_local_file(
                            file_key="/{get_current_date()}/{get_device_model()}/p2p_analysis_report.json",
                            file_content=""
                        )

    """
    if not file_key:
        error_msg = "错误：文件路径为空，请提供有效的file_key参数"
        logging.error(error_msg)
        return error_msg

    if not file_content:
        error_msg = "错误：file_content参数为空无法写入，请检查file_content参数是否正确"
        logging.error(error_msg)
        return error_msg

    # 验证内容不是空JSON，但允许写入空JSON以创建文件
    if file_content.strip() in ['{}', '[]', '""', "''"]:
        print(f"警告：写入空内容到 {file_key}，内容为: {file_content}")
        # 继续执行，允许写入空内容

    try:
        file_key = process_file_key(file_key)

        print(f"写入文件: {file_key}")
        print(f"内容长度: {len(file_content)} 字符")
        print(f"内容类型: {type(file_content)}")
        print(f"内容预览: {file_content[:200]}...")

        with open(file_key, 'w', encoding='utf-8') as f:
            f.write(file_content)

        # 验证写入结果
        written_size = os.path.getsize(file_key)

        if written_size != len(file_content.encode('utf-8')):
            return f"警告：写入大小不匹配，期望: {len(file_content.encode('utf-8'))}, 实际: {written_size}"

        return f"已成功写入内容到本地文件: {file_key} (内容长度: {len(file_content)}字符, 文件大小: {written_size}字节)"

    except Exception as e:
        error_message = f"写入本地文件错误: {str(e)}"
        logging.error(error_message)
        return error_message


@tool
def write_local_file_html(file_key: str, file_content: str) -> str:
    f"""
    将HTML内容写入本地文件的以下两个路径下:
    /{get_current_date()}/{get_device_model()}/p2p_analysis_report.html
    /{get_current_date()}/{get_device_model()}.html
    /{get_current_date()}/summary.html
    并自动设置正确的Content-Type和Content-Disposition.
    确保文件写入到正确的路径


    参数:
    - file_key: 本地中的文件路径/键
    如"/{get_current_date()}/{get_device_model()}/p2p_analysis_report.html"
    如"/{get_current_date()}/{get_device_model()}.html"
    如"/{get_current_date()}/summary.html"
    - file_content: 要写入的HTML内容
    - content_type: 内容类型, 默认为"text/html", 也可以是"text/html; charset=utf-8"等

    返回:
    写入操作的结果信息, 包哈成功写入的文件完整路径或错误信息.

    特点:
    1. 自动添加.html扩展名(如果没有)
    2. 设置正确的Content-Type
    3. 设置inline Content-Disposition以便浏览器直接显示
    4. 自动添加日期前缀(如果没有)

    示例调用:
    1. 写入到P2P HTML文档: write_local_file(
                            file_key="/{get_current_date()}/{get_device_model()}/p2p_analysis_report.html"
                            file_content=""
                         ),
                        write_local_file(
                            file_key="/{get_current_date()}/{get_device_model()}.html"
                            file_content=""
                         ),
                         write_local_file(
                            file_key="/{get_current_date()}/summary.html"
                            file_content=""
                         ),


    """
    # 参数验证
    if not file_key:
        return "错误：文件路径为空，请提供有效的file_key参数"

    if not file_content:
        return "错误：file_content参数为空无法写入，请检查file_content参数是否正确"

    try:
        file_key = process_file_key(file_key)
        ensure_directory_exists(file_key)

        # 确保文件扩展名为.html
        if not file_key.endswith('.html'):
            file_key += '.html'

        # 写入HTML内容
        with open(file_key, 'w', encoding='utf-8') as f:
            f.write(file_content)

        return f"已成功写入HTML内容到本地文件: {file_key} (内容长度: {len(file_content)}字符)"

    except Exception as e:
        error_message = f"写入本地HTML文件错误: {str(e)}"
        logging.error(error_message)
        return error_message


@tool
def get_local_file_metadata(file_key: str) -> str:
    """
    获取本地文件的元数据信息, 包括文件大小, 最后修改时间等.

    参数:
    - file_key: 本地中的文件路径/键, 如"reports/analysis.md"或"data.json"
     * 如不包含日期前缀, 将自动添加当前日期格式为"YYYY-MM-DD/"
     * 完整路径示例: "2025-09-12/report.md/"或如果自动添加日期:"data.json"变为"2025-09-12/data.json"

     返回:
     文件的元数据信息，包括:
     - 文件的完整路径
     - 文件大小(字节和KB)
     - 最后修改时间
     - ETag(文件内容的MD5哈希)
     - Content-Type
     - 用户自定义元数据(如果存在)

     示例调用:
     1. 查看报告文件信息: get_local_file_metadata(file_key="reports/analysis.md")
     2. 检查指定日期数据: get_local_file_metadata(file_key="2025-09-12/data.json")
     3. 验证日志文件是否存在: get_local_file_metadata(file_key="logs/app.log")
    """
    try:
        file_key = process_file_key(file_key)

        if not os.path.exists(file_key):
            return f"错误：文件不存在: {file_key}"

        # 获取文件元数据
        stat_info = os.stat(file_key)
        file_size = stat_info.st_size
        modified_time = datetime.fromtimestamp(stat_info.st_mtime)

        # 获取文件类型
        if file_key.endswith('.html'):
            content_type = 'text/html'
        elif file_key.endswith('.txt'):
            content_type = 'text/plain'
        elif file_key.endswith('.json'):
            content_type = 'application/json'
        elif file_key.endswith(('.zip', '.rar')):
            content_type = 'application/zip'
        else:
            content_type = 'application/octet-stream'

        # 格式化元数据信息
        metadata = {
            "文件路径": file_key,
            "文件大小": f"{file_size} 字节 ({file_size / 1024:.2f} KB)",
            "最后修改时间": modified_time.strftime("%Y-%m-%d %H:%M:%S"),
            "文件类型": content_type,
            "是否为目录": "是" if os.path.isdir(file_key) else "否"
        }

        # 格式化输出
        output = "\n本地文件元数据信息:\n" + "\n".join([f"{k}: {v}" for k, v in metadata.items()])
        return output

    except Exception as e:
        error_message = f"获取本地文件元数据错误: {str(e)}"
        logging.error(error_message)
        return error_message


@tool
def write_local_file_zip(device_model: str, file_key: str, file_content: str) -> str:
    f"""
    将HTML内容压缩成Zip文件，并写入本地目录: /{get_current_date()}/{get_device_model()}/p2p_analysis_report.zip
    只压缩HTML文件, 不压缩JSON文件

    参数:
    - device_model: 设备型号
    - file_key: 最终ZIP文件的本地路径(如"/{get_current_date()}/p2p_analysis_report.zip")
    - file_content: 要压缩的HTML文件内容

    返回:
    写入操作的完整信息，包括成功写入的信息和错误写入的信息

    特点:
    - 只压缩HTML文件，自动跳过JSON文件
    - 自动添加.zip后缀(如果没有)
    - 自动添加日期(如果没有)
    - ZIP文件位置: /{get_current_date()}/p2p_analysis_report.zip

    示例调用:
    - 写入P2P Zip文件: write_local_file_zip(
                        file_key: "/{get_current_date()}/p2p_analysis_report.zip",
                        file_content: "<!DOCTYPE html>...")
    """
    logging.info(f"device_model: {device_model}, file_key: {file_key}")

    if not file_key:
        return "错误，文件路径为空"

    if not file_content:
        return "错误，file_content参数为空，无法写入，请检查file_content参数是否正确"

    if not file_content.strip().startswith('<!DOCTYPE html') and not file_content.strip().startswith('<html'):
        return f"跳过非HTML文件内容，不进行压缩: {file_content[:100]}..."

    try:
        file_key = process_file_key(file_key)
        ensure_directory_exists(file_key)

        # 确保文件以.zip结尾
        if not file_key.endswith('.zip'):
            file_key += '.zip'

        # 处理ZIP文件（如已存在但损坏，则重建）
        zip_buffer = None
        mode = 'w'
        if os.path.exists(file_key):
            try:
                with open(file_key, 'rb') as f:
                    existing_zip_bytes = f.read()
                # 校验是否为有效ZIP
                test_buf = BytesIO(existing_zip_bytes)
                with zipfile.ZipFile(test_buf, mode='r') as zf:
                    _ = zf.namelist()
                # 有效则以追加模式打开
                zip_buffer = BytesIO(existing_zip_bytes)
                mode = 'a'
                logging.info(f"找到有效zip, 以追加模式写入")
            except Exception:
                # 损坏则重建
                logging.warning(f"检测到损坏的zip，重新创建: {file_key}")
                zip_buffer = BytesIO()
                mode = 'w'
        else:
            zip_buffer = BytesIO()
            mode = 'w'
            logging.info(f"未找到zip文件，准备新建")

        with zipfile.ZipFile(zip_buffer, mode=mode, compression=zipfile.ZIP_DEFLATED) as myzip:
            html_filename = f"{device_model}.html"
            myzip.writestr(html_filename, file_content.encode('utf-8'))
            logging.info(f"成功将HTML文件 {html_filename} 添加到ZIP中")

        zip_buffer.seek(0)

        # 写入ZIP文件
        with open(file_key, 'wb') as f:
            f.write(zip_buffer.getvalue())

        success_message = f"已为设备{device_model}的HTML文件写入到ZIP: {file_key} (HTML内容长度: {len(file_content)})"
        return success_message

    except Exception as e:
        error_message = f"写入本地Zip文件错误: {str(e)}"
        logging.error(error_message)
        return error_message


@tool
def read_local_file(file_key: str) -> str:
    f"""
    读取本地文件内容，支持文本文件和二进制文件，并返回文件内容

    参数:
    - file_key: 本地中的文件名/键
        - 按App版本统计的设备连接率数据: file_key="/{get_current_date()}/<device_model>/device_connection_app_rates.json"
        - 按固件版本统计的设备连接率数据: file_key="/{get_current_date()}/<device_model>/device_connection_firmware_rates.json"
        - 按App版本统计的设备连接速度数据: file_key="/{get_current_date()}/<device_model>/device_connection_app_speeds.json"
        - 按固件版本统计的设备连接速度数据: file_key="/{get_current_date()}/<device_model>/device_connection_firmware_speeds.json"
        - App发版数据: file_key="/{get_current_date()}/<device_model>/app_release_data.json"
        - 固件版本历史: file_key="/{get_current_date()}/<device_model>/firmware_release_data.json"
        - P2p JSON报告: file_key="/{get_current_date()}/<device_model>/p2p_analysis_report.json"
        - p2p HTML文档:
         file_key="/{get_current_date()}/<device_model>/p2p_analysis_report.html"
         file_key="/{get_current_date()}/<device_model>.html"
        - P2P ZIP文件: file_key="/{get_current_date()}/p2p_analysis_report.zip"

    """
    try:
        file_key = process_file_key(file_key=file_key)

        if not os.path.exists(file_key):
            return f"错误：文件不存在: {file_key}"

        # 读取文件内容
        read_mode = 'rb' if any(
            file_key.endswith(ext) for ext in ['.zip', '.bin', '.exe', '.dll', '.so', '.dylib']) else 'r'

        if read_mode == 'rb':
            with open(file_key, 'rb') as f:
                file_content = f.read()
            # 对于二进制文件，返回base64编码的字符串
            content = base64.b64encode(file_content).decode('utf-8')
        else:
            with open(file_key, 'r', encoding='utf-8') as f:
                content = f.read()

        return content

    except Exception as e:
        error_message = f"读取本地文件错误: {str(e)}"
        logging.error(error_message)
        return error_message


