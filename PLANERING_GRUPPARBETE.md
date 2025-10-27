
#### VIKTIG INFO ####

##################################################################################
####### Plan för nätverksskanner-projektet (2+ timmar) Onsdag till Söndag! #######
##################################################################################

Vi kör som standard 2 timmar varje dag tills uppgiften är klar.
Här kommer lite regler att följa, vill ni lägga till något så hojta till så fixar jag det.

## Alla ska vara med hela tiden, diskutera, testa och skriva kod ihop.
## En person skriver, och vi byter skrivare var 30–45 minuter så alla får bidra.
## Fokus är att få skannern att fungera med kvalitet.

##################################################################

# Arbetsupplägg
• Vi jobbar tillsammans på en dator. (Skrivaren streamar på discord eller i klassen)
• En skriver, resten hjälper till att tänka, googla, förklara och testa.
• Vi roterar skrivare efter varje delmoment eller efter 30-45 min.
• Alla ska förstå vad som händer i koden. INGEN bara “tittar på”. annars är du underkänd :D 
• Vi gör anteckningar medan vi kodar så dokumentationen blir lätt sen.
       (Kanske han som skriver koden kör annteckningar också?)

##################################################################

# Plan – steg för steg

0. Start ! 

• Importera socket. Duuh..?!
• Testa att ni kan ansluta till scanme.nmap.org port 80 för att se att det funkar.
• Om det går bra då kör vi vidare på nästa steg!

1. Enkel portkontroll 

# Mål: Kolla om en port är öppen eller stängd.
• Skriv en funktion som testar EN port. 
• Hantera fel: timeout, connection refused, osv.
• Printa “Port X: öppen” eller “Port X: stängd”. (förslag) ?
• Testa mot scanme.nmap.org, port 80.
• Diskutera varför man måste stänga socketen. (why!?!?)

#### ! När det fungerar: vi går vidare. ! ####

2. Flera portar!

# Mål: Skanna flera portar i rad (t.ex. 20–100).
• Gör en loop som går igenom portarna.
• Sätt timeout (t.ex. 0.5-2 sekunder).
• Visa resultat löpande i terminalen.
• Testa att den hittar öppna portar.
• Skriv ut tydligt vilka som är öppna/stängda.

Har vi gjort alla dessa steg är grunden klar.

3. Banner grabbing!

# Mål: Identifiera vilken tjänst som körs på en öppen port.
• När ni hittar en öppen port, försök ta emot data med recv().
• Om ni får text, skriv ut den (t.ex. “SSH” eller “HTTP”).
• Fånga fel så programmet inte kraschar.
• Testa på scanme.nmap.org och se om ni får något svar.

#### Diskutera: Varför vissa tjänster inte svarar direkt. ####

4. Fixa enkel användarvänlighet!

# Mål: Göra programmet lite smidigare.
Välj 2–3 saker som ni hinner:
• Låta användaren skriva in IP och portintervall.
• Visa förlopp (t.ex. “Skannar port 30/100”).
• Spara resultat till textfil.
• Färga utdata (valfritt, om ni hinner).

 ### Prioritet: IP + portintervall + spara resultat. ####

5. Test & dokumentation

# Mål: Testa snabbt och se att allt fungerar.
• Testa med felaktiga IP-adresser och intervall.
• Se att det inte kraschar.
• Testa utan nätverk... vad händer? :O
• Skriv några korta kommentarer i koden.
• Skapa (#README#) som kort men detaljerat beskriver hur man kör programmet.

## Kör en sån här också så det blir tydligt för alla oss ## 

## Dag 1 - 2 (Onsdag - Torsdag) ##
# Mål: Få den enkla portskannern att fungera (Steg 1–2)
# Resultat: Enkel skanner som listar öppna/stängda portar.
• Skapa Python-fil och importera socket.
• Skriv funktion för att testa en port (hantera timeout och connection refused).
• Utöka till loop för portintervall (t.ex. 20–100).
• Kör test mot scanme.nmap.org och verifiera öppna/stängda portar.
# Diskussionspunkter:
• Skillnaden mellan timeout och connection refused.
• Varför stänga socketen ordentligt?

## Dag 2 - 3 (Torsdag - Fredag) ##
# Mål: Lägg till banner grabbing (Steg 3) och minst en användarfunktion (Steg 4)
# Resultat: Skanner identifierar minst en tjänst och har grundläggande UX-funktion.
• När port är ÖPPEN: försök recv() för att läsa banner.
• Tolka enkla banners (t.ex. innehåll som visar SSH eller HTTP).
• Implementera minst en extra funktion (välj 1–2):
• Spara resultat till fil, eller
• Förloppsindikator (t.ex. “Skannar 30/100”)....
• CLI-argument för host/start/end/timeout.
# Diskussionspunkter:
• Varför svarar vissa tjänster inte direkt?
• Rimliga timeout-värden (0.5–1s).

## Dag 3 - 5 (Fredag - Söndag) ##
Mål: Testa noggrant, skriva README och förbereda inlämning/presentation
Resultat: Fullt testad skanner + dokumentation redo att lämnas in.
# Att göra: #
• Testa på scanme.nmap.org med olika intervall.
• Testa felhantering: ogiltig host, ogiltigt intervall, nätverksbortfall.
• Skriv kort README: hur man kör (exempelkommando), vad programmet gör, kända begränsningar.
• Förbered och samla leverabler: kodfil(er), scan_results.txt, README.
# Diskussionspunkter:
• Vad var svårast och vad lärde vi oss?
• Vad skulle vi vilja lägga till om vi haft mer tid?
•------------------------------------------------------
End of program... Time to sleep...........
                                    ................
                                        .................











