from fastapi import FastAPI, HTTPException, Query, Depends, APIRouter, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
import sqlite3
import json
from datetime import datetime
import os
from contextlib import contextmanager
import logging
import time

# Importar módulos do projeto original
from src.database.queries import get_dashboard_stats, unified_search_people, search_by_designation, search_by_id_vivo, search_by_address, search_by_ggl_gr
from src.database.connection import get_connection, get_tables, load_table, insert_row, update_row, delete_row, get_primary_key_column
from src.editor.operations import (
    get_lojas, get_circuitos, get_inventario,
    create_loja, update_loja, delete_loja,
    create_circuito, update_circuito, delete_circuito,
    create_inventario_item, update_inventario_item, delete_inventario_item
)
from src.editor.audit import log_change, get_audit_log
from src.cache.memory_cache import get_cache, set_cache, clear_cache, get_cache_stats

app = FastAPI(
    title="ConsultaVD API",
    description="API REST para o sistema ConsultaVD",
    version="2.0.0"
)

# Configurar CORS para permitir requisições do frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem (desenvolvimento)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de logging e performance
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # ms
    log_params = {
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "process_time_ms": round(process_time, 2),
        "timestamp": datetime.now().isoformat(),
    }
    logging.info(f"[API] {log_params['method']} {log_params['path']} - {log_params['status_code']} - {log_params['process_time_ms']}ms @ {log_params['timestamp']}")
    return response

# Modelos Pydantic para validação
class LojaCreate(BaseModel):
    nome: str
    endereco: str
    cidade: str
    uf: str
    status: str = "ATIVA"
    people_code: Optional[str] = None
    peop_code: Optional[str] = None
    ggl: Optional[str] = None
    gr: Optional[str] = None

