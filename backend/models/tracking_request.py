from datetime import datetime, timezone
import enum
from sqlalchemy import String, Text, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class RequestStatus(str, enum.Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"


class RequestPriority(str, enum.Enum):
    low = "low"
    normal = "normal"
    high = "high"


class TrackingRequest(Base):
    __tablename__ = "tracking_requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Сохраняем Enum как строку в SQLite
    status: Mapped[RequestStatus] = mapped_column(
        Enum(RequestStatus), default=RequestStatus.new, nullable=False
    )
    priority: Mapped[RequestPriority] = mapped_column(
        Enum(RequestPriority), default=RequestPriority.normal, nullable=False
    )

    # Время создания и обновления в UTC
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
