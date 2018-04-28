"""
system config file
"""
import os

download_path = "/tmp/proxyDL"
default_path_win = "C:/proxyDL"
default_path_linux = "/tmp/proxyDL"

template_folder = os.path.join(os.path.dirname(__file__), "templates")
static_folder = os.path.join(os.path.dirname(__file__), "static")
debug = True
