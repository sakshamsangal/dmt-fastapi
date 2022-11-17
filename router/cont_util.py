from fastapi import APIRouter
from pydantic import BaseModel
import os

import service.xml_split as chunk

util = APIRouter()


class DirMaker(BaseModel):
    folder_name: list
    loc: str
    # ct: Optional[str] = None


class XMLChunk(BaseModel):
    loc: str
    ct: str
    tag_selected: object
    all_dir: bool
    prod_names: list


@util.post("/dir-maker", status_code=201)
async def create_item(item: DirMaker):
    loc = item.loc
    print(item.folder_name)
    for x in item.folder_name:
        for y in ['xml', 'excel', 'word', 'pdf', 'res']:
            os.makedirs(f'{loc}/{x}/{y}', exist_ok=True)
        os.makedirs(f'{loc}/{x}/xml/xml_{x}_orig', exist_ok=True)
        os.makedirs(f'{loc}/{x}/xml/xml_{x}_chunk', exist_ok=True)
        os.makedirs(f'{loc}/{x}/xml/xml_{x}_zip', exist_ok=True)
    return item


@util.post('/xml-chunk', status_code=201)
def xml_chunk(item: XMLChunk):
    print(item)
    ct = item.ct
    loc = item.loc
    tag_selected = item.tag_selected
    prod_names = item.prod_names
    all_dir = item.all_dir
    chunk.process_xml_chunk(loc, ct, tag_selected, all_dir, prod_names)
    return {'ct': ct, 'loc': loc, 'status': True, 'tag_selected': tag_selected}
