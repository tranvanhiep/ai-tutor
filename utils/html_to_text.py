import os
import pytesseract
from PIL import Image
from html2image import Html2Image

class HTMLToText:
    """Class to handle HTML to text conversion via image processing"""

    def __init__(self, output_path='temp', lang='jpn'):
        """
        Initialize HTMLToText converter
        Args:
            output_path (str): Path to store temporary images
            lang (str): Language for OCR (default: Japanese)
        """
        self.output_path = output_path
        self.lang = lang
        self._setup_output_dir()

    def _setup_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def html_to_image(self, html_content, id):
        """Convert HTML content to image with settings optimized for Japanese text"""
        if not html_content:
            return None

        try:
            # Initialize Html2Image with updated settings for new headless mode
            hti = Html2Image(
                output_path=self.output_path,
                size=(1024, 768),
                custom_flags=[
                    '--headless=new',
                    '--disable-gpu',
                    '--force-device-scale-factor=2',
                    '--hide-scrollbars',
                    '--virtual-time-budget=5000'
                ]
            )

            # Generate unique filename
            filename = f"question_{id}.png"

            # Convert HTML to image
            hti.screenshot(
                html_str=html_content,
                save_as=filename
            )

            return os.path.join(self.output_path, filename)
        except Exception as e:
            print(f"Error converting HTML to image: {e}")
            return None

    def image_to_text(self, image_path):
        """Convert image content to text using OCR with language configuration"""
        try:
            image = Image.open(image_path)

            # Configure pytesseract
            custom_config = f'--oem 3 --psm 6 -l {self.lang}'
            text = pytesseract.image_to_string(
                image,
                lang=self.lang,
                config=custom_config
            )

            return text.strip()
        except Exception as e:
            print(f"Error converting image to text: {e}")
            return None

    def process_content(self, content, content_type, item_id):
        """
        Process HTML content and convert to text
        Args:
            content (dict or str): Content to process
            content_type (str): Type of content ('question' or 'answer')
            item_id (str): Problem item ID
        Returns:
            tuple: (extracted_text, image_path) or (text_content, None)
        """
        if content_type == 'question':
            has_html = '<' in content['item_description'] or '<' in content['question']
            html_content = f"""
            <div style="font-family: 'Noto Sans JP', Arial, sans-serif; padding: 20px;">
                <div>{content['item_description']}</div>
                <div>{content['question']}</div>
            </div>
            """ if has_html else None
            text_content = f"{content['item_description']}\n{content['question']}"
        else:  # answer
            has_html = '<' in content
            html_content = f"""
            <div style="font-family: 'Noto Sans JP', Arial, sans-serif; padding: 20px;">
                <div>{content['answer']}</div>
            </div>
            """ if has_html else None
            text_content = content['answer']

        if has_html:
            image_path = self.html_to_image(html_content, f"{item_id}_{content_type}")
            if image_path is None:
                print(f"Error converting {content_type} HTML to image")
                raise ValueError("Error converting HTML to image")

            extracted_text = self.image_to_text(image_path)
            if extracted_text is None:
                print(f"Error converting {content_type} image to text")
                raise ValueError("Error converting image to text")

            return extracted_text, image_path

        return text_content, None

    @staticmethod
    def cleanup_temp_files(image_path):
        """Remove temporary image files"""
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            print(f"Error cleaning up temporary file: {e}")
