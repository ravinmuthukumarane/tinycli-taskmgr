# create_timeline.py (Final Version with Boundary Checks)

from PIL import Image, ImageDraw, ImageFont
from datetime import date

# Helper class to manage label positions for collision detection
class Label:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def collides_with(self, other_label, padding=5):
        if (self.x < other_label.x + other_label.width + padding and
            self.x + self.width + padding > other_label.x and
            self.y < other_label.y + other_label.height + padding and
            self.y + self.height + padding > other_label.y):
            return True
        return False

def generate_timeline_image(projected_date: date, output_filename: str):
    """
    Generates a timeline image with boundary checks to prevent text clipping.
    """
    # --- Configuration ---
    img_width = 500
    img_height = 100 
    bar_y_start = 35 
    bar_height = 25
    text_label_y = 10 
    date_label_y_initial = bar_y_start + bar_height + 5
    date_label_y_collision_offset = 15

    # Colors
    color_bg = (255, 255, 255)
    color_green = (46, 204, 113)
    color_red = (231, 76, 60)
    color_text = (50, 50, 50)
    color_line = (180, 180, 180)

    # --- Date Logic ---
    target_date = date(projected_date.year, 1, 31)
    start_date = date(projected_date.year, 1, 1)
    end_of_scale_date = max(target_date, projected_date)
    total_days_in_scale = (end_of_scale_date - start_date).days

    if total_days_in_scale == 0:
        total_days_in_scale = 1
        
    def date_to_x(d: date) -> int:
        days_from_start = (d - start_date).days
        return int((days_from_start / total_days_in_scale) * (img_width - 1))

    # --- Image Drawing ---
    image = Image.new('RGB', (img_width, img_height), color_bg)
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except IOError:
        font = ImageFont.load_default()

    bbox = font.getbbox("Tg")
    font_height = bbox[3] - bbox[1]
    placed_date_labels = []
    placed_top_labels = []  # Track top labels (Target/Projected) for collision detection

    # Helper function to calculate a safe X position for a label
    def get_safe_text_x(x_pos, text_width):
        # --- FIX: This is the core logic to prevent clipping ---
        # 1. Try to center the text
        centered_x = x_pos - text_width // 2
        # 2. Prevent it from going off the left edge (x < 0)
        safe_x = max(0, centered_x)
        # 3. Prevent it from going off the right edge
        # The maximum x can be is the image width minus the text width
        safe_x = min(safe_x, img_width - text_width)
        return safe_x

    def add_date_label_with_collision_check(date_obj, x_pos, marker_color=color_text):
        label_text = date_obj.strftime('%b %d')
        text_width = font.getlength(label_text)
        
        # Use the helper function to get a safe X position
        text_x = get_safe_text_x(x_pos, text_width)
        current_y = date_label_y_initial
        
        new_label = Label(text_x, current_y, text_width, font_height, label_text)

        # Check collision with existing date labels
        for existing_label in placed_date_labels:
            if new_label.collides_with(existing_label):
                new_label.y = existing_label.y + font_height + date_label_y_collision_offset
        
        # Check collision with top labels (Target/Projected)
        for top_label in placed_top_labels:
            if new_label.collides_with(top_label):
                new_label.y = max(new_label.y, top_label.y + font_height + date_label_y_collision_offset)
        
        draw.line([x_pos, bar_y_start, x_pos, bar_y_start + bar_height + 5], fill=marker_color, width=1)
        draw.text((new_label.x, new_label.y), new_label.text, fill=color_text, font=font)
        placed_date_labels.append(new_label)

    # --- Draw Bars and Text Based on the Scenario ---
    target_x = date_to_x(target_date)
    projected_x = date_to_x(projected_date)

    # Calculate safe positions for the top labels ("Target", "Projected")
    target_label_text = "Target"
    target_label_width = font.getlength(target_label_text)
    target_label_x = get_safe_text_x(target_x, target_label_width)

    projected_label_text = "Projected"
    projected_label_width = font.getlength(projected_label_text)
    projected_label_x = get_safe_text_x(projected_x, projected_label_width)
    
    # Draw bars based on scenario
    if projected_date <= target_date:
        draw.rectangle([0, bar_y_start, projected_x, bar_y_start + bar_height], fill=color_green)
    else:
        draw.rectangle([0, bar_y_start, target_x, bar_y_start + bar_height], fill=color_green)
        draw.rectangle([target_x, bar_y_start, projected_x, bar_y_start + bar_height], fill=color_red)

    # Draw Text Labels with collision detection
    target_label_y = text_label_y
    projected_label_y = text_label_y
    
    # Create label objects to check for collision
    target_label = Label(target_label_x, target_label_y, target_label_width, font_height, target_label_text)
    projected_label = Label(projected_label_x, projected_label_y, projected_label_width, font_height, projected_label_text)
    
    # Check if top labels collide and adjust projected label if needed
    if target_label.collides_with(projected_label, padding=3):
        # Move the projected label down to avoid collision
        projected_label_y = target_label_y + font_height + 2
        projected_label = Label(projected_label_x, projected_label_y, projected_label_width, font_height, projected_label_text)
    
    # Draw the labels
    draw.text((target_label_x, target_label_y), target_label_text, fill=color_text, font=font)
    draw.text((projected_label_x, projected_label_y), projected_label_text, fill=color_text, font=font)
    
    # Store top labels for collision detection with date labels
    placed_top_labels.append(target_label)
    placed_top_labels.append(projected_label)
    
    add_date_label_with_collision_check(target_date, target_x, marker_color=color_line)
    add_date_label_with_collision_check(projected_date, projected_x)
        
    image.save(output_filename)
    print(f"✅ Image saved as '{output_filename}'")


# --- Main execution block ---
if __name__ == "__main__":
    print("Generating timeline images with boundary checks...")

    # Projected date far behind target (should be right-aligned)
    generate_timeline_image(
        projected_date=date(2026, 2, 28), 
        output_filename="timeline_far_behind_v3.png"
    )

    # Projected date slightly behind target (dates below should shift)
    generate_timeline_image(
        projected_date=date(2026, 2, 1),
        output_filename="timeline_close_behind_v3.png"
    )

    # Projected date on track, close to target (dates below should shift)
    generate_timeline_image(
        projected_date=date(2026, 1, 28),
        output_filename="timeline_close_on_track_v3.png"
    )
    
    # Projected date far on track (should be centered)
    generate_timeline_image(
        projected_date=date(2026, 1, 15), 
        output_filename="timeline_far_on_track_v3.png"
    )

    print("\nDone!")