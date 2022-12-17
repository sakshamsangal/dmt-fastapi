import time

from fastapi import APIRouter
from pydantic import BaseModel

import os

from starlette.responses import StreamingResponse

import service.xml_split as chunk

util = APIRouter()


class DirMaker(BaseModel):
    ct: str
    loc: str
    # ct: Optional[str] = None


class XMLChunk(BaseModel):
    loc: str
    ct: str
    tag_selected: str
    att_sel: str
    all: bool
    prod: list


@util.post("/dir-maker", status_code=201)
async def create_item(item: DirMaker):
    try:
        loc = item.loc
        print(item.ct)
        # for x in item.ct:
        for y in ['xml', 'excel', 'word', 'pdf', 'res']:
            os.makedirs(f'{loc}/{item.ct}/{y}', exist_ok=True)
        os.makedirs(f'{loc}/{item.ct}/xml/xml_{item.ct}_orig', exist_ok=True)
        os.makedirs(f'{loc}/{item.ct}/xml/xml_{item.ct}_chunk', exist_ok=True)
        os.makedirs(f'{loc}/{item.ct}/xml/xml_{item.ct}_zip', exist_ok=True)
        return {"status": 'success'}
        # return {"status": 'success', 'time': str(datetime.now())}
    except Exception as e:
        return str(e)


# async def fake_video_streamer():
#     for i in range(5):
#         yield b"some fake video bytes"
#         time.sleep(1)

    # yield b"AKSHU<br>"
    # time.sleep(2)
    # yield b"some fake video bytes<br>"
    # time.sleep(2)
    # yield b"AKSHU<br>"


@util.post('/xml-chunk', status_code=201)
async def xml_chunk(item: XMLChunk):
    try:
        print(item)
        return StreamingResponse(chunk.process_xml_chunk(item.loc, item.ct, item.tag_selected, item.att_sel, item.all, item.prod),
                                 media_type="text/html")
        # return {"status": 'success'}
    except Exception as e:
        return str(e)


@util.post('/dir')
def get_dir(item: DirMaker):
    try:
        print(item)
        ls = chunk.get_folder_name(item.loc, item.ct)
        print(ls)
        return {"status": 'success', 'ls': ls}
    except Exception as e:
        return str(e)
