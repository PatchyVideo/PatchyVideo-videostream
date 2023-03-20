from os import getenv
import uvicorn
from core.server import server


def main():
    uvicorn.run(
        server,
        host=getenv("HOST", "0.0.0.0"),
        port=int(getenv("PORT", "5006"))
    )


if __name__ == "__main__":
    main()
