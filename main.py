import os
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from tryon import generate_virtual_tryon

app = FastAPI()

@app.post("/tryon")
async def try_on(person: UploadFile = File(...), cloth: UploadFile = File(...)):
    os.makedirs("static", exist_ok=True)
    person_path = f"static/{person.filename}"
    cloth_path = f"static/{cloth.filename}"
    output_path = f"static/result_{person.filename}"

    with open(person_path, "wb") as f:
        f.write(await person.read())
    with open(cloth_path, "wb") as f:
        f.write(await cloth.read())

    result_path = generate_virtual_tryon(person_path, cloth_path, output_path)
    return FileResponse(result_path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
