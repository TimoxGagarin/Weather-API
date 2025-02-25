from fastapi import HTTPException, status

CityDoesntExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="City doesn't exist"
)
