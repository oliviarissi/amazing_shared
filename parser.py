from typing import List, Tuple, Dict
import unicodedata

HEX_CHARS = "0123456789ABCDEF"
HEX_MAP = {c: c for c in HEX_CHARS}
HEX_MAP.update({c.lower(): c for c in HEX_CHARS})
# Add common unicode lookalikes if needed:
LOOKALIKES = {
    "０":"0","１":"1","２":"2","３":"3","４":"4","５":"5","６":"6","７":"7","８":"8","９":"9",
    "Ａ":"A","Ｂ":"B","Ｃ":"C","Ｄ":"D","Ｅ":"E","Ｆ":"F",
    "ａ":"A","ｂ":"B","ｃ":"C","ｄ":"D","ｅ":"E","ｆ":"F",
    # some accented or other glyphs that appear in sample
    "À":"A","Á":"A","Â":"A","Ã":"A","Ä":"A","Å":"A",
    "à":"A","á":"A","â":"A","ã":"A","ä":"A","å":"A",
    "Ç":"C","ç":"C",
    "Ø":"0","ø":"0",
}
HEX_MAP.update(LOOKALIKES)

def _hex_char_to_int(c: str) -> int:
    if c in HEX_MAP:
        return int(HEX_MAP[c], 16)
    raise ValueError(f"Invalid hex digit: {c!r}")

def parse_maze_file(path: str) -> Dict[str, object]:
    with open(path, "r", encoding="utf-8") as f:
        raw_lines = [ln.rstrip("\n\r") for ln in f]

    # Keep only non-empty lines (trim whitespace)
    non_empty = [ln for ln in raw_lines if ln.strip() != ""]
    if len(non_empty) < 4:
        raise ValueError("File must contain at least one maze line and 3 footer lines (start,end,path).")

    start_line = non_empty[-3].strip()
    end_line   = non_empty[-2].strip()
    path_line  = non_empty[-1].strip()
    maze_lines = non_empty[:-3]
    if not maze_lines:
        raise ValueError("No maze lines found.")

    # Normalize and map characters, collect invalids
    width = len(maze_lines[0])
    for ln in maze_lines:
        if len(ln) != width:
            raise ValueError("All maze lines must have the same length.")

    maze: List[List[int]] = []
    invalids = []
    for r, ln in enumerate(maze_lines, start=1):
        row: List[int] = []
        # normalize to decompose accents etc.
        norm = unicodedata.normalize("NFKC", ln)
        for c_idx, ch in enumerate(norm, start=1):
            mapped = HEX_MAP.get(ch)
            if mapped is None:
                # try uppercase ASCII fallback
                ch_up = ch.upper()
                mapped = HEX_MAP.get(ch_up)
            if mapped is None:
                invalids.append((r, c_idx, ch))
            else:
                row.append(int(mapped, 16))
        maze.append(row)

    if invalids:
        sample = ", ".join([f"({r},{c}):{repr(ch)}" for r,c,ch in invalids[:6]])
        raise ValueError(f"Invalid hex characters in maze at positions {sample}"
                         + ("" if len(invalids)<=6 else f" and {len(invalids)-6} more"))

    def _parse_coord(s: str) -> Tuple[int,int]:
        parts = [p.strip() for p in s.split(",")]
        if len(parts) != 2:
            raise ValueError(f"Invalid coordinate line: {s!r}")
        try:
            r = int(parts[0])
            c = int(parts[1])
        except Exception:
            raise ValueError(f"Coordinates must be integers: {s!r}")
        return (r, c)

    start = _parse_coord(start_line)
    end = _parse_coord(end_line)
    raw_path = path_line
    path_dirs = [c.upper() for c in raw_path if c.strip() != ""]

    return {
        "maze": maze,
        "start": start,
        "end": end,
        "raw_path": raw_path,
        "path_dirs": path_dirs
    }
