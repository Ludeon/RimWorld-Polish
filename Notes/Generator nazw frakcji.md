Generator nazwy frakcji, jak to się robi.

Pliki można nazywać jak się chcę, ale trzeba potem trzymać się tych nazw.

Mas = Masculine = Męski      = czerwony
Fem = Feminine  = Żeński     = czerwona
Neu = Neuter    = Nijaki     = czerwone
Gen = Genetive  = Dopełniacz = kiszka -> kiszek

<li>r_name(p=0.4)->The Eaters of [Gore]</li>
(p=liczba)   Priorytet, im wyższa liczba, tym większa szansa na pojawienie się tej nazwy. Kod (p=0.4) oznacza, że będzie się pojawiać bardzo rzadko. Stosowanie tego kodu pojawia się w niektórych przypadkach.


<li>r_name->The Eaters of [Gore]</li>
[Gore] prowadzi do pliku: \Strings\Words\Nouns\Gore.txt   (a w  nim mamy  np. słowo "kiszka", "serce")

czyli tłumaczymy zwykły tekst:
<li>r_name(p=0.4)->Zjadacze [Gore]</li>
efekt końcowy: Zjadacze kiszka, Zjadacze serce - czyli nie tego nam trzeba


Stworzymy teraz plik Gore_Gen.txt, chociaż możemy posłużyć się Gore.txt, to dla lepszej czytelności stworzymy własny oznaczony Gen - Dopełniacz. 
Teraz w pliku Gore_Gen.txt robimy słowa "kiszek", "serc".

Ale teraz musimy wskazać ścieżkę do pliku Gore_Gen.txt  za pomocą  <Nazwa.rulePack.rulesFiles> i ścieżki  gore->Words/Nouns/Gore_Gen

<NamerFactionPirate.rulePack.rulesFiles>  
   <li>gore->Words/Nouns/Gore_Gen</li>
</NamerFactionPirate.rulePack.rulesFiles>


<NamerFactionPirate.rulePack.rulesStrings>
   <li>r_name(p=0.4)->Zjadacze [Gore]</li>   - kod [Gore] prowadzi teraz do Gore_Gen-txt więc przydało by się zmienić [Gore] na [Gore_Gen] dla czytelności.
</NamerFactionPirate.rulePack.rulesStrings>


<li>gore_gen->Words/Nouns/Gore_Gen</li>   i od teraz stosujemy [Gore_Gen] 
<li>r_name(p=0.4)->Zjadacze [Gore_Gen]</li>

efekt:
Zjadacze Kiszek, Zjadacze Serc, itd. w zależności od wpisanych słów do pliku .txt



Na koniec taki przykład:

ścieżki plików:
<NamerFactionPirate.rulePack.rulesFiles>  
  <li>kolory_żeński->Words/Nouns/kolorki_fem</li>    [kolory_żeński] będzie odczytywał słowa z pliku "kolorki_fem.txt"
  <li>kolory_męski->Words/Nouns/kolorki_mas</li>
  <li>zwierzęta_żeński->Words/Nouns/zwierzaki_fem</li>
  <li>weapon_male->Words/Nouns/bronie_masc</li>
</NamerFactionPirate.rulePack.rulesFiles>

kody:
<NamerFactionPirate.rulePack.rulesStrings>
   <li>r_name->[kolory_żeński] jak [zwierzęta_żeński]</li>
   <li>r_name->Straszliwy [weapon_male]</li>
   <li>r_name->Straszliwy [kolory_męski] [weapon_male]</li>
</NamerFactionPirate.rulePack.rulesStrings>


efekty:
Czerwona jak Alpaka 
Straszliwy Miecz
Straszliwy Czarny Karabin


Oczywiście to tylko taki tutorial, nazwy robimy porządniejsze ;)


