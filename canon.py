import pygame
import time
import random
import traceback
import socket
import threading
import pickle
import pygame.font

class CannonGame:
    def __init__(self, width=800, height=600):
        # Initialize pygame
        pygame.init()

        # Set screen width and height
        self.screen_width = width
        self.screen_height = height
        self.balls_shot = 0

        # Create the game window
        try:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        except pygame.error:
            traceback.print_exc()
            pygame.quit()
            raise SystemExit

        # Create a client or server socket to communicate with another instance of the game
        self.client_socket = socket.socket()

        try:
            self.client_socket.connect(('localhost', 8000))
            print('Connected to server as client...')
            self.screen_number = 1
        except socket.error:
            self.server_socket = socket.socket()
            self.server_socket.bind(('0.0.0.0', 8000))
            self.server_socket.listen(1)
            print('Server started, waiting for a connection...')
            self.client_socket, address = self.server_socket.accept()
            print('Connection from', address)
            self.screen_number = 2

        # Set the connection object to use for communication based on whether this instance is client or server
        if self.screen_number == 1:
            self.connection = self.client_socket
        else:
            self.connection = self.client_socket

        # Set the window caption
        pygame.display.set_caption(f"Cannon Game - Screen {self.screen_number}")

        # Set up some color constants
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)

        # Set up some variables for the game objects and their movements
        self.cannon_width = 50
        self.cannon_height = 100
        self.ball_radius = 10
        self.ball_vel = 7

        # Set the initial position and movement direction of the cannon
        self.cannon_x = self.screen_width - self.cannon_width
        self.cannon_y = self.screen_height // 2 - self.cannon_height // 2
        self.cannon_vel = 6

        # Set up some variables for the ball object and its movement
        self.reset_ball()
        self.next_ball_time = time.time() + 3

        # Set up some variables for the paddle object and its movement
        self.paddle_width = 10
        self.paddle_height = 80
        self.paddle_vel = 5
        self.paddle_x = self.paddle_width
        self.paddle_y = self.screen_height // 2 - self.paddle_height // 2

        # Set up the game clock and running flag
        self.clock = pygame.time.Clock()
        self.running = True

        # Set up the initial scores and the winning score
        self.player_score = 0
        self.cannon_score = 0
        self.winning_score = 3

        # Start a thread to receive data from the other instance of the game
        threading.Thread(target=self.receive_data, daemon=True).start()

    def get_network_status(self):
        if self.screen_number == 1:
            return "Connected to server"
        else:
            return "Connected to client"

    # Handle events, such as the user closing the game window
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    # Draw the current scores on the screens
    def draw_score(self):
        # Set up a font object to use for the score text
        font = pygame.font.Font(None, 36)
        # Create text surfaces for the player and cannon scores
        player_score_text = font.render(f"Player: {self.player_score}", True, self.black)
        cannon_score_text = font.render(f"Cannon: {self.cannon_score}", True, self.black)
        # Blit the score text surfaces onto the game window
        self.screen.blit(player_score_text, (10, 10))
        self.screen.blit(cannon_score_text, (self.screen_width - 150, 10))

    # Receive and update game data from the other instance of the game
    def receive_data(self):
        while self.running:
            try:
                data = self.connection.recv(1024)
                if not data:
                    break
                data = pickle.loads(data)
                self.paddle_y = data["paddle_y"]
                self.cannon_y = data["cannon_y"]
                self.ball_x = data["ball_x"]
                self.ball_y = data["ball_y"]
                self.ball_dx = data["ball_dx"]
                self.ball_dy = data["ball_dy"]
                self.player_score = data["player_score"]
                self.cannon_score = data["cannon_score"]
            except:
                traceback.print_exc()
                self.running = False

    # Send game data to the other instance of the game
    def send_data(self):
        data = {
            "paddle_y": self.paddle_y,
            "cannon_y": self.cannon_y,
            "ball_x": self.ball_x,
            "ball_y": self.ball_y,
            "ball_dx": self.ball_dx,
            "ball_dy": self.ball_dy,
            "player_score": self.player_score,
            "cannon_score": self.cannon_score,
        }
        data = pickle.dumps(data)
        self.connection.sendall(data)

    # Draw the background color on the game window
    def draw_background(self):
        self.screen.fill(self.white)

    # Move the cannon up or down and reverse direction if it reaches the top or bottom of the game window
    def move_cannon(self):
        self.cannon_y += self.cannon_vel
        if self.cannon_y <= 0 or self.cannon_y + self.cannon_height >= self.screen_height:
            self.cannon_vel *= -1

    # Draw the cannon object on the game window, but only on the client's screen
    def draw_cannon(self):
        if self.screen_number == 1:
            pygame.draw.rect(self.screen, self.black, (self.cannon_x, self.cannon_y, self.cannon_width, self.cannon_height))

    # Launch a new ball if enough time has passed since the last one
    def shoot_ball(self):
        if time.time() >= self.next_ball_time:
            self.next_ball_time = time.time() + max(3 - (0.2 * self.balls_shot), 1)
            self.balls_shot += 1
            self.paddle_vel = 5 + (0.5 * self.balls_shot)

            self.reset_ball()

    # Check if either player has reached the winning score and display the winner if so
    def check_winner(self):
        if self.cannon_score >= self.winning_score:
            self.display_winner("Cannon")

    # Display the winning player's name on the game window and wait for 10 seconds before restarting the game
    def display_winner(self, winner):
        # Display the winning player's name on the game window
        font = pygame.font.SysFont(None, 48)
        text = font.render(f"Winner: {winner}", True, self.black)
        text_rect = text.get_rect()
        text_rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.screen.blit(text, text_rect)
        pygame.display.update()

        # Display the countdown message on the screen
        font = pygame.font.SysFont(None, 36)
        countdown = 10
        while countdown >= 0:
            countdown_text = font.render(f"Restarting in 10 Seconds... Please Wait !", True, self.black)
            countdown_rect = countdown_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
            self.screen.blit(countdown_text, countdown_rect)
            pygame.display.update()
            time.sleep(1)
            countdown -= 1

        # Reset the game variables
        self.balls_shot = 0
        self.player_score = 0
        self.cannon_score = 0
        self.reset_ball()

        # Reconnect to the other instance of the game
        if self.screen_number == 1:
            self.client_socket = socket.socket()
            self.client_socket.connect(('localhost', 8000))
            self.connection = self.client_socket
        else:
            self.server_socket.close()
            self.server_socket = socket.socket()
            self.server_socket.bind(('0.0.0.0', 8000))
            self.server_socket.listen(1)
            self.client_socket, address = self.server_socket.accept()
            self.connection = self.client_socket

        # Start a thread to receive data from the other instance of the game
        threading.Thread(target=self.receive_data, daemon=True).start()

    # Move the ball and check for collisions with the paddle or cannon, update the scores accordingly
    def move_ball(self):
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        # Reverse the ball's vertical direction if it hits the top or bottom of the game window
        if self.ball_y - self.ball_radius <= 0 or self.ball_y + self.ball_radius >= self.screen_height:
            self.ball_dy *= -1
        # If the ball hits the paddle, reverse its horizontal direction and update the player's score
        if self.ball_x - self.ball_radius <= self.paddle_width:
            if self.screen_number == 2:
                if self.ball_y >= self.paddle_y and self.ball_y <= self.paddle_y + self.paddle_height:
                    self.ball_dx *= -1
                    self.player_score += 1
                    self.send_data()
                else:
                    # If the ball misses the paddle, reset it and update the cannon's score
                    self.ball_x = self.screen_width - self.ball_radius
                    self.cannon_score += 1
                    self.send_data()
        # If the ball hits the cannon, reverse its horizontal direction
        elif self.ball_x + self.ball_radius >= self.screen_width - self.cannon_width:
            if self.screen_number == 1:
                if self.ball_y >= self.cannon_y and self.ball_y <= self.cannon_y + self.cannon_height:
                    self.ball_dx *= -1
                else:
                    # If the ball misses the cannon, reset it and send game data to the other instance
                    self.reset_ball()
                    self.send_data()

    # Draw the ball object on the game window, but only on the client's screen
    def draw_ball(self):
        if self.screen_number == 1 and self.ball_x - self.ball_radius > 0:
            pygame.draw.circle(self.screen, self.red, (self.ball_x, self.ball_y), self.ball_radius)
        elif self.screen_number == 2 and self.ball_x + self.ball_radius < self.screen_width:
            ball_x_on_screen_2 = self.screen_width - self.ball_radius - (self.screen_width - self.ball_x)
            pygame.draw.circle(self.screen, self.red, (ball_x_on_screen_2, self.ball_y), self.ball_radius)

    # Move the player's paddle up or down based on user input
    def move_paddle(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.paddle_y > 0:
            self.paddle_y -= self.paddle_vel
        if keys[pygame.K_DOWN] and self.paddle_y + self.paddle_height < self.screen_height:
            self.paddle_y += self.paddle_vel

    # Draw the player's paddle object on the game window, but only on the server's screen
    def draw_paddle(self):
        if self.screen_number == 2:
            pygame.draw.rect(self.screen, self.green, (self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height))

    def update_display(self):
        # Calculate the current fps
        fps = self.clock.get_fps()

        # Set up a font object to use for the fps and network status text
        font = pygame.font.Font(None, 24)

        # Create text surfaces for the fps and network status
        fps_text = font.render(f"FPS: {int(fps)}", True, self.black)
        network_status_text = font.render(self.get_network_status(), True, self.black)

        # Blit the fps and network status text surfaces onto the game window at the top center and bottom center, respectively
        fps_rect = fps_text.get_rect(center=(self.screen_width // 2, 10))
        network_status_rect = network_status_text.get_rect(center=(self.screen_width // 2, self.screen_height - 10))
        self.screen.blit(fps_text, fps_rect)
        self.screen.blit(network_status_text, network_status_rect)

        # Draw the current scores
        self.draw_score()

        # Update the game window display
        pygame.display.update()

    # Limit the game's frame rate to 60 fps
    def limit_frame_rate(self):
        self.clock.tick(60)

    # Reset the ball to its starting position with a random vertical velocity
    def reset_ball(self):
        self.ball_dx = -self.ball_vel
        self.ball_dy = random.randint(-self.ball_vel, self.ball_vel)
        self.ball_x = self.cannon_x - self.ball_radius
        self.ball_y = self.cannon_y + self.cannon_height // 2

    # Start a thread to receive data from the other game instance
    def run(self):
        # Start a thread to receive data from the other instance of the game
        threading.Thread(target=self.receive_data, daemon=True).start()

        # Handle game events, update game state, and redraw the game window
        while self.running:
            # Handle events, such as the user closing the game window
            self.handle_events()
            # Draw the background color on the game window
            self.draw_background()
            # Move the cannon up or down and reverse direction if it reaches the top or bottom of the game window
            self.move_cannon()
            # Draw the cannon object on the game window, but only on the client's screen
            self.draw_cannon()
            # Launch a new ball if enough time has passed since the last one
            self.shoot_ball()
            # Move the ball and check for collisions with the paddle or cannon, update the scores accordingly
            self.move_ball()
            # Draw the ball object on the game window, but only on the client's screen
            self.draw_ball()
            # Move the player's paddle up or down based on user input
            self.move_paddle()
            # Draw the player's paddle object on the game window, but only on the server's screen
            self.draw_paddle()
            # Draw the current scores on the game window
            self.draw_score()

            # Check if either player has reached the winning score and display the winner if so
            if self.player_score >= self.winning_score:
                self.display_winner("Player")
            elif self.cannon_score >= self.winning_score:
                self.display_winner("Cannon")

            # Update the game window display
            self.update_display()

            # Limit the game's frame rate to 60 fps
            self.limit_frame_rate()

        # Quit pygame and exit the program
        pygame.quit()
        raise SystemExit

# Create a new instance of the CannonGame class and start the game
if __name__ == "__main__":
    game = CannonGame()
    game.run()