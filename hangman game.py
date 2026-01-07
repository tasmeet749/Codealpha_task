import random
import os
import time
from collections import defaultdict

class Color:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_hangman(incorrect_guesses):
    """Enhanced hangman display with colors"""
    stages = [
        f"""
{Color.RED}           -----{Color.END}
           |   |
           |   {Color.RED}O{Color.END}
           |  {Color.RED}/|\\{Color.END}
           |  {Color.RED}/ \\\\{Color.END}
           |
        -----
        """,
        f"""
{Color.RED}           -----{Color.END}
           |   |
           |   {Color.RED}O{Color.END}
           |  {Color.RED}/|\\{Color.END}
           |  {Color.RED}/{Color.END} 
           |
        -----
        """,
        f"""
{Color.RED}           -----{Color.END}
           |   |
           |   {Color.RED}O{Color.END}
           |  {Color.RED}/|\\{Color.END}
           |  
           |
        -----
        """,
        f"""
{Color.RED}           -----{Color.END}
           |   |
           |   {Color.RED}O{Color.END}
           |  {Color.RED}/|{Color.END}
           |  
           |
        -----
        """,
        f"""
{Color.RED}           -----{Color.END}
           |   |
           |   {Color.RED}O{Color.END}
           |  {Color.RED}|{Color.END}
           |  
           |
        -----
        """,
        f"""
{Color.RED}           -----{Color.END}
           |   |
           |   {Color.RED}O{Color.END}
           |   
           |  
           |
        -----
        """,
        """
           -----
           |   |
           |   
           |   
           |  
           |
        -----
        """
    ]
    return stages[incorrect_guesses]

