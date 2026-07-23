Pliki generatora nazw akceptują dodatkowe zasady, nawet jeśli nie ma ich w angielskim tekście. Są to obecnie:
(asker_gender==) Male, Female, (Neuter?)
  ⤷ Płeć questgivera.
(joiner_gender==Male)
  ⤷ Płeć questgivera (jeżeli jest uciekinierem/dezerterem).
(animal==) Dog, Cat, ...
  ⤷ Gatunek zwierzęcia.
(animalCount==) 1, 2, 3, ...
  ⤷ Liczba zwierząt.
(askerIsNull==) true, false
  ⤷ Sprawdza czy questgiver to konkretna postać, która może pojawić się w grze, np. John "Jan" Smith z frakcji Imperium (false) czy pozostaje niezdefiniowana np. "handlarz orbitalny" (true)
(asker_royalInCurrentFaction==) True, False
  ⤷ Sprawdza czy questgiver posiada tytuł szlachecki.
(asker_factionLeader==)
  ⤷ Sprawdza czy questgiver to lider frakcji.

Nawiasy akceptują dowolny operator matematyczny, np. ==, >=, <=, itd.

Dla przykładu, oryginał:
```
XML

  <!-- EN:
    <li>questName->the [adjAny] [asker_royalTitleInCurrentFaction]</li>
    <li>adjAny->hunted</li>
    <li>adjAny->fleeing</li>
    <li>adjAny->solitary</li>
    <li>adjAny->ambushed</li>
  -->

```

Zaś weersja przetłumaczona wygląda tak:
```
XML

  <Intro_Wimp.questNameRules.rulesStrings>
    <li>questName->[adjAny] [asker_royalTitleInCurrentFaction]</li>
    <li>adjAny(asker_gender==Male)->goniony</li>
    <li>adjAny(asker_gender==Female)->goniona</li>
    <li>adjAny(asker_gender==Male)->uciekający</li>
    <li>adjAny(asker_gender==Female)->uciekająca</li>
    <li>adjAny(asker_gender==Male)->samotny</li>
    <li>adjAny(asker_gender==Female)->samotna</li>
    <li>adjAny(asker_gender==Male)->zaatakowany</li>
    <li>adjAny(asker_gender==Female)->zaatakowana</li>
    <li>adjAny(asker_gender==Male)->napadnięty</li>
    <li>adjAny(asker_gender==Female)->napadnięta</li>
  </Intro_Wimp.questNameRules.rulesStrings>

```
