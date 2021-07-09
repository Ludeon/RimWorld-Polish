Tutorialik generatora nazw frakcji oraz innych, jak to się robi.

Pliki można nazywać jak się chcę, ale trzeba potem trzymać się tych nazw.

Mas = Masculine = Męski      = czerwony
Fem = Feminine  = Żeński     = czerwona
Neu = Neuter    = Nijaki     = czerwone
Gen = Genetive  = Dopełniacz = kiszka -> kiszek

<li>r_name(p=0.4)->The Eaters of [Gore]</li>
(p=liczba)   Priorytet, im wyższa liczba, tym większa szansa na pojawienie się tej nazwy. Kod (p=0.4) oznacza, że będzie się pojawiać bardzo rzadko. Stosowanie tego kodu pojawia się w niektórych przypadkach. Najlepiej trzymajmy się domyślnych wartości.


<li>r_name->The Eaters of [Gore]</li>
[Gore] oryginalnie prowadzi do pliku: \Strings\Words\Nouns\Gore.txt   (a w  nim mamy  np. słowo "kiszka", "serce")

czyli tłumaczymy zwykły tekst:
<li>r_name(p=0.4)->Zjadacze [Gore]</li>
efekt końcowy: Zjadacze kiszka, Zjadacze serce - czyli nie tego nam trzeba


Stworzymy teraz własny plik ze słówkami i nazwiemy go Gore_Gen.txt
Teraz w pliku Gore_Gen.txt robimy słowa "kiszek", "serc".

Ale teraz musimy wskazać ścieżkę do Gore_Gen.txt  za pomocą  <Nazwa.rulePack.rulesFiles>  wybieramy_jakas_nazwe->Words/Nouns/Gore_Gen

przykładowo będzie: goRe_mnoga-> czyli:
<NamerFactionPirate.rulePack.rulesFiles>  
   <li>goRe_mnoga->Words/Nouns/Gore_Gen</li>
</NamerFactionPirate.rulePack.rulesFiles>

Dlaczego goRe -zwracamy uwagę na wielkość liter, jeśli jest goRe_mnoga->  musimy używać potem [goRe_mnoga] bo inaczej będzie problem. Ja daje wszystko z małych. Więc jak zrobimy sobie ColorBadass_GEN->  to [colorbadass_gen] nie podziała :)

I tym sposobem kod [goRe_mnoga] bierze słówka z pliku Words/Nouns/Gore_Gen

<li>r_name(p=0.4)->Zjadacze [goRe_mnoga]</li>
efekt:
Zjadacze Kiszek, Zjadacze Serc, itd. w zależności od wpisanych słówek do pliku .txt



Na koniec taki przykład

ścieżki plików:
<NamerFactionPirate.rulePack.rulesFiles>  
  <li>KoloryFem->Words/Nouns/Kolorki_Fem</li>
  <li>animals_fem->Words/Nouns/Zwierzaki_Fem</li>
</NamerFactionPirate.rulePack.rulesFiles>

kod:
<NamerFactionPirate.rulePack.rulesStrings>
   <li>r_name->[KoloryFem] [animals_fem]</li>   = Czerwona Żaba
</NamerFactionPirate.rulePack.rulesStrings>





