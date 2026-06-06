import os.path
import sys
import argparse
import re
import s2sphere
import staticmaps
import frontmatter

POST_PATH = "./content/posts"
IMAGE_WIDTH = 720
IMAGE_HEIGHT = 360
FRONTMATTER_KEY = "maps"

# Use Paul Tol's Bright color scheme for colour blind friendly colors
# See https://cran.r-project.org/web/packages/khroma/vignettes/tol.html#bright
green = staticmaps.parse_color("#228833")
red = staticmaps.parse_color("#EE6677")
blue = staticmaps.parse_color("#4477AA")


tile_provider_OSM = staticmaps.TileProvider(
    "osm",
    url_pattern="https://tile.openstreetmap.org/$z/$x/$y.png",
    max_zoom=19,
)


class TextLabel(staticmaps.Object):
    def __init__(self, latlng: s2sphere.LatLng, text: str) -> None:
        staticmaps.Object.__init__(self)
        self._latlng = latlng
        self._text = text
        self._font_size = 12

    def latlng(self) -> s2sphere.LatLng:
        return self._latlng

    def bounds(self) -> s2sphere.LatLngRect:
        return s2sphere.LatLngRect.from_point(self._latlng)

    def extra_pixel_bounds(self) -> staticmaps.PixelBoundsT:
        w = len(self._text) * self._font_size
        h = self._font_size
        return (int(w / 2), int(h / 2), int(w / 2), int(h / 2))

    def render_svg(self, renderer: staticmaps.SvgRenderer) -> None:
        x, y = renderer.transformer().ll2pixel(self.latlng())
        filter = renderer.group().add(
            renderer.drawing().filter(
                id="textbackground",
                start=(0, 0),
                size=(1, 1),
            )
        )
        filter.feFlood(flood_color="white")
        filter.feComposite()

        renderer.group().add(
            renderer.drawing().text(
                self._text,
                text_anchor="middle",
                dominant_baseline="central",
                insert=(x, y + (self._font_size)),
                font_family="sans-serif",
                font_size=f"{self._font_size}px",
                font_variant="small-caps",
                font_weight="bold",
                fill="#000000",
                filter="url(#textbackground)",
            )
        )


class NewMapException(Exception):
    pass


def read_map_definitions_from_file(file_path: str) -> list:
    with open(file_path) as f:
        post = frontmatter.loads(f.read())
        if FRONTMATTER_KEY in post:
            return post[FRONTMATTER_KEY]
    return []


def process_file(file_path: str):
    post_maps = read_map_definitions_from_file(file_path)
    output_folder = os.path.dirname(file_path)

    for post_map in post_maps:
        process_map(output_folder, post_map)


def process_map(directory: str, post_map: dict):
    context = staticmaps.Context()
    context.set_tile_provider(tile_provider_OSM)

    points = []
    labels = []

    conf_points = post_map["points"]
    for idx, conf_point in enumerate(conf_points):
        point = staticmaps.create_latlng(
            float(conf_point["lat"]), float(conf_point["lon"])
        )
        points.append(point)

        if "colour" in conf_point:
            marker_color = staticmaps.parse_color(conf_point["colour"])
        elif idx == 0 and len(conf_points) > 1:
            marker_color = green
        elif idx == len(conf_points) - 1:
            marker_color = red
        else:
            marker_color = blue
        context.add_object(staticmaps.Marker(point, color=marker_color, size=12))

        if "name" in conf_point:
            labels.append(TextLabel(point, conf_point["name"]))

    if "line" in post_map and bool(post_map["line"]):
        context.add_object(staticmaps.Line(points, color=staticmaps.BLUE, width=4))

    for label in labels:
        context.add_object(label)

    if "zoom" in post_map:
        context.set_zoom(int(post_map["zoom"]))

    map_name = post_map["name"]
    map_path = f"{directory}/{map_name}.svg"
    exists_already = os.path.isfile(map_path)

    height = IMAGE_HEIGHT
    width = IMAGE_WIDTH
    if "height" in post_map:
        height = post_map["height"]
    if "width" in post_map:
        width = post_map["width"]

    svg_image = context.render_svg(width, height)
    with open(map_path, "w", encoding="utf-8") as svg:
        svg_image.write(svg, pretty=True)

    if not exists_already:
        raise NewMapException(f"New map '{map_path}' generated")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args()
    map_generated = False

    for argument in args.filenames:
        pattern = re.compile(r"^content/(posts/.*|demo)/index\.md$")
        if pattern.match(argument):
            try:
                process_file(argument)
            except NewMapException as e:
                print(e)
                map_generated = True

    return 1 if map_generated else 0


if __name__ == "__main__":
    sys.exit(main())
