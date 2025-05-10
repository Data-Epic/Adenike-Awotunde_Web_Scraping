# ⚽ Webscraping: Premier League 2024/2025 Season Data

This project automates the scraping of Premier League statistics for the 2024/2025 season from [FBRef](https://fbref.com/en/comps/9/Premier-League-Stats) and exports the cleaned data to a structured Google Sheets document.

It is built with Python and uses `BeautifulSoup`, `pandas`, and `gspread` to process the data and send it to Google Sheets.

---

## 📌 Features

- Scrapes **all tables** from the Premier League 2024/2025 stats page
- Parses data using `pandas` and `BeautifulSoup`
- Automatically **adds a "Last Updated" timestamp** to each record
- Each table is **exported to a separate worksheet** in a Google Sheet
- Clears previous data before every new update
- Keeps a history of actions via logging (`history.log`)

---

## 🛠️ Technologies Used

- Python 3.x  
- BeautifulSoup (`bs4`)  
- pandas  
- gspread  
- gspread-dataframe  
- python-dotenv  
- Google OAuth2 Service Account

---

---

## 🔐 Setup Instructions

### 1. Clone this repository

```
git clone https://github.com/Data-Epic/Adenike-Awotunde_Web_Scraping.git
cd Adenike-Awotunde_Web_Scraping 
```
### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root and add the following:

```env
SHEET_ID=your_google_sheet_id
CREDENTIALS_FILE=full/path/to/credentials.json
```
---

### 4. Set Up Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create/select a project → Enable **Google Sheets API**
3. Go to **Credentials** → Click **Create Credentials > Service Account**
4. Under the new service account, go to **Keys** → **Add Key > JSON**
5. Save the `.json` file to your project (e.g., `credentials.json`)
6. Add this to your `.env` file:

    ```env
    CREDENTIALS_FILE=path/to/credentials.json
    ```

7. Share your Google Sheet with the service account email (from the JSON file) and give **Editor** access

---
---

### ✅ How to Run

1. Activate your virtual environment:
```
   source .venv/bin/activate  # On macOS/Linux
   .venv\Scripts\activate     # On Windows
   ```
Run the script
```
python main.py
```

## 📝 License
This project is licensed under the MIT License. Feel free to use, modify, and distribute with attribution.

## 👤 Author

**Adenike Awotunde**  
- [GitHub](https://github.com/AdenikeAwotunde)  
- [LinkedIn](https://www.linkedin.com/in/adenike-awotunde-b9740b80)
- [Email](adenikeisblessed@gmail.com)

