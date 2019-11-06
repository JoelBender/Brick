import random
import rdflib
import time
from pprint import pprint

word_net = {}
classes = {}


def map_words(cls, words):
    print(cls)
    if not cls.startswith("https://brickschema.org/schema/1.1.0/Brick#"):
        print("    ^^^^^")
        return

    classes[words] = cls
    for i in range(len(words)):
        for j in range(i + 1, len(words) + 1):
            p, w, n = words[i - 1 : i], words[i:j], words[j : j + 1]
            if w not in word_net:
                word_net[w] = {"p": set(), "n": set()}
            if p:
                word_net[w]["p"].add(p[0])
            if n:
                word_net[w]["n"].add(n[0])


g = rdflib.Graph()
start_time = time.time()
g.load("Brick.ttl", format="turtle")
end_time = time.time()
print("loaded: {}".format(end_time - start_time))

start_time = end_time
for cls, label in g.query(
    "SELECT ?cls ?label WHERE { ?cls rdf:type owl:Class . ?cls rdfs:label ?label . }"
):
    map_words(cls, tuple(word.lower() for word in label.value.split()))
end_time = time.time()
print("mapped: {}".format(end_time - start_time))

single_words = sorted(k[0] for k in word_net if len(k) == 1)
print("single_words: {}".format(single_words))

while True:
    try:
        words = tuple(input().split(" "))
        print(words, "?")
    except EOFError:
        break

    if len(words) == 1 and words not in word_net:
        w = [z for z in single_words if z.startswith(words[0])]
        if len(w) != 1:
            print("pick from:", w)
            print("")
            continue
        words = (w[0],)

    while True:
        print("?", words)

        wnet = word_net.get(words, None)
        if not wnet:
            wnet = word_net.get(words[:-1], None)
            if wnet:
                next_words = sorted(list(wnet["n"]))
                w = [z for z in next_words if z.startswith(words[-1])]
                if not w:
                    print("no choices")
                    print("-")
                    break
                elif len(w) == 1:
                    print("pick:", w[0])
                    words = words[:-1] + (w[0],)
                    continue
                else:
                    print("pick from:", w)
                    print("-")
                    break
            else:
                print("off in the weeds")
                break

        prev_words = sorted(list(wnet["p"]))
        next_words = sorted(list(wnet["n"]))
        print(prev_words, words, next_words)

        if words not in classes and len(next_words) == 1:
            print("pick:", next_words[0])
            words = words + (next_words[0],)
            continue

        if words not in classes and len(prev_words) == 1:
            print("pick:", prev_words[0])
            words = (prev_words[0],) + words
            continue

        if words in classes:
            print(classes[words])
            print("")
        break
