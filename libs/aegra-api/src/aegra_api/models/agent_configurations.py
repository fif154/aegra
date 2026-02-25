"""Pydantic models for agent configuration endpoints."""

from datetime import datetime

from pydantic import BaseModel, Field


class AgentConfigurationCreate(BaseModel):
    """Request body for creating an agent configuration."""

    name: str = Field(..., description="Human-readable name for this configuration.")
    metadata: dict = Field(default_factory=dict, description="Arbitrary metadata for the configuration.")


class AgentConfiguration(BaseModel):
    """Agent configuration response model."""

    id: str
    name: str
    metadata: dict = Field(alias="metadata_json")
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True, "populate_by_name": True}


class AgentConfigurationList(BaseModel):
    """Paginated list of agent configurations."""

    configurations: list[AgentConfiguration]
    total: int
