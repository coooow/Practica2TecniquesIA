def main():
    print("Tria quin joc vols jugar:")
    print("1. Joc del Laberint")
    print("2. Joc de Cartes")
    choice = input("Introdueix el número del joc que vols jugar: ")
    if choice == "1":
        import labyrinth
        labyrinth.play()
    elif choice == "2":
        import card
        card.play()
    
if __name__ == "__main__":
    main()