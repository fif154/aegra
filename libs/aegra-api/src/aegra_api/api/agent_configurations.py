"""Agent configuration CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aegra_api.core.auth_deps import auth_dependency
from aegra_api.core.orm import AgentConfiguration as AgentConfigurationORM
from aegra_api.core.orm import get_session
from aegra_api.models.agent_configurations import (
    AgentConfiguration,
    AgentConfigurationCreate,
    AgentConfigurationList,
)
from aegra_api.models.errors import NOT_FOUND

router = APIRouter(tags=["Agent Configurations"], dependencies=auth_dependency)


@router.post("/agent-configurations", response_model=AgentConfiguration, response_model_by_alias=False)
async def create_agent_configuration(
    request: AgentConfigurationCreate,
    session: AsyncSession = Depends(get_session),
) -> AgentConfiguration:
    """Create a new agent configuration."""
    row = AgentConfigurationORM(
        name=request.name,
        metadata_json=request.metadata,
    )
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return AgentConfiguration.model_validate(row)


@router.get("/agent-configurations", response_model=AgentConfigurationList, response_model_by_alias=False)
async def list_agent_configurations(
    session: AsyncSession = Depends(get_session),
) -> AgentConfigurationList:
    """List all agent configurations."""
    rows = (await session.scalars(select(AgentConfigurationORM))).all()
    return AgentConfigurationList(
        configurations=[AgentConfiguration.model_validate(r) for r in rows],
        total=len(rows),
    )


@router.delete("/agent-configurations/{configuration_id}", status_code=204, responses={**NOT_FOUND})
async def delete_agent_configuration(
    configuration_id: str,
    session: AsyncSession = Depends(get_session),
) -> None:
    """Delete an agent configuration by ID."""
    row = await session.scalar(
        select(AgentConfigurationORM).where(AgentConfigurationORM.id == configuration_id)
    )
    if not row:
        raise HTTPException(status_code=404, detail=f"Agent configuration '{configuration_id}' not found")
    await session.delete(row)
    await session.commit()
