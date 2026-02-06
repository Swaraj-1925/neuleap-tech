import json
from fastapi import APIRouter, HTTPException
import aiofiles

from model import InternBase, DailyActivity, InternResponse, StatisticsResponse
from intern import Intern
from utils import DATA_FILE, generate_intern_id, Status

router = APIRouter(tags=["Intern"])


async def read_intern_data() -> dict:
    try:
        async with aiofiles.open(DATA_FILE, "r") as f:
            content = await f.read()
            raw = json.loads(content)
        return {k: Intern.from_dict(v) for k, v in raw.items()}
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


async def write_intern_data(interns: dict):
    data = {k: v.to_dict() for k, v in interns.items()}
    async with aiofiles.open(DATA_FILE, "w") as f:
        await f.write(json.dumps(data, indent=4))


@router.post("/interns", description="Add a new intern")
async def add_new_intern(intern_data: InternBase):
    interns = await read_intern_data()
    intern_id = generate_intern_id(len(interns))

    new_intern = Intern(
        intern_id=intern_id,
        name=intern_data.name,
        role=intern_data.role,
        daily_hours=intern_data.daily_hours,
        daily_tasks=intern_data.daily_tasks
    )

    interns[intern_id] = new_intern
    await write_intern_data(interns)

    return {
        "message": "Intern added successfully",
        "intern_id": intern_id
    }


@router.post("/interns/{intern_id}/activity", description="Add daily activity for an intern")
async def add_daily_activity(intern_id: str, daily_activity: DailyActivity):
    interns = await read_intern_data()

    if intern_id not in interns:
        raise HTTPException(status_code=404, detail="Intern not found")

    intern = interns[intern_id]

    if intern.status != Status.ACTIVE:
        raise HTTPException(
            status_code=400,
            detail=f"Activity allowed only for ACTIVE interns. Current status: {intern.status.value}"
        )

    intern.hours.append(daily_activity.hours)
    intern.tasks.append(daily_activity.task)

    await write_intern_data(interns)

    return {
        "message": "Activity recorded successfully",
        "intern_id": intern_id,
        "total_hours": intern.total_hours(),
        "days_worked": len(intern.hours)
    }


@router.get("/interns/{intern_id}", response_model=InternResponse, description="Get intern summary")
async def intern_summary(intern_id: str):
    interns = await read_intern_data()

    if intern_id not in interns:
        raise HTTPException(status_code=404, detail="Intern not found")

    intern = interns[intern_id]

    return InternResponse(
        intern_id=intern.intern_id,
        name=intern.name,
        role=intern.role,
        daily_hours=intern.daily_hours,
        daily_tasks=intern.daily_tasks,
        status=intern.status.value,
        days_worked=len(intern.hours),
        total_hours=intern.total_hours(),
        average_hours=intern.average_hours(),
        daily_work=[{"hours": h, "task": t} for h, t in zip(intern.hours, intern.tasks)],
        last_task=intern.tasks[-1] if intern.tasks else None
    )


@router.get("/statistics", response_model=StatisticsResponse, description="Get overall statistics of all interns")
async def get_statistics():
    interns = await read_intern_data()

    if not interns:
        return StatisticsResponse(
            total_interns=0,
            active_interns=0,
            average_hours=0.0,
            top_performer=None,
            top_performer_hours=None
        )

    total_interns = len(interns)
    active_interns = sum(1 for i in interns.values() if i.status == Status.ACTIVE)

    total_hours = sum(i.total_hours() for i in interns.values())
    total_days = sum(len(i.hours) for i in interns.values())
    avg_hours = total_hours / total_days if total_days > 0 else 0.0

    top = max(interns.values(), key=lambda i: i.total_hours(), default=None)

    return StatisticsResponse(
        total_interns=total_interns,
        active_interns=active_interns,
        average_hours=round(avg_hours, 2),
        top_performer=top.name if top and top.total_hours() > 0 else None,
        top_performer_hours=top.total_hours() if top and top.total_hours() > 0 else None
    )


@router.patch("/interns/{intern_id}/status", description="Update intern status")
async def update_intern_status(intern_id: str, status: str):
    interns = await read_intern_data()

    if intern_id not in interns:
        raise HTTPException(status_code=404, detail="Intern not found")

    status_map = {
        "active": Status.ACTIVE,
        "inactive": Status.INACTIVE,
        "completed": Status.COMPLETED
    }

    status_lower = status.lower()
    if status_lower not in status_map:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: Active, Inactive, Completed"
        )

    interns[intern_id].status = status_map[status_lower]
    await write_intern_data(interns)

    return {
        "message": "Status updated successfully",
        "intern_id": intern_id,
        "new_status": status_map[status_lower].value
    }
