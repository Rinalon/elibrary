def make_case(base_data: dict, updates=None, remove_keys=None):
    """Создаёт копию base_data с изменениями."""
    data = base_data.copy()

    if remove_keys:
        for key in remove_keys:
            data.pop(key, None)

    if updates:
        data.update(updates)

    return data