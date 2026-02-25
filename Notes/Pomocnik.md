# Krzesło z drewna - materiały
[Plik] = Misc.xml
<ThingMadeOfStuffLabel> {1} {0} <ThingMadeOfStuffLabel>
<ThingMadeOfStuffLabel> {1=mebel} {0=surowiec} <ThingMadeOfStuffLabel>

Słowa brane z: 
{1} - [DefInjected\ThingDef\Buildings_Furniture.xml]
{0} - [DefInjected\ThingDef\Items_Resource_Stuff.xml]

`Problem: Śpiwór Wełna owcy`
``Rozwiązanie: Śpiwór z owczej wełny`` - w [DefInjected\ThingDef\Items_Resource_Stuff.xml] jest możliwość zdefiniowania formy przymiotnikowej.

# Ktoś z rodziny - relacje
[Plik] = Misc_Gameplay.xml
<Relationship>To {0} {1}<Relationship>

{0} - DefInjected\PawnRelationDef\PawnRelations_FamilyByBlood.xml
{1} - kolonista IMIE

`Problem: To brat kolonista John ` - jak utworzyć formę dopełniacza?

#