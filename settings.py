import yaml


class Config:
    def __init__(self, loc="config.yaml"):
        self.loc = loc
        self.config = {}
        pass

    def read_config(self):
        self.file = open(self.loc, "r")
        try:
            self.config = yaml.safe_load(self.file)
            return self.config
        except yaml.YAMLError as e:
            print(e)

    def get_config(self):
        return self.read_config()


if __name__ == "__main__":
    print(Config().get_config())


DEBUG = True
