# 全局变量，用于跟踪当前设备索引
_current_device_index = 0


def get_device_model(index=None):
    """
    获取设备型号

    如果不提供索引参数，则会自动循环返回设备列表中的下一个设备。
    每次调用都会自动切换到下一个设备，实现设备的循环遍历。

    Args:
        index: 可选，指定要获取的设备型号索引
              如果不提供，则根据内部计数器返回下一个设备

    Returns:
        如果提供了有效索引，返回对应的设备型号
        如果没有提供索引，返回当前计数器对应的设备型号，并将计数器加1
        如果计数器超出范围，会自动重置为0
    """
    global _current_device_index
    device_model_list = [""]

    # 如果提供了索引，返回对应的设备型号
    if index is not None:
        # 确保索引在有效范围内
        if 0 <= index < len(device_model_list):
            return device_model_list[index]
        else:
            raise IndexError(f"设备索引 {index} 超出范围 (0-{len(device_model_list) - 1})")

    # 如果没有提供索引，返回当前计数器对应的设备型号，并将计数器加1
    current_device = device_model_list[_current_device_index]

    # 更新计数器，如果超出范围则重置为0
    _current_device_index = (_current_device_index + 1) % len(device_model_list)

    return current_device




