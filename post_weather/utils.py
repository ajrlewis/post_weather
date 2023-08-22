from datetime import datetime, timedelta


def chunk_dates(start_date: str, end_date: str, chunk_size: int = 365) -> list:
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end_date - start_date
    total_days = delta.days
    if total_days <= chunk_size:
        return [(f"{start_date.date()}", f"{end_date.date()}")]
    chunks = []
    current_date = start_date
    while current_date < end_date:
        chunk_end_date = min(current_date + timedelta(days=chunk_size), end_date)
        chunks.append((f"{current_date.date()}", f"{chunk_end_date.date()}"))
        current_date = chunk_end_date + timedelta(days=1)
    return chunks
