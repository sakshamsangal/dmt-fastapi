from fastapi import APIRouter
from pydantic import BaseModel

import service.xml_split as chunk

ch = APIRouter()


class XMLChunk(BaseModel):
    loc: str
    ct: str
    tag_selected: object
    all_dir: bool
    prod_names: list


@ch.post('/xml-chunk', status_code=201)
def xml_chunk(item: XMLChunk):
    print(item)
    ct = item.ct
    loc = item.loc
    tag_selected = item.tag_selected
    prod_names = item.prod_names
    all_dir = item.all_dir
    chunk.process_xml_chunk(loc, ct, tag_selected, all_dir, prod_names)
    return {'ct': ct, 'loc': loc, 'status': True, 'tag_selected': tag_selected}
