
import qrcode
from qrcode.constants import ERROR_CORRECT_L

def generate_qr(data, path):
    """Generate QR code with optimized settings for faster generation"""
    # OPTIMIZED: Use faster QR code settings
    qr = qrcode.QRCode(
        version=1,  # Smaller version = faster generation
        error_correction=ERROR_CORRECT_L,  # Lower error correction = faster
        box_size=10,  # Smaller box size = faster rendering
        border=4,  # Standard border
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create image with optimized settings
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path, optimize=True)  # Optimize file size
