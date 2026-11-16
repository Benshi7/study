#!/usr/bin/env python3
"""Build practice/data/bank.js and recipes.js from the JSON sources (stdlib only).

Usage: python3 practice/build.py [--strict]
  --strict  exit with status 1 if any item was rejected.

Why JS wrappers: the app must work from file:// where fetch() of JSON is blocked,
so data is loaded through <script> tags that set window.BANK / window.RECIPES.
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

TOPICS = {
    "descriptiva", "probabilidad", "condicional-bayes", "contingencia", "va-discreta",
    "binomial", "poisson", "hipergeometrica", "normal", "suma-variables",
    "muestral-media", "muestral-proporcion", "ic-media", "ic-proporcion",
    "tamano-muestra", "regresion",
}
KINDS = {"numeric", "concept", "planteo"}


def is_str(v, min_len=1):
    return isinstance(v, str) and len(v.strip()) >= min_len


def validate_question(q):
    """Return a list of error strings (empty list = valid)."""
    errs = []
    if not isinstance(q, dict):
        return ["item is not an object"]
    if not is_str(q.get("id")):
        errs.append("missing/empty id")
    if q.get("topic") not in TOPICS:
        errs.append("unknown topic %r" % (q.get("topic"),))
    if q.get("kind") not in KINDS:
        errs.append("kind must be one of %s, got %r" % (sorted(KINDS), q.get("kind")))
    d = q.get("difficulty")
    if not (isinstance(d, int) and not isinstance(d, bool) and 1 <= d <= 3):
        errs.append("difficulty must be an int 1-3")
    if not is_str(q.get("stem")):
        errs.append("missing stem")
    opts = q.get("options")
    if not (isinstance(opts, list) and len(opts) == 5 and all(is_str(o) for o in opts)):
        errs.append("options must be 5 non-empty strings")
    elif len({o.strip() for o in opts}) != 5:
        errs.append("options contain duplicates")
    ans = q.get("answer")
    if not (isinstance(ans, int) and not isinstance(ans, bool) and 0 <= ans <= 4):
        errs.append("answer must be an int 0-4")
    steps = q.get("steps")
    if not (isinstance(steps, list) and steps):
        errs.append("steps must be a non-empty list")
    else:
        for i, s in enumerate(steps):
            if not isinstance(s, dict) or not is_str(s.get("label")):
                errs.append("step %d needs a label" % (i + 1))
                continue
            for k in ("text", "formula", "calc"):
                if k in s and s[k] is not None and not isinstance(s[k], str):
                    errs.append("step %d: %s must be a string" % (i + 1, k))
            if not any(is_str(s.get(k)) for k in ("text", "formula", "calc")):
                errs.append("step %d needs text, formula or calc" % (i + 1))
    if not is_str(q.get("why")):
        errs.append("missing why")
    traps = q.get("traps")
    if not (isinstance(traps, list) and len(traps) == 5 and all(isinstance(t, str) for t in traps)):
        errs.append("traps must be 5 strings")
    elif isinstance(ans, int) and 0 <= ans <= 4:
        if traps[ans] != "":
            errs.append("traps[answer] must be an empty string")
        for i, t in enumerate(traps):
            if i != ans and not t.strip():
                errs.append("traps[%d] is empty but option %d is a distractor" % (i, i))
    if "source" in q and not isinstance(q["source"], str):
        errs.append("source must be a string")
    return errs


def validate_recipe(r):
    errs = []
    if not isinstance(r, dict):
        return ["item is not an object"]
    for k in ("id", "topic", "title", "when", "output_meaning"):
        if not is_str(r.get(k)):
            errs.append("missing %s" % k)
    keys = r.get("keys")
    if not (isinstance(keys, list) and keys and all(is_str(k) for k in keys)):
        errs.append("keys must be a non-empty list of strings")
    inputs = r.get("inputs")
    if not (isinstance(inputs, list) and all(isinstance(i, dict) and is_str(i.get("name")) and is_str(i.get("meaning")) for i in inputs)):
        errs.append("inputs must be a list of {name, meaning}")
    traps = r.get("traps")
    if not (isinstance(traps, list) and all(isinstance(t, str) for t in traps)):
        errs.append("traps must be a list of strings")
    ex = r.get("example")
    if ex is not None and not (isinstance(ex, dict) and isinstance(ex.get("inputs", {}), dict)):
        errs.append("example must be {inputs:{}, output}")
    return errs


def load_json_array(path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print("ERROR  %s: %s" % (os.path.basename(path), exc))
        return None
    if not isinstance(data, list):
        print("ERROR  %s: top level must be an array" % os.path.basename(path))
        return None
    return data


def write_js(path, global_name, items):
    payload = json.dumps(items, ensure_ascii=False, indent=1)
    # keep the script tag safe even if some text contains "</script>"
    payload = payload.replace("</", "<\\/")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("/* generated by practice/build.py - do not edit */\n")
        fh.write("window.%s = %s;\n" % (global_name, payload))


def collect(files, validator, label):
    items, seen, rejected = [], {}, 0
    for path in files:
        name = os.path.basename(path)
        data = load_json_array(path)
        if data is None:
            rejected += 1
            continue
        for idx, item in enumerate(data):
            ident = item.get("id", "#%d" % idx) if isinstance(item, dict) else "#%d" % idx
            errs = validator(item)
            if errs:
                rejected += 1
                print("SKIP   %s [%s]: %s" % (name, ident, "; ".join(errs)))
                continue
            if item["id"] in seen:
                rejected += 1
                print("SKIP   %s [%s]: duplicate id (first seen in %s)" % (name, ident, seen[item["id"]]))
                continue
            seen[item["id"]] = name
            items.append(item)
    return items, rejected


def main():
    strict = "--strict" in sys.argv
    rejected_total = 0

    bank_files = sorted(glob.glob(os.path.join(DATA, "bank-*.json")))
    real = [f for f in bank_files if os.path.basename(f) != "bank-sample.json"]
    if real:
        bank_files = real  # the sample is only a fallback
    elif bank_files:
        print("NOTE   no real bank files found: using bank-sample.json (source \"sample\")")
    else:
        print("WARN   no bank-*.json files found; the bank will be empty")

    bank, rej = collect(bank_files, validate_question, "bank")
    rejected_total += rej
    for q in bank:
        if os.path.basename(bank_files[0]) == "bank-sample.json" and not real:
            q["source"] = "sample"
    write_js(os.path.join(DATA, "bank.js"), "BANK", bank)

    recipes = []
    rpath = os.path.join(DATA, "calc-recipes.json")
    if os.path.exists(rpath):
        recipes, rej = collect([rpath], validate_recipe, "recipes")
        rejected_total += rej
    else:
        print("NOTE   calc-recipes.json not found: RECIPES will be empty")
    write_js(os.path.join(DATA, "recipes.js"), "RECIPES", recipes)

    by_topic = {}
    for q in bank:
        by_topic[q["topic"]] = by_topic.get(q["topic"], 0) + 1
    print("bank.js     %d questions from %d file(s)" % (len(bank), len(bank_files)))
    for t in sorted(by_topic):
        print("            %-20s %d" % (t, by_topic[t]))
    print("recipes.js  %d recipes" % len(recipes))
    print("rejected    %d item(s)" % rejected_total)
    if strict and rejected_total:
        sys.exit(1)


if __name__ == "__main__":
    main()
