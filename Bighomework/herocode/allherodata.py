import urllib.response
import herogetAgent
import json


def main():
    path = "./herodata.json"
    result = json.load(open(path, "r", encoding="utf-8"))
    print(result)
    json.dump(result,
              open(path, "w", encoding="utf-8"),
              ensure_ascii=False,
              indent=2)


if __name__ == '__main__':
    main()
