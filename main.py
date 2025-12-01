from mirror import Mirror
import os
from banner import banner2
from table import print_user_table, print_user_info
from colorama import Fore, Style

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPress Enter to continue...")

def commands():
    print(Style.BRIGHT + Fore.MAGENTA + "Comandos:" + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.YELLOW + "info <username>" + Style.RESET_ALL + "            - Informacion del user" )
    print(Style.BRIGHT + Fore.YELLOW + "followers <username>" + Style.RESET_ALL + "       - Lista de seguidores de un usuario")
    print(Style.BRIGHT + Fore.YELLOW + "following <username>" + Style.RESET_ALL + "       - Lista de seguidos de un usuario")
    print(Style.BRIGHT + Fore.YELLOW + "mutuals <username>" + Style.RESET_ALL + "         - Mutuals de un usuario")
    print(Style.BRIGHT + Fore.YELLOW + "notfollowed <username>" + Style.RESET_ALL + "     - Seguidos que no siguen de vuelta al user")
    print(Style.BRIGHT + Fore.YELLOW + "notfollowing <username>" + Style.RESET_ALL + "    - Seguidores que el user no sigue de vuelta")
    print(Style.BRIGHT + Fore.YELLOW + "exit" + Style.RESET_ALL + "                       - Salir")
    print("")

def main():
    cls()
    banner2()
    ig = None
    
    # First, try to use saved session (no credentials needed yet)
    print("Checking for saved session...")
    try:
        # Create Mirror with dummy credentials; it will try session first
        ig = Mirror("", "")
    except Exception as e:
        # Session failed or doesn't exist; ask for real credentials
        print(f"Session loading failed: {e}\n")
        username = input("Usuario de ig: ")
        password = input("Contraseña de ig: ")
        ig = Mirror(username, password)

    while True:
        cls()
        banner2()
        commands()

        cmd = input(Style.BRIGHT + Fore.CYAN + "mirror> " + Style.RESET_ALL).strip().split()

        if len(cmd) == 0:
            continue

        action = cmd[0].lower()

        # info 
        if action == "info" and len(cmd) == 2:
            target = cmd[1]
            print(f"{Fore.CYAN}{Style.BRIGHT}\nObteniendo informacion de {target}. Puede tardar un momento...\n{Style.RESET_ALL}")
            info = ig.getUserInfo(target)

            if info:
                print_user_info(info)
            
            pause()

        # followers 
        elif action == "followers" and len(cmd) == 2:
            target = cmd[1]
            print(f"{Fore.CYAN}{Style.BRIGHT}\nObteniendo followers de {target}. Puede tardar un momento...\n{Style.RESET_ALL}")
            followers = ig.getFollowers(target)

            if followers is not None:
                print(f"{Fore.YELLOW}{Style.BRIGHT}Total: {len(followers)}{Style.RESET_ALL}")
                print_user_table(followers, title="Followers de " + target)

            pause()

        # following
        elif action == "following" and len(cmd) == 2:
            target = cmd[1]
            print(f"{Fore.CYAN}{Style.BRIGHT}\nObteniendo following de {target}. Puede tardar un momento...\n{Style.RESET_ALL}")
            following = ig.getFollowing(target)

            if following is not None:
                print(f"{Fore.YELLOW}{Style.BRIGHT}Total: {len(following)}{Style.RESET_ALL}")
                print_user_table(following, title="Following de " + target)

            pause()

        # notfollowing
        elif action == "notfollowing" and len(cmd) == 2:
            target = cmd[1]
            print(f"{Fore.CYAN}{Style.BRIGHT}\nObteniendo seguidores que {target} no sigue de vuelta. Puede tardar un momento...\n{Style.RESET_ALL}")
            not_following_back = ig.getNotFollowingBack(target)

            if not_following_back is not None:
                print(f"{Fore.YELLOW}{Style.BRIGHT}Total: {len(not_following_back)}{Style.RESET_ALL}")
                print_user_table(not_following_back, title="Seguidores que " + target + " no sigue de vuelta")

            pause()

        # mutuals
        elif action == "mutuals" and len(cmd) == 2:
            target = cmd[1]
            print(f"{Fore.CYAN}{Style.BRIGHT}\nObteniendo mutuals de {target}. Puede tardar un momento...\n{Style.RESET_ALL}")
            mutuals = ig.getMutuals(target)

            if mutuals is not None:
                print(f"{Fore.YELLOW}{Style.BRIGHT}Total: {len(mutuals)}{Style.RESET_ALL}")
                print_user_table(mutuals, title="Mutuals de " + target)

            pause()
        
        # notfollowed
        elif action == "notfollowed" and len(cmd) == 2:
            target = cmd[1]
            print(f"{Fore.CYAN}{Style.BRIGHT}\nObteniendo seguidos que no siguen de vuelta a {target}. Puede tardar un momento...\n{Style.RESET_ALL}")
            not_followed = ig.getNotFollowedBack(target)

            if not_followed is not None:
                print(f"{Fore.YELLOW}{Style.BRIGHT}Total: {len(not_followed)}{Style.RESET_ALL}")
                print_user_table(not_followed, title="Seguidos que no siguen de vuelta a " + target)

            pause()

        elif action == "exit":
            print("Saliendo...")
            break

if __name__ == "__main__":
    main()
