## 1. Projektets syfte och uppställning
 
**Syfte *(antagande)*:** Undersöka hur en enkel LDR reagerar på ljus från en RGB-LED, kanal för kanal och i kombination. Det är ett första steg mot en billig "RGB-ljussensor", där man vill veta om och hur en enda LDR kan användas för att skilja färger åt.

Ett delmål av projektet cirkulerade dessutom kring om hur man enkelt skulle kunna extrahera och dokumentera serial-data. 

**Hårdvara:**
 
| Komponent | Koppling | Källa |
|---|---|---|
| Arduino Uno | - | - |
| RGB-LED, röd | pin 11 (PWM) | `#define RED 11` |
| RGB-LED, blå | pin 10 (PWM) | `#define BLUE 10` |
| RGB-LED, grön | pin 9 (PWM) | `#define GREEN 9` |
| LDR | `A0` (analog in, 10 bitar → 0-1023) | `#define LDR A0` |
 
**Dataflöde:**

```
 sin()-svep ──► PWM (RGB-LED) ──► ljus ──► LDR ──► ADC (A0)
                                                      │
 data.csv ◄── py-monitor.py ◄── seriell text ◄────────┘
     │
     └──► py-plotter.py ──► grafer (python/img/*.png)
```

---

## 2. Kod
 
Koden består av tre filer som tillsammans bildar en mätkedja: Arduinon styr ljuset och mäter, och Python sparar och ritar resultatet.
 
| Fil | Vad den gör |
|---|---|
| `src/main.cpp` | Arduino-program. Svepar RGB-LED:ens färger med sinuskurvor (PWM) och skickar LDR-värdet över serieporten. |
| `scripts/py-monitor.py` | Läser serieporten och sparar raderna i en ny fil; `data.csv`. |
| `scripts/py-plotter.py` | Läser `data.csv` och ritar LDR-värdet mot mätindex. |

---
 
## 3. Tolkning av resultaten
 
### 3.1 Så läser du graferna
 
- **X-axel:** mätindex (radnummer i `data.csv`), alltså en tidsliknande axel men utan känd tidsenhet.
- **Y-axel:** LDR-avläsningen på ADC:n (0–1023). Axeln heter "LED Strength" i graferna.
- **"Whole"-bilder:** hela mätserien över ett par sekunder. 
- **"Clip"-bilder:** zoom på ~80 punkter, där man ser den snabba växlingen punkt för punkt.


### 3.2 Resultat

1. **Principen fungerar.** LDR:n följer LED-ljusets sinusvariation tydligt, i alla fyra körningarna.
2. **Svaret är inverterat** (mer ljus → lägre värde). Det tyder på att LDR:n sitter i den nedre delen av en spänningsdelare, mot GND *(slutsats från datan, kopplingsschema saknas)*.
3. **Dynamiken är mycket liten.** Hela signalen ligger nära ADC-taket (≈ 1012–1023), och en enskild färg ger bara 0,6–1 % av skalan. Med ett brusgolv på ± några steg är det svårt att skilja färger åt med nuvarande uppställning. Det tyder på att motståndsvärdet i spänningsdelaren inte är anpassat till LDR:ns resistans, eller att LDR och LED sitter för långt isär eller att omgivningsljuset är för starkt *(hypotes)*.
4. **Ordningen mellan färgerna (grön ≳ röd > blå)** kan bero på att LDR:er ofta är känsligast i det gröna/gula området, men den kan lika gärna bero på att LED-kanalerna lyser olika starkt vid samma PWM-värde. Experimentet kan inte skilja dessa effekter åt utan en kalibrerad referens.

### 3.3 Går det att beräkna den exakta färgen på ljuset?
Kort sagt, nej. LDR:n ger bara ett enda tal, och det talet räcker inte för att avgöra vilken färg ljuset har.

1. En färg består av tre delar (R, G, B), men LDR:n summerar allt ljus som träffar den till ett värde mellan 0 och 1023. Det går därför inte att räkna ut hur mycket av varje färg som ingick. I körningen “alla samtidigt” ligger värdet på ≈ 993–1022, men det avslöjar inte vilken kanal som bidrog med vad. Olika färgblandningar kan ge samma värde. Det syns också på att svaret verkar vara ungefär additivt: 6 + 9 + 11 ≈ 26, vilket är nära det samlade utslaget på ≈ 30. Ljuset från de tre kanalerna blandas ihop till en enda siffra.
2. LDR-värdet beror på både ljusstyrka och färg.
3. Skillnaderna mellan färgerna är för små. Hela signalen ligger nära ADC-taket, och utslaget är bara ≈ 6 steg för blå, ≈ 9 för röd och ≈ 11 för grön. Den regelbundna snabba svängningen är ± 2–3 steg (upp till ≈ 15 vid samtidig körning), och röd-serien har dalar ner till ≈ 947. Skillnaden mellan färgerna är alltså av samma storlek som störningarna, och vid ADC-taket klipps signalen dessutom (platåerna vid 1023).
