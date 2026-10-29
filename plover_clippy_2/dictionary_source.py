import os

_DELETED = "{plover:deleted}"


def outline_of(translation):
    rtfcre = translation.rtfcre
    if isinstance(rtfcre, str):
        return tuple(part for part in rtfcre.split("/") if part)
    return tuple(rtfcre)


def _matches(engine, outline):
    lookup = getattr(engine, "lookup_from_all", None)
    if lookup is not None:
        return lookup(outline) or []

    collection = getattr(engine, "dictionaries", None)
    if collection is None:
        return []
    matches = []
    for dictionary in collection.dicts:
        if not getattr(dictionary, "enabled", True):
            continue
        value = dictionary.get(outline)
        if value:
            matches.append((value, dictionary))
    return matches


def dictionary_name(dictionary):
    path = getattr(dictionary, "path", None) or ""
    return os.path.basename(str(path).replace("\\", "/"))


def dictionary_for_outline(engine, outline):
    if isinstance(outline, str):
        outline = tuple(part for part in outline.split("/") if part)
    else:
        outline = tuple(outline)
    if not outline:
        return ""
    matches = _matches(engine, outline)
    if not matches:
        return ""
    text, dictionary = matches[0]
    if text is None or str(text).lower() == _DELETED:
        return ""
    return dictionary_name(dictionary)


def dictionary_for_translation(engine, translation):
    return dictionary_for_outline(engine, outline_of(translation))


def _join_names(names):
    joined = []
    for name in names:
        if name and (not joined or joined[-1] != name):
            joined.append(name)
    return ", ".join(joined)


def dictionaries_for_phrase(engine, phrase):
    return _join_names(
        dictionary_for_translation(engine, translation)
        for translation in phrase
    )


def dictionaries_for_outlines(engine, outlines):
    # The briefs on the left of "<". Add Translation shows these entries,
    # not the dictionaries of the longer strokes that were written.
    return _join_names(
        dictionary_for_outline(engine, outline) for outline in outlines
    )


def dictionary_suffix(name):
    if not name:
        return ""
    return f" ({name})"
