#KicadBoard Usage
---------------------------

## Creating an outline
Creating a 50x50mm outline with 0.2 line width:

    >>> from kicad_board import KicadBoard
    >>> board = KicadBoard('file.kicad_pcb')
    >>> board.add_rect_outline(50, 50, 0, 0.2)
    >>> board.save()

Creating a 50x50mm outline with 0.2 line width and 5mm radius corners:

    >>> from kicad_board import KicadBoard
    >>> board = KicadBoard('file.kicad_pcb')
    >>> board.add_rect_outline(50, 50, 5, 0.2)
    >>> board.save()

Creating a outline centered at (100,100):

    >>> from kicad_board import KicadBoard
    >>> board = KicadBoard('file.kicad_pcb')
    >>> board.add_rect_outline_at_point((100, 100), 50, 50, 5, 0.2)
    >>> board.save()
