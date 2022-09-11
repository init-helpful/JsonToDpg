from keywords import *

example = {
    viewport: {
        title: "Multi Window Example",
        width: 1000,
        height: 1000,
    },
    "windows": [
        {
            window: {
                label: "test window",
                width: 400,
                height: 400,
                pos: [100, 0],
                table: {
                    "_columns": [
                        {table_column: {}},
                        {table_column: {}},
                        {table_column: {}},
                    ],
                    "_rows": [
                        {
                            table_row: {
                                "cells": [
                                    {table_cell: {text: {default_value: "test1"}}},
                                    {table_cell: {text: {default_value: "test2"}}},
                                    {table_cell: {text: {default_value: "test3"}}},
                                ]
                            }
                        },
                        {
                            table_row: {
                                "cells": [
                                    {table_cell: {text: {default_value: "test1"}}},
                                    {table_cell: {text: {default_value: "test2"}}},
                                    {table_cell: {text: {default_value: "test3"}}},
                                ]
                            }
                        },
                        {
                            table_row: {
                                "cells": [
                                    {table_cell: {text: {default_value: "test1"}}},
                                    {table_cell: {text: {default_value: "test2"}}},
                                    {table_cell: {text: {default_value: "test3"}}},
                                ]
                            }
                        },
                    ],
                },
            }
        },
    ],
}
