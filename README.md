# tkblock  
tkblock is a package to support tkinter widget placement with relative ease.  

There are ack functions for placing widgets in tkinter: place, grid, and p. If you are new to tkinter, it is difficult to distinguish between these three functions.  
If you are new to tkinter, it is difficult to distinguish between these three.  
Therefore, this package allows users to place widgets without having to call the place function.  
For specifying the layout for placing the widget, we use the old HTML/CSS idea of table layout.  
Therefore, the number of rows and columns of the table are specified when the root object is created, and the widget is placed by specifying those rows and columns when the widget is created.  


## how to use
Please refer to the examples under Sample.  

Some basic usage is described below.  

```python
from tkinter import ttk
from tkblock.block_service import BlockService
root = BlockService.init(10, 20, 500, 1000)
frame = BlockService.create_frame("test")
label = ttk.Label(self.frame, text="label", anchor=tk.CENTER)
label.layout = BlockService.layout(5, 6, 10, 12)
BlockService.place_frame_widget()
frame.tkraise()
```


# LICENSE
This software is released under the MIT License, see LICENSE.