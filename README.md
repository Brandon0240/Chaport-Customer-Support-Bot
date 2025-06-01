# Chaport AI Chatbot 

An AI chatbot system designed to assist with product inquiries and inventory checks based on a company's inventory catalog or website data. It contains catogory routing, stock data gathering, staged interactions, and Chaport API integration.

## Setup

### 1. Clone the Repo
```bash
git clone https://github.com/Brandon0240/Chaport-API-Customer-Support-Chatbot.git
cd chaport-chatbot
```

### 2. Make an .env File
Create a `.env` file in the root directory with the following:
```bash
HUGGINGFACE_TOKEN=your_token_here
CHAPORT_API_KEY=your_key_here
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```
### 4. Install Cuda Support
Check Cuda Version

```bash
nvidia-smi
```
Install Torch support depending on the cuda version
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
or
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```
### 5. Gather files
Run ```all_url_till_error.py``` to get your urls

Run ```bulk_webscraper.py``` or ```excel_scraper.py``` to adds files to Spreadsheets or directory. 

Change app/config/paths.py excel path name to your file's name 
```bash
excel_file_name = "Wesco Inventory All 250324.xls"
```

### 6. Change your Chaport OperatorID in ```app/chaport/send_response.py```

```bash
OperatorID=your_chaport_operator_here
```
