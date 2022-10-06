import os
import time

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from openpyxl import load_workbook
import service.mapping as mapping
import service.filling as filling
import service.master as tm
from fastapi.responses import StreamingResponse


class MapXpath(BaseModel):
    loc: str
    ct: str
    fn: str
    sn: str


class MSFileName(BaseModel):
    fn: str
    sn: str


class DMFileName(BaseModel):
    fn: str
    sn: str


class DMSheet(BaseModel):
    loc: str
    ct: str
    dm: DMFileName
    ms: MSFileName


class DirMaker(BaseModel):
    folder_name: list
    loc: str
    # ct: Optional[str] = None


class LocCt(BaseModel):
    loc: str
    ct: str


app = FastAPI()


@app.post("/dir-maker", status_code=201)
async def create_item(item: DirMaker):
    loc = item.loc
    print(item.folder_name)
    for x in item.folder_name:
        for y in ['xml', 'excel', 'word', 'pdf', 'res']:
            os.makedirs(f'{loc}/{x}/{y}', exist_ok=True)
        os.makedirs(f'{loc}/{x}/xml/ox_{x}', exist_ok=True)
        os.makedirs(f'{loc}/{x}/xml/cx_{x}', exist_ok=True)
        os.makedirs(f'{loc}/{x}/xml/zx_{x}', exist_ok=True)
    return item


@app.post("/dm-sheet", status_code=200)
async def dm_sheet(item: DMSheet):
    print(item)
    wb = load_workbook(f'{item.loc}/{item.ct}/excel/{item.ct}_rule.xlsx',
                       read_only=True)  # open an Excel file and return a workbook
    if 'tag_master' not in wb.sheetnames:
        tm.tag_master(item.loc, item.ct, item.ms.fn, item.ms.sn)
    if 'tag_map' not in wb.sheetnames:
        mapping.map_tag(item.loc, item.ct)
    mapping.map_xpath(item.loc, item.ct, item.dm.fn, item.dm.sn)
    mapping.map_tag(item.loc, item.ct)
    filling.fill_feat(item.loc, item.ct)
    x = filling.fill_comp_style(item.loc, item.ct)
    return x


@app.post("/tag-master", status_code=200)
async def tag_master(item: MapXpath):
    res = tm.tag_master(item.loc, item.ct, item.fn, item.sn)
    return {'status': res}


@app.post("/map-xpath", status_code=200)
async def map_xpath(item: MapXpath):
    res = mapping.map_xpath(item.loc, item.ct, item.fn, item.sn)
    return {'status': res}


@app.post("/fill-tm-by-dd", status_code=200)
async def fill_tm_by_dd(item: LocCt):
    res = filling.fill_tm_by_dd(item.loc, item.ct)
    return {'status': res}


@app.post("/map-tag", status_code=200)
async def map_tag(item: LocCt):
    res = mapping.map_tag(item.loc, item.ct)
    return {'status': res}


@app.post("/create-dd", status_code=200)
async def create_dd(item: LocCt):
    res = mapping.create_dd(item.loc, item.ct)
    return {'status': res}


@app.post("/fill-feat", status_code=200)
async def fill_feat(item: LocCt):
    res = filling.fill_feat(item.loc, item.ct)
    return {'status': res}


@app.post("/fill-comp-style", status_code=200)
async def fill_comp_style(item: LocCt):
    x = filling.fill_comp_style(item.loc, item.ct)
    return x


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", reload=True)


# '''
# .\venv\Scripts\activate
# uvicorn main:app --reload
# '''


async def fake_video_streamer():
    # for i in range(5):
    yield b"some fake video bytes<br>"
    time.sleep(2)
    yield b"AKSHU<br>"
    time.sleep(2)
    yield b"some fake video bytes<br>"
    time.sleep(2)
    yield b"AKSHU<br>"


@app.get("/")
async def main():
    return StreamingResponse(fake_video_streamer(), media_type="text/html")