class LojaUpdate(BaseModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    status: Optional[str] = None
    people_code: Optional[str] = None
    peop_code: Optional[str] = None
    ggl: Optional[str] = None
    gr: Optional[str] = None

class CircuitoCreate(BaseModel):
    designacao: str
    operadora: str
    tipo: str
    status: str = "ATIVO"
    loja_id: int

class CircuitoUpdate(BaseModel):
    designacao: Optional[str] = None
    operadora: Optional[str] = None
    tipo: Optional[str] = None
    status: Optional[str] = None
    loja_id: Optional[int] = None

class InventarioCreate(BaseModel):
    loja_id: int
    equipamento: str
    modelo: str
    serial: str
    status: str = "FUNCIONANDO"

class InventarioUpdate(BaseModel):
    loja_id: Optional[int] = None
    equipamento: Optional[str] = None
    modelo: Optional[str] = None
    serial: Optional[str] = None
    status: Optional[str] = None

# Resposta padrão da API
class ApiResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None

class PaginatedResponse(BaseModel):
    success: bool
    data: List[Any]
    pagination: Dict[str, Any]
    error: Optional[str] = None

class SQLRequest(BaseModel):
    query: str

# Modelos para Templates
class TemplateCreate(BaseModel):
    tipo: str  # 'informativo' ou 'alerta'
    nome: str
    conteudo: dict  # será serializado como JSON

class TemplateOut(BaseModel):
    id: int
    tipo: str
    nome: str
    conteudo: dict
    criado_em: str

# Health Check
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Dashboard
@app.get("/api/dashboard/stats", response_model=ApiResponse)
async def get_dashboard_statistics():
    try:
        stats = get_dashboard_stats()
        return ApiResponse(success=True, data=stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Lojas
@app.get("/api/lojas", response_model=PaginatedResponse)
async def get_lojas_api(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = None,
    uf: Optional[str] = None,
    search: Optional[str] = None
):
    try:
        offset = (page - 1) * limit
        lojas = get_lojas(limit=limit, offset=offset, status=status, uf=uf, search=search)
        
        # Contar total para paginação
        with get_connection() as conn:
            cursor = conn.cursor()
            count_query = "SELECT COUNT(*) FROM lojas WHERE 1=1"
            params = []
            if status:
                count_query += " AND status = ?"
                params.append(status)
            if uf:
                count_query += " AND uf = ?"
                params.append(uf)
            if search:
                count_query += " AND (nome LIKE ? OR endereco LIKE ?)"
                params.extend([f"%{search}%", f"%{search}%"])
            
            cursor.execute(count_query, params)
            total = cursor.fetchone()[0]
        
        return PaginatedResponse(
            success=True,
            data=lojas,
            pagination={
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/lojas/{loja_id}", response_model=ApiResponse)
async def get_loja_by_id(loja_id: int):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lojas WHERE id = ?", (loja_id,))
            loja = cursor.fetchone()
            
            if not loja:
                raise HTTPException(status_code=404, detail="Loja não encontrada")
            
            columns = [description[0] for description in cursor.description]
            loja_dict = dict(zip(columns, loja))
            
            return ApiResponse(success=True, data=loja_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/lojas", response_model=ApiResponse)
async def create_loja_api(loja: LojaCreate):
    try:
        new_loja = create_loja(loja.dict())
        return ApiResponse(success=True, data=new_loja, message="Loja criada com sucesso")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/lojas/{loja_id}", response_model=ApiResponse)
async def update_loja_api(loja_id: int, loja: LojaUpdate):
    try:
        updated_loja = update_loja(loja_id, loja.dict(exclude_unset=True))
        return ApiResponse(success=True, data=updated_loja, message="Loja atualizada com sucesso")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/lojas/{loja_id}")
async def delete_loja_api(loja_id: int):
    try:
        delete_loja(loja_id)
        return ApiResponse(success=True, message="Loja excluída com sucesso")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Circuitos
@app.get("/api/circuitos", response_model=PaginatedResponse)
async def get_circuitos_api(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    operadora: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None
):
    try:
        offset = (page - 1) * limit
        circuitos = get_circuitos(limit=limit, offset=offset, operadora=operadora, status=status, search=search)
        
        # Contar total para paginação
        with get_connection() as conn:
            cursor = conn.cursor()
            count_query = "SELECT COUNT(*) FROM circuitos WHERE 1=1"
            params = []
            if operadora:
                count_query += " AND operadora = ?"
                params.append(operadora)
            if status:
                count_query += " AND status = ?"
                params.append(status)
            if search:
                count_query += " AND (designacao LIKE ? OR operadora LIKE ?)"
                params.extend([f"%{search}%", f"%{search}%"])
            
            cursor.execute(count_query, params)
            total = cursor.fetchone()[0]
        
        return PaginatedResponse(
            success=True,
            data=circuitos,
            pagination={
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/circuitos", response_model=ApiResponse)
async def create_circuito_api(circuito: CircuitoCreate):
    try:
        new_circuito = create_circuito(circuito.dict())
        return ApiResponse(success=True, data=new_circuito, message="Circuito criado com sucesso")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/circuitos/{circuito_id}", response_model=ApiResponse)
async def update_circuito_api(circuito_id: int, circuito: CircuitoUpdate):
    try:
        updated_circuito = update_circuito(circuito_id, circuito.dict(exclude_unset=True))
        return ApiResponse(success=True, data=updated_circuito, message="Circuito atualizado com sucesso")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/circuitos/{circuito_id}")
async def delete_circuito_api(circuito_id: int):
    try:
        delete_circuito(circuito_id)
        return ApiResponse(success=True, message="Circuito excluído com sucesso")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Inventário
@app.get("/api/inventario", response_model=PaginatedResponse)
async def get_inventario_api(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = None,
    search: Optional[str] = None
):
    try:
        offset = (page - 1) * limit
        inventario = get_inventario(limit=limit, offset=offset, status=status, search=search)
        
        # Contar total para paginação
        with get_connection() as conn:
            cursor = conn.cursor()
            count_query = "SELECT COUNT(*) FROM inventario WHERE 1=1"
            params = []
            if status:
                count_query += " AND status = ?"
                params.append(status)
            if search:
                count_query += " AND (equipamento LIKE ? OR modelo LIKE ? OR serial LIKE ?)"
                params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
            
            cursor.execute(count_query, params)
            total = cursor.fetchone()[0]
        
        return PaginatedResponse(
            success=True,
            data=inventario,
            pagination={
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/inventario", response_model=ApiResponse)
async def create_inventario_api(item: InventarioCreate):
    try:
        new_item = create_inventario_item(item.dict())
        return ApiResponse(success=True, data=new_item, message="Item de inventário criado com sucesso")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/inventario/{item_id}", response_model=ApiResponse)
async def update_inventario_api(item_id: int, item: InventarioUpdate):
    try:
        updated_item = update_inventario_item(item_id, item.dict(exclude_unset=True))
        return ApiResponse(success=True, data=updated_item, message="Item de inventário atualizado com sucesso")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/inventario/{item_id}")
async def delete_inventario_api(item_id: int):
    try:
        delete_inventario_item(item_id)
        return ApiResponse(success=True, message="Item de inventário excluído com sucesso")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Busca Unificada
@app.get("/api/search/unified", response_model=ApiResponse)
async def unified_search_api(q: str = Query(..., min_length=1)):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Buscar em lojas
            cursor.execute("""
                SELECT 'loja' as tipo, id, nome as titulo, endereco as descricao, status
                FROM lojas 
                WHERE nome LIKE ? OR endereco LIKE ? OR people_code LIKE ? OR peop_code LIKE ?
            """, (f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"))
            lojas = cursor.fetchall()
            
            # Buscar em circuitos
            cursor.execute("""
                SELECT 'circuito' as tipo, id, designacao as titulo, operadora as descricao, status
                FROM circuitos 
                WHERE designacao LIKE ? OR operadora LIKE ?
            """, (f"%{q}%", f"%{q}%"))
            circuitos = cursor.fetchall()
            
            # Buscar em inventário
            cursor.execute("""
                SELECT 'inventario' as tipo, id, equipamento as titulo, modelo as descricao, status
                FROM inventario 
                WHERE equipamento LIKE ? OR modelo LIKE ? OR serial LIKE ?
            """, (f"%{q}%", f"%{q}%", f"%{q}%"))
            inventario = cursor.fetchall()
            
            results = {
                "lojas": [{"id": l[1], "titulo": l[2], "descricao": l[3], "status": l[4]} for l in lojas],
                "circuitos": [{"id": c[1], "titulo": c[2], "descricao": c[3], "status": c[4]} for c in circuitos],
                "inventario": [{"id": i[1], "titulo": i[2], "descricao": i[3], "status": i[4]} for i in inventario]
            }
            
            return ApiResponse(success=True, data=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Auditoria
@app.get("/api/audit/logs", response_model=PaginatedResponse)
async def get_audit_logs_api(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100)
):
    try:
        print("INICIANDO AUDITORIA")
        logs = get_audit_log(limit=limit)
        print("LOGS LIDOS:", logs)
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM audit_log")
            total = cursor.fetchone()[0]
        print("TOTAL:", total)
        return PaginatedResponse(
            success=True,
            data=logs,
            pagination={
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        )
    except Exception as e:
        import traceback
        print("ERRO AO BUSCAR LOGS DE AUDITORIA:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Cache
@app.get("/api/cache/stats", response_model=ApiResponse)
async def get_cache_stats_api():
    try:
        stats = get_cache_stats()
        return ApiResponse(success=True, data=stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cache/clear")
async def clear_cache_api():
    try:
        clear_cache()
        return ApiResponse(success=True, message="Cache limpo com sucesso")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Export
@app.get("/api/export/{table}")
async def export_data_api(table: str, format: str = Query("csv", regex="^(csv|excel)$")):
    try:
        with get_connection() as conn:
            if table not in ["lojas", "circuitos", "inventario"]:
                raise HTTPException(status_code=400, detail="Tabela inválida")
            
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
            
            if format == "csv":
                filename = f"{table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                filepath = f"temp/{filename}"
                os.makedirs("temp", exist_ok=True)
                df.to_csv(filepath, index=False)
                return FileResponse(filepath, filename=filename)
            else:
                filename = f"{table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                filepath = f"temp/{filename}"
                os.makedirs("temp", exist_ok=True)
                df.to_excel(filepath, index=False)
                return FileResponse(filepath, filename=filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export/search-results")
async def export_search_results_api(data: dict = Body(...)):
    try:
        results = data.get("results", [])
        search_type = data.get("searchType", "busca")
        filters = data.get("filters", {})
        
        if not results:
            raise HTTPException(status_code=400, detail="Nenhum resultado para exportar")
        
        # Criar DataFrame com os resultados
        df = pd.DataFrame(results)
        
        # Adicionar metadados da busca
        metadata = {
            "Data_Exportacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Tipo_Busca": search_type,
            "Total_Resultados": len(results),
            "Filtros_Aplicados": str(filters)
        }
        
        # Adicionar metadados como primeira linha
        metadata_df = pd.DataFrame([metadata])
        df_with_metadata = pd.concat([metadata_df, df], ignore_index=True)
        
        # Gerar nome do arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"resultados_{search_type}_{timestamp}.csv"
        filepath = f"temp/{filename}"
        
        # Criar diretório temp se não existir
        os.makedirs("temp", exist_ok=True)
        
        # Exportar para CSV
        df_with_metadata.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        return FileResponse(
            filepath, 
            filename=filename,
            media_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/people", response_model=ApiResponse)
async def search_people_api(code: str = Query(..., min_length=1)):
    try:
        df = unified_search_people(code)
        # Transformar DataFrame em SearchResult (lojas, circuitos, inventario)
        # Para simplificar, vamos colocar tudo em 'lojas' (ajuste conforme necessário)
        lojas = df.to_dict(orient="records")
        result = {
            "lojas": lojas,
            "circuitos": [],
            "inventario": []
        }
        return ApiResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/designation", response_model=ApiResponse)
async def search_designation_api(designation: str = Query(..., min_length=1)):
    try:
        df = search_by_designation(designation)
        circuitos = []
        lojas = []
        lojas_ids = set()
        for idx, row in df.iterrows():
            logging.warning(f"Linha {idx}: {row.to_dict()}")
            loja_id = (
                row.get("CODIGO") or row.get("CÓDIGO") or row.get("Codigo") or row.get("codigo") or
                row.get("codigo_loja") or row.get("id") or row.get("ID") or row.get("id_loja")
            )
            # Fallback: se não houver dados da loja, buscar manualmente
            loja_vazia = not (row.get("LOJAS") or row.get("ENDEREÇO") or row.get("CIDADE"))
            loja_data = None
            if loja_vazia and row.get("People/PEOP"):
                # Buscar manualmente na tabela de lojas
                with get_connection() as conn_fallback:
                    cursor = conn_fallback.cursor()
                    cursor.execute("SELECT LOJAS, CODIGO, ENDEREÇO, CIDADE, UF, STATUS, PEOP, NOME_GGL, NOME_GR FROM lojas_lojas WHERE PEOP = ?", (row.get("People/PEOP"),))
                    loja_row = cursor.fetchone()
                    if loja_row:
                        loja_data = {
                            "id": loja_row[1],
                            "nome": loja_row[0],
                            "endereco": loja_row[2],
                            "cidade": loja_row[3],
                            "uf": loja_row[4],
                            "status": loja_row[5],
                            "people_code": loja_row[6],
                            "peop_code": loja_row[6],
                            "ggl": loja_row[7],
                            "gr": loja_row[8]
                        }
                        loja_id = loja_row[1]
            circuito = {
                "designacao": row.get("Circuito_Designação") or row.get("Novo_Circuito_Designação"),
                "operadora": row.get("Operadora"),
                "tipo": row.get("Tipo", ""),
                "status": row.get("Status_Loja", "")
            }
            circuitos.append(circuito)
            if loja_id and loja_id not in lojas_ids:
                if loja_data:
                    # Padronizar campos para o frontend
                    loja = {
                        "LOJAS": loja_data.get("LOJAS", ""),
                        "CODIGO": loja_data.get("CODIGO", ""),
                        "Status_Loja": loja_data.get("Status_Loja", "") or loja_data.get("STATUS", ""),
                        "ENDEREÇO": loja_data.get("ENDEREÇO", ""),
                        "BAIRRO": loja_data.get("BAIRRO", ""),
                        "CIDADE": loja_data.get("CIDADE", ""),
                        "UF": loja_data.get("UF", ""),
                        "CEP": loja_data.get("CEP", ""),
                        "TELEFONE1": loja_data.get("TELEFONE1", ""),
                        "TELEFONE2": loja_data.get("TELEFONE2", ""),
                        "CELULAR": loja_data.get("CELULAR", ""),
                        "E_MAIL": loja_data.get("E_MAIL", ""),
                        "VD NOVO": loja_data.get("VD NOVO", ""),
                        "People/PEOP": loja_data.get("People/PEOP", ""),
                        "STATUS": loja_data.get("Status_Loja", "") or loja_data.get("STATUS", ""),
                        "NOME_GGL": loja_data.get("NOME_GGL", ""),
                        "NOME_GR": loja_data.get("NOME_GR", "")
                    }
                    lojas.append(loja)
                else:
                    loja = {
                        "LOJAS": row.get("LOJAS", ""),
                        "CODIGO": row.get("CODIGO", ""),
                        "Status_Loja": row.get("Status_Loja", "") or row.get("STATUS", ""),
                        "ENDEREÇO": row.get("ENDEREÇO", ""),
                        "BAIRRO": row.get("BAIRRO", ""),
                        "CIDADE": row.get("CIDADE", ""),
                        "UF": row.get("UF", ""),
                        "CEP": row.get("CEP", ""),
                        "TELEFONE1": row.get("TELEFONE1", ""),
                        "TELEFONE2": row.get("TELEFONE2", ""),
                        "CELULAR": row.get("CELULAR", ""),
                        "E_MAIL": row.get("E_MAIL", ""),
                        "VD NOVO": row.get("VD_NOVO", ""),
                        "People/PEOP": row.get("People/PEOP", ""),
                        "STATUS": row.get("Status_Loja", "") or row.get("STATUS", ""),
                        "NOME_GGL": row.get("NOME_GGL", ""),
                        "NOME_GR": row.get("NOME_GR", "")
                    }
                    lojas.append(loja)
                lojas_ids.add(loja_id)
        result = {
            "lojas": lojas,
            "circuitos": circuitos,
            "inventario": []
        }
        return ApiResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/address", response_model=ApiResponse)
async def search_address_api(address: str = Query(..., min_length=1)):
    try:
        df = search_by_address(address)
        lojas = df.to_dict(orient="records")
        result = {
            "lojas": lojas,
            "circuitos": [],
            "inventario": []
        }
        return ApiResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/id-vivo", response_model=ApiResponse)
async def search_id_vivo_api(id_vivo: str = Query(..., min_length=1)):
    try:
        df = search_by_id_vivo(id_vivo)
        lojas = []
        lojas_ids = set()
        for idx, row in df.iterrows():
            logging.warning(f"Linha {idx}: {row.to_dict()}")
            loja_id = (
                row.get("CODIGO") or row.get("CÓDIGO") or row.get("Codigo") or row.get("codigo") or
                row.get("codigo_loja") or row.get("id") or row.get("ID") or row.get("id_loja")
            )
            loja_vazia = not (row.get("LOJAS") or row.get("ENDEREÇO") or row.get("CIDADE"))
            loja_data = None
            if loja_vazia and row.get("People/PEOP"):
                with get_connection() as conn_fallback:
                    cursor = conn_fallback.cursor()
                    cursor.execute("SELECT LOJAS, CODIGO, ENDEREÇO, BAIRRO, CIDADE, UF, CEP, TELEFONE1, TELEFONE2, CELULAR, E_MAIL, STATUS, PEOP, NOME_GGL, NOME_GR, VD_NOVO FROM lojas_lojas WHERE PEOP = ?", (row.get("People/PEOP"),))
                    loja_row = cursor.fetchone()
                    if loja_row:
                        loja_data = {
                            "LOJAS": loja_row[0],
                            "CODIGO": loja_row[1],
                            "ENDEREÇO": loja_row[2],
                            "BAIRRO": loja_row[3],
                            "CIDADE": loja_row[4],
                            "UF": loja_row[5],
                            "CEP": loja_row[6],
                            "TELEFONE1": loja_row[7],
                            "TELEFONE2": loja_row[8],
                            "CELULAR": loja_row[9],
                            "E_MAIL": loja_row[10],
                            "Status_Loja": row.get("Status_Loja", "") or loja_row[11],
                            "People/PEOP": loja_row[12],
                            "NOME_GGL": loja_row[13],
                            "NOME_GR": loja_row[14],
                            "VD NOVO": loja_row[15],
                            "STATUS": row.get("Status_Loja", "") or loja_row[11]
                        }
                        loja_id = loja_row[1]
            if loja_id and loja_id not in lojas_ids:
                if loja_data:
                    loja = loja_data
                else:
                    loja = {
                        "LOJAS": row.get("LOJAS", ""),
                        "CODIGO": row.get("CODIGO", ""),
                        "ENDEREÇO": row.get("ENDEREÇO", ""),
                        "BAIRRO": row.get("BAIRRO", ""),
                        "CIDADE": row.get("CIDADE", ""),
                        "UF": row.get("UF", ""),
                        "CEP": row.get("CEP", ""),
                        "TELEFONE1": row.get("TELEFONE1", ""),
                        "TELEFONE2": row.get("TELEFONE2", ""),
                        "CELULAR": row.get("CELULAR", ""),
                        "E_MAIL": row.get("E_MAIL", ""),
                        "Status_Loja": row.get("Status_Loja", "") or row.get("STATUS", ""),
                        "People/PEOP": row.get("People/PEOP", ""),
                        "NOME_GGL": row.get("NOME_GGL", ""),
                        "NOME_GR": row.get("NOME_GR", ""),
                        "VD NOVO": row.get("VD_NOVO", ""),
                        "STATUS": row.get("Status_Loja", "") or row.get("STATUS", "")
                    }
                lojas.append(loja)
                lojas_ids.add(loja_id)
        result = {
            "lojas": lojas,
            "circuitos": [],
            "inventario": []
        }
        return ApiResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/ggl-gr", response_model=ApiResponse)
async def search_ggl_gr_api(ggl_gr: str = Query(..., min_length=1)):
    try:
        df = search_by_ggl_gr(ggl_gr)
        # Transformar DataFrame em SearchResult
        lojas = df.to_dict(orient="records")
        result = {
            "lojas": lojas,
            "circuitos": [],
            "inventario": []
        }
        return ApiResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/lojas", response_model=ApiResponse)
async def search_lojas_api(q: str = Query(..., min_length=1)):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT l.CODIGO as id, l.PEOP as codigo, l.LOJAS as nome, l.ENDEREÇO as endereco, l.CIDADE as cidade, l.UF as uf, l.STATUS as status
                FROM lojas_lojas l
                WHERE l.LOJAS LIKE ? OR l.PEOP LIKE ? OR l.CODIGO LIKE ?
                ORDER BY l.LOJAS
                LIMIT 20
            """, (f"%{q}%", f"%{q}%", f"%{q}%"))
            
            lojas = []
            for row in cursor.fetchall():
                lojas.append({
                    "id": row[0],
                    "codigo": row[1],
                    "nome": row[2],
                    "endereco": row[3],
                    "cidade": row[4],
                    "uf": row[5],
                    "status": row[6]
                })
            
            return ApiResponse(success=True, data=lojas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/lojas/{loja_id}/operadoras", response_model=ApiResponse)
async def get_operadoras_by_loja(loja_id: str):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT i.Operadora
                FROM inventario_planilha1 i
                JOIN lojas_lojas l ON i.People = l.PEOP
                WHERE l.PEOP = ? OR l.CODIGO = ?
                ORDER BY i.Operadora
            """, (loja_id, loja_id))
            
            operadoras = [row[0] for row in cursor.fetchall()]
            return ApiResponse(success=True, data=operadoras)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/lojas/{loja_id}/operadoras/{operadora}/circuitos", response_model=ApiResponse)
async def get_circuitos_by_loja_operadora(loja_id: str, operadora: str):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT i.Circuito_Designação
                FROM inventario_planilha1 i
                JOIN lojas_lojas l ON i.People = l.PEOP
                WHERE (l.PEOP = ? OR l.CODIGO = ?) AND i.Operadora = ?
                ORDER BY i.Circuito_Designação
            """, (loja_id, loja_id, operadora))
            
            circuitos = [row[0] for row in cursor.fetchall()]
            return ApiResponse(success=True, data=circuitos)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/loja-operadora-circuito", response_model=ApiResponse)
async def search_loja_operadora_circuito(
    loja_id: str = Query(..., description="ID da loja"),
    operadora: str = Query(..., description="Nome da operadora"),
    circuito: str = Query(..., description="Designação do circuito")
):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    l.CODIGO as loja_id,
                    l.PEOP as people_code,
                    l.LOJAS as loja_nome,
                    l.ENDEREÇO as endereco,
                    l.BAIRRO as bairro,
                    l.CIDADE as cidade,
                    l.UF as uf,
                    l.CEP as cep,
                    l.TELEFONE1 as telefone1,
                    l.TELEFONE2 as telefone2,
                    l.CELULAR as celular,
                    l."E_MAIL" as email,
                    l.STATUS as loja_status,
                    l.NOME_GGL as nome_ggl,
                    l.NOME_GR as nome_gr,
                    l.VD_NOVO as vd_novo,
                    l."2ª_a_6ª" as horario_seg_sex,
                    l.SAB as horario_sabado,
                    l.DOM as horario_domingo,
                    l."FUNC." as funcionario,
                    i.Operadora,
                    i.Circuito_Designação as designacao,
                    i.Novo_Circuito_Designação as novo_designacao,
                    i.Velocidade,
                    i.Serviço as servico,
                    i.Status_Serviço as circuito_status
                FROM lojas_lojas l
                JOIN inventario_planilha1 i ON l.PEOP = i.People
                WHERE (l.PEOP = ? OR l.CODIGO = ?) 
                  AND i.Operadora = ? 
                  AND (i.Circuito_Designação = ? OR i.Novo_Circuito_Designação = ?)
            """, (loja_id, loja_id, operadora, circuito, circuito))
            results = []
            for row in cursor.fetchall():
                loja = {
                    "LOJAS": row[2],
                    "CODIGO": row[0],
                    "Status_Loja": row[12],
                    "ENDEREÇO": row[3],
                    "BAIRRO": row[4],
                    "CIDADE": row[5],
                    "UF": row[6],
                    "CEP": row[7],
                    "TELEFONE1": row[8],
                    "TELEFONE2": row[9],
                    "CELULAR": row[10],
                    "E_MAIL": row[11],
                    "People/PEOP": row[1],
                    "NOME_GGL": row[13],
                    "NOME_GR": row[14],
                    "VD NOVO": row[15],
                    "STATUS": row[12],
                    "2ª_a_6ª": row[17],
                    "SAB": row[18],
                    "DOM": row[19],
                    "FUNC.": row[20]
                }
                results.append(loja)
            result = {
                "lojas": results,
                "circuitos": [],
                "inventario": []
            }
            return ApiResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/api/sql/execute')
async def execute_sql(request: SQLRequest):
    query = request.query.strip()
    if not query.lower().startswith('select'):
        raise HTTPException(status_code=400, detail='Apenas SELECT permitido')
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
        return {"columns": columns, "data": [dict(zip(columns, row)) for row in rows]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/tables", response_model=ApiResponse)
async def list_tables():
    try:
        tables = get_tables()
        return ApiResponse(success=True, data=tables)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/table/{table_name}", response_model=ApiResponse)
async def get_table_data(table_name: str, limit: int = 100, offset: int = 0, search: Optional[str] = None, orderBy: Optional[str] = None, orderDir: Optional[str] = 'asc'):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Buscar colunas de texto
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns_info = cursor.fetchall()
            text_columns = [col[1] for col in columns_info if col[2] in ("TEXT", "VARCHAR", "CHAR")]
            all_columns = [col[1] for col in columns_info]
            # Montar filtro de busca
            where = ""
            params = []
            if search and text_columns:
                like_expr = " OR ".join([f"{col} LIKE ?" for col in text_columns])
                where = f"WHERE {like_expr}"
                params = [f"%{search}%"] * len(text_columns)
            # Buscar total
            count_query = f"SELECT COUNT(*) FROM {table_name} {where}"
            cursor.execute(count_query, params)
            total = cursor.fetchone()[0]
            # Montar ordenação
            order_clause = ""
            if orderBy and orderBy in all_columns:
                order_dir = 'DESC' if (orderDir and orderDir.lower() == 'desc') else 'ASC'
                order_clause = f"ORDER BY {orderBy} {order_dir}"
            # Buscar dados paginados
            data_query = f"SELECT * FROM {table_name} {where} {order_clause} LIMIT ? OFFSET ?"
            cursor.execute(data_query, params + [limit, offset])
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            data = [dict(zip(columns, row)) for row in rows]
        return ApiResponse(success=True, data={"columns": columns, "rows": data, "total": total})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/table/{table_name}", response_model=ApiResponse)
async def insert_table_row(table_name: str, data: dict = Body(...)):
    try:
        rowid = insert_row(table_name, data)
        return ApiResponse(success=True, data={"id": rowid})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/table/{table_name}/{row_id}", response_model=ApiResponse)
async def update_table_row(table_name: str, row_id: int, data: dict = Body(...)):
    try:
        pk_col = get_primary_key_column(table_name)
        affected = update_row(table_name, pk_col, row_id, data)
        return ApiResponse(success=True, data={"updated": affected})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/table/{table_name}/{row_id}", response_model=ApiResponse)
async def delete_table_row(table_name: str, row_id: int):
    try:
        pk_col = get_primary_key_column(table_name)
        affected = delete_row(table_name, pk_col, row_id)
        return ApiResponse(success=True, data={"deleted": affected})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/templates", response_model=List[TemplateOut])
async def list_templates(tipo: Optional[str] = None):
    try:
        from src.database.connection import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT id, tipo, nome, conteudo, criado_em FROM templates"
        params = []
        if tipo:
            query += " WHERE tipo = ?"
            params.append(tipo)
        query += " ORDER BY criado_em DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        result = []
        for row in rows:
            result.append(TemplateOut(
                id=row[0],
                tipo=row[1],
                nome=row[2],
                conteudo=json.loads(row[3]),
                criado_em=row[4],
            ))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/templates", response_model=TemplateOut)
async def create_template(template: TemplateCreate):
    try:
        from src.database.connection import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO templates (tipo, nome, conteudo, criado_em) VALUES (?, ?, ?, ?)",
            (template.tipo, template.nome, json.dumps(template.conteudo), now)
        )
        template_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return TemplateOut(id=template_id, tipo=template.tipo, nome=template.nome, conteudo=template.conteudo, criado_em=now)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/templates/{template_id}")
async def delete_template(template_id: int):
    try:
        from src.database.connection import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM templates WHERE id = ?", (template_id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        if affected == 0:
            raise HTTPException(status_code=404, detail="Template não encontrado")
        return {"success": True, "message": "Template removido"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 