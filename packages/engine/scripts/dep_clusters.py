#!/usr/bin/env python3
# pyright: basic
"""Analyze class/function dependencies and output DOT graph."""

from pathlib import Path

# Known groupings - for filtering/clustering
GROUPS: dict[str, set[str]] = {
    "ubiquitous": {"Card", "GameState", "Suit", "Rank", "Phase", "Trick"},
    "collections": {"Cards", "Player", "Hand", "Deck"},
    "tty": {"SupportsTTY", "format"},
}

EXCLUDE = set()
# EXCLUDE = GROUPS["ubiquitous"] | GROUPS["collections"] | GROUPS["tty"]

# Visual clusters - use "/" for nesting (e.g., "ending/scoring")
CLUSTERS: dict[str, set[str]] = {
    "play": {
        "valid_plays",
        "valid_follows",
        "valid_leads",
        "is_first_trick",
        "can_lead_hearts",
        "has_suit",
        "cards_of_suit",
        "is_point_card",
    },
    "start": {
        "start_new_round",
        "create_deck",
        "hands_from_deck",
        "new_game",
        "find_two_of_clubs_holder",
        "start_playing_phase",
    },
    "actions": {
        "valid_actions",
        "apply_action",
        "valid_pass_selections",
        "SelectPass",
        "PlayCard",
        "ChooseMoonOption",
        "apply_play",
    },
    "passing": {
        "apply_pass",
        "next_player_for_passing",
        "execute_passes",
        "pass_target",
        "pass_direction_for_round",
    },
    "ending": {
        "trick_winner",
        "complete_trick",
        "complete_round",
        "check_shot_moon",
        "check_game_end",
        "apply_moon_choice",
    },
    "ending/scoring": {
        "apply_normal_scoring",
        "round_points",
        "trick_points",
        "card_points",
    },
}

CLUSTER_COLORS = {
    "play": "#fff0f0",
    "start_new_round": "#f0fff0",
    "actions": "#f0f0ff",
    "passing": "#fffff0",
    "ending": "#fff0ff",
    "ending/scoring": "#ffe0ff",
}

from astroid import parse
from astroid.nodes import Attribute
from astroid.nodes import ClassDef
from astroid.nodes import FunctionDef
from astroid.nodes import Import
from astroid.nodes import ImportFrom
from astroid.nodes import Name


