from fastapi import APIRouter

router = APIRouter(prefix="/faq", tags=["faq"])

@router.get("/")
async def get_faq():
    return {"faqs": [], "message": "FAQ list"}

@router.get("/test")
async def test():
    return {"message": "FAQ router is working"}
