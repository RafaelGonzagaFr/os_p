from datetime import date, datetime
from http import HTTPStatus
from typing import Annotated, Optional
from sqlalchemy import select
from pinea.database import get_session
from pinea.models import OS, Entregue
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from pinea.models import OS
from pinea.models import OS
from pinea.schemas import Message, OSSchema, OSPublica, OSList, EntregueUpdate
from sqlalchemy.orm import Session, joinedload


router = APIRouter(prefix='/os', tags=['os'])
T_Session = Annotated[Session, Depends(get_session)]

@router.post('/', status_code=HTTPStatus.OK, response_model=OSPublica)
def criar_os(os: OSSchema, session: T_Session):

    db_os = OS(
        cliente=os.cliente,
        entrega=os.entrega,
        telefone=os.telefone,
        entregue=Entregue.nao
    )

    session.add(db_os)
    session.commit()
    session.refresh(db_os)

    return db_os

@router.get('/', status_code=HTTPStatus.OK, response_model=OSList)
def listar_os(
    session: T_Session,
    data: str | None = Query(None, description="Data no formato DD/MM/YYYY"),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(20, ge=1, le=100, description="Número máximo de registros a retornar"),
):
    query = select(OS)
    
    if data:
        try:
            data_convertida = datetime.strptime(data, "%d/%m/%Y").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de data inválido. Use DD/MM/YYYY.")
        
        start_datetime = datetime.combine(data_convertida, datetime.min.time())
        end_datetime = datetime.combine(data_convertida, datetime.max.time())
        query = query.where(OS.created_at >= start_datetime, OS.created_at <= end_datetime)

    query = query.offset(skip).limit(limit)

    os = session.scalars(query).all()
    return {'os': os}

@router.patch('/{os_id}', status_code=HTTPStatus.OK, response_model=OSPublica)
def atualizar_entregue(
    session: T_Session,
    os_id: int = Path(..., description="ID da OS para atualizar"),
    entregue_update: EntregueUpdate = Body(...),
):
    os_obj = session.get(OS, os_id)
    if not os_obj:
        raise HTTPException(status_code=404, detail="OS não encontrada")

    os_obj.entregue = entregue_update.entregue
    session.add(os_obj)
    session.commit()
    session.refresh(os_obj)
    return os_obj