def main() -> None:
    src = Path(__file__).parent.parent / "src" / "hearts_engine"

    # Build cluster mapping: symbol -> cluster name
    cluster_map: dict[str, str] = {}
    for cluster_path, symbols in CLUSTERS.items():
        for sym in symbols:
            cluster_map[sym] = cluster_path

    # Pass 1: collect all defined symbols and their types
    # symbol_name -> (module, kind, lines)
    defined: dict[str, tuple[str, str, int]] = {}

    for path in sorted(src.glob("*.py")):
        if path.name.startswith("_") or "_test" in path.name:
            continue
        mod = parse(path.read_text(), module_name=path.stem)
        for node in mod.body:
            if isinstance(node, ClassDef):
                # Check if it's an Enum subclass
                is_enum = any(
                    (isinstance(b, Name) and b.name == "Enum")
                    for b in node.bases
                )
                kind = "enum" if is_enum else "class"
                end = node.end_lineno or node.lineno or 1
                start = node.lineno or 1
                lines = end - start + 1
                defined[node.name] = (path.stem, kind, lines)
            elif isinstance(node, FunctionDef):
                end = node.end_lineno or node.lineno or 1
                start = node.lineno or 1
                lines = end - start + 1
                defined[node.name] = (path.stem, "func", lines)

    # Shape and color config
    shape = {"enum": "diamond", "class": "box", "func": "ellipse"}
    fillcolor = {"enum": "#ffffcc", "class": "#ccffcc", "func": "#ccccff"}

    # Size scaling based on line count
    def node_size(lines: int) -> tuple[float, float]:
        """Return (width, height) with area linear to lines."""
        # area = width * height ∝ lines
        # maintain ~2.5:1 aspect ratio
        min_area = 1.0  # minimum area for readability
        area = min_area + lines * 0.15
        aspect = 2.5
        height = (area / aspect) ** 0.5
        width = height * aspect
        return width, height

    # Edge colors by target module
    module_colors = {
        "card": "#e41a1c",
        "cards": "#377eb8",
        "state": "#4daf4a",
        "rules": "#984ea3",
        "main": "#ff7f00",
        "passing": "#a65628",
        "play": "#f781bf",
        "round": "#999999",
        "player": "#66c2a5",
        "tty": "#8da0cb",
    }

    print("digraph {")
    print("  rankdir=LR")
    print("  splines=true")
    print("  nodesep=0.3")
    print("  ranksep=0.3")
    # print('  size="7.5,10"')  # disabled to see natural size
    # print("  ratio=compress")
    print('  node [style=filled fontsize=14 margin="0.01,0.005"]')
    print()

    # Build cluster tree from paths
    # tree[path] = {"symbols": set, "children": [child_paths], "loc": 0}
    cluster_tree: dict[str, dict] = {}
    for path in CLUSTERS:
        cluster_tree[path] = {
            "symbols": CLUSTERS[path],
            "children": [],
            "loc": 0,
        }

    # Link children to parents
    for path in sorted(
        CLUSTERS.keys(), key=lambda p: p.count("/"), reverse=True
    ):
        if "/" in path:
            parent = path.rsplit("/", 1)[0]
            if parent in cluster_tree:
                cluster_tree[parent]["children"].append(path)

    # Render cluster recursively
    def render_cluster(path: str, indent: str = "  ") -> int:
        """Render cluster, return total LOC."""
        node = cluster_tree[path]
        name = path.rsplit("/", 1)[-1]  # leaf name for label
        cluster_color = CLUSTER_COLORS.get(path, "#f0f0f0")
        cluster_id = path.replace("/", "_")

        print(f"{indent}subgraph cluster_{cluster_id} {{")
        print(f"{indent}  style=filled")
        print(f'{indent}  fillcolor="{cluster_color}"')

        total_loc = 0
        # Render child clusters first
        for child_path in node["children"]:
            total_loc += render_cluster(child_path, indent + "  ")

        # Render symbols
        for sym in sorted(node["symbols"]):
            if sym in defined and sym not in EXCLUDE:
                _, kind, lines = defined[sym]
                total_loc += lines
                w, h = node_size(lines)
                print(
                    #  width={w:.2f} height={h:.2f}
                    f'{indent}  "{sym}" [shape={shape[kind]} fillcolor="{fillcolor[kind]}" label="{sym} ({lines})"]'
                )

        print(f'{indent}  label="{name} ({total_loc})"')
        print(f"{indent}}}")
        node["loc"] = total_loc
        return total_loc

    # Render only top-level clusters
    for path in CLUSTERS:
        if "/" not in path:
            render_cluster(path)
            print()

    # Declare unclustered nodes
    for sym, (mod, kind, lines) in sorted(defined.items()):
        if sym in EXCLUDE:
            continue
        if sym in cluster_map:
            continue  # already in a cluster
        w, h = node_size(lines)
        print(
            #  width={w:.2f} height={h:.2f}
            f'  "{sym}" [shape={shape[kind]} fillcolor="{fillcolor[kind]}" label="{sym} ({lines})"]'
        )
    print()

    # Pass 2: collect edges
    edges: list[tuple[str, str, str]] = []  # (from, to, target_module)

    for path in sorted(src.glob("*.py")):
        if path.name.startswith("_") or "_test" in path.name:
            continue
        module_name = path.stem
        mod = parse(path.read_text(), module_name=module_name)

        imports: dict[str, str] = {}
        for node in mod.body:
            if isinstance(node, ImportFrom):
                for alias, asname in node.names:
                    imports[asname or alias] = alias
            elif isinstance(node, Import):
                for alias, asname in node.names:
                    imports[asname or alias] = alias

        for node in mod.body:
            if isinstance(node, (ClassDef, FunctionDef)):
                used: set[str] = set()

                for child in node.nodes_of_class(Name):
                    name = imports.get(child.name, child.name)
                    if name in defined and name != node.name:
                        used.add(name)

                for child in node.nodes_of_class(Attribute):
                    if isinstance(child.expr, Name):
                        name = imports.get(child.expr.name, child.expr.name)
                        if name in defined and name != node.name:
                            used.add(name)

                for dep in used:
                    target_mod = defined[dep][0]
                    edges.append((node.name, dep, target_mod))

    # Print edges with colors
    for src_sym, dst_sym, target_mod in edges:
        if dst_sym in EXCLUDE or src_sym in EXCLUDE:
            continue
        color = module_colors.get(target_mod, "#000000")
        print(f'  "{src_sym}" -> "{dst_sym}" [color="{color}"]')

    print("}")


if __name__ == "__main__":
    main()
