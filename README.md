# Donizo Material Scraper

A Python-based web scraper designed to extract renovation material pricing data from French suppliers for Donizo's pricing engine.

## 🎯 Objective

Extract at least 100 products across multiple categories (tiles, sinks, toilets, paint, vanities, showers) from French renovation material suppliers and structure the data in a developer-friendly format.

## 📦 Project Structure

```
/donizo-material-scraper/
├── scraper.py              # Main scraping script
├── config/
│   └── scraper_config.yaml # Configuration for categories and URLs
├── data/
│   └── materials.json      # Output data file
├── tests/
│   └── test_scraper.py     # Unit tests
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Chrome browser
- Internet connection

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Run the scraper:
```bash
python scraper.py
```

The script will:
1. Load configuration from `config/scraper_config.yaml`
2. Set up a headless Chrome browser
3. Scrape each configured category
4. Save results to `data/materials.json`

## ⚙️ Configuration

Edit `config/scraper_config.yaml` to modify:
- Target website base URL
- Category paths
- Number of products per category

### Current Configuration

The scraper is currently configured for **ManoMano** (`manomano.fr`) with the following categories:
- Carrelage (Tiles)
- Éviers (Sinks) 
- WC (Toilets)
- Peinture (Paint)
- Meubles de salle de bains (Bathroom Vanities)
- Receveurs de douche (Shower Trays)

## 📊 Output Format

Data is saved as JSON with the following structure:

```json
[
  {
    "product_name": "Product Name",
    "category": "Category Name",
    "price": 29.99,
    "currency": "EUR",
    "product_url": "https://example.com/product",
    "brand": "Brand Name",
    "measurement_unit": "per m²",
    "photo_url": "https://example.com/image.jpg"
  }
]
```

### Data Fields

- **product_name**: Name of the product
- **category**: Product category (from config)
- **price**: Numeric price value
- **currency**: Currency code (EUR)
- **product_url**: Direct link to product page
- **brand**: Brand name (if available)
- **measurement_unit**: Unit of measurement (if available)
- **photo_url**: Product image URL (if available)

## 🔧 Technical Implementation

### Anti-Bot Measures Handled

1. **Cookie Consent Banners**: Automatically detects and accepts cookie banners
2. **Dynamic Content Loading**: Implements scrolling to trigger lazy-loaded content
3. **Browser Simulation**: Uses Selenium with realistic headers and user agent
4. **Session Management**: Maintains browser session across requests

### Scraping Strategy

1. **Page Navigation**: Handles pagination with `?page=N` parameters
2. **Content Parsing**: Uses BeautifulSoup for HTML parsing
3. **Data Extraction**: Targets specific CSS selectors for each data field
4. **Error Handling**: Graceful handling of missing elements and timeouts

## 🚨 Current Status & Challenges

### ⚠️ Anti-Scraping Detection

The scraper has encountered significant anti-bot measures from all tested suppliers:

1. **Leroy Merlin**: Returns 403 Forbidden errors
2. **Castorama**: Shows CAPTCHA challenges
3. **ManoMano**: Implements sophisticated bot detection

### Technical Challenges

- **Dynamic Content**: Products load via JavaScript after page load
- **Cookie Management**: Complex consent flow with multiple overlays
- **Rate Limiting**: Requests are throttled or blocked
- **Fingerprinting**: Browser fingerprinting detects automated access

### Current Limitations

- **No Data Extraction**: Due to anti-scraping measures, no products are currently being scraped
- **Selector Instability**: HTML structure changes frequently
- **Performance**: Slow due to browser automation and wait times

## 🛠️ Potential Solutions

### Advanced Approaches

1. **XHR Interception**: Monitor network requests to capture API endpoints
2. **Proxy Rotation**: Use multiple IP addresses to avoid detection
3. **Headless Browser Optimization**: Reduce fingerprinting signals
4. **Request Rate Limiting**: Implement delays between requests
5. **Alternative Data Sources**: Consider official APIs or partnerships

### Recommended Next Steps

1. **API Investigation**: Research if suppliers offer official APIs
2. **Partnership Opportunities**: Contact suppliers for data access
3. **Alternative Suppliers**: Explore smaller, less protected websites
4. **Manual Data Collection**: Consider manual data entry for initial dataset

## 🧪 Testing

Run tests:
```bash
python -m pytest tests/
```

## 📝 Data Assumptions & Transformations

### Price Handling
- Prices are converted from French format (comma decimal separator) to standard format
- Currency is assumed to be EUR for French suppliers
- Missing prices are set to `null`

### URL Processing
- Relative URLs are converted to absolute URLs
- Product URLs are validated before saving

### Data Validation
- Products without name, price, or URL are filtered out
- Empty or invalid data fields are set to `null`

## 🤝 Contributing

To improve the scraper:

1. **Update Selectors**: Modify CSS selectors in `parse_product()` function
2. **Add Categories**: Extend `scraper_config.yaml` with new categories
3. **Enhance Error Handling**: Add more robust error recovery
4. **Optimize Performance**: Reduce wait times and improve efficiency

## 📄 License

This project is created for the Donizo Data Engineer Test Case 2.

## 🔗 Dependencies

- **requests**: HTTP library
- **beautifulsoup4**: HTML parsing
- **PyYAML**: Configuration file parsing
- **selenium**: Browser automation
- **webdriver-manager**: Chrome driver management

---

**Note**: This scraper is for educational and testing purposes. Always respect website terms of service and robots.txt files when scraping.
# material-scraper
