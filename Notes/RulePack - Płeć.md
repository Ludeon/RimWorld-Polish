Pliki generatora nazw akceptują dodatkowe zasady, nawet jeśli nie ma ich w angielskim tekście. Są to obecnie:
(asker_gender==) Male, Female, (Neuter?)
(animal==)...  


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
