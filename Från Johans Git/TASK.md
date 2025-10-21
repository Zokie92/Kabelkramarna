# Nätverksskanner-projekt

**Uppskattad tid:** 4 timmar  
**Svårighetsgrad:** Nybörjare  
**Gruppstorlek:** 2-3 studenter (rekommenderat)

## Lärandemål

I slutet av detta projekt kommer du att förstå:

- Hur nätverksportar fungerar och varför de är viktiga
- Hur man använder Pythons socket-bibliotek för nätverkskommunikation
- Grundläggande nätverksprotokoll (TCP/UDP)
- Hur man hanterar nätverkstimeouts och fel
- Hur nätverksskanningsverktyg fungerar

## Bakgrund: Vad du behöver veta

### Vad är en port?

Tänk på en IP-adress som en byggnadsadress och portar som individuella lägenhetsnummer. En dator kan ha många tjänster som körs (webbserver, e-post, fildelning), och varje tjänst "lyssnar" på ett annat portnummer.

**Vanliga portar:**

- Port 80: HTTP (webbplatser)
- Port 443: HTTPS (säkra webbplatser)
- Port 22: SSH (säker fjärråtkomst)
- Port 21: FTP (filöverföring)

### Vad är portskanning?

Portskanning är att kontrollera vilka "dörrar" (portar) på en dator som är öppna och accepterar anslutningar. Detta är användbart för:

- Nätverksadministratörer som kontrollerar sina egna system
- Att förstå vilka tjänster som körs
- Att lära sig om nätverkssäkerhet

**Viktigt:** Skanna endast system du äger eller har explicit tillstånd att skanna!

## Projektsteg

### Steg 1: Kontroll av en enskild port (45 minuter)

**Mål:** Skapa ett program som kontrollerar om EN specifik port är öppen på EN målvärd.

**Vad du behöver ta reda på:**

1. Hur man importerar och använder Pythons `socket`-bibliotek
2. Hur man skapar en socket-anslutning till en specifik IP-adress och port
3. Hur man avgör om anslutningen lyckades eller misslyckades
4. Hur man hanterar att anslutningen stängs ordentligt

**Testa din kod på:**

- `scanme.nmap.org`
- Port 80

**Frågor att diskutera i din grupp:**

- Vad händer när du försöker ansluta till en stängd port?
- Vilket undantag/fel ger Python dig?
- Varför behöver vi stänga socketen efter testning?

### Steg 2: Skanner för flera portar (60 minuter)

**Mål:** Utöka ditt program för att skanna ett INTERVALL av portar (t.ex. port 20-100).

**Nya utmaningar:**

1. Hur kommer du att loopa igenom flera portnummer?
2. Hur bör du lagra och visa resultaten?
3. Vad händer om skanningen är väldigt långsam? (Tips: tänk på timeouts)

**Saker att överväga:**

- Ska ditt program skriva ut resultat när det hittar dem, eller allt på en gång i slutet?
- Hur kan du göra skanningen snabbare utan att bryta saker?
- Vad är ett rimligt timeout-värde? För kort? För långt?

**Utdata bör visa:**

```
Skannar 192.168.1.1...
Port 22: ÖPPEN
Port 23: STÄNGD
Port 80: ÖPPEN
...
```

### Steg 3: Tjänsteidentifiering (60 minuter)

**Mål:** När du hittar en öppen port, försök identifiera vilken TJÄNST som körs där.

**Utmaning:** Olika tjänster svarar olika när du ansluter till dem. Vissa tjänster skickar en "banner" som identifierar dem.

**Vad du behöver undersöka:**

1. Hur man tar emot data från en socket efter anslutning
2. Hur tjänster identifierar sig själva (banner grabbing)
3. Hur man hanterar tjänster som inte skickar data omedelbart

**Skapa en funktion som:**

- Ansluter till en öppen port
- Försöker ta emot bannern/hälsningen
- Identifierar vanliga tjänster (HTTP, SSH, FTP, etc.)
- OBS: Räcker att identifiera en tjänst

**Tips:** Vissa tjänster behöver att du skickar data först innan de svarar!

### Steg 4: Användargränssnitt & funktioner (60 minuter)

**Mål:** Gör din skanner användarvänlig och lägg till användbara funktioner.

**Funktioner att implementera (välj minst 3):**

1. **Kommandoradsargument:** Låt användare specificera mål och portintervall
2. **Förloppsindikator:** Visa skanningsförlopp (t.ex. "Skannar port 45/100")
3. **Spara resultat:** Skriv resultat till en textfil
4. **Flera värdar:** Skanna flera IP-adresser från en lista
5. **Färgad utdata:** Använd färger för att markera öppna portar (undersök `colorama`-biblioteket)
6. **Skanningshastighetsalternativ:** Snabb, normal eller grundlig läge

