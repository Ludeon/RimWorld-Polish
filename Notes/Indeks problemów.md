# "Krzesło z drewna" - materiały
{Rozwiązane przez Ludeon}  
[Plik] = Misc.xml  
[Fragment] = <ThingMadeOfStuffLabel> {1} {0} <ThingMadeOfStuffLabel>  

Na podstawie linijki tekstu powyżej, gra tworzy nazwę dla mebli według wzoru:  
{1} = mebel  
{0} = materiał  
Jeżeli zostawimy to tak jak jest, w grze zobaczymy następującą, błędną konstrukcję:
`Krzesło drewno` – zamiast tego, chcemy uzyskać naturalnie brzmiący rezultat, w tym przypadku "drewniane krzesło", ewentualnie "krzesło z drewna"

Słowa brane są z: 
{1} - [DefInjected\ThingDef\Buildings_Furniture.xml] (krzesło, szafa, stół warsztatowy...)  
{0} - [DefInjected\ThingDef\Items_Resource_Stuff.xml] (drewno, stal, jadeit...)  

Rozwiązanie:  
Chociaż forma `drewniane krzesło`, `stalowa szafa` nie została zaimplementowana (ponieważ nie ma możliwości odmiany przez rodzaje, tzn. mielibyśmy `drewniane krzesło`, `drewniane szafa`, `drewniane warsztat`) — w pliku [DefInjected\ThingDef\Items_Resource_Stuff.xml] jest możliwość zdefiniowania formy przymiotnikowej – zamiast to robić (co dałoby nieodmieniany, nienaturalny rezultat) potraktujemy to jako apppendix czyli użyjemy formy `X z materiału`, zamiast `materiałowe X`.  

Dzięki temu, dostaniemy `krzesło z drewna`, `stół warszatowy ze stali` itd.  

# "Jan, brat Anny" - relacje
NIEROZWIĄZANE  
[Plik] = Misc_Gameplay.xml  
[Fragment] = <Relationship>To {0} {1}<Relationship>  

{0} - DefInjected\PawnRelationDef\PawnRelations_FamilyByBlood.xml  
{1} - kolonista IMIE  

`Problem: To brat kolonista John ` - jak utworzyć formę dopełniacza?
