import mods.keyence as keyence
import mods.config as config


def main():
    formats = {"Keyence":keyence.keyence}
    formats[config.format]()
    print("Done!")


if __name__ == '__main__':
    main()