from fastapi import APIRouter

from dbs_assignment.endpoints import users, cards

router = APIRouter()

router.include_router(users.router, tags=["users"])
router.include_router(cards.router, tags=["cards"])

