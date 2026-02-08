# Workflow Automation - AI-Powered Onboarding Form Generator

An automated workflow system that uses AI to create personalized onboarding forms by analyzing app store reviews and brand elements. This project demonstrates prompt engineering and workflow automation by scraping user reviews, extracting brand information, and generating customized onboarding experiences with AI-generated educational content.

## Overview

This project automates the creation of onboarding forms for mobile applications by:
1. **Scraping** user reviews from app stores (Google Play Store)
2. **Analyzing** reviews using GPT-4 to understand user needs and preferences
3. **Generating** structured onboarding forms with rating questions and educational content
4. **Extracting** brand elements (colors, fonts, logos) from screenshots
5. **Creating** AI-generated images for educational slides using DALL-E 3

## Features

- **Automated Review Scraping**: Uses Selenium and BeautifulSoup to scrape and parse app store reviews with infinite scroll handling
- **Intelligent Form Generation**: Leverages GPT-4 to create nuanced onboarding questions based on real user feedback
- **Brand Analysis**: Extracts brand colors, fonts, and visual elements from screenshots using OCR and image analysis
- **AI Image Generation**: Creates custom educational images for onboarding slides using DALL-E 3
- **JSON-Based Output**: Generates structured, machine-readable onboarding forms in JSON format

## Project Structure

### Core Modules

#### `scraping.py`
Web scraping module for extracting app store reviews:
- Uses Selenium WebDriver for handling dynamic content and infinite scrolling
- Implements headless Chrome for automated browsing
- Extracts review text from Google Play Store pages
- Returns structured review data with count information

#### `llm.py`
LLM integration for generating onboarding forms:
- Connects to OpenAI's GPT-4 API
- Processes scraped reviews to generate personalized onboarding questions
- Creates rating questions (1-5 scale) based on user feedback insights
- Generates educational content slides with H1/H2 text and image placeholders
- Outputs structured JSON with onboarding form questions and educational content

#### `brand_elements.py`
Brand analysis tool for extracting visual elements:
- Captures screenshots using PyAutoGUI
- Performs OCR text extraction with bounding box information using Tesseract
- Analyzes dominant colors from images
- Uses GPT-4 to identify brand's primary/secondary colors, font information, logo details, and button styling
- Saves brand information in JSON format

#### `image_generation.py`
AI image generation for educational content:
- Loads onboarding form data from JSON
- Generates image prompts based on educational slide headers
- Uses DALL-E 3 to create custom, text-free illustrations
- Downloads and saves generated images locally
- Updates JSON with image URLs and local file paths

## Installation

### Prerequisites

- Python 3.10 or higher
- Google Chrome browser (for Selenium)
- Tesseract OCR (for text extraction)
- OpenAI API key

### Dependencies

Install required Python libraries:

```bash
pip install beautifulsoup4 selenium webdriver-manager openai pillow numpy pytesseract requests pyautogui
```

**Required Libraries:**
- `beautifulsoup4` - HTML/XML parsing for web scraping
- `selenium` - Browser automation for dynamic content
- `webdriver-manager` - Automatic ChromeDriver management
- `openai` - OpenAI API integration (GPT-4 and DALL-E 3)
- `pillow` (PIL) - Image processing
- `numpy` - Numerical operations for color analysis
- `pytesseract` - OCR text extraction
- `requests` - HTTP requests for image downloads
- `pyautogui` - Screenshot capture

### Tesseract Installation

**Linux/Ubuntu:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download and install from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

## Configuration

1. Create an `api_key.txt` file in the project root directory
2. Add your OpenAI API key to the file:
```
sk-your-api-key-here
```

## Usage

### 1. Scrape App Reviews

The scraping module automatically runs when imported by `llm.py`:

```python
import scraping

# Reviews are automatically scraped from the configured URL
reviews = scraping.output['reviews']
review_count = scraping.output['review_count']
```

Default configuration scrapes Lumosity app reviews from Google Play Store.

### 2. Generate Onboarding Form

Run the LLM module to analyze reviews and create onboarding questions:

```bash
python llm.py
```

This will:
- Scrape reviews from the app store
- Send reviews to GPT-4 for analysis
- Generate structured onboarding questions
- Create educational content slides
- Save output to `output_response.json`

### 3. Extract Brand Elements

Capture and analyze brand elements from a screenshot:

```bash
python brand_elements.py
```

This will:
- Take a screenshot of your current screen
- Extract text and colors from the image
- Use GPT-4 to identify brand elements
- Save brand information to `brand_info.json`

### 4. Generate Educational Images

Create AI-generated images for educational slides:

```bash
python image_generation.py
```

This will:
- Load onboarding form data from `output_response.json`
- Generate custom images using DALL-E 3 for each educational slide
- Download images to the `images/` directory
- Update `updated_output_response.json` with image URLs and local paths

## Workflow

```
1. Scrape Reviews (scraping.py)
   └─> Extract user feedback from app store

2. Generate Form (llm.py)
   └─> Analyze reviews with GPT-4
   └─> Create onboarding questions and educational content
   └─> Output: output_response.json

3. Extract Brand (brand_elements.py)
   └─> Capture screenshot
   └─> Extract colors and text
   └─> Identify brand elements with GPT-4
   └─> Output: brand_info.json

4. Generate Images (image_generation.py)
   └─> Load educational content
   └─> Create images with DALL-E 3
   └─> Download and save images
   └─> Output: updated_output_response.json
```

## Output Format

### Onboarding Form JSON Structure

```json
{
  "onboarding_form": [
    {
      "question_type": "rating",
      "question_text": "How would you rate your interest in improving memory skills?",
      "responses": [
        "1 - Not interested",
        "2 - Slightly interested",
        "3 - Moderately interested",
        "4 - Very interested",
        "5 - Extremely interested"
      ]
    }
  ],
  "educational_content": [
    {
      "H1_text": "Unlock Your Full Cognitive Potential",
      "H2_text": "Discover games that enhance your memory, attention, and problem-solving skills.",
      "generated_image_url": "https://...",
      "local_image_path": "images/slide_1.png"
    }
  ]
}
```

### Brand Information JSON Structure

```json
{
  "brand_info": {
    "primary_colour": "#hexcode",
    "secondary_colour": "#hexcode"
  },
  "font": {
    "type": "Font Name",
    "colour": "#hexcode"
  },
  "logo": {
    "type": "Font Name",
    "colour": "#hexcode"
  },
  "button": {
    "colour": "#hexcode",
    "font_type": "Font Name"
  }
}
```

## Example Use Case

This project was developed to automate the creation of onboarding forms for the Lumosity brain training app. By analyzing user reviews, it identifies key user preferences and pain points to create targeted onboarding questions that:
- Understand user goals (memory improvement, attention span, etc.)
- Educate users about app features
- Personalize the user experience
- Address common user concerns identified in reviews

## Notes

- The scraping module is configured for Google Play Store URLs
- Review scraping includes handling for infinite scroll and dynamic loading
- Educational images are generated without text overlays (visual-only)
- The system filters out free user complaints about premium features for better insights
- All API calls require a valid OpenAI API key with access to GPT-4 and DALL-E 3

## License

This project is provided as-is for educational and development purposes.
