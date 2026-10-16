
from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path

# Locate the original photo
folder = Path(__file__).parent
input_path = folder / "assets" / "profile.jpg"
output_path = folder / "assets" / "profile-prepped.png"

# Open the photo
image = Image.open(input_path).convert("RGB")

# Crop to a portrait format
image = ImageOps.fit(image, (400, 500))

# Convert to black and white
image = ImageOps.grayscale(image)

# Increase contrast for clearer ASCII characters
image = ImageEnhance.Contrast(image).enhance(1.8)

# Save the prepared image
image.save(output_path)

print("Photo prepared successfully!")
print(f"Saved to: {output_path}")
