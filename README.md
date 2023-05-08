
# Canon Game

Dit is een multiplayer-spel genaamd "Cannon Game" dat is ontwikkeld met het behulp van Pygame en Python 3. Het spel draait op twee computers en communiceert over het netwerk sockets om gegevens tussen de twee computers te verzenden.



## Installatie

Dit spel vereist Python 3 en de Pygame-bibliotheek. Als je Python nog niet hebt geïnstalleerd, download en installeer het dan van de officiële Python-website. Pygame kan worden geïnstalleerd met behulp van pip:

```bash
pip install pygame
```

Voor de zekerheid kunt u ook de volgende commando's uitvoeren: 
```bash
pip install time
``` 
```bash
pip install random
``` 
```bash
pip install traceback
``` 
```bash
pip install socket
``` 
```bash
pip install threading
``` 
```bash
pip install pickle
``` 

## Gebruik
Voer het canon.py bestand uit in twee verschillende terminals om twee instanties van het spel te starten. De twee terminals zullen automatisch verbinding maken en het spel starten. Om foutmeldingen te voorkomen, dient u 5 seconden te wachten voordat u canon.py in de tweede terminal uitvoert.

Voorbeeld:
```bash
python canon.py

```
De speler gebruikt de pijltoetsen om de paddle omhoog of omlaag te bewegen en moet de bal terug naar de tegenstander schoppen. 

Het spel gaat door totdat een van de spelers 3 punten bereikt heeft, dat kan worden ingesteld met de variabele winning_score.
## Variabelen
- self.screen_width en self.screen_height: breedte en hoogte van het venster van de game.
- self.balls_shot: aantal ballen dat is afgevuurd door de speler.
- self.screen: het venster van het spel dat wordt gemaakt door Pygame.
- self.client_socket: de socket-object voor het client-server communicatie.
- self.screen_number: het nummer van het huidige venster (1 of 2).
- self.connection: de socket-object dat gebruikt wordt voor communicatie met het andere venster.
- self.white, self.black, self.red, self.green: RGB-tuple kleuren die worden gebruikt voor het tekenen van de achtergrond, objecten, tekst, etc.
- self.cannon_width, self.cannon_height: breedte en hoogte van het kanon.
- self.ball_radius: de straal van de bal die afgevuurd wordt door het kanon.
- self.ball_vel: de snelheid waarmee de bal beweegt.
- self.cannon_x, self.cannon_y: de coordinaten van de linkerbovenhoek van het kanon.
- self.cannon_vel: de snelheid waarmee het kanon beweegt.
- self.reset_ball(): een functie om de bal terug te zetten naar de beginpositie.
- self.next_ball_time: de tijd waarop de volgende bal afgevuurd moet worden.
- self.paddle_width, self.paddle_height: breedte en hoogte van de paddle.
- self.paddle_vel: de snelheid waarmee de paddle beweegt.
- self.paddle_x, self.paddle_y: de coordinaten van de linkerbovenhoek van de paddle.
- self.clock: de klok die gebruikt wordt om de tijd te beheren en de frames te limiteren.
- self.running: een waarde die aangeeft of het spel nog draait of niet.
- self.player_score, self.cannon_score: scores van de speler en het kanon.
- self.winning_score: de score die nodig is om het spel te winnen.
- self.get_network_status(): een functie om de netwerkstatus op te halen.
- self.handle_events(): een functie om gebeurtenissen te verwerken, zoals het sluiten van het venster.
- self.draw_score(): een functie om de scores op het scherm te tekenen.
- self.receive_data(): een functie om gegevens van het andere venster te ontvangen en de gamestatus bij te werken.
- self.send_data(): een functie om gegevens naar het andere venster te verzenden.
- self.draw_background(): een functie om de achtergrondkleur op het scherm te tekenen.
- self.move_cannon(): een functie om het kanon op en neer te bewegen.
- self.draw_cannon(): een functie om het kanon op het scherm te tekenen.
- self.shoot_ball(): een functie om een nieuwe bal af te vuren.
- self.check_winner(): een functie om te controleren of een van de spelers gewonnen heeft


## Tutorials die ik gevolgd heb om dit te spel te maken

 - [Make Pong With Python!](https://www.youtube.com/watch?v=vVGTZlnnX3U&t=120s)
 - [I coded Agar.io with Python (Using Sockets/Networking and Pygame)](https://www.youtube.com/watch?v=SR8xeaRXLcg)
 - [Online Multiplayer Game With Python - Sockets and Networking](https://www.youtube.com/watch?v=-3B1v-K1oXE&t=118s)
 - [Simple Cannon Game using Python](https://www.youtube.com/watch?v=E0UXAC6WnZI)
 - [Creating a Cannon Game Using Python](https://www.youtube.com/watch?v=7QjrOIbw2bg)
 - [Python Object Oriented Programming (OOP) - For Beginners](https://www.youtube.com/watch?v=JeznW_7DlB0)
 - [Python Pygame Tutorial - Episode 6! Creating Restart Code and Previous Run and High Score Tracking!](https://www.youtube.com/watch?v=atoGQ9o0ooI)
