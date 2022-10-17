
import io
import sys
from sqlalchemy import create_engine, MetaData
from sqlacodegen.codegen import CodeGenerator

def generate_model(url_src, schema=None, outfile=None):
    engine = create_engine(url_src)
    metadata = MetaData(bind=engine)
    if schema:
        metadata.reflect(schema=schema)
    else:
        metadata.reflect()
    outfile = io.open(
        outfile, 'w', encoding='utf-8') if outfile else sys.stdout
    generator = CodeGenerator(metadata)
    generator.render(outfile)
