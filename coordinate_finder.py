"""
Interactive coordinate finder for insurance documents
Helps users find precise coordinates for field extraction

Usage: python coordinate_finder.py path/to/image.png
"""
import cv2
import sys
from pathlib import Path

class CoordinateFinder:
    """Interactive tool to find coordinates in images"""
    
    def __init__(self, image_path):
        self.image_path = image_path
        self.img = None
        self.display_img = None
        self.drawing = False
        self.start_point = None
        self.rectangles = []
        self.current_rect = None
        self.field_name = ""
        
    def load_image(self):
        """Load the image"""
        self.img = cv2.imread(str(self.image_path))
        if self.img is None:
            raise ValueError(f"Could not load image: {self.image_path}")
        
        # Create a copy for display
        self.display_img = self.img.copy()
        
    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events for rectangle drawing"""
        
        if event == cv2.EVENT_LBUTTONDOWN:
            # Start drawing
            self.drawing = True
            self.start_point = (x, y)
            
        elif event == cv2.EVENT_MOUSEMOVE:
            # Update current rectangle while drawing
            if self.drawing:
                temp_img = self.display_img.copy()
                cv2.rectangle(temp_img, self.start_point, (x, y), (0, 255, 0), 2)
                cv2.imshow('Coordinate Finder', temp_img)
                
        elif event == cv2.EVENT_LBUTTONUP:
            # Finish drawing
            self.drawing = False
            end_point = (x, y)
            
            # Calculate rectangle coordinates
            x1 = min(self.start_point[0], end_point[0])
            y1 = min(self.start_point[1], end_point[1])
            x2 = max(self.start_point[0], end_point[0])
            y2 = max(self.start_point[1], end_point[1])
            
            width = x2 - x1
            height = y2 - y1
            
            # Store the rectangle
            self.current_rect = {
                'coords': (x1, y1, width, height),
                'start': (x1, y1),
                'end': (x2, y2)
            }
            
            # Draw the rectangle
            cv2.rectangle(self.display_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.imshow('Coordinate Finder', self.display_img)
            
            # Print coordinates
            self.print_coordinates()
            
    def print_coordinates(self):
        """Print the current rectangle coordinates"""
        if self.current_rect:
            x, y, w, h = self.current_rect['coords']
            print("\n" + "="*60)
            print(f"Coordinates: ({x}, {y}, {w}, {h})")
            print("="*60)
            print("Python format:")
            print(f"'{self.field_name}': ({x}, {y}, {w}, {h}),")
            print("="*60)
            
    def run(self):
        """Run the coordinate finder"""
        
        print("\n" + "="*60)
        print("Interactive Coordinate Finder")
        print("="*60)
        print("\nInstructions:")
        print("1. Click and drag to draw a rectangle around a field")
        print("2. Coordinates will be displayed in the terminal")
        print("3. Press 's' to save current rectangle")
        print("4. Press 'c' to clear all rectangles")
        print("5. Press 'r' to reset image")
        print("6. Press 'q' to quit")
        print("="*60)
        print()
        
        # Load image
        self.load_image()
        
        # Create window and set mouse callback
        cv2.namedWindow('Coordinate Finder')
        cv2.setMouseCallback('Coordinate Finder', self.mouse_callback)
        
        # Display image
        cv2.imshow('Coordinate Finder', self.display_img)
        
        saved_fields = []
        
        while True:
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                # Quit
                break
                
            elif key == ord('s'):
                # Save current rectangle
                if self.current_rect:
                    field_name = input("\nEnter field name (e.g., 'policy_number'): ").strip()
                    if field_name:
                        self.field_name = field_name
                        saved_fields.append({
                            'name': field_name,
                            'coords': self.current_rect['coords']
                        })
                        self.rectangles.append(self.current_rect)
                        print(f"✓ Saved: {field_name}")
                        self.current_rect = None
                        
            elif key == ord('c'):
                # Clear all rectangles
                self.display_img = self.img.copy()
                self.rectangles = []
                self.current_rect = None
                saved_fields = []
                cv2.imshow('Coordinate Finder', self.display_img)
                print("\n✓ Cleared all rectangles")
                
            elif key == ord('r'):
                # Reset to original image
                self.display_img = self.img.copy()
                # Redraw saved rectangles
                for rect in self.rectangles:
                    cv2.rectangle(self.display_img, rect['start'], 
                                rect['end'], (0, 255, 0), 2)
                cv2.imshow('Coordinate Finder', self.display_img)
                print("\n✓ Reset image")
        
        cv2.destroyAllWindows()
        
        # Print summary
        if saved_fields:
            print("\n" + "="*60)
            print("SAVED FIELDS SUMMARY")
            print("="*60)
            print("\nCopy this to your template_manager.py:")
            print("\n'your_company': {")
            for field in saved_fields:
                x, y, w, h = field['coords']
                print(f"    '{field['name']}': ({x}, {y}, {w}, {h}),")
            print("}")
            print("\n" + "="*60)

def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        print("Usage: python coordinate_finder.py <image_path>")
        print("\nExample:")
        print("  python coordinate_finder.py documents/sample.png")
        sys.exit(1)
    
    image_path = Path(sys.argv[1])
    
    if not image_path.exists():
        print(f"Error: File not found: {image_path}")
        sys.exit(1)
    
    try:
        finder = CoordinateFinder(image_path)
        finder.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()