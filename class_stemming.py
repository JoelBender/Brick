import rdflib

word_net = {}


def map_words(words):
    for i in range(len(words)):
        for j in range(i + 1, len(words) + 1):
            p, w, n = words[i - 1 : i], tuple(words[i:j]), words[j : j + 1]
            if w not in word_net:
                word_net[w] = {"p": set(), "n": set()}
            if p:
                word_net[w]["p"].add(p[0])
            if n:
                word_net[w]["n"].add(n[0])


g = rdflib.Graph()
g.load("Brick.ttl", format="turtle")
print(f"{len(g)} triples")

x = list(
    (a, b.value.split())
    for a, b in g.query(
        "SELECT ?s ?l WHERE { ?s rdf:type owl:Class . ?s rdfs:label ?l . }"
    )
)
print(f"{len(x)} classes")

for z in x:
    map_words(z[1])
print(f"{len(word_net)} words")

while True:
    try:
        words = tuple(input().split(" "))
        print(words, "?")
    except EOFError:
        break

    wnet = word_net.get(words, None)
    if wnet:
        print("p:", wnet["p"])
        print("n:", wnet["n"])
    else:
        print("-")
    print("")
