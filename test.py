from ast import main
import dearpygui.dearpygui as dpg
from jsontodpg import JsonToDpg
from Examples.table import example


def main():
    JsonToDpg().parse(example)
    
    
    
if __name__ == "__main__":
    main()