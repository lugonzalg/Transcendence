import requests
import json
import pathlib
import os

http_callbacks = {
    "GET": requests.get,
    "POST": requests.post,
    "DELETE": requests.delete,
    "PATCH": requests.patch,
    "PUT": requests.put
}

def main() -> int:

    paths = os.environ["PATHS"].rstrip(",\n").split(",")

    print(paths)
    for path in paths:

        conf_path = pathlib.Path(path)
        if conf_path.exists():
            for elem in conf_path.iterdir():
                if elem.name.endswith('.json'):

                    with open(elem) as fd:
                        data = json.load(fd)
                        http_method = data.get('http_method')
                        url = data.get('url')
                        values = data.get('values')

                        if http_method is None or url is None or values is None:
                            print("Error")
                            continue

                        res = http_callbacks[http_method](url, json=values)
                        print(res.status_code) 
                        print(res.json()) 


    return 0

if __name__ == "__main__":
    main()