from fastapi import FastAPI, Request,Body,Form
from fastapi.responses import HTMLResponse , JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Optional, List, Dict , Union
import base64
import matplotlib.pyplot as plt
import io
from config.database import Session, engine,Base
from models.db_estadisticas import Db_estadisticas
from fastapi.encoders import jsonable_encoder
app = FastAPI()
templates = Jinja2Templates(directory="templates")
Base.metadata.create_all(bind=engine)

estats = {
    "nombre":['a'],
    "correo":['aaaaaaa@aaaa'],
    "ingenieria": [1],
    "medicina": [1],
    "economia": [1],
}
class stat(BaseModel):
    id: Optional[int]=None
    nombre: str = Field(min_lenght=1,max_length=30)
    correo: str = Field(min_lenght=1,max_length=50)
    ingenieria: int = Field(le=2022)
    medicina: int = Field(le=2022)
    economia: int = Field(le=2022)
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/estadisticas", response_class=JSONResponse)
def estadisticas()->List[stat]:
    db = Session()
    resultado=db.query(Db_estadisticas).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(resultado))

@app.post("/vocacional", response_class=HTMLResponse)
async def procesar_respuestas(
    nombre: str = Form(...),
    correo: str = Form(...),
    pregunta1: int = Form(...),
    pregunta2: int = Form(...),
    pregunta3: int = Form(...),
    pregunta4: int = Form(...),
    pregunta5: int = Form(...),
    pregunta6: int = Form(...),
    pregunta7: int = Form(...),
    pregunta8: int = Form(...),
    pregunta9: int = Form(...),
):
    # Realizar cálculos y generar el gráfico

    ingenieria = pregunta1 + pregunta2 + pregunta3 + pregunta4
    carreras_medicina = pregunta5 + pregunta6 + pregunta7 + pregunta8
    sociedad_economia = pregunta9
    puntajes = [ingenieria, carreras_medicina, sociedad_economia]
    areas = ['Ingeniería', 'Carreras de Medicina', 'Sociedad/Economía']


    med=0
    ing=0
    soc=0
    if ingenieria>carreras_medicina and ingenieria>sociedad_economia:
        ing=1
    elif carreras_medicina > ingenieria and carreras_medicina> sociedad_economia:
        med=1
    elif sociedad_economia> ingenieria and sociedad_economia>carreras_medicina:
        soc=1
    else:
        ing=0
        med=0
        soc=0     
    Nombre=nombre
    Correo=correo      
    estats["nombre"].append(nombre)
    estats["correo"].append(correo)
    estats["ingenieria"].append(ing)
    estats["medicina"].append(med)
    estats["economia"].append(soc)

    plt.figure(figsize=(8, 6))
    plt.bar(areas, puntajes, color='skyblue')
    plt.title('Puntajes por área de interés')
    plt.xlabel('Área de interés')
    plt.ylabel('Puntaje')
    plt.ylim(0, max(puntajes) + 10)
    plt.grid(axis='y')
    plt.tight_layout()

    # Guardar el gráfico en un objeto BytesIO
    img_bytesio = io.BytesIO()
    plt.savefig(img_bytesio, format='png')
    img_bytesio.seek(0)

    # Convertir la imagen a formato base64
    img_base64 = base64.b64encode(img_bytesio.read()).decode('utf-8')
    db = Session()
    new_Db = Db_estadisticas(nombre=Nombre, correo=Correo, ingenieria=ing, medicina=med, economia=soc)
    db.add(new_Db)
    db.commit()
    # Formar el HTML con la imagen y el botón
    html_response = f'''
        <img src="data:image/png;base64,{img_base64}" alt="Gráfico de puntajes">
        <form action="/estadisticas">
        <button type="submit">Ver estadísticas</button>
        </form>
    '''

    return HTMLResponse(content=html_response, status_code=200)