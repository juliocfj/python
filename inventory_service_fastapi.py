"""
Inventory Service (FastAPI + SQLite)

Features:
- CRUD de produtos (SKU, nome, unidade, estoque mínimo)
- Lançamentos de estoque (entrada/saída) com histórico
- Endpoint para consultar saldo atual e abaixo do mínimo
- Transações atômicas (SQLite) para evitar inconsistências

Como rodar:
1) pip install fastapi uvicorn sqlalchemy pydantic
2) uvicorn inventory_service_fastapi:app --reload

Exemplos rápidos:
- Criar produto:
  curl -X POST http://localhost:8000/products -H 'Content-Type: application/json' \
       -d '{"sku":"ABC-001","name":"Álcool 70%","unit":"un","min_stock":10}'
- Entrada de estoque:
  curl -X POST http://localhost:8000/products/1/movements -H 'Content-Type: application/json' \
       -d '{"change": 50, "kind": "IN", "note": "Compra"}'
- Saída de estoque:
  curl -X POST http://localhost:8000/products/1/movements -H 'Content-Type: application/json' \
       -d '{"change": 5, "kind": "OUT", "note": "Venda"}'
- Saldo atual de todos:
  curl http://localhost:8000/stock

"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Literal, Dict

from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, Field, constr
from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, ForeignKey, CheckConstraint, Text,
    func, select
)
from sqlalchemy.orm import declarative_base, relationship, Session, sessionmaker

# ===========================
# DB setup
# ===========================
DATABASE_URL = "sqlite:///./inventory.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ===========================
# Models
# ===========================
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    unit = Column(String(16), nullable=False, default="un")
    min_stock = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    movements = relationship("StockMovement", back_populates="product", cascade="all, delete-orphan")


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    # change > 0 sempre. A direção (IN/OUT) é marcada em kind
    change = Column(Integer, nullable=False)
    kind = Column(String(3), nullable=False)  # IN | OUT
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    __table_args__ = (
        CheckConstraint("change > 0", name="ck_change_positive"),
        CheckConstraint("kind IN ('IN','OUT')", name="ck_kind_valid"),
    )

    product = relationship("Product", back_populates="movements")


# ===========================
# Schemas
# ===========================
SkuType = constr(strip_whitespace=True, min_length=1, max_length=64)
UnitType = constr(strip_whitespace=True, min_length=1, max_length=16)

class ProductCreate(BaseModel):
    sku: SkuType
    name: constr(strip_whitespace=True, min_length=1, max_length=255)
    unit: UnitType = "un"
    min_stock: int = Field(0, ge=0)

class ProductUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1, max_length=255)] = None
    unit: Optional[UnitType] = None
    min_stock: Optional[int] = Field(None, ge=0)

class ProductOut(BaseModel):
    id: int
    sku: str
    name: str
    unit: str
    min_stock: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MovementCreate(BaseModel):
    change: int = Field(..., gt=0)
    kind: Literal["IN", "OUT"]
    note: Optional[str] = None

class MovementOut(BaseModel):
    id: int
    product_id: int
    change: int
    kind: Literal["IN", "OUT"]
    note: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class StockSnapshot(BaseModel):
    product_id: int
    sku: str
    name: str
    unit: str
    min_stock: int
    current_stock: int
    below_minimum: bool

# ===========================
# FastAPI app
# ===========================
app = FastAPI(title="Inventory Service", version="1.0.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables
Base.metadata.create_all(bind=engine)

# ===========================
# Helpers
# ===========================

def compute_stock_for_product(db: Session, product_id: int) -> int:
    # Sum IN as +change and OUT as -change
    stmt_in = select(func.coalesce(func.sum(StockMovement.change), 0)).where(
        StockMovement.product_id == product_id, StockMovement.kind == "IN"
    )
    stmt_out = select(func.coalesce(func.sum(StockMovement.change), 0)).where(
        StockMovement.product_id == product_id, StockMovement.kind == "OUT"
    )
    total_in = db.execute(stmt_in).scalar_one()
    total_out = db.execute(stmt_out).scalar_one()
    return int(total_in) - int(total_out)


def product_to_snapshot(db: Session, p: Product) -> StockSnapshot:
    current = compute_stock_for_product(db, p.id)
    return StockSnapshot(
        product_id=p.id,
        sku=p.sku,
        name=p.name,
        unit=p.unit,
        min_stock=p.min_stock,
        current_stock=current,
        below_minimum=current < p.min_stock,
    )

# ===========================
# Product Endpoints
# ===========================
@app.post("/products", response_model=ProductOut, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    # SKU must be unique
    existing = db.execute(select(Product).where(Product.sku == payload.sku)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="SKU já existe")

    p = Product(sku=payload.sku, name=payload.name, unit=payload.unit, min_stock=payload.min_stock)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@app.get("/products", response_model=List[ProductOut])
def list_products(q: Optional[str] = Query(None, description="Busca por nome ou SKU"), db: Session = Depends(get_db)):
    stmt = select(Product)
    if q:
        pattern = f"%{q}%"
        stmt = stmt.where((Product.name.ilike(pattern)) | (Product.sku.ilike(pattern)))
    stmt = stmt.order_by(Product.id.desc())
    rows = db.execute(stmt).scalars().all()
    return rows


@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    p = db.get(Product, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return p


@app.patch("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    p = db.get(Product, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    if payload.name is not None:
        p.name = payload.name
    if payload.unit is not None:
        p.unit = payload.unit
    if payload.min_stock is not None:
        p.min_stock = payload.min_stock
    db.commit()
    db.refresh(p)
    return p


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    p = db.get(Product, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(p)
    db.commit()
    return None

# ===========================
# Stock Endpoints
# ===========================
@app.post("/products/{product_id}/movements", response_model=MovementOut, status_code=201)
def create_movement(product_id: int, payload: MovementCreate, db: Session = Depends(get_db)):
    p = db.get(Product, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Prevent negative stock on OUT
    if payload.kind == "OUT":
        current = compute_stock_for_product(db, product_id)
        if payload.change > current:
            raise HTTPException(status_code=409, detail=f"Saída maior que o saldo atual ({current} {p.unit})")

    m = StockMovement(product_id=product_id, change=payload.change, kind=payload.kind, note=payload.note)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@app.get("/products/{product_id}/movements", response_model=List[MovementOut])
def list_movements(product_id: int, db: Session = Depends(get_db)):
    p = db.get(Product, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    stmt = (
        select(StockMovement)
        .where(StockMovement.product_id == product_id)
        .order_by(StockMovement.created_at.desc(), StockMovement.id.desc())
    )
    return db.execute(stmt).scalars().all()


@app.get("/stock", response_model=List[StockSnapshot])
def list_stock(
    q: Optional[str] = Query(None, description="Busca por nome ou SKU"),
    only_below_min: bool = Query(False, description="Apenas itens abaixo do mínimo"),
    db: Session = Depends(get_db),
):
    stmt = select(Product)
    if q:
        pattern = f"%{q}%"
        stmt = stmt.where((Product.name.ilike(pattern)) | (Product.sku.ilike(pattern)))
    products = db.execute(stmt).scalars().all()
    snapshots = [product_to_snapshot(db, p) for p in products]
    if only_below_min:
        snapshots = [s for s in snapshots if s.below_minimum]
    # Ordena: abaixo do mínimo primeiro, depois por nome
    snapshots.sort(key=lambda s: (not s.below_minimum, s.name.lower()))
    return snapshots


@app.get("/products/{product_id}/stock", response_model=StockSnapshot)
def get_product_stock(product_id: int, db: Session = Depends(get_db)):
    p = db.get(Product, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product_to_snapshot(db, p)


# ===========================
# Health & meta
# ===========================
@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "time": datetime.utcnow().isoformat()}
