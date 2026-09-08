def format_timestamp(seconds: float):
    milliseconds = round((seconds % 1) * 1000)
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)

    hours = int(minutes // 60)
    minutes = int(minutes % 60)

    return f"{hours:02}:{minutes:02}:{remaining_seconds:02},{milliseconds:03}"