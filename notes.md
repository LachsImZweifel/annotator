## PLANNING

### NEXT STEPS
→  add visibility to keypoints

### TODOS
-> clear keypoints (annotation view)
-> saving performance edit vs dump
-> when a skeleton has only null/ (0,0,0) keypoints -> dont save
→ set Image (flexible)
→ Änderungen werfen → nur cache löschen z.B. [strg] + [esc]

### REFACTORING
→ _on_next_kp erzeugt skelet:
    -> Idee: Neues Bild ohne Skelet -> set keypoint -> on_next_kp -> Skelet erzeugen
    -> Besser: Neues Bild -> Skelet erzeugen
→ refactor toolkit (color / shape -> seperate)
→ QApplication nicht in Controller, sondern in app.py
→  seperate shortcut / signal logic from app.py
→ seperate signal logic from controller.py
-> keypoints -> skeletons_data

## CONCEPTS

### CONTROLS (by Frequency)
1. set keypoint
    1.1 overwater & annotated -> [left click] + [w] | _[w] hier Sicherheitsmaßnahme_
    1.2 under water & annotated -> [right click] + [w] | _[w] hier Sicherheitsmaßnahme_
    1.3 estimated & annotated -> [left click] + [right click] + [w] | _[w] hier Sicherheitsmaßnahme_
    1.4 invisible & not annotated -> {next keypoint}
2. image navigation
    2.1 zoom step -> [left click] (if zoomed out) | _nur sinnvoll, wenn Taste mit panning geteilt wird_
    2.2 zoom adjustment -> [mouse wheel]
    2.3 panning -> [left click] (if zoomed in)
3. annotation navigation
    3.1 next keypoint
        3.1.1 manual -> [e]
        3.1.2 automatic -> {set keypoint}
    3.2 previous keypoint -> [q]
    3.3 next skeleton -> [d] | _Handposition muss leicht verändert werden_
    3.4 previous skeleton -> [a] | _Handposition muss leicht verändert werden_
    3.5 track id -> [1] - [9] | _Wie mit >9 umgehen?_
4. dataset navigation
    4.1 next image -> [right key] | _Links und Rechts weiter weg aber intuitiv_
    4.2 previous image -> [left key]

**BUTTONS REMAINING**: [s], [tab]?, [umschalt]