**Exempel på god användarupplevelse:**

```
Nätverksskanner v1.0
====================
Mål: 192.168.1.1
Portintervall: 20-1000
Timeout: 1 sekund

Skannar... [████████░░] 80%

Resultat:
---------
Port 22 [ÖPPEN] - SSH (OpenSSH 8.2)
Port 80 [ÖPPEN] - HTTP (nginx)
Port 443 [ÖPPEN] - HTTPS

Skanning slutförd på 45 sekunder
3 öppna portar hittades
Resultat sparade i scan_results.txt
```

### Steg 5: Testning & dokumentation (15 minuter)

**Mål:** Testa din skanner noggrant och dokumentera din kod.

**Testchecklista:**

- [ ] Testa på scanme.nmap.org
- [ ] Testa med giltiga och ogiltiga IP-adresser
- [ ] Testa med ogiltiga portintervall
- [ ] Testa felhantering (vad händer om internet är frånkopplat?)
- [ ] Testa med olika timeout-värden

**Dokumentation:**

- Lägg till kommentarer som förklarar varje funktion
- Skapa en README som förklarar hur man använder din skanner
- Dokumentera eventuella begränsningar eller kända problem

## Tips & råd (Inte lösningar!)

### Komma igång med sockets

```python
import socket

# Du behöver:
# 1. Skapa ett socket-objekt
# 2. Sätta en timeout (så att den inte väntar för evigt)
# 3. Försöka ansluta till (host, port)
# 4. Hantera framgång eller misslyckande
# 5. Stänga socketen
```

### Hantera fel

Nätverksoperationer kan misslyckas av många anledningar! Du bör hantera:

- Connection refused (port stängd)
- Timeouts (värd svarar inte)
- Ogiltiga värdnamn/IP-adresser
- Nätverket är onåbart

Undersök: Vilka undantag kastar socket.connect?

### Göra det snabbare

Om skanning av 1000 portar tar för lång tid, tänk på:

- Är din timeout för lång?
- Kan du skanna flera portar samtidigt? (Avancerat: undersök threading)
- Väntar du i onödan mellan skanningar?

### Arbeta i grupper

**Föreslagen arbetsfördelning:**

- **Person 1:** Grundläggande skanningslogik (Steg 1-2)
- **Person 2:** Tjänsteidentifiering och banner grabbing (Steg 3)
- **Person 3:** Användargränssnitt och funktioner (Steg 4)

**Viktigt:** Även om ni delar upp uppgifter ska alla förstå ALL kod!

## Utmaningar för vidareutveckling (Om ni blir klara i förtid)

1. **Trådad skanning:** Använd Pythons `threading`-modul för att skanna flera portar samtidigt
2. **OS-detektion:** Försök gissa vilket operativsystem målet kör
3. **Skanningsprofiler:** Skapa förinställda skanningstyper (snabb, standard, omfattande)
4. **Nätverksintervallskanning:** Skanna alla datorer i ett subnät (t.ex. 192.168.1.1-254)
5. **GUI-version:** Skapa ett grafiskt gränssnitt med tkinter
6. **Jämför med Nmap:** Installera nmap och jämför dina resultat med det professionella verktyget

## Resurser att utforska

- Pythons socket-dokumentation
- Lista över vanliga portnummer
- Skillnader mellan TCP och UDP
- Nätverksprotokollspecifikationer

## Leverabler

I slutet av sessionen ska din grupp ha:

1. Fungerande Python-skanner som kontrollerar flera portar
2. Kod med kommentarer och dokumentation
3. README-fil med användningsinstruktioner
4. Testresultat som visar att det fungerar på åtminstone scanme.nmap.org

## Viktiga påminnelser

⚠️ **Skanna ENDAST system du äger eller har tillstånd att skanna!**  
⚠️ Att skanna obehöriga system kan vara olagligt  
⚠️ Vissa nätverk kan blockera eller flagga skanningsaktivitet  
⚠️ Testa alltid på scanme.nmap.org först

## Frågor att överväga under utveckling

1. Varför kan vissa portar verka stängda även om en tjänst körs?
2. Vad är skillnaden mellan en stängd port och en filtrerad port?
3. Varför tar nätverksskanningar tid? Kan de någonsin vara omedelbara?
4. Hur påverkar brandväggar portskanning?
5. Vilka etiska överväganden finns för nätverksskanningsverktyg?

---

**Lycka till! Kom ihåg: samarbete och experiment är nyckeln. Var inte rädd för att prova saker och se vad som händer!**
