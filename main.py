import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from router import cont_dm_sheet
from router import cont_xml_chunk

app = FastAPI()

app.include_router(cont_dm_sheet.dm)
app.include_router(cont_xml_chunk.ch)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", reload=True)
