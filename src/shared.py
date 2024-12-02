from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ADDRESS = os.getenv("MCSMANAGER_ADDRESS")
API_KEY = os.getenv("MCSMANAGER_API_KEY")
OUTPUT_SIZE = os.getenv("OUT_PUT_SIZE")
PAGE_SIZE = os.getenv("PAGE_SIZE")
PAGE = os.getenv("PAGE")

headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json; charset=UTF-8",
}

PAGE_SIZE_PAGE = f"&page_size={PAGE_SIZE}&page={PAGE}"

instanceData = {}
daemonData = {}
userData = {}
