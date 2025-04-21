from diffusers import StableDiffusionImg2ImgPipeline
import torch
from PIL import Image
import io

# Load the img2img model (use a specific model ID)
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe.to("cuda")

# Predefined styles for the room
styles = {
    "classic": "Classic luxury design with elegant decor, gold detailing, vintage furniture, warm lighting",
    "bohemian": "Bohemian design with natural wooden furniture, handcrafted rustic decor, earthy colors, woven textures",
    "modern": "Modern minimalist design with sleek furniture, neutral colors, open space, and clean aesthetics"
}

# Predefined room types
room_types = {
    "bedroom": "a cozy and well-arranged bedroom with stylish furniture",
    "living room": "a comfortable and elegant living room with carefully arranged seating and lighting",
    "dining room": "a sophisticated dining room with a well-set dining table and modern lighting"
}

def generate_furnished_room(empty_room_stream, room_type, style, room_dimensions, strength=0.7):
    """Generate a furnished room image based on an empty room image, style, and room type."""
    if style not in styles or room_type not in room_types:
        raise ValueError("Invalid room type or style! Please choose from the available options.")

    # Load the empty room image from the byte stream
    init_image = Image.open(empty_room_stream).convert("RGB").resize((512, 512))

    prompt = (
        f"{styles[style]} added to {room_types[room_type]}, "
        f"room size: {room_dimensions} meters. Ultra realistic, high quality, detailed lighting."
    )

    # Generate the furnished room image
    image = pipe(prompt=prompt, image=init_image, strength=strength, guidance_scale=7.5).images[0]

    return image
