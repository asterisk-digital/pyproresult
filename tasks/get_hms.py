import os

from pyproresult import ApiClient


def main():
    # Load .env
    import dotenv

    dotenv.load_dotenv()

    client = ApiClient(
        account_id=os.environ["PRORESULT_ACCOUNT_ID"],
        api_secret=os.environ["PRORESULT_API_SECRET"],
    )
    hms = client.get_hms()
    print(hms)


if __name__ == "__main__":
    main()
