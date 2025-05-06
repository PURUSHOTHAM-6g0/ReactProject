from fastapi import APIRouter, UploadFile, File, Depends ,HTTPException,Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from PyPDF2 import PdfReader
from app.database import get_db
from app.services.resume_parser import parse_resume_with_openai
from app.services.resume_generator import generate_resume_from_parsed_data
from auth.auth import JWTBearer
from io import BytesIO
from fastapi.responses import StreamingResponse

router = APIRouter(dependencies=[Depends(JWTBearer())])

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    pdf = PdfReader(file.file)
    text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    parsed_data = await parse_resume_with_openai(text)
    return parsed_data
@router.post("/download_resume")
async def download_resume(parsed_data: dict = Body(...)):  # Accept as generic dict
    try:
        # Call function to generate PDF from parsed data
        pdf_bytes = generate_resume_from_parsed_data(parsed_data)  # No need to call `.dict()`
        buffer = BytesIO(pdf_bytes)

        return StreamingResponse(buffer, media_type="application/pdf", headers={
            "Content-Disposition": "attachment; filename=resume.pdf"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating resume: {str(e)}")