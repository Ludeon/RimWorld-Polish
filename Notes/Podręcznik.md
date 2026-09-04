# Zamiana ze starego backstories, używanie form z pliku Grammar.xml
NAME --> [PAWN_nameDef] - nazwa (np. Jan, Anna)  
HE, HECAP --> [PAWN_pronoun] - on, ona, ono  
HIM --> [PAWN_objective] - go, ją, to  
HIS --> [PAWN_possessive] - jego, jej, tego  

# Dodanie wyrazów względem płci
{PAWN_gender ? : a}

∗ ∗ ∗

PRZYKŁAD:  
To [PAWN_pronoun], [PAWN_nameDef], był{PAWN_gender ? y : a : y} farmer{PAWN_gender ? : ka}. Lubią [PAWN_possessive] psy, a [PAWN_possessive] koty są dobrze wychowane.  

CO DAJE (zależnie od płci postaci):  
To on, Jan, były farmer. Lubią go psy, a jego koty są dobrze wychowane.  
To ona, Anna, była farmerka. Lubią ją psy, a jej koty są dobrze wychowane.  
To ono, XYZ-12, były farmer. Lubią to psy, a tego koty są dobrze wychowane.  

∗ ∗ ∗

PORADA:  

Dobrą praktyką jest używanie {PAWN_gender} do dodawania końcówek, zamiast całych wyrazów, czyli:  

biurokrat{PAWN_gender ? a : ka}, zamiast {PAWN_gender ? biurokrata : biurokratka}  

Ostatecznie, wybór formy pozostaje do decyzji tłumacza, ale pierwszy wzór redukuje rozmiar pliku i długość linijki, przede wszystkim w dużych plikach typu Backstories.xml.  

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

∗ ∗ ∗

PRZYKŁAD:  
Do Twojej kolonii przybyły następujące postaci:\n\nJan\nAnna\nXYZ-12  

CO DAJE (w grze – np. w wiadomości):  
Do Twojej kolonii przybyły następujące postaci:  

Jan  
Anna  
XYZ-12  

∗ ∗ ∗

# Objaśnienia tagów
Pracując nad tłumaczeniem możesz napotkać następujące tagi:
* TODO  
    ⤷ Najpowszechniejszy tag, wprowadzany automatycznie podczas czyszczenia tłumaczenia. Przy generowaniu raportu tłumaczenia odpowiada za ostrzeżenie "translations missing". Zastępujemy go tłumaczeniem.  
* FIXME  
    ⤷ Tag wstawiany przez innych tłumaczy. Gdy takowy zauważysz, przeanalizuj dokładnie tekst oryginalny oraz obecne tłumaczenie i zastanów się, co można zrobić lepiej.  
* UNUSED  
    ⤷ Tag wprowadzany automatycznie podczas czyszczenia tłumaczenia. Przy generowaniu raportu tłumaczenia odpowiada za ostrzeżenie "translations load errors". Aby się go pozbyć, należy usunąć nieużywane linijki kodu znajdujące się poniżej – ważne! – zweryfikuj najpierw ich stan generując raport tłumaczenia. Kieruj się instrukcjami z raportu.  

### PRZYKŁAD: TODO

Wycinek z TranslationReport.txt:
```
UseGlobalStyle 'Use global style' (English file: Dialogs_Various.xml:10) (placeholder exists in Dialogs_Various.xml:16)
```
...kieruje on nas do pliku `Dialogs_Various.xml`, 16 linijka (nie musimy też kierować się tutaj raportem tłumaczenia — korzystając z Visual Studio Code wystarczy, że użyjemy Ctrl+Shift+F i wpiszemy "TODO" — wyszukiwarka pokaże nam wszystkie tego typu tagi w plikach tłumaczenia.)

```
XML
  <!-- EN: Use global style -->
  <UseGlobalStyle>TODO</UseGlobalStyle>
```
Tłumaczymy taką linjkę normalnie, uważając by nie skasować przypadkiem któregoś z nawiasów (> <):
```
XML
  <!-- EN: Use global style -->
  <UseGlobalStyle>Używaj stylu globalnego.</UseGlobalStyle>
```
Przetłumaczone :]


### PRZYKŁAD: UNUSED

Wycinek z TranslationReport.txt:
```
Found no RimWorld.AbilityDef named AnimaTreeLinking to match AnimaTreeLinking.label (Abilities.xml)
```

Udajemy się do wskazanego pliku i usuwamy nieużywane linijki tłumaczenia. (W tym konkretnym przypadku, usunąłem również plik oraz folder, które zostałyby puste.)
