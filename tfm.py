import bin.keyence as keyence
import bin.config as config


def main():
    formats = {"Keyence":keyence.keyence}
    formats[config.format]()
    print("Done!")


if __name__ == '__main__':
    main()