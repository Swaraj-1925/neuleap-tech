from pydantic import BaseModel, Field
from typing import Optional, List


class InternBase(BaseModel):
    name: str = Field(..., min_length=1, description="Intern's name")
    role: str = Field(..., min_length=1, description="Intern's role")
    daily_hours: int = Field(..., ge=0, description="Expected daily hours")
    daily_tasks: int = Field(..., ge=0, description="Expected daily tasks")


class DailyActivity(BaseModel):
    hours: int = Field(..., ge=0, description="Hours worked")
    task: str = Field(..., min_length=1, description="Task description")


class DailyWorkEntry(BaseModel):
    hours: int
    task: str


class InternResponse(BaseModel):
    intern_id: str
    name: str
    role: str
    daily_hours: int
    daily_tasks: int
    status: str
    days_worked: int
    total_hours: int
    average_hours: float
    daily_work: List[DailyWorkEntry]
    last_task: Optional[str] = None


class StatisticsResponse(BaseModel):
    total_interns: int
    active_interns: int
    average_hours: float
    top_performer: Optional[str] = None
    top_performer_hours: Optional[int] = None
