import rdflib

g = rdflib.Graph()
g.load("Brick.ttl", format="turtle")

for prefix, uriref in g.namespaces():
    if prefix == "brick":
        BRICK = rdflib.Namespace(uriref)
        break
else:
    raise RuntimeError("brick namespace prefix not found")

seen = set()


def gen_tree(x, indent=0):
    child_list = list(
        g.query("SELECT ?c WHERE {{ ?c rdfs:subClassOf <{}> . }}".format(x))
    )

    if x in seen:
        print("    " * indent, x, "!!!")
        return

    print("    " * indent, x)

    seen.add(x)
    for child in child_list:
        gen_tree(child, indent + 1)


gen_tree(BRICK["Location"])
