from collections import defaultdict
from datetime import datetime, timedelta

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_session

from .models import Task, create_tables


class Result(BaseModel):
    employee_id: int
    total_task_hours: int
    max_concurrent_tasks: int


def sweepline_algo(session: Session):
    """
    Imperative approach
    """
    stmt = select(Task)

    rows = session.execute(stmt).scalars().all()
    tasks = defaultdict(list)

    results = []

    for row in rows:
        tasks[row.employee_id].append([row.task_id, row.start_time, row.end_time])

    for eid in tasks:
        event_points = [(row[1], 1) for row in tasks[eid]] + [
            (row[2], -1) for row in tasks[eid]
        ]

        event_points.sort()

        mx_concurrency = 0
        curr = 0

        for idx in range(len(event_points)):
            event, delta = event_points[idx]
            curr += delta
            if idx + 1 < len(event_points) and event_points[idx + 1][0] == event:
                continue
            mx_concurrency = max(mx_concurrency, curr)

        time = [(row[1], row[2]) for row in tasks[eid]]
        time.sort()

        mn_start = datetime(1991, 1, 1, 0, 0, 0)
        mx_end = datetime(1991, 1, 1, 0, 0, 0)

        acc = timedelta(0)

        for st, end in time:
            if st > mx_end:
                acc += mx_end - mn_start
                mn_start = st
            mx_end = max(mx_end, end)

        acc += mx_end - mn_start

        total_hours = acc.total_seconds() / 3600
        results.append(
            {
                "employee_id": eid,
                "total_task_hours": total_hours,
                "max_concurrent_tasks": mx_concurrency,
            }
        )
    return [Result.model_validate(row) for row in results]


def main() -> None:
    create_tables()

    try:
        with get_session() as session:
            rows = sweepline_algo(session)
    except NotImplementedError as exc:
        print(exc)
        return

    if not rows:
        print("No rows found.")
        return

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
