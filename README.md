# JSON to Dear PyGui (jsontodpg)

JSON to Dear PyGui (jsontodpg) is a Python library that allows you to create Dear PyGui user interfaces using JSON-like structures. It provides a simple way to define UI components and layouts using nested dictionaries, making it easier to manage complex interfaces and separate UI definition from application logic.

## Key Features

- Convert JSON-like structures to Dear PyGui UI components
- Support for asynchronous functions and event handling
- Built-in controller for managing UI state and interactions
- Plugin system for extending functionality
- Automatic generation of keyword files for Dear PyGui components

## Installation

To install jsontodpg, run:

```
pip install jsontodpg
```

## Usage Example

Here's a simple example of how to use jsontodpg:

```python
from jsontodpg import JsonToDpg
from dpgkeywords import *

j_to_dpg = JsonToDpg(generate_keyword_file_name=False, debug=False)
c = j_to_dpg.controller

main = {
    viewport: {width: 800, height: 600},
    window: {
        label: "Example Window",
        width: 400,
        height: 300,
        pos: [200, 150],
        input_text: {
            default_value: "Enter some text",
            tag: "input_to_print"
        },
        button: {
            label: "Submit",
            callback: lambda: print(c.get_value("input_to_print")),
        },
    },
}

j_to_dpg.start(main)

```
This example creates a simple Dear PyGui application with a viewport, a window, an input field, and a button.
When the button is pressed, the text in the input_field is printed to the console.

## Advanced Features

jsontodpg offers several advanced features:

1. Asynchronous Functions: You can define asynchronous functions that run at regular intervals.

2. Controller: The built-in controller allows you to interact with UI components programmatically.

3. Plugins: Extend functionality by adding custom plugins.

4. Keyword Generation: Automatically generate keyword files for Dear PyGui components and custom plugins.


## Contributing

Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to the Dear PyGui community for their ongoing development and support of the library.