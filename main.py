def main():
    print("Choose which game you want to play:")
    print("1. Labyrinth Game")
    print("2. Card Game")
    choice = input("Enter the number of the game you want to play: ")
    if choice == "1":
        import labyrinth
        labyrinth.play()
    elif choice == "2":
        import card
        card.play()
    
if __name__ == "__main__":
    main()