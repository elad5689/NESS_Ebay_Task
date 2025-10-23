# eBay Automation Test Project

This project contains automated tests for eBay shopping flow, including login, product search, price filtering, adding to cart, and total verification.

## System Requirements

1. **Python** - Version 3.9 or higher
   - [Download Python](https://www.python.org/downloads/)
   - During installation, check `Add Python to PATH`

2. **Java JDK** - Required for Allure Reports
   - [Download Eclipse Temurin JDK](https://adoptium.net/en-GB/)
   - Download the latest OpenJDK version (LTS recommended)
   - After installation, verify Java is installed by running `java -version` in the terminal

3. **Allure Command Line**
   ```bash
   npm install -g allure-commandline
   ```
   (Requires Node.js - download from [https://nodejs.org/](https://nodejs.org/))

## Project Setup

1. Clone the repository or download the source code
2. Create and activate a virtual environment (recommended):
   ```bash
   # For Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # For Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `data.json` file in the project directory:
   ```json
   {
     "search_term": "product to search",
     "max_price": 100,
     "item_limit": 3,
     "username": "your_email@example.com",
     "password": "your_password"
   }
   ```

2. (Optional) Configure environment variables in `.env` file:
   ```
   BASE_URL=https://www.ebay.com
   BROWSER=chrome
   HEADLESS=False
   ```

## Running Tests

### Basic Test Run
```bash
pytest test_ebay_flow.py --alluredir=allure-results
```

### Verbose Test Run
```bash
pytest test_ebay_flow.py -v --alluredir=allure-results
```

### Viewing Reports
After running tests, generate and view the Allure report:
```bash
allure serve allure-results
```

## Project Structure

```
├── README.md               # This file
├── requirements.txt        # Project dependencies
├── data.json              # Test configuration (add to .gitignore)
├── .env                   # Environment variables (add to .gitignore)
├── test_ebay_flow.py      # Main test file
├── base_page.py           # Base page object class
├── home_page.py           # Home page object
├── search_results_page.py # Search results page object
├── product_page.py        # Product page object
├── cart_page.py           # Cart page object
└── login_page.py          # Login page object
```

## Common Issues

### Screenshot Locations in Allure Report
Screenshots are available in the report under:  
`Behaviors > Ebay Shopping Flow Test > test_ebay_shopping_journey`

### Cleaning Previous Results
Before a new test run, clean the `allure-results` directory:
```bash
# Windows
rmdir /s /q allure-results

# Mac/Linux
rm -rf allure-results
```

### Login Issues with CAPTCHA
If you encounter CAPTCHA during login:
1. Tests will automatically continue if they hit this issue
2. To test the full login flow, you may need to run the tests multiple times
3. This is a known limitation with eBay automation

### Chrome WebDriver Errors
If you encounter Chrome WebDriver issues, update it:
```bash
python -m pip install --upgrade webdriver-manager
```

## Sharing the Project

### Initializing Git Repository
```bash
git init
git add .
git commit -m "Initial commit"
```

### Pushing to GitHub
1. Create a new repository on GitHub (don't initialize with README)
2. Follow the instructions to push your existing repository:
   ```bash
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

### Sharing with Team Members
1. Team members should clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   ```
2. Create their own `data.json` file with their credentials
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## License
This project is licensed under the MIT License.
