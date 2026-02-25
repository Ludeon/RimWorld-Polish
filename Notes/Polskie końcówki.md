# Zamiana ze starego backstories, używanie form z pliku Grammar.xml
NAME --> [PAWN_nameDef] - nazwa
HE, HECAP --> [PAWN_pronoun] - on, ona, ono
HIM --> [PAWN_objective] - go, ją, to
HIS --> [PAWN_possessive] - jego, jej, tego

# Dodanie wyrazów względem płci
{PAWN_gender ? : a}

# Powtórka z angielskiego
Mas = Masculine = Męski      = czerwony
Fem = Feminine  = Żeński     = czerwona
Neu = Neuter    = Nijaki     = czerwone
Gen = Genetive  = Dopełniacz = kiszka -> kiszek

# Znaki specjalne
Rimworld używa niestandardowego znaku NEWLINE (czyli takiego, który przenosi tekst do następnego wiersza):
\n      (pojedynczy)
oraz

\n\n    (podwójny)