class HangmanGame:
    def __init__(self):
        self.word_categories = {
            'Animals': ['elephant', 'giraffe', 'penguin', 'dolphin', 'kangaroo', 
                       'butterfly', 'crocodile', 'octopus', 'peacock', 'rhinoceros'],
            'Countries': ['brazil', 'japan', 'egypt', 'canada', 'australia', 
                         'france', 'india', 'mexico', 'norway', 'thailand'],
            'Technology': ['computer', 'internet', 'software', 'database', 'algorithm',
                          'encryption', 'blockchain', 'artificial', 'programming', 'network'],
            'Sports': ['basketball', 'football', 'tennis', 'swimming', 'volleyball',
                      'cricket', 'baseball', 'hockey', 'golf', 'boxing'],
            'Food': ['pizza', 'hamburger', 'spaghetti', 'chocolate', 'sandwich',
                    'pancake', 'burrito', 'sushi', 'croissant', 'lasagna']
        }
        
        self.difficulty_levels = {
            'Easy': {'max_guesses': 8, 'min_length': 5, 'score_multiplier': 1},
            'Medium': {'max_guesses': 6, 'min_length': 6, 'score_multiplier': 2},
            'Hard': {'max_guesses': 4, 'min_length': 7, 'score_multiplier': 3}
        }
        
        self.hints = {
            'elephant': 'Largest land animal with a trunk',
            'giraffe': 'Tallest animal with a long neck',
            'brazil': 'Largest country in South America',
            'computer': 'Electronic device for processing data',
            'basketball': 'Sport played with a hoop and ball',
            'pizza': 'Italian dish with cheese and toppings',
            # Add more hints as needed
        }
        
        self.player_stats = {
            'games_played': 0,
            'games_won': 0,
            'total_score': 0,
            'current_streak': 0,
            'best_streak': 0,
            'words_completed': []
        }
        
    def get_word(self, category, difficulty):
        """Select a random word based on category and difficulty"""
        words = self.word_categories[category]
        min_len = self.difficulty_levels[difficulty]['min_length']
        valid_words = [w for w in words if len(w) >= min_len]
        return random.choice(valid_words)
    
    def calculate_score(self, word, incorrect_guesses, difficulty):
        """Calculate score based on word length, remaining guesses, and difficulty"""
        base_score = len(word) * 10
        remaining_guesses = self.difficulty_levels[difficulty]['max_guesses'] - incorrect_guesses
        bonus = remaining_guesses * 5
        multiplier = self.difficulty_levels[difficulty]['score_multiplier']
        return (base_score + bonus) * multiplier
    
    def display_stats(self):
        """Display player statistics"""
        print(f"\n{Color.CYAN}=== Your Statistics ==={Color.END}")
        print(f"Games Played: {self.player_stats['games_played']}")
        print(f"Games Won: {self.player_stats['games_won']}")
        if self.player_stats['games_played'] > 0:
            win_rate = (self.player_stats['games_won'] / self.player_stats['games_played']) * 100
            print(f"Win Rate: {win_rate:.1f}%")
        print(f"Total Score: {self.player_stats['total_score']}")
        print(f"Current Streak: {self.player_stats['current_streak']}")
        print(f"Best Streak: {self.player_stats['best_streak']}")
        if self.player_stats['words_completed']:
            print(f"Words Completed: {', '.join(self.player_stats['words_completed'][-5:])}")
    
    def play_round(self):
        """Play a single round of Hangman"""
        try:
            # Select difficulty
            print(f"\n{Color.YELLOW}Select Difficulty:{Color.END}")
            difficulties = list(self.difficulty_levels.keys())
            for i, diff in enumerate(difficulties, 1):
                print(f"{i}. {diff} ({self.difficulty_levels[diff]['max_guesses']} guesses)")
            
            while True:
                try:
                    choice = int(input("Enter your choice (1-3): ")) - 1
                    if 0 <= choice < len(difficulties):
                        difficulty = difficulties[choice]
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a number.")
            
            # Select category
            print(f"\n{Color.YELLOW}Select Category:{Color.END}")
            categories = list(self.word_categories.keys())
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            
            while True:
                try:
                    choice = int(input("Enter your choice: ")) - 1
                    if 0 <= choice < len(categories):
                        category = categories[choice]
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a number.")
            
            # Initialize game
            word = self.get_word(category, difficulty)
            word_letters = list(word)
            guessed_letters = []
            incorrect_guesses = 0
            max_incorrect = self.difficulty_levels[difficulty]['max_guesses']
            hints_used = 0
            start_time = time.time()
            
            clear_screen()
            print(f"{Color.BOLD}{Color.HEADER}=== HANGMAN ==={Color.END}")
            print(f"Category: {Color.CYAN}{category}{Color.END}")
            print(f"Difficulty: {Color.YELLOW}{difficulty}{Color.END}")
            print(f"Word has {len(word)} letters")
            print(f"You have {max_incorrect} incorrect guesses allowed.")
            print(f"Type {Color.GREEN}'hint'{Color.END} for a hint (costs 5 points)")
            print("------------------------------------")
            
            # Main game loop
            while incorrect_guesses < max_incorrect:
                clear_screen()
                print(display_hangman(incorrect_guesses))
                print(f"\nCategory: {Color.CYAN}{category}{Color.END}")
                print(f"Difficulty: {Color.YELLOW}{difficulty}{Color.END}")
                
                # Display word with guessed letters revealed
                display_word = ""
                for letter in word_letters:
                    if letter in guessed_letters:
                        display_word += f"{Color.GREEN}{letter}{Color.END} "
                    else:
                        display_word += "_ "
                print(f"\nWord: {display_word}")
                
                # Display guessed letters
                if guessed_letters:
                    print(f"Guessed letters: {Color.RED}{', '.join(guessed_letters)}{Color.END}")
                
                print(f"\n{Color.YELLOW}Incorrect guesses remaining: {max_incorrect - incorrect_guesses}{Color.END}")
                
                # Check if player has won
                if all(letter in guessed_letters for letter in word_letters):
                    elapsed_time = int(time.time() - start_time)
                    score = self.calculate_score(word, incorrect_guesses, difficulty) - (hints_used * 5)
                    score = max(0, score)  # Ensure score doesn't go negative
                    
                    print(f"\n{Color.GREEN}{Color.BOLD}🎉 CONGRATULATIONS! 🎉{Color.END}")
                    print(f"You guessed the word: {Color.GREEN}{word.upper()}{Color.END}")
                    print(f"Time taken: {elapsed_time} seconds")
                    print(f"Score: {Color.YELLOW}{score}{Color.END}")
                    
                    # Update stats
                    self.player_stats['games_played'] += 1
                    self.player_stats['games_won'] += 1
                    self.player_stats['total_score'] += score
                    self.player_stats['current_streak'] += 1
                    self.player_stats['best_streak'] = max(self.player_stats['best_streak'], 
                                                           self.player_stats['current_streak'])
                    self.player_stats['words_completed'].append(word)
                    
                    # Show word meaning if available
                    if word in self.hints:
                        print(f"\n{Color.CYAN}Fun Fact: {self.hints[word]}{Color.END}")
                    
                    break
                
                # Get player's guess
                guess = input(f"\n{Color.BLUE}Guess a letter (or 'hint'/'quit'): {Color.END}").lower()
                
                # Handle special commands
                if guess == 'quit':
                    return False
                elif guess == 'hint':
                    if hints_used < 2:
                        # Find an unguessed letter
                        unguessed = [l for l in word_letters if l not in guessed_letters]
                        if unguessed:
                            hint_letter = random.choice(unguessed)
                            print(f"\n{Color.YELLOW}Hint: The word contains the letter '{hint_letter}'{Color.END}")
                            hints_used += 1
                            input("Press Enter to continue...")
                            continue
                        else:
                            print("No more hints available!")
                            input("Press Enter to continue...")
                            continue
                    else:
                        print("You've used all your hints!")
                        input("Press Enter to continue...")
                        continue
                
                # Validate input
                if len(guess) != 1 or not guess.isalpha():
                    print("Please enter a single alphabetical character.")
                    input("Press Enter to continue...")
                    continue
                
                # Check if letter was already guessed
                if guess in guessed_letters:
                    print(f"{Color.RED}You've already guessed '{guess}'. Try another letter.{Color.END}")
                    input("Press Enter to continue...")
                    continue
                
                # Add guess to guessed letters
                guessed_letters.append(guess)
                
                # Check if guess is correct
                if guess not in word_letters:
                    incorrect_guesses += 1
                    print(f"{Color.RED}Sorry, '{guess}' is not in the word.{Color.END}")
                    input("Press Enter to continue...")
            
            # Game over - player ran out of guesses
            if incorrect_guesses == max_incorrect:
                clear_screen()
                print(display_hangman(incorrect_guesses))
                print(f"\n{Color.RED}{Color.BOLD}GAME OVER!{Color.END}")
                print(f"The word was: {Color.RED}{word.upper()}{Color.END}")
                
                # Update stats
                self.player_stats['games_played'] += 1
                self.player_stats['current_streak'] = 0
                
                if word in self.hints:
                    print(f"\n{Color.CYAN}Fun Fact: {self.hints[word]}{Color.END}")
            
            return True
        
        except Exception as e:
            print(f"\n{Color.RED}An error occurred during the game: {str(e)}{Color.END}")
            return True  # Return True to keep the game running
    
    def run(self):
        """Main game loop with improved error handling"""
        try:
            print(f"{Color.BOLD}{Color.HEADER}🎮 WELCOME TO ENHANCED HANGMAN! 🎮{Color.END}")
            print(f"{Color.CYAN}A more challenging and enjoyable word-guessing game!{Color.END}\n")
            
            while True:
                try:
                    print(f"\n{Color.YELLOW}=== MAIN MENU ==={Color.END}")
                    print("1. Play Game")
                    print("2. View Statistics")
                    print("3. Instructions")
                    print("4. Quit")
                    
                    choice = input("\nEnter your choice (1-4): ").strip()
                    
                    if choice == '1':
                        if not self.play_round():
                            break
                    elif choice == '2':
                        clear_screen()
                        self.display_stats()
                        input("\nPress Enter to continue...")
                    elif choice == '3':
                        clear_screen()
                        print(f"\n{Color.BOLD}=== HOW TO PLAY ==={Color.END}")
                        print("1. Select a difficulty level (Easy, Medium, or Hard)")
                        print("2. Choose a word category")
                        print("3. Guess letters one at a time")
                        print("4. Use hints wisely (they cost points!)")
                        print("5. Complete the word before running out of guesses")
                        print("6. Build your streak and beat your high score!")
                        print("\nScoring:")
                        print("- Base points: 10 × word length")
                        print("- Bonus: 5 × remaining guesses")
                        print("- Difficulty multiplier: Easy (1x), Medium (2x), Hard (3x)")
                        print("- Hint penalty: -5 points per hint")
                        input("\nPress Enter to continue...")
                    elif choice == '4':
                        print(f"\n{Color.GREEN}Thanks for playing Hangman!{Color.END}")
                        if self.player_stats['games_played'] > 0:
                            print(f"Final Score: {self.player_stats['total_score']}")
                            print(f"Best Streak: {self.player_stats['best_streak']}")
                        break
                    else:
                        print("Invalid choice. Please try again.")
                        input("Press Enter to continue...")
                
                except KeyboardInterrupt:
                    print(f"\n\n{Color.YELLOW}Game interrupted by user.{Color.END}")
                    break
                except Exception as e:
                    print(f"\n{Color.RED}An error occurred: {str(e)}{Color.END}")
                    input("Press Enter to continue...")
        
        except Exception as e:
            print(f"\n{Color.RED}Fatal error in game: {str(e)}{Color.END}")
        finally:
            print(f"\n{Color.GREEN}Game session ended.{Color.END}")

# Start the game
if __name__ == "__main__":
    try:
        game = HangmanGame()
        game.run()
    except Exception as e:
        print(f"\n{Color.RED}Failed to start game: {str(e)}{Color.END}")