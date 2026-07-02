from enum import Enum

class SortTicket(str, Enum):
    ASC = "asc"
    DESC = "desc"

class TicketStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TicketPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"