
class KicadBoard:
    def __init__(self, file_path):
        # Read kicad_pcb file
        self.file_path = file_path

        with open(file_path, 'r') as f:
            self.board_raw = f.readlines()


    def add_rect_outline(self, width, height, corner_round_radius = 0, line_width = 0.2):
        return self.add_rect_outline_at_point((0,0), width, height, corner_round_radius, line_width)

    def add_rect_outline_at_point(self, center_point, width, height, corner_round_radius = 0, line_width = 0.2):
        outline = []

        # Generate corners:
        corners = [ [-width / 2.0,-height/2.0], [width/2.0, -height/2.0], [width/2.0, height/2.0], [-width/2.0, height/2.0]]

        # Apply offset:
        for i in range(len(corners)):
            corners[i][0] += center_point[0]
            corners[i][1] += center_point[1]

        if corner_round_radius > 0:
            # Do outline with curved corners
            # Generate straight segments:
            origins = [point[:] for point in corners]
            origins[0][0] += corner_round_radius
            origins[1][1] += corner_round_radius
            origins[2][0] -= corner_round_radius
            origins[3][1] -= corner_round_radius

            ends = [point[:] for point in corners]
            ends.append(ends.pop(0)) # Shift list by 1
            ends[0][0] -= corner_round_radius
            ends[1][1] -= corner_round_radius
            ends[2][0] += corner_round_radius
            ends[3][1] += corner_round_radius

            for origin, end in zip(origins, ends):
                outline.append('(gr_line (start %f %f) (end %f %f) (angle 90) (layer Edge.Cuts) (width %f))' % ( origin[0], origin[1], end[0], end[1], line_width))

            # Generate arcs
            arc_origins = [point[:] for point in ends]
            arc_origins[0][1] += corner_round_radius
            arc_origins[1][0] -= corner_round_radius
            arc_origins[2][1] -= corner_round_radius
            arc_origins[3][0] += corner_round_radius

            arc_start = [point[:] for point in ends]

            for origin, end in zip(arc_origins, arc_start):
                outline.append('(gr_arc (start %f %f) (end %f %f) (angle 90) (layer Edge.Cuts) (width %f))' % ( origin[0], origin[1], end[0], end[1], line_width))

        else:
            for i in range(len(corners)):
                origin = corners[i]
                end = corners[(i+1)%len(corners)]
                outline.append('(gr_line (start %f %f) (end %f %f) (angle 90) (layer Edge.Cuts) (width %f))' % ( origin[0], origin[1], end[0], end[1], line_width))

        # Add outline to the end of the file:
        self.board_raw = self.board_raw[:-1]
        for line in outline:
            self.board_raw.append('  '+line+'\n')
        self.board_raw.append(')\n')

        print(self.board_raw)

        # Return result
        return outline

    def save(self, out_file = None):
        if not out_file:
            out_file = self.file_path

        with open(out_file, 'w') as f:
                f.writelines(self.board_raw)

if __name__ == '__main__':
    board = KicadBoard('../../etch-a-sketch.kicad_pcb')
    for line in board.add_rect_outline(50, 50, 5, 0.2):
        print(line)


    board.save()