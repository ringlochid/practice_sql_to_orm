from sqlalchemy import case, extract, func, literal, select, union_all
from sqlalchemy.orm import Session

from database import get_session

from .models import Task, create_tables


def get_employee_task_duration_and_concurrent_tasks(session: Session):
    event_points = union_all(
        select(
            Task.employee_id,
            Task.task_id,
            Task.start_time.label("event_pt"),
            literal(1).label("delta"),
        ),
        select(
            Task.employee_id,
            Task.task_id,
            Task.end_time.label("event_pt"),
            literal(-1).label("delta"),
        ),
    ).cte("event_points")

    concurrent_tasks = (
        select(
            event_points.c.employee_id,  # not Task.employee_id
            func.sum(event_points.c.delta)
            .over(
                partition_by=event_points.c.employee_id,  # not Task.employee_id
                order_by=[event_points.c.event_pt.asc(), event_points.c.delta.asc()],
            )
            .label("concurrent_task"),
        )
        .select_from(event_points)
        .cte("concurrent_tasks")
    )

    mx_concurrent_tasks = (
        select(
            concurrent_tasks.c.employee_id,
            func.max(concurrent_tasks.c.concurrent_task).label("mx_concurrent"),
        )
        .group_by(concurrent_tasks.c.employee_id)  # not event_points.c.employee_id
        .cte("max_concurrent_tasks")
    )

    mx_end_times = select(
        Task.employee_id,
        Task.task_id,
        Task.start_time,
        Task.end_time,
        func.max(Task.end_time)
        .over(partition_by=Task.employee_id, order_by=Task.start_time, rows=(None, -1))
        .label("mx_end"),
    ).cte("mx_end_times")

    start_time_deltas = select(
        mx_end_times.c.employee_id,
        mx_end_times.c.task_id,
        mx_end_times.c.start_time,
        mx_end_times.c.end_time,
        case((mx_end_times.c.start_time > mx_end_times.c.mx_end, 1), else_=0).label(
            "start_delta"
        ),
    ).cte("start_time_delta")

    grouped_tasks = select(
        start_time_deltas.c.employee_id,
        start_time_deltas.c.task_id,
        start_time_deltas.c.start_time,
        start_time_deltas.c.end_time,
        func.sum(start_time_deltas.c.start_delta)
        .over(
            partition_by=start_time_deltas.c.employee_id,
            order_by=start_time_deltas.c.start_time,
        )
        .label("group_id"),
    ).cte("grouped_tasks")

    minmax_groups = (
        select(
            grouped_tasks.c.employee_id,
            func.min(grouped_tasks.c.start_time).label("start_pt"),
            func.max(grouped_tasks.c.end_time).label("end_pt"),
        )
        .group_by(grouped_tasks.c.employee_id, grouped_tasks.c.group_id)
        .cte("minmax_groups")
    )

    total_durations = (
        select(
            minmax_groups.c.employee_id,
            func.sum(
                extract("epoch", minmax_groups.c.end_pt - minmax_groups.c.start_pt)
                / 3600.0
            ).label("total_duration"),
        )
        .group_by(minmax_groups.c.employee_id)
        .cte("total_durations")
    )

    stmt = select(
        mx_concurrent_tasks.c.employee_id,
        func.floor(total_durations.c.total_duration).label("total_task_hours"),
        mx_concurrent_tasks.c.mx_concurrent.label("max_concurrent_tasks"),
    ).join_from(
        mx_concurrent_tasks,
        total_durations,
        mx_concurrent_tasks.c.employee_id == total_durations.c.employee_id,
    )

    return session.execute(stmt).all()


def main() -> None:
    create_tables()

    try:
        with get_session() as session:
            rows = get_employee_task_duration_and_concurrent_tasks(session)
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
