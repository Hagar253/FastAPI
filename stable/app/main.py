from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from io import BytesIO
from app.model import generate_furnished_room 

app = FastAPI()

@app.post("/generate-room/")
async def generate_room(
    file: UploadFile = File(...),  # File input (the empty room image)
    room_type: str = Form(...),    # Room type (bedroom, living room, etc.)
    style: str = Form(...),        # Design style (classic, bohemian, modern)
    room_dimensions: str = Form(...),  # Room dimensions (e.g., "4x8")
):
    # Save the uploaded file to a temporary location in memory
    image_bytes = await file.read()
    image_stream = BytesIO(image_bytes)
    
    # Generate the furnished room image using the model
    furnished_image = generate_furnished_room(
        image_stream, 
        room_type, 
        style, 
        room_dimensions
    )
    
    # Convert the image to a byte stream to send as response
    img_byte_arr = BytesIO()
    furnished_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")
