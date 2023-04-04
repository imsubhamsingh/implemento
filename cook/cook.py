import os
import shutil

class Makefile:
    def __init__(self):
        self.targets = {}

    def add_target(self, name, dependencies, actions):
        self.targets[name] = (dependencies, actions)

    def run_target(self, name):
        if name not in self.targets:
            raise ValueError(f"Target {name} not defined.")
        dependencies, actions = self.targets[name]
        for dependency in dependencies:
            self.run_target(dependency)
        for action in actions:
            action()

    def clean(self):
        for target in self.targets:
            if target != "clean":
                dependencies, actions = self.targets[target]
                for action in actions:
                    if action.__name__ == "clean":
                        action()
                shutil.rmtree(target, ignore_errors=True)

    def print_help(self):
        print("Makefile commands:")
        print("  make <target>: Build the specified target")
        print("  make clean: Remove all built targets")
        print("  make help: Print this help message")

makefile = Makefile()

def clean():
    print("Cleaning...")

def build():
    print("Building...")

def run():
    print("Running...")

makefile.add_target("clean", [], [clean])
makefile.add_target("build", ["clean"], [build])
makefile.add_target("run", ["build"], [run])

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        makefile.print_help()
    elif sys.argv[1] == "help":
        makefile.print_help()
    elif sys.argv[1] == "clean":
        makefile.clean()
    else:
        makefile.run_target(sys.argv[1])

