import os
import re
import unittest
import json
import subprocess
import pathlib

def replace_home_var(config):
    for k, v in config.items():
        config[k] = v.replace(r"$home", str(pathlib.Path.home()))
    return config

class TestConfiguration(unittest.TestCase):

    def read_config(self, config_path):
        with open(config_path) as f:
            return replace_home_var(json.load(f))

    def active_config_from_buildcache(self):
        cmd = [os.path.join(os.getcwd(), "buildcache"), "--show-config"]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)

        active_config = {}
        for line in p.stdout.split("\n"):
            if re.search("BUILDCACHE_*", line):
                line_content = line.split(":")
                config_variable = line_content[0].strip()
                value = ":".join(line_content[1:]).strip()
                if config_variable in active_config:
                    raise Exception(f"Config variable '{config_variable}' found more than once!")
                active_config[config_variable] = value
        return active_config

    def test_default_configuration(self):
        default_reference_config = self.read_config(os.path.join(os.path.dirname(__file__), "default_config.json"))

        default_config = self.active_config_from_buildcache()

        for (k,v),(k1,v1) in zip(default_config.items(), default_reference_config.items()):
            self.assertEqual(k, k1)
            self.assertEqual(v, v1)
        
        self.assertEqual(default_config, default_reference_config)


if __name__ == "__main__":
    print(os.listdir("."))
    unittest.main()
