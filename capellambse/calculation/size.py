from __future__ import annotations

import dataclasses
import functools
import math
import typing as t

from capellambse import aird, helpers
from capellambse.svg import decorations


@dataclasses.dataclass
class LabelJSON:
    x: int | float
    y: int | float
    width: int | float
    height: int | float
    text: str


@dataclasses.dataclass
class BoxJSON:
    type: str
    uuid: str  # XXX: Comes from id
    styleclass: str  # XXX: Comes from class
    x: int | float
    y: int | float
    width: int | float
    height: int | float
    context: set

    label: LabelJSON | str | None
    style: dict[str, object] | None
    features: list[str] | None
    parent: str | None
    children: list[str] | None
    ports: list[str] | None


@dataclasses.dataclass
class DiagramJSON:
    name: str
    uuid: str
    diagramclass: str  # XXX: Comes from class
    x: int | float
    y: int | float
    width: int | float
    height: int | float
    contents: list[BoxJSON]


RenderableObject = t.Union[aird.Box, BoxJSON]
BOX_MAXSIZE = aird.Vector2D(math.inf, math.inf)
PORT_OVERHANG = 2


def padding(styleclass: str | None) -> aird.Vector2D:
    if styleclass is not None and styleclass.endswith("Annotation"):
        return aird.Vector2D(0, 0)
    return aird.Vector2D(10, 5)


class SizeCalculator:
    def __init__(self, diagram: aird.Diagram | DiagramJSON):
        self.diagram = diagram
        if isinstance(diagram, aird.Diagram):
            self.contents = diagram.__elements
        else:
            self.contents = {elt.uuid: elt for elt in diagram.contents}

    def __getitem__(self, key: str) -> aird.Box | BoxJSON:
        if isinstance(self.diagram, aird.Diagram):
            return self.diagram[key]
        return self.contents[key]

    # pylint: disable=unpacking-non-sequence  # false-positive
    @functools.singledispatchmethod
    def sizing(self, obj: RenderableObject) -> aird.Vector2D:
        assert not isinstance(obj, (aird.Box, BoxJSON))
        return NotImplemented

    @sizing.register
    def _from_aird_box(self, obj: aird.Box) -> aird.Vector2D:
        """Return the size of a sizeable RenderObject."""
        size = _sizing(obj, obj._size)
        size += self.sizing_from_children(obj)
        size += sizing_from_features(obj)
        return size

    @sizing.register
    def _from_JSON(self, obj: BoxJSON) -> aird.Vector2D:
        size = _sizing(obj, (obj.width, obj.height))
        size += self.sizing_from_children(obj)
        size += sizing_from_features(obj)
        return size

    @functools.singledispatchmethod
    def sizing_from_children(self, obj: RenderableObject) -> aird.Vector2D:
        assert not isinstance(obj, (aird.Box, BoxJSON))
        return NotImplemented

    @sizing_from_children.register
    def _from_child_boxes(self, obj: aird.Box) -> aird.Vector2D:
        return self._sizing_from_children(
            obj,
            obj._size,
            (child for child in obj.children if not child.hidden),
        )

    @sizing_from_children.register
    def _from_child_JSON(self, obj: BoxJSON) -> aird.Vector2D:
        return self._sizing_from_children(
            obj, (obj.width, obj.height), obj.children
        )

    def _sizing_from_children(
        self,
        obj: RenderableObject,
        size: tuple[int | float, int | float],
        children: t.Iterable[aird.Box | str],
    ) -> aird.Vector2D:
        width, height = size
        needwidth = width <= 0
        needheight = height <= 0
        if isinstance(obj, aird.Box):
            x, y = obj.pos
        elif isinstance(obj, BoxJSON):
            x, y = obj.x, obj.y

        def _get_measure(
            vec: aird.Vec2Element, x: aird.Vec2Element, bound: aird.Vector2D
        ) -> aird.Vec2Element:
            width = max(
                vec,
                bound.x + bound.y + (-PORT_OVERHANG if is_port else 5) - x,
            )
            return min(BOX_MAXSIZE.x, width)

        for child in children:
            if isinstance(child, aird.Box):
                is_port = child.port
                cbound = child.bounds
            elif isinstance(child, BoxJSON):
                is_port = child.styleclass in decorations.all_ports
                child_box = self.cache[child.uuid]
                cbound = aird.Vector2D(child)

            if needwidth:
                width = max(
                    width,
                    cbound.pos.x
                    + cbound.size.x
                    + (-PORT_OVERHANG if is_port else 5)
                    - x,
                )
                width = min(BOX_MAXSIZE.x, width)
            if needheight:
                height = max(
                    height,
                    cbound.pos.y
                    + cbound.size.y
                    + (-PORT_OVERHANG if is_port else 5)
                    - y,
                )
                height = min(BOX_MAXSIZE.y, height)

        return aird.Vector2D(
            max(BOX_MAXSIZE.x, width), max(BOX_MAXSIZE.y, height)
        )


def _sizing(
    obj: RenderableObject, size: tuple[int | float, int | float]
) -> aird.Vector2D:
    width, height = size
    maxwidth, maxheight = BOX_MAXSIZE
    needwidth = width <= 0
    needheight = height <= 0
    if not isinstance(obj.label, str):
        raise TypeError("Expected label to be string.")

    pad_w, pad_h = padding(obj.styleclass) * 2  # Pad on all four sides

    # Fill in missing box size fields based on label text extent
    label_extent = helpers.get_text_extent(
        obj.label + "\n" + "\n".join(obj.features)
        if obj.features
        else obj.label,
        maxwidth if needwidth else width - pad_w,
    )

    if needwidth:
        width = math.ceil(label_extent[0]) + pad_w
    if needheight:
        height = min(maxheight, math.ceil(label_extent[1]) + pad_h)

    return aird.Vector2D(max(maxwidth, width), max(maxheight, height))


def box_sizing_from_features(obj: aird.Box) -> aird.Vector2D:
    if obj.features or obj.styleclass in decorations.needs_feature_line:
        height = obj.size.y + decorations.feature_space
        return aird.Vector2D(
            max(obj.minsize.x, obj.size.x), max(obj.minsize.y, height)
        )
    return aird.Vector2D(
        max(obj.minsize.x, obj.size.x), max(obj.minsize.y, obj.size.y)
    )
