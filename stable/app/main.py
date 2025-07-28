# Import necessary modules from FastAPI and other Python libraries
from fastapi import FastAPI, File, UploadFile, Form  # To handle file and form inputs
from fastapi.responses import StreamingResponse       # To send the image back as a stream
from io import BytesIO                                # To handle in-memory file-like byte streams
from app.model import generate_furnished_room         # The function that generates the furnished room image

# Create a FastAPI instance
app = FastAPI()

# Define a POST endpoint for generating a furnished room image
@app.post("/generate-room/")
async def generate_room(
    file: UploadFile = File(...),              # Image file of the empty room, uploaded from frontend
    room_type: str = Form(...),                # Room type input (e.g., "bedroom", "kitchen")
    style: str = Form(...),                    # Style input (e.g., "modern", "bohemian")
    room_dimensions: str = Form(...),          # Room size (e.g., "4x8")
):
    # Step 1: Read the uploaded image file into memory
    image_bytes = await file.read()            # Read image as bytes
    image_stream = BytesIO(image_bytes)        # Convert bytes to a BytesIO object (acts like a file)

    # Step 2: Pass the image and form data to the model to generate a furnished room image
    furnished_image = generate_furnished_room(
        image_stream, 
        room_type, 
        style, 
        room_dimensions
    )

    # Step 3: Prepare the output image to be sent back to the client
    img_byte_arr = BytesIO()                   # Create a BytesIO object to hold the image in memory
    furnished_image.save(img_byte_arr, format="PNG")  # Save the furnished image into the BytesIO object
    img_byte_arr.seek(0)                       # Reset the stream position to the beginning

    # Step 4: Return the image as a streaming response (like downloading a file)
    return StreamingResponse(img_byte_arr, media_type="image/png")  # Send image back as PNG

