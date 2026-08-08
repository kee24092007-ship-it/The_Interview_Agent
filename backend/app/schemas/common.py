"""Shared enums used across API schemas."""
from enum import Enum


class SessionStatus(str, Enum):
    scheduled = "scheduled"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class QuestionType(str, Enum):
    behavioral = "behavioral"
    technical = "technical"
    coding = "coding"
    situational = "situational"
    strengths = "strengths"
    custom = "custom"


class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"
