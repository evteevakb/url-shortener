"""Contains API endpoints"""
import time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from ...db.db import get_session

router = APIRouter()



