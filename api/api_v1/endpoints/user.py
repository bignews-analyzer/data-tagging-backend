from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def test_user():
    return 'user'
