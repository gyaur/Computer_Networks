 Áramkör szimuláció

Készíts programot, ami leszimulálja az erőforrások lefoglalását és felszabadítását a JSON fájlban megadott topológia, kapacitások és igények alapján!

Script paraméterezése: python3 program.py cs.json

A program kimenete:

    esemény sorszám. <esemény név>: <node1><-><node2> st:<szimuálciós idő> [- <sikeres/sikertelen>]

Pl.:

    igény foglalás: A<->C st:1 – sikeres

    igény foglalás: B<->C st:2 – sikeres

    igény felszabadítás: A<->C st:5

    igény foglalás: D<->C st:6 – sikeres

    igény foglalás: A<->C st:7 – sikertelen

…

Leadás: A program leadása a BE-AD rendszeren .zip formátumban, amiben egy client.py szerepeljen!