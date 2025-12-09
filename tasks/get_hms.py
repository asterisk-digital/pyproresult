import os

from pyproresult import ApiClient

def main():
    # Load .env from cwd
    import dotenv
    dotenv.load_dotenv()

    client = ApiClient(account_id=os.getenv("PRORESULT_ACCOUNT_ID"), api_secret=os.getenv("PRORESULT_API_SECRET"))
    hms = client.get_hms()
    print(hms)

if __name__ == "__main__":
    main()
