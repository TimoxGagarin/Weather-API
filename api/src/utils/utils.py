def remove_none_values(data):
    return {key: value for key, value in data.items() if value is not None}
