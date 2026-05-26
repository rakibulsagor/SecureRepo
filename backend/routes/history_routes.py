from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from backend.services.firebase_service import FirebaseService

router = APIRouter()
firebase_service = FirebaseService()

@router.get("/scans/{user_id}", response_model=List[Dict[str, Any]])
def get_user_scan_history(user_id: str):
    """Retrieves previous scans performed by a specific user."""
    try:
        scans = firebase_service.get_user_scans(user_id)
        return scans
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch scan history: {str(e)}")

@router.delete("/scan/{scan_id}")
def delete_scan_record(scan_id: str):
    """Deletes a completed scan from user history."""
    success = firebase_service.delete_scan(scan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Scan record not found or could not be deleted.")
    return {"status": "success", "message": f"Scan {scan_id} deleted successfully."